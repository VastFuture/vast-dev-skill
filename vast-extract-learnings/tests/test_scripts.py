from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = SKILL_ROOT / "scripts" / f"{name}.py"
    if not path.is_file():
        raise AssertionError(f"missing script: {path}")
    spec = importlib.util.spec_from_file_location(f"vast_extract_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_script("config")

    def test_round_trip_and_project_root_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            docs = Path(tmp) / "knowledge" / "docs"
            nested = root / "src" / "feature"
            docs.mkdir(parents=True)
            nested.mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")

            settings = {
                "version": 1,
                "project_id": "sample-project",
                "docs_root": str(docs),
                "learnings_dir": "lessons",
                "overwrite_existing": True,
            }
            self.config.write_config(root, settings)

            self.assertEqual(self.config.read_config(root), settings)
            located = self.config.find_project_root(nested, use_git=False)
            self.assertEqual(located["project_root"], str(root.resolve()))
            self.assertEqual(located["reason"], "vast-config")
            self.assertFalse(located["needs_confirmation"])

    def test_initialize_requires_existing_docs_root_and_safe_learnings_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()

            with self.assertRaises(self.config.ConfigError):
                self.config.initialize_config(
                    root,
                    Path(tmp) / "missing-docs",
                    learnings_dir="lessons",
                )

            docs = Path(tmp) / "docs"
            docs.mkdir()
            with self.assertRaises(self.config.ConfigError):
                self.config.initialize_config(
                    root,
                    docs,
                    learnings_dir="../outside",
                )

    def test_initialize_creates_learnings_and_gitignore_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            docs = Path(tmp) / "docs"
            root.mkdir()
            docs.mkdir()
            (root / ".git").mkdir()

            result = self.config.initialize_config(
                root,
                docs,
                project_id="project",
                create_learnings=True,
                update_gitignore=True,
            )
            self.assertTrue((docs / "lessons").is_dir())
            self.assertEqual(result["gitignore_status"], "added")

            self.config.ensure_gitignore(root)
            lines = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines.count(".vast/config.yml"), 1)

    def test_round_trip_preserves_quoted_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            docs = Path(tmp) / 'knowledge "quoted"' / "docs"
            root.mkdir()
            docs.mkdir(parents=True)
            settings = {
                "version": 1,
                "project_id": 'project "alpha"',
                "docs_root": str(docs),
                "learnings_dir": "lessons",
                "overwrite_existing": True,
            }

            self.config.write_config(root, settings)

            self.assertEqual(self.config.read_config(root), settings)


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.discover = load_script("discover")

    def test_discovers_artifacts_and_excludes_generated_lessons(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            docs_root = Path(tmp) / "knowledge" / "docs"
            plan = root / "docs" / "exec-plans" / "payment-PLAN.md"
            explicit = root / "notes" / "payment-evidence.txt"
            ignored = root / "node_modules" / "ignored-PLAN.md"
            generated = docs_root / "lessons" / "2026-11-11-payment-learnings.md"
            for path in (plan, explicit, ignored, generated):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("evidence\n", encoding="utf-8")

            result = self.discover.discover_artifacts(
                root,
                sources=[explicit],
                docs_root=docs_root,
                learnings_dir="lessons",
            )
            candidates = {item["path"]: item for item in result["candidates"]}

            self.assertEqual(candidates[str(explicit.resolve())]["priority"], 1)
            self.assertIn(str(plan.resolve()), candidates)
            self.assertNotIn(str(ignored.resolve()), candidates)
            self.assertNotIn(str(generated.resolve()), candidates)
            self.assertTrue(result["suggested_topic_hints"])

    def test_missing_explicit_source_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            result = self.discover.discover_artifacts(
                root,
                sources=[root / "missing.md"],
            )
            self.assertEqual(result["missing_sources"], [str((root / "missing.md").resolve())])

    def test_excludes_external_clones_and_worktrees(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            expected = root / "docs" / "exec-plans" / "feature-SUMMARY.md"
            clone = root / ".ref-project" / "template" / "docs" / "testing" / "guide.md"
            worktree = root / ".worktrees" / "other" / "docs" / "exec-plans" / "old.md"
            for path in (expected, clone, worktree):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("evidence\n", encoding="utf-8")

            result = self.discover.discover_artifacts(root)
            candidates = {item["path"] for item in result["candidates"]}

            self.assertIn(str(expected.resolve()), candidates)
            self.assertNotIn(str(clone.resolve()), candidates)
            self.assertNotIn(str(worktree.resolve()), candidates)

    def test_excludes_directory_guides_from_auto_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            summary = root / "docs" / "exec-plans" / "feature-SUMMARY.md"
            readme = root / "docs" / "exec-plans" / "README.md"
            index = root / "docs" / "testing" / "index.md"
            for path in (summary, readme, index):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("text\n", encoding="utf-8")

            result = self.discover.discover_artifacts(root)
            candidates = {item["path"] for item in result["candidates"]}

            self.assertIn(str(summary.resolve()), candidates)
            self.assertNotIn(str(readme.resolve()), candidates)
            self.assertNotIn(str(index.resolve()), candidates)


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_script("validate_output")

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        base = Path(self.tempdir.name)
        self.project = base / "project"
        self.docs_root = base / "knowledge" / "docs"
        self.output = self.docs_root / "lessons" / "2026-11-11-payment-learnings.md"
        self.source = self.project / "docs" / "payment-summary.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("# Payment summary\n", encoding="utf-8")
        self.output.parent.mkdir(parents=True)

    def tearDown(self):
        self.tempdir.cleanup()

    def valid_document(self) -> str:
        return """---
schema_version: 1
project: sample
completion_date: "2026-11-11"
generated: "2026-11-11T10:30:00+08:00"
generated_by: vast-extract-learnings
counts:
  decisions: 1
  lessons: 1
  patterns: 1
  surprises: 1
---

# Payment Learnings

## Decisions

### Use idempotency keys
The callback stores a stable idempotency key.

**Rationale:** Duplicate callbacks must not create duplicate orders.
**Source:** `docs/payment-summary.md#decision`

## Lessons

### Retry behavior needs explicit tests
Retries exposed an ordering assumption.

**Context:** Fault injection produced out-of-order callbacks.
**Source:** `docs/payment-summary.md#verification`

## Patterns

### Persist before acknowledging
Persist the event before returning success.

**When to use:** External systems retry delivery after timeouts.
**Source:** `docs/payment-summary.md#pattern`

## Surprises

### Sandbox retries faster than production
The sandbox repeated callbacks immediately.

**Impact:** The verification script needed rate control.
**Source:** `docs/payment-summary.md#surprise`
"""

    def test_valid_document_passes(self):
        self.output.write_text(self.valid_document(), encoding="utf-8")
        result = self.validator.validate_document(
            self.output,
            docs_root=self.docs_root,
            project_root=self.project,
        )
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["actual_counts"]["decisions"], 1)

    def test_empty_category_is_allowed_and_counts_as_zero(self):
        content = self.valid_document().replace(
            "  surprises: 1", "  surprises: 0"
        ).replace(
            "### Sandbox retries faster than production\n"
            "The sandbox repeated callbacks immediately.\n\n"
            "**Impact:** The verification script needed rate control.\n"
            "**Source:** `docs/payment-summary.md#surprise`",
            "无（本轮未发现）",
        )
        self.output.write_text(content, encoding="utf-8")
        result = self.validator.validate_document(
            self.output,
            docs_root=self.docs_root,
            project_root=self.project,
        )
        self.assertTrue(result["ok"], result["errors"])

    def test_rejects_path_escape_count_mismatch_and_missing_source(self):
        outside = self.docs_root.parent / "outside.md"
        outside.write_text(
            self.valid_document()
            .replace("  decisions: 1", "  decisions: 2")
            .replace("docs/payment-summary.md", "docs/missing.md"),
            encoding="utf-8",
        )
        result = self.validator.validate_document(
            outside,
            docs_root=self.docs_root,
            project_root=self.project,
        )
        errors = "\n".join(result["errors"])
        self.assertFalse(result["ok"])
        self.assertIn("outside docs_root", errors)
        self.assertIn("count mismatch", errors)
        self.assertIn("source does not exist", errors)

    def test_rejects_missing_required_item_field(self):
        self.output.write_text(
            self.valid_document().replace("**Rationale:** Duplicate", "**Reason:** Duplicate"),
            encoding="utf-8",
        )
        result = self.validator.validate_document(
            self.output,
            docs_root=self.docs_root,
            project_root=self.project,
        )
        self.assertFalse(result["ok"])
        self.assertIn("missing Rationale", "\n".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()
