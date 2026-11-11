from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_contains_approved_behavior_contract(self):
        skill_path = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_path.is_file(), "SKILL.md must exist")
        text = skill_path.read_text(encoding="utf-8")

        required_phrases = (
            "name: vast-extract-learnings",
            "Use when",
            ".vast/config.yml",
            "AI 判断",
            "YYYY-MM-DD-<topic>-learnings.md",
            "Decision",
            "Lesson",
            "Pattern",
            "Surprise",
            "每条学习必须有 Source",
            "generated_by: vast-extract-learnings",
            "人工文档",
            "不要修改索引",
        )
        for phrase in required_phrases:
            self.assertIn(phrase, text)

        self.assertLessEqual(len(text.splitlines()), 500)

    def test_bundled_resources_exist(self):
        required = (
            "references/extraction-model.md",
            "references/artifact-discovery.md",
            "assets/learnings-template.md",
        )
        for relative in required:
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
