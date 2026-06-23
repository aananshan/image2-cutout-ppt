from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


FORBIDDEN_STAGE1 = [
    "make this into a polished diagram:",
    "coverage lock",
    "preferred composition",
    "text policy",
    "no readable text",
    "guide box",
    "asset board",
    "cutout-ready",
    "row-major",
    "leave open space",
    "editable powerpoint labels",
    "fixed color palette",
]


def read_required(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"Missing required file: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Required file is empty: {path}")
    return text


def validate_stage1_prompt(path: Path) -> None:
    text = read_required(path)
    lower = text.lower()
    for phrase in FORBIDDEN_STAGE1:
        if phrase in lower:
            raise ValueError(f"Forbidden in Stage 1 prompt: {phrase}")


def validate_user_approval(path: Path) -> None:
    read_required(path)


def validate_aftercare(path: Path) -> None:
    text = read_required(path).lower()
    required = ["style", "omission", "content"]
    for word in required:
        if word not in text:
            raise ValueError(f"Stage 1 aftercare must mention {word!r}: {path}")


def validate_coverage_lock(path: Path) -> None:
    lock = json.loads(read_required(path))
    if not lock.get("must_cover_mechanism_content"):
        raise ValueError("coverage_lock.json must include must_cover_mechanism_content")
    carriers = lock.get("carrier_assignment") or {}
    if not carriers.get("image2_cutout_visual_units"):
        raise ValueError("coverage_lock.json must include carrier_assignment.image2_cutout_visual_units")


def validate_stage2_prompt(path: Path) -> None:
    text = read_required(path).lower()
    required = ["cutout-ready asset board", "coverage lock", "must-cover visual units"]
    for phrase in required:
        if phrase not in text:
            raise ValueError(f"Stage 2 prompt must mention {phrase!r}: {path}")


def validate_project(project_root: Path) -> list[str]:
    analysis = project_root / "analysis"
    checks = [
        lambda: validate_stage1_prompt(analysis / "stage1_prompt.txt"),
        lambda: validate_user_approval(analysis / "stage1_user_approval.md"),
        lambda: validate_aftercare(analysis / "stage1_aftercare.md"),
        lambda: validate_coverage_lock(project_root / "coverage_lock.json"),
        lambda: validate_stage2_prompt(analysis / "stage2_prompt.txt"),
    ]
    errors: list[str] = []
    for check in checks:
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - CLI should report all gate failures.
            errors.append(str(exc))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Image2 cutout PPT generation flow.")
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args(argv)

    errors = validate_project(args.project_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Generation flow gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
