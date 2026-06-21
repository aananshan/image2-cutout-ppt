from __future__ import annotations

import json
import math
import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images" / "image2_framed_chromakey_sheet_v3.png"
CUT_DIR = ROOT / "cutouts" / "framed_chromakey_v3"
ANALYSIS_DIR = ROOT / "analysis"

ASSET_IDS = [
    "lps",
    "ros",
    "tlr4",
    "mitochondrion",
    "nlrp3",
    "cytokine_particles",
    "drug",
    "barrier_injury",
    "cytokine_storm",
    "tissue_fibrosis",
    "empty",
]


def row_major(boxes: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    if not boxes:
        return []
    heights = [box[3] for box in boxes]
    row_tol = max(20, int(np.median(heights) * 0.35))
    rows: list[list[tuple[int, int, int, int]]] = []
    for box in sorted(boxes, key=lambda b: (b[1] + b[3] / 2, b[0])):
        cy = box[1] + box[3] / 2
        for row in rows:
            row_cy = sum(item[1] + item[3] / 2 for item in row) / len(row)
            if abs(cy - row_cy) <= row_tol:
                row.append(box)
                break
        else:
            rows.append([box])
    rows.sort(key=lambda row: sum(item[1] for item in row) / len(row))
    ordered: list[tuple[int, int, int, int]] = []
    for row in rows:
        ordered.extend(sorted(row, key=lambda b: b[0]))
    return ordered


def detect_guide_boxes(
    image: Image.Image,
    min_width: int = 120,
    min_height: int = 120,
    min_fill_ratio: float = 0.90,
) -> list[tuple[int, int, int, int]]:
    bgr = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates: list[tuple[int, int, int, int]] = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        x, y, w, h = cv2.boundingRect(contour)
        if len(approx) != 4 or w < min_width or h < min_height:
            continue
        area = cv2.contourArea(contour)
        if area / max(1, w * h) < min_fill_ratio:
            continue
        candidates.append((int(x), int(y), int(w), int(h)))

    deduped: list[tuple[int, int, int, int]] = []
    for box in sorted(candidates, key=lambda b: b[2] * b[3], reverse=True):
        x, y, w, h = box
        cx, cy = x + w / 2, y + h / 2
        if all(abs(cx - (bx + bw / 2)) > 30 or abs(cy - (by + bh / 2)) > 30 for bx, by, bw, bh in deduped):
            deduped.append(box)
    return row_major(deduped)


def trim_alpha(image: Image.Image, pad: int = 14) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image
    x0, y0, x1, y1 = bbox
    return image.crop(
        (
            max(0, x0 - pad),
            max(0, y0 - pad),
            min(image.width, x1 + pad),
            min(image.height, y1 + pad),
        )
    )


def remove_border_connected_background(
    image: Image.Image,
    distance_threshold: float = 42.0,
    global_background_threshold: float = 72.0,
    alpha_threshold: int = 16,
) -> Image.Image:
    rgba = np.array(image.convert("RGBA"))
    rgb = rgba[:, :, :3].astype(np.float32)
    h, w = rgb.shape[:2]
    band = max(2, min(h, w) // 30)
    samples = np.concatenate(
        [
            rgb[:band, :, :].reshape(-1, 3),
            rgb[-band:, :, :].reshape(-1, 3),
            rgb[:, :band, :].reshape(-1, 3),
            rgb[:, -band:, :].reshape(-1, 3),
        ],
        axis=0,
    )
    background = np.median(samples, axis=0)
    background_chroma = float(background.max() - background.min())
    distance = np.linalg.norm(rgb - background, axis=2)
    candidate = (distance <= distance_threshold).astype(np.uint8)
    strict_background = (distance <= global_background_threshold) if background_chroma >= 80 else np.zeros_like(distance, dtype=bool)

    count, labels = cv2.connectedComponents(candidate, connectivity=8)
    if count > 1:
        border_labels = set(np.unique(labels[0, :]))
        border_labels.update(np.unique(labels[-1, :]))
        border_labels.update(np.unique(labels[:, 0]))
        border_labels.update(np.unique(labels[:, -1]))
        border_labels.discard(0)
        if border_labels:
            background_mask = np.isin(labels, list(border_labels))
            rgba[:, :, 3] = np.where(background_mask, 0, rgba[:, :, 3])

    rgba[:, :, 3] = np.where(strict_background, 0, rgba[:, :, 3])
    rgba[:, :, 3] = np.where(rgba[:, :, 3] <= alpha_threshold, 0, rgba[:, :, 3])
    return Image.fromarray(rgba)


def crop_cell(image: Image.Image, box: tuple[int, int, int, int], border_trim: int = 10) -> Image.Image:
    x, y, w, h = box
    left = min(x + border_trim, x + w)
    top = min(y + border_trim, y + h)
    right = max(left, x + w - border_trim)
    bottom = max(top, y + h - border_trim)
    return image.crop((left, top, right, bottom))


def foreground_count(image: Image.Image, alpha_threshold: int = 16) -> int:
    alpha = np.array(image.convert("RGBA").getchannel("A"))
    return int((alpha > alpha_threshold).sum())


def extract_framed_cutouts(
    image: Image.Image,
    min_foreground_pixels: int = 2500,
    border_trim: int = 10,
    trim_pad: int = 16,
) -> list[dict]:
    boxes = detect_guide_boxes(image)
    records: list[dict] = []
    for index, box in enumerate(boxes):
        cell = crop_cell(image, box, border_trim=border_trim)
        cutout = trim_alpha(remove_border_connected_background(cell), pad=trim_pad)
        pixels = foreground_count(cutout)
        if pixels < min_foreground_pixels:
            continue
        asset_id = ASSET_IDS[index] if index < len(ASSET_IDS) else f"asset_{index + 1:02d}"
        if asset_id == "empty":
            asset_id = f"asset_{index + 1:02d}"
        records.append(
            {
                "id": asset_id,
                "index": index + 1,
                "box": list(box),
                "foreground_pixels": pixels,
                "size_px": [cutout.width, cutout.height],
                "image": cutout,
            }
        )
    return records


def write_detection_audit(image: Image.Image, records: list[dict], boxes: list[tuple[int, int, int, int]], out: Path) -> None:
    audit = image.convert("RGB")
    draw = ImageDraw.Draw(audit)
    used = {tuple(record["box"]) for record in records}
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for index, box in enumerate(boxes, 1):
        x, y, w, h = box
        color = (20, 145, 70) if tuple(box) in used else (145, 145, 145)
        draw.rectangle((x, y, x + w, y + h), outline=color, width=5)
        draw.text((x + 10, y + 10), str(index), fill=color, font=font)
    audit.save(out)


def write_overview(records: list[dict], out: Path) -> None:
    cols = 4
    tile_w, tile_h = 360, 260
    pad = 24
    rows = max(1, math.ceil(len(records) / cols))
    sheet = Image.new("RGB", (cols * tile_w + (cols + 1) * pad, rows * tile_h + (rows + 1) * pad), "white")
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for index, rec in enumerate(records):
        col, row = index % cols, index // cols
        x = pad + col * (tile_w + pad)
        y = pad + row * (tile_h + pad)
        tile = Image.new("RGBA", (tile_w, tile_h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(tile)
        draw.rectangle((0, 0, tile_w - 1, tile_h - 1), outline=(190, 198, 210), width=1)
        draw.text((10, 8), rec["id"], fill=(20, 32, 58), font=font)
        for yy in range(42, tile_h - 10, 14):
            for xx in range(10, tile_w - 10, 14):
                if (xx // 14 + yy // 14) % 2:
                    draw.rectangle((xx, yy, min(xx + 13, tile_w - 11), min(yy + 13, tile_h - 11)), fill=(232, 236, 242))
        cut = rec["image"]
        max_w, max_h = tile_w - 30, tile_h - 60
        scale = min(max_w / cut.width, max_h / cut.height, 1.4)
        shown = cut.resize((max(1, round(cut.width * scale)), max(1, round(cut.height * scale))), Image.Resampling.LANCZOS)
        tile.alpha_composite(shown, ((tile_w - shown.width) // 2, 48 + (max_h - shown.height) // 2))
        sheet.paste(tile.convert("RGB"), (x, y))
    sheet.save(out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract transparent cutouts from an Image2 framed asset sheet.")
    parser.add_argument("--source", type=Path, default=SRC, help="Input asset sheet with visible rectangular guide boxes.")
    parser.add_argument("--cut-dir", type=Path, default=CUT_DIR, help="Directory for transparent PNG cutouts and manifest.json.")
    parser.add_argument("--analysis-dir", type=Path, default=ANALYSIS_DIR, help="Directory for audit/overview images.")
    parser.add_argument("--min-foreground-pixels", type=int, default=2500, help="Skip guide boxes with fewer foreground pixels.")
    parser.add_argument("--border-trim", type=int, default=10, help="Pixels to trim from inside each guide box border.")
    parser.add_argument("--trim-pad", type=int, default=16, help="Padding to keep around nontransparent content.")
    parser.add_argument("--asset-ids", default=",".join(ASSET_IDS), help="Comma-separated ids assigned in row-major guide-box order.")
    return parser.parse_args()


def write_outputs(
    source_path: Path = SRC,
    cut_dir: Path = CUT_DIR,
    analysis_dir: Path = ANALYSIS_DIR,
    min_foreground_pixels: int = 2500,
    border_trim: int = 10,
    trim_pad: int = 16,
    asset_ids: list[str] | None = None,
) -> dict:
    global ASSET_IDS
    old_asset_ids = ASSET_IDS
    if asset_ids is not None:
        ASSET_IDS = asset_ids
    cut_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(source_path).convert("RGB")
    boxes = detect_guide_boxes(source)
    records = extract_framed_cutouts(
        source,
        min_foreground_pixels=min_foreground_pixels,
        border_trim=border_trim,
        trim_pad=trim_pad,
    )
    manifest = []
    for rec in records:
        image = rec.pop("image")
        path = cut_dir / f"{rec['id']}.png"
        image.save(path)
        try:
            rec["path"] = str(path.relative_to(cut_dir.parent))
        except ValueError:
            rec["path"] = str(path)
        manifest.append(rec)
    manifest_path = cut_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    audit_path = analysis_dir / "framed_cutout_detection_audit.png"
    overview_path = analysis_dir / "framed_cutouts_overview.png"
    write_detection_audit(source, manifest, boxes, audit_path)
    overview_records = []
    for rec in manifest:
        image_path = Path(rec["path"])
        if not image_path.is_absolute():
            image_path = cut_dir.parent / image_path
        overview_records.append({**rec, "image": Image.open(image_path).convert("RGBA")})
    write_overview(overview_records, overview_path)
    ASSET_IDS = old_asset_ids
    return {
        "source": str(source_path),
        "boxes": len(boxes),
        "cutouts": len(manifest),
        "cutout_dir": str(cut_dir),
        "manifest": str(manifest_path),
        "audit": str(audit_path),
        "overview": str(overview_path),
    }


def main() -> None:
    args = parse_args()
    asset_ids = [item.strip() for item in args.asset_ids.split(",") if item.strip()]
    print(
        json.dumps(
            write_outputs(
                source_path=args.source,
                cut_dir=args.cut_dir,
                analysis_dir=args.analysis_dir,
                min_foreground_pixels=args.min_foreground_pixels,
                border_trim=args.border_trim,
                trim_pad=args.trim_pad,
                asset_ids=asset_ids,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
