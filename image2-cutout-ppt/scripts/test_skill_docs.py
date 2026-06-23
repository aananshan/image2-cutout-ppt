from __future__ import annotations

import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


class SkillDocsTests(unittest.TestCase):
    def test_documents_two_stage_beautiful_first_workflow(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        self.assertLess(skill.index("source-only prompt"), skill.index("cutout-ready asset board"))
        self.assertLess(skill.index("stage 1 user approval gate"), skill.index("stage 1 aftercare gate"))
        self.assertLess(skill.index("stage 1 aftercare gate"), skill.index("coverage lock source gate"))
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

    def test_requires_image2_unless_user_explicitly_overrides(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()
        readme_path = SKILL_DIR.parents[0] / "README.md"
        readme = readme_path.read_text(encoding="utf-8").lower() if readme_path.exists() else ""

        self.assertIn("image2-first", skill)
        self.assertIn("must use image2", skill)
        self.assertIn("unless the user explicitly authorizes a fallback", skill)
        self.assertIn("do not substitute", skill)
        self.assertIn("stage 1 must be generated with image2", prompts)
        self.assertIn("stage 2 must be generated with image2", prompts)
        if readme:
            self.assertIn("image2-first", readme)
            self.assertNotIn("provider-agnostic", readme)
        self.assertNotIn("other ai-generated", skill)

    def test_stage1_prompt_is_source_only_and_stage1_aftercare_is_defined(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8")
        prompts_lower = prompts.lower()

        self.assertIn("source-only", prompts_lower)
        self.assertIn("[user content or stage 0 source brief only]", prompts_lower)
        self.assertIn("send only the user's own content", prompts_lower)
        self.assertIn("do not add a fixed style prompt", prompts_lower)
        self.assertIn("stage 1 user approval", prompts_lower)
        self.assertIn("stage 1 aftercare", prompts_lower)
        self.assertIn("style master", skill)
        self.assertIn("stage 1 user approval gate", skill)
        self.assertIn("stage 1 aftercare gate", skill)
        self.assertIn("coverage lock source gate", skill)
        self.assertNotIn("create a complete polished scientific mechanism diagram", prompts_lower)
        self.assertNotIn("high-impact journal", prompts_lower)

    def test_strict_generation_gates_are_documented(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        prompts = (SKILL_DIR / "references" / "prompts.md").read_text(encoding="utf-8").lower()

        for required in [
            "stage 0",
            "stage 1 prompt audit",
            "stage 1 user approval gate",
            "stage 1 aftercare gate",
            "coverage lock source gate",
            "stage 2 prompt audit",
            "validate_generation_flow.py",
        ]:
            self.assertIn(required, skill + prompts)

        self.assertLess(skill.index("stage 1 prompt audit"), skill.index("stage 1 aftercare gate"))
        self.assertLess(skill.index("stage 1 user approval gate"), skill.index("stage 1 aftercare gate"))
        self.assertLess(skill.index("stage 1 aftercare gate"), skill.index("coverage lock source gate"))
        self.assertLess(skill.index("coverage lock source gate"), skill.index("stage 2 prompt audit"))
        self.assertIn("do not read coverage_lock", skill)
        self.assertIn("do not infer required mechanism content from the stage 1 image", prompts)
        self.assertIn("forbidden in stage 1", prompts)

    def test_generation_flow_validator_is_bundled(self):
        validator = SKILL_DIR / "scripts" / "validate_generation_flow.py"
        self.assertTrue(validator.exists(), "validate_generation_flow.py must be bundled")


if __name__ == "__main__":
    unittest.main()
