---
name: image2-cutout-ppt
description: Use when turning Image2 or other AI-generated scientific mechanism diagrams, technical route maps, process diagrams, flowcharts, or figure concepts into a polished reference image first, then transparent cutout PNG modules and a cutout-only editable PowerPoint asset library.
---

# Image2 Cutout PPT

## Overview

Use a two-stage raster workflow with a coverage lock. First generate a complete polished diagram so Image2 can solve style, composition, visual hierarchy, and scientific storytelling. Then define the mechanism content that must survive conversion before generating a cutout-ready asset board. Do not skip the complete diagram stage unless the user already provides a polished reference image or explicitly asks for assets only.

## Two-Stage Workflow

1. Generate or receive a **complete polished diagram**.
   - Let Image2 make the full beautiful mechanism, technical route map, process diagram, or flowchart.
   - Use this as the aesthetic/style master, not as the direct crop source.
   - Check whether the overall visual style is worth preserving before continuing.
2. Write a **coverage lock** before the cutout-ready asset board.
   - List every mechanism point that must survive: entities, states, branches, validation results, and outcomes.
   - Assign each item to either `Image2 cutout`, `native PPT text`, `native PPT arrow/box`, or `do not include`.
   - Do not let Image2 choose only the most visually salient objects.
   - If a mechanism point needs a pictorial cue, include a dedicated visual unit for it in the asset-board prompt.
3. Use the completed diagram as the visual reference for a **cutout-ready asset board**.
   - Ask Image2 to preserve the style and redraw only complex pictorial objects.
   - Do not preserve the original layout.
   - Exclude text, arrows, simple rectangles, containers, flow lines, panels, cards, labels, and captions.
   - Put one complex object per thin rectangular guide box with generous padding.
   - Use multiple asset boards when the coverage lock has too many visual units for one grid.
4. Extract transparent PNG modules from the framed asset board with `scripts/extract_framed_cutouts.py`.
5. Inspect the detection audit and cutout overview for missing boxes, incomplete crops, unwanted text fragments, object-edge loss, or missing mechanism content.
6. Build a cutout-only PPT asset library with `scripts/build_cutout_only_ppt.py`.
7. Verify the PPT contains independent picture objects and editable text labels only; no redrawn mechanism layout.

## Prompt References

Read `references/prompts.md` when generating images. Use:

- **Stage 1 Complete Polished Diagram** for the first full Image2 generation.
- **Coverage Lock** before the second generation.
- **Stage 2 Cutout-Ready Asset Board** for the second Image2 generation using the completed diagram and coverage lock as references.
- **Stronger Extraction Variant** if the first asset board crops poorly.

## Commands

Extract cutouts:

```powershell
$SKILL_DIR = "path\to\image2-cutout-ppt"
python "$SKILL_DIR\scripts\extract_framed_cutouts.py" `
  --source path\to\asset_sheet.png `
  --cut-dir path\to\cutouts `
  --analysis-dir path\to\analysis `
  --asset-ids lps,ros,tlr4,mitochondrion,nlrp3,cytokine_particles,drug,barrier_injury,cytokine_storm,tissue_fibrosis,empty
```

Build PPT:

```powershell
$SKILL_DIR = "path\to\image2-cutout-ppt"
python "$SKILL_DIR\scripts\build_cutout_only_ppt.py" `
  --manifest path\to\cutouts\manifest.json `
  --project-root path\to\project `
  --out path\to\exports\cutout_assets.pptx `
  --preview path\to\analysis\cutout_assets_preview.png
```

## Validation

Before reporting success:

- Confirm a complete polished diagram exists or the user explicitly skipped stage 1.
- Confirm a coverage lock exists and every required mechanism point is assigned to a cutout or native PPT element.
- Run `python ...\scripts\test_framed_cutouts.py`.
- Run `python ...\scripts\test_cutout_only_ppt.py`.
- Display the overview/preview image.
- Check the generated PPT has picture objects for all cutouts.
- Check non-picture objects are only text boxes.
- Mention any incomplete crops, missing expected objects, or text fragments.

## Common Mistakes

- Do not start with the asset board when the user wants a beautiful mechanism figure; that loses Image2's composition advantage.
- Do not let the asset board contain only pretty biological objects when the mechanism also needs state changes, loss-of-function branches, validation outcomes, or pathway statuses.
- Do not crop a finished diagram directly when a second asset-board generation can produce cleaner isolated objects.
- Do not ask Image2 for text labels in the asset board; AI text causes dirty cutouts.
- Do not include arrows or simple boxes as cutouts unless the user insists; PPT native shapes are cleaner.
- Do not force everything into one image; use multiple asset boards when required for full coverage.
- Do not trust the cutout count blindly; inspect the detection audit before using the PPT.
