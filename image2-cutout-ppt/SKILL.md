---
name: image2-cutout-ppt
description: Use when turning Image2-generated scientific mechanism diagrams, technical route maps, process diagrams, flowcharts, or figure concepts into a polished reference image first, then transparent cutout PNG modules and a cutout-only editable PowerPoint asset library.
---

# Image2 Cutout PPT

## Overview

Use an Image2-first two-stage raster workflow with mandatory generation gates. Stage 1 must use Image2 with a minimal source-only prompt: the user's requested figure content, or a concise Stage 0 source brief, as the entire prompt. Do not add a fixed wrapper, style block, layout instruction, no-text policy, or cutout instruction. Stage 1 is a free style master, not a content lock. After Stage 1, show the image and stop for user approval before any Stage 2 work. Stage 2 must use Image2 again, with the approved Stage 1 image and coverage lock as references, to generate the cutout-ready asset board. Do not substitute another image generator, SVG renderer, slide generator, or manual redraw path unless the user explicitly authorizes a fallback.

If Image2 is unavailable, stop and report the missing Image2 access or configuration. Do not silently downgrade to another generator. Do not skip the complete diagram stage unless the user already provides a polished Image2 reference image or explicitly asks for assets only.

## Strict Generation Workflow

0. Create a task-local **Stage 0 source brief** from the user's content, paper, sketch, or notes.
   - Keep it task-specific. Do not store domain-specific mechanism content inside this skill.
   - Use ASCII for fragile symbols when needed, such as `alpha-Mangostin` instead of a Greek letter that may be corrupted.
1. Pass the **Stage 1 prompt audit** before generating the style master.
   - Must use Image2 with a source-only Stage 1 prompt.
   - The exact Image2 prompt must be only the user's content or the Stage 0 source brief. Do not add a wrapper such as "Make this into a polished diagram".
   - Do not read coverage_lock, coverage_lock.json, Stage 2 prompts, asset lists, or cutout requirements while constructing Stage 1.
   - Forbidden in Stage 1: fixed wrapper, fixed style prompt, preferred composition, text policy, no-readable-text rules, guide boxes, asset board language, cutout-ready language, row-major order, editable PowerPoint label zones, and fixed color palettes.
   - Save the exact prompt as `analysis/stage1_prompt.txt`.
2. Generate or receive a **complete polished Image2 diagram**.
   - Use this as the style master, not as the content source of truth or direct crop source.
   - Do not judge Stage 1 by exact text, exact coverage, or crop readiness.
   - Check whether the overall visual style is worth preserving before continuing.
3. Pass the **Stage 1 user approval gate**.
   - Display the Stage 1 image to the user.
   - Ask whether the overall style and completeness are good enough to continue to the cutout-ready Stage 2.
   - Do not write the coverage lock, Stage 2 prompt, asset board, cutouts, or PPT until the user approves Stage 1.
   - If the user is not satisfied, regenerate Stage 1 using only the original source content plus the user's explicit revision feedback. Keep Stage 2 terms out of the prompt.
   - Save the approval record as `analysis/stage1_user_approval.md`.
4. Pass the **Stage 1 aftercare gate**.
   - Record visual language worth preserving: object style, module shapes, color palette, rendering texture, layout density, and visual motifs.
   - Identify obvious style problems that would hurt Stage 2, such as severe clutter, unreadable object boundaries, or a look that does not match the requested figure type.
   - Compare the Stage 1 image with the user's actual content; do not copy Image2's omissions into the next step.
   - Save this as `analysis/stage1_aftercare.md` before writing the coverage lock.
5. Pass the **coverage lock source gate**.
   - List every mechanism point that must survive: entities, states, branches, validation results, and outcomes.
   - Assign each item to either `Image2 cutout`, `native PPT text`, `native PPT arrow/box`, or `do not include`.
   - Write the coverage lock from the user's content, paper, sketch, or notes, not from Stage 1 visual omissions or hallucinated additions.
   - Do not let Image2 choose only the most visually salient objects.
   - If a mechanism point needs a pictorial cue, include a dedicated visual unit for it in the asset-board prompt.
   - Save this as `coverage_lock.json` or `coverage_lock.md`.
