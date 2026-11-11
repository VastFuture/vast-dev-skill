#!/usr/bin/env python3
"""Manage project-local vast-extract-learnings configuration."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


CONFIG_RELATIVE_PATH = Path(".vast/config.yml")
GITIGNORE_RULE = ".vast/config.yml"
PROJECT_MARKERS = (
    "AGENTS.md",
    "CLAUDE.md",
    "package.json",
    "pyproject.toml",
    "go.mod",
    "Cargo.toml",
)
CONFIG_KEYS = (
    "version",
    "project_id",
    "docs_root",
    "learnings_dir",
    "overwrite_existing",
)


class ConfigError(ValueError):
    pass


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"invalid quoted config value: {exc}") from exc
        if not isinstance(parsed, str):
            raise ConfigError("quoted config values must be strings")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _quote_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def validate_learnings_dir(value: str) -> str:
    path = Path(value)
    if (
        not value
        or path.is_absolute()
        or len(path.parts) != 1
        or value in {".", ".."}
        or ".." in path.parts
    ):
        raise ConfigError("learnings_dir must be one safe relative directory name")
    return value


def validate_settings(settings: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in CONFIG_KEYS if key not in settings]
    if missing:
        raise ConfigError(f"missing config keys: {', '.join(missing)}")
    if settings["version"] != 1:
        raise ConfigError("unsupported config version")
    if not isinstance(settings["project_id"], str) or not settings["project_id"].strip():
        raise ConfigError("project_id must be a non-empty string")
    docs_root = Path(str(settings["docs_root"])).expanduser()
    if not docs_root.is_absolute():
        raise ConfigError("docs_root must be an absolute path")
    if not docs_root.is_dir():
        raise ConfigError(f"docs_root does not exist: {docs_root}")
    settings = dict(settings)
    settings["docs_root"] = str(docs_root.resolve())
    settings["learnings_dir"] = validate_learnings_dir(str(settings["learnings_dir"]))
    if not isinstance(settings["overwrite_existing"], bool):
        raise ConfigError("overwrite_existing must be true or false")
    return settings


def read_config(project_root: Path | str) -> dict[str, Any]:
    path = Path(project_root).resolve() / CONFIG_RELATIVE_PATH
    if not path.is_file():
        raise ConfigError(f"config not found: {path}")
    settings: dict[str, Any] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ConfigError(f"invalid config line {line_number}: {raw_line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if key not in CONFIG_KEYS:
            raise ConfigError(f"unsupported config key: {key}")
        try:
            settings[key] = _parse_scalar(raw_value)
        except ConfigError as exc:
            raise ConfigError(f"invalid config line {line_number}: {exc}") from exc
    return validate_settings(settings)


def write_config(project_root: Path | str, settings: dict[str, Any]) -> Path:
    root = Path(project_root).resolve()
    validated = validate_settings(settings)
    path = root / CONFIG_RELATIVE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(
        (
            f"version: {validated['version']}",
            f"project_id: {_quote_string(validated['project_id'])}",
            f"docs_root: {_quote_string(validated['docs_root'])}",
            f"learnings_dir: {_quote_string(validated['learnings_dir'])}",
            f"overwrite_existing: {str(validated['overwrite_existing']).lower()}",
            "",
        )
    )
    path.write_text(content, encoding="utf-8")
    return path


def _git_root(start: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    return Path(value).resolve() if value else None


def _parents_inclusive(start: Path):
    yield start
    yield from start.parents


def find_project_root(start: Path | str, use_git: bool = True) -> dict[str, Any]:
    current = Path(start).expanduser().resolve()
    if current.is_file():
        current = current.parent
    if use_git:
        git_root = _git_root(current)
        if git_root:
            return {
                "project_root": str(git_root),
                "reason": "git",
                "needs_confirmation": False,
            }
    for candidate in _parents_inclusive(current):
        if (candidate / CONFIG_RELATIVE_PATH).is_file():
            return {
                "project_root": str(candidate),
                "reason": "vast-config",
                "needs_confirmation": False,
            }
    for candidate in _parents_inclusive(current):
        if any((candidate / marker).exists() for marker in PROJECT_MARKERS):
            return {
                "project_root": str(candidate),
                "reason": "project-marker",
                "needs_confirmation": False,
            }
    return {
        "project_root": str(current),
        "reason": "current-directory",
        "needs_confirmation": True,
    }


def is_git_project(project_root: Path | str) -> bool:
    root = Path(project_root).resolve()
    return (root / ".git").exists() or _git_root(root) == root


def ensure_gitignore(project_root: Path | str) -> str:
    root = Path(project_root).resolve()
    if not is_git_project(root):
        return "not-git"
    path = root / ".gitignore"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    if GITIGNORE_RULE in {line.strip() for line in lines}:
        return "already-present"
    prefix = "" if not path.exists() or path.stat().st_size == 0 else "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{prefix}{GITIGNORE_RULE}\n")
    return "added"


def initialize_config(
    project_root: Path | str,
    docs_root: Path | str,
    *,
    project_id: str | None = None,
    learnings_dir: str = "lessons",
    overwrite_existing: bool = True,
    create_learnings: bool = False,
    update_gitignore: bool = False,
) -> dict[str, Any]:
    root = Path(project_root).expanduser().resolve()
    docs = Path(docs_root).expanduser()
    if not docs.is_absolute():
        raise ConfigError("docs_root must be an absolute path")
    if not docs.is_dir():
        raise ConfigError(f"docs_root does not exist: {docs}")
    learnings_name = validate_learnings_dir(learnings_dir)
    learnings_path = docs.resolve() / learnings_name
    if not learnings_path.exists():
        if not create_learnings:
            raise ConfigError(f"learnings directory does not exist: {learnings_path}")
        learnings_path.mkdir()
    elif not learnings_path.is_dir():
        raise ConfigError(f"learnings path is not a directory: {learnings_path}")

    settings = {
        "version": 1,
        "project_id": project_id or root.name,
        "docs_root": str(docs.resolve()),
        "learnings_dir": learnings_name,
        "overwrite_existing": overwrite_existing,
    }
    config_path = write_config(root, settings)
    gitignore_status = ensure_gitignore(root) if update_gitignore else "not-requested"
    return {
        "config_path": str(config_path),
        "learnings_path": str(learnings_path),
        "gitignore_status": gitignore_status,
        "settings": settings,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    locate = subparsers.add_parser("locate", help="locate the current project root")
    locate.add_argument("--start", default=os.getcwd())

    read = subparsers.add_parser("read", help="read and validate project config")
    read.add_argument("--project-root", required=True)

    for command in ("init", "rebind"):
        sub = subparsers.add_parser(command, help=f"{command} the docs binding")
        sub.add_argument("--project-root", required=True)
        sub.add_argument("--docs-root", required=True)
        sub.add_argument("--project-id")
        sub.add_argument("--learnings-dir", default="lessons")
        sub.add_argument("--create-learnings", action="store_true")
        sub.add_argument("--update-gitignore", action="store_true")

    ignore = subparsers.add_parser("ensure-gitignore", help="add the local config ignore rule")
    ignore.add_argument("--project-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "locate":
            result = find_project_root(args.start)
        elif args.command == "read":
            result = read_config(args.project_root)
        elif args.command in {"init", "rebind"}:
            result = initialize_config(
                args.project_root,
                args.docs_root,
                project_id=args.project_id,
                learnings_dir=args.learnings_dir,
                create_learnings=args.create_learnings,
                update_gitignore=args.update_gitignore,
            )
        else:
            result = {"status": ensure_gitignore(args.project_root)}
    except ConfigError as exc:
        _print_json({"ok": False, "error": str(exc)})
        return 1
    _print_json({"ok": True, "result": result})
    return 0


if __name__ == "__main__":
    sys.exit(main())
