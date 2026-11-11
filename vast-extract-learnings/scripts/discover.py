#!/usr/bin/env python3
"""Discover evidence artifacts for vast-extract-learnings."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ARTIFACT_SUFFIXES = (
    "-PLAN.md",
    "-SUMMARY.md",
    "-VERIFICATION.md",
    "-UAT.md",
    "-REVIEW.md",
    "-RETROSPECTIVE.md",
    "-POSTMORTEM.md",
)
GLOBAL_ARTIFACTS = {
    "STATE.md",
    "CHANGELOG.md",
    "REVIEW.md",
    "RETROSPECTIVE.md",
    "POSTMORTEM.md",
}
EVIDENCE_DIR_NAMES = {
    ".planning",
    "exec-plans",
    "testing",
    "handover",
    "retrospectives",
    "postmortems",
}
EXCLUDED_DIR_NAMES = {
    ".git",
    ".ref-project",
    ".working",
    ".worktrees",
    "_sandbox",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "__pycache__",
}
EXPLICIT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}


def _is_within(path: Path, root: Path | None) -> bool:
    if root is None:
        return False
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _excluded(path: Path, target_lessons: Path | None) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    return _is_within(path, target_lessons)


def _artifact_priority(path: Path) -> tuple[int, str] | None:
    name = path.name
    if name.lower() in {"readme.md", "index.md"}:
        return None
    if name.endswith(ARTIFACT_SUFFIXES):
        if name.endswith(("-PLAN.md", "-SUMMARY.md", "-VERIFICATION.md", "-UAT.md")):
            return 3, "phase-artifact"
        return 4, "review-artifact"
    if name in GLOBAL_ARTIFACTS:
        return 5, "project-artifact"
    if path.suffix.lower() == ".md" and any(part in EVIDENCE_DIR_NAMES for part in path.parts):
        return 4, "evidence-directory"
    return None


def _topic_hint(path: Path) -> str | None:
    value = path.stem
    value = re.sub(
        r"(?i)-(plan|summary|verification|uat|review|retrospective|postmortem|learnings)$",
        "",
        value,
    )
    value = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", value)
    value = value.strip("-_. ")
    if not value or value.upper() in {"STATE", "CHANGELOG", "README"}:
        return None
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower() or None


def _explicit_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for candidate in path.rglob("*"):
        if candidate.is_file() and candidate.suffix.lower() in EXPLICIT_EXTENSIONS:
            yield candidate


def discover_artifacts(
    project_root: Path | str,
    *,
    sources: Iterable[Path | str] | None = None,
    docs_root: Path | str | None = None,
    learnings_dir: str = "lessons",
) -> dict[str, Any]:
    root = Path(project_root).expanduser().resolve()
    docs = Path(docs_root).expanduser().resolve() if docs_root else None
    target_lessons = docs / learnings_dir if docs else None
    found: dict[str, dict[str, Any]] = {}
    missing_sources: list[str] = []
    excluded: list[str] = []

    def add(path: Path, priority: int, reason: str) -> None:
        resolved = path.resolve()
        key = str(resolved)
        existing = found.get(key)
        if existing and existing["priority"] <= priority:
            return
        try:
            relative = str(resolved.relative_to(root))
        except ValueError:
            relative = None
        found[key] = {
            "path": key,
            "relative_path": relative,
            "priority": priority,
            "reason": reason,
        }

    for raw_source in sources or []:
        source = Path(raw_source).expanduser()
        if not source.is_absolute():
            source = root / source
        source = source.resolve()
        if not source.exists():
            missing_sources.append(str(source))
            continue
        for candidate in _explicit_files(source):
            if _excluded(candidate, target_lessons):
                excluded.append(str(candidate.resolve()))
            else:
                add(candidate, 1, "explicit-source")

    for candidate in root.rglob("*"):
        if not candidate.is_file():
            continue
        if _excluded(candidate, target_lessons):
            continue
        artifact = _artifact_priority(candidate)
        if artifact:
            add(candidate, *artifact)

    candidates = sorted(found.values(), key=lambda item: (item["priority"], item["path"]))
    hints: list[str] = []
    for item in candidates:
        hint = _topic_hint(Path(item["path"]))
        if hint and hint not in hints:
            hints.append(hint)

    return {
        "project_root": str(root),
        "candidates": candidates,
        "missing_sources": sorted(set(missing_sources)),
        "excluded": sorted(set(excluded)),
        "suggested_topic_hints": hints,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--docs-root")
    parser.add_argument("--learnings-dir", default="lessons")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = discover_artifacts(
        args.project_root,
        sources=args.source,
        docs_root=args.docs_root,
        learnings_dir=args.learnings_dir,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
