from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPT = Path(__file__).with_name("extract_framed_cutouts.py")


def load_module():
    spec = importlib.util.spec_from_file_location("extract_framed_cutouts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FramedCutoutTests(unittest.TestCase):
    def make_sheet(self) -> Image.Image:
        sheet = Image.new("RGB", (520, 240), "#EAF0F6")
        draw = ImageDraw.Draw(sheet)
        draw.rectangle((24, 24, 224, 216), outline="#5B6F8C", width=3)
        draw.rectangle((292, 24, 492, 216), outline="#5B6F8C", width=3)
        draw.rounded_rectangle(
            (74, 74, 174, 154),
            radius=28,
            fill=(252, 252, 248),
            outline=(45, 110, 70),
            width=4,
        )
        draw.rectangle((74, 74, 124, 154), fill=(30, 140, 60), outline=(45, 110, 70), width=4)
        return sheet

    def test_detect_guide_boxes_finds_rectangular_crop_guides(self):
        mod = load_module()
        boxes = mod.detect_guide_boxes(self.make_sheet(), min_width=120, min_height=120)

        self.assertEqual(2, len(boxes))
        self.assertLess(boxes[0][0], boxes[1][0])

    def test_extract_framed_cutouts_skips_empty_boxes_and_preserves_white_foreground(self):
        mod = load_module()
        records = mod.extract_framed_cutouts(self.make_sheet(), min_foreground_pixels=500)

        self.assertEqual(1, len(records))
        cutout = records[0]["image"]
        self.assertEqual(0, cutout.getpixel((0, 0))[3])
        self.assertGreater(cutout.getpixel((cutout.width - 35, cutout.height // 2))[3], 220)

    def test_background_removal_clears_enclosed_chroma_key_holes(self):
        mod = load_module()
        cell = Image.new("RGB", (120, 90), "#FF00FF")
        draw = ImageDraw.Draw(cell)
        draw.ellipse((25, 15, 95, 75), outline=(180, 70, 90), width=5)

        result = mod.remove_border_connected_background(cell)

        self.assertEqual(0, result.getpixel((60, 45))[3])
        self.assertGreater(result.getpixel((25, 45))[3], 220)


if __name__ == "__main__":
    unittest.main()
