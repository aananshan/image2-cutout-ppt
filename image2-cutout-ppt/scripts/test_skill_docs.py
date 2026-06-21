from __future__ import annotations

import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


class SkillDocsTests(unittest.TestCase):
    def test_documents_two_stage_beautiful_first_workflow(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        self.assertLess(skill.index("complete polished diagram"), skill.index("cutout-ready asset board"))
        self.assertIn("two-stage", skill)
        self.assertIn("do not skip the complete diagram stage", skill)
        self.assertIn("stage 1", prompts)
        self.assertIn("stage 2", prompts)
        self.assertIn("use the completed diagram as the visual reference", prompts)
        self.assertIn("not a final diagram", prompts)

    def test_documents_coverage_lock_before_asset_board(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        self.assertLess(skill.index("coverage lock"), skill.index("cutout-ready asset board"))
        self.assertIn("do not let image2 choose only the most visually salient objects", skill)
        self.assertIn("use multiple asset boards", skill)
        self.assertIn("missing mechanism content", skill)
        self.assertIn("coverage lock", prompts)
        self.assertIn("must-cover visual units", prompts)
        self.assertIn("do not omit any listed unit", prompts)
        self.assertIn("if the list is too long", prompts)

    def test_documents_real_failure_modes_from_artemia_example(self):
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        self.assertIn("state changes", prompts)
        self.assertIn("loss-of-function branches", prompts)
        self.assertIn("validation outcomes", prompts)
        self.assertIn("pathway statuses", prompts)

    def test_default_prompts_do_not_contain_domain_specific_pollution(self):
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        for forbidden in ["artemia", "cyclin k", "cdk9", "erk", "rsk", "tunel", "nauplius"]:
            self.assertNotIn(forbidden, prompts)


if __name__ == "__main__":
    unittest.main()
