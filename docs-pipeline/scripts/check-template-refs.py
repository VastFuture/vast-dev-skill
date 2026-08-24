#!/usr/bin/env python3
"""Validate docs-pipeline template references and template tree hygiene."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
DOC_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "README.md",
    SKILL_DIR / "USAGE.md",
    SKILL_DIR / "ADVANCED.md",
]
TEMPLATE_REF_RE = re.compile(r"`assets/templates/([^`]+)`")


def collect_refs() -> list[tuple[Path, str]]:
    refs: list[tuple[Path, str]] = []
    for doc in DOC_FILES:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        for ref in sorted(set(TEMPLATE_REF_RE.findall(text))):
            refs.append((doc, ref))
    return refs


def main() -> int:
    missing: list[tuple[Path, str]] = []
    for doc, ref in collect_refs():
        if not (TEMPLATES_DIR / ref).is_file():
            missing.append((doc, ref))

    polluted = sorted(TEMPLATES_DIR.glob(".omc/state/*"))

    if missing:
        print("Missing template references:")
        for doc, ref in missing:
            print(f"  {doc.relative_to(SKILL_DIR)} -> assets/templates/{ref}")

    if polluted:
        print("Runtime state files found under assets/templates:")
        for path in polluted:
            print(f"  {path.relative_to(SKILL_DIR)}")

    if missing or polluted:
        return 1

    print("Template reference check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
