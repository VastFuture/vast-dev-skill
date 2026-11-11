#!/usr/bin/env python3
"""Validate a generated learnings Markdown document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CATEGORIES = {
    "Decisions": ("decisions", "Rationale"),
    "Lessons": ("lessons", "Context"),
    "Patterns": ("patterns", "When to use"),
    "Surprises": ("surprises", "Impact"),
}
EMPTY_TEXTS = {"无（本轮未发现）", "None found."}


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _frontmatter(text: str) -> tuple[str, str] | None:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return None
    return match.group(1), text[match.end() :]


def _declared_counts(frontmatter: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    in_counts = False
    for line in frontmatter.splitlines():
        if re.fullmatch(r"counts:\s*", line):
            in_counts = True
            continue
        if in_counts:
            match = re.fullmatch(r"\s{2}([a-z]+):\s*(\d+)\s*", line)
            if match:
                counts[match.group(1)] = int(match.group(2))
                continue
            if line and not line.startswith(" "):
                break
    return counts


def _frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", frontmatter)
    return match.group(1).strip() if match else None


def _sections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^## (Decisions|Lessons|Patterns|Surprises)\s*$", body))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        result[match.group(1)] = body[match.end() : end].strip()
    return result


def _items(section: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^### .+\s*$", section))
    result: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        result.append(section[match.start() : end].strip())
    return result


def _source_values(item: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r"(?m)^\*\*Source:\*\*\s*`?([^`\n]+)`?\s*$", item):
        values.append(match.group(1).strip())
    return values


def _source_path(value: str, project_root: Path) -> Path:
    raw_path = value.split("#", 1)[0].strip()
    candidate = Path(raw_path).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (project_root / candidate).resolve()


def validate_document(
    file_path: Path | str,
    *,
    docs_root: Path | str,
    project_root: Path | str,
) -> dict[str, Any]:
    path = Path(file_path).expanduser().resolve()
    docs = Path(docs_root).expanduser().resolve()
    project = Path(project_root).expanduser().resolve()
    errors: list[str] = []

    if not _is_within(path, docs):
        errors.append(f"output is outside docs_root: {path}")
    if not path.is_file():
        errors.append(f"output file does not exist: {path}")
        return {"ok": False, "errors": errors, "actual_counts": {}}

    parsed = _frontmatter(path.read_text(encoding="utf-8"))
    if not parsed:
        errors.append("missing YAML frontmatter")
        return {"ok": False, "errors": errors, "actual_counts": {}}
    frontmatter, body = parsed
    if _frontmatter_value(frontmatter, "generated_by") != "vast-extract-learnings":
        errors.append("generated_by must be vast-extract-learnings")

    declared = _declared_counts(frontmatter)
    sections = _sections(body)
    actual: dict[str, int] = {}
    checked_sources: set[str] = set()

    for heading, (count_key, required_field) in CATEGORIES.items():
        if heading not in sections:
            errors.append(f"missing section: {heading}")
            actual[count_key] = 0
            continue
        section = sections[heading]
        entries = _items(section)
        if not entries and section.strip() not in EMPTY_TEXTS:
            errors.append(f"{heading} must contain items or the explicit empty marker")
        actual[count_key] = len(entries)
        for entry in entries:
            title = entry.splitlines()[0].removeprefix("### ")
            if not re.search(rf"(?m)^\*\*{re.escape(required_field)}:\*\*\s*\S", entry):
                errors.append(f"{heading} item '{title}' missing {required_field}")
            sources = _source_values(entry)
            if not sources:
                errors.append(f"{heading} item '{title}' missing Source")
            for source in sources:
                if source in checked_sources:
                    continue
                checked_sources.add(source)
                if not _source_path(source, project).is_file():
                    errors.append(f"source does not exist: {source}")

    for key in (value[0] for value in CATEGORIES.values()):
        if key not in declared:
            errors.append(f"missing declared count: {key}")
        elif declared[key] != actual.get(key, 0):
            errors.append(
                f"count mismatch for {key}: declared {declared[key]}, actual {actual.get(key, 0)}"
            )

    return {"ok": not errors, "errors": errors, "actual_counts": actual}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True)
    parser.add_argument("--docs-root", required=True)
    parser.add_argument("--project-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_document(
        args.file,
        docs_root=args.docs_root,
        project_root=args.project_root,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
