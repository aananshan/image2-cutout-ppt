from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_DIR / "scripts" / "validate_generation_flow.py"


def write_project(root: Path, *, stage1_prompt: str) -> None:
    analysis = root / "analysis"
    analysis.mkdir(parents=True)
    (analysis / "stage1_prompt.txt").write_text(stage1_prompt, encoding="utf-8")
    (analysis / "stage1_user_approval.md").write_text(
        "User approved Stage 1 in chat; continue to the cutout-ready Stage 2.",
        encoding="utf-8",
    )
    (analysis / "stage1_aftercare.md").write_text(
        "\n".join(
            [
                "Style notes: soft biomedical objects.",
                "Stage 1 omissions: do not treat omissions as content truth.",
                "Decision: preserve style and continue.",
            ]
        ),
        encoding="utf-8",
    )
    (root / "coverage_lock.json").write_text(
        '{"must_cover_mechanism_content":["A"],'
        '"carrier_assignment":{"image2_cutout_visual_units":[{"id":"a","visual":"A"}]}}',
        encoding="utf-8",
    )
    (analysis / "stage2_prompt.txt").write_text(
        "Create a cutout-ready asset board, not a final diagram. "
        "Use the coverage lock. Must-cover visual units: a.",
        encoding="utf-8",
    )


class GenerationFlowValidatorTests(unittest.TestCase):
    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--project-root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_strict_stage1_prompt_and_required_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root, stage1_prompt="alpha pathway")

            result = self.run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_stage1_prompt_polluted_with_stage2_constraints(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(
                root,
                stage1_prompt=(
                    "Make this into a polished diagram:\n"
                    "Preferred composition: 16:9 mechanism.\n"
                    "Text policy: no readable text labels.\n"
                    "Use the coverage lock and guide boxes."
                ),
            )

            result = self.run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden in stage 1", (result.stdout + result.stderr).lower())

    def test_rejects_missing_stage1_user_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root, stage1_prompt="alpha pathway")
            (root / "analysis" / "stage1_user_approval.md").unlink()

            result = self.run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stage1_user_approval.md", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