6. Pass the **Stage 2 prompt audit**, then use the completed diagram as the visual reference for a **cutout-ready asset board**.
   - Must use Image2 for the asset board unless the user explicitly authorizes a fallback.
   - Ask Image2 to preserve the style and redraw only complex pictorial objects.
   - Do not preserve the original layout.
   - Exclude text, arrows, simple rectangles, containers, flow lines, panels, cards, labels, and captions.
   - Put one complex object per thin rectangular guide box with generous padding.
   - Use multiple asset boards when the coverage lock has too many visual units for one grid.
   - Save the exact prompt as `analysis/stage2_prompt.txt`.
7. Run `scripts/validate_generation_flow.py --project-root <project>` before extracting cutouts when these files exist.
8. Extract transparent PNG modules from the framed asset board with `scripts/extract_framed_cutouts.py`.
9. Inspect the detection audit and cutout overview for missing boxes, incomplete crops, unwanted text fragments, object-edge loss, or missing mechanism content.
10. Build a cutout-only PPT asset library with `scripts/build_cutout_only_ppt.py`.
11. Verify the PPT contains independent picture objects and editable text labels only; no redrawn mechanism layout.

## Prompt References

Read `references/prompts.md` when generating images. Use:

- **Stage 1 Source-Only Style-Master Prompt** for the first Image2 generation.
- **Stage 1 User Approval** immediately after the first image is generated.
- **Stage 1 Aftercare** after the first image is generated.
- **Coverage Lock** before the second generation.
- **Stage 2 Cutout-Ready Asset Board** for the second Image2 generation using the completed diagram and coverage lock as references.
- **Stronger Extraction Variant** if the first asset board crops poorly.
- **Generation Flow Validator** if a project stores `analysis/stage1_prompt.txt`, `analysis/stage1_aftercare.md`, `coverage_lock.json`, and `analysis/stage2_prompt.txt`.

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

Validate generation gates:

```powershell
$SKILL_DIR = "path\to\image2-cutout-ppt"
python "$SKILL_DIR\scripts\validate_generation_flow.py" --project-root path\to\project
```

## Validation

Before reporting success:

- Confirm a complete polished diagram exists or the user explicitly skipped stage 1.
- Confirm Stage 1 and Stage 2 used Image2, or record the user's explicit fallback authorization.
- Confirm `analysis/stage1_prompt.txt` passes the Stage 1 prompt audit.
- Confirm `analysis/stage1_user_approval.md` exists before any Stage 2 artifact.
- Confirm `analysis/stage1_aftercare.md` exists before the coverage lock.
- Confirm a coverage lock exists and every required mechanism point is assigned to a cutout or native PPT element.
- Confirm Stage 2 prompt references the coverage lock and does not ask for a final diagram.
- Run `python ...\scripts\validate_generation_flow.py --project-root <project>` when the project stores generation audit files.
- Run `python ...\scripts\test_framed_cutouts.py`.
- Run `python ...\scripts\test_cutout_only_ppt.py`.
- Display the overview/preview image.
- Check the generated PPT has picture objects for all cutouts.
- Check non-picture objects are only text boxes.
- Mention any incomplete crops, missing expected objects, or text fragments.

## Common Mistakes

- Do not start with the asset board when the user wants a beautiful mechanism figure; that loses Image2's composition advantage.
- Do not substitute other image generators, PPT-master SVG, hand-drawn reconstruction, or native PPT drawing for the Image2 generation stages unless the user explicitly authorizes a fallback.
- Do not let the asset board contain only pretty biological objects when the mechanism also needs state changes, loss-of-function branches, validation outcomes, or pathway statuses.
- Do not continue after Stage 1 until the user explicitly approves the first image.
- Do not build Stage 1 from a wrapper prompt, coverage lock, asset list, preferred composition block, text policy, or cutout prompt.
- Do not infer required mechanism content from the Stage 1 image; infer only style from Stage 1.
- Do not crop a finished diagram directly when a second asset-board generation can produce cleaner isolated objects.
- Do not ask Image2 for text labels in the asset board; AI text causes dirty cutouts.
- Do not include arrows or simple boxes as cutouts unless the user insists; PPT native shapes are cleaner.
- Do not force everything into one image; use multiple asset boards when required for full coverage.
- Do not trust the cutout count blindly; inspect the detection audit before using the PPT.
