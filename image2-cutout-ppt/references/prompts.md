# Prompt Patterns

## Stage 1 Source-Only Style-Master Prompt

Use this for the first Image2 generation. Stage 1 must be generated with Image2 unless the user explicitly authorizes a fallback. The goal is a useful style master, not content locking, crop-readiness, or exact text.

Create a task-local Stage 0 source brief from the user's content, paper, sketch, or notes. The brief may describe the mechanism in plain words, but it must not contain layout instructions, extraction instructions, guide-box instructions, fixed color palettes, or the coverage lock. The skill must never store domain-specific mechanism content in its own files.

Do not add a fixed wrapper. Do not add a fixed style prompt, domain-specific style language, journal-style adjectives, or extraction constraints. Send only the user's own content or the Stage 0 source brief as the entire Image2 prompt. If the user gives one sentence, send that one sentence. If the source is a long paper or messy notes, first compress it into a factual source brief, then send only that brief.

```text
[User content or Stage 0 source brief only]
```

Forbidden in Stage 1: fixed wrapper text, coverage lock, preferred composition, text policy, no readable text, guide box, asset board, cutout-ready, row-major order, leave open space for editable PowerPoint labels, and fixed color palette.

Save the exact Stage 1 prompt as `analysis/stage1_prompt.txt`. Run the Stage 1 prompt audit before calling Image2.

## Stage 1 User Approval

After Stage 1, display the generated image and stop. Ask the user whether the first image is good enough as the style master before continuing to Stage 2. Do not write the coverage lock, Stage 2 prompt, asset board, cutouts, or PPT until the user approves.

Suggested user-facing question:

```text
第一版整体风格和完整度满意吗？满意的话我再进入可抠图第二版；不满意的话我只按你的反馈重生第一版。
```

If the user is not satisfied, regenerate Stage 1 using the original content plus the user's explicit revision feedback. Keep Stage 2 terms out of the new Stage 1 prompt.

Save the approval record as `analysis/stage1_user_approval.md`.

## Stage 1 Aftercare

After the user approves Stage 1, inspect the image as a style master. Do not treat it as the content source of truth. Record the visual language worth preserving: object style, module shapes, color palette, rendering texture, layout density, and any visual motifs. Then compare the user's actual content against the Stage 1 image and write the coverage lock from the user's content, not from Image2's omissions. Do not infer required mechanism content from the Stage 1 image. Stage 2 receives both the approved Stage 1 image for style and the coverage lock for required content.

Save `analysis/stage1_aftercare.md` before creating or finalizing the coverage lock. This file should contain: style notes, Stage 1 omissions or hallucinations, and the decision to preserve or regenerate the style master.

## Coverage Lock

Write this checklist before Stage 2. Fill it from the paper, user notes, sketch, or other user-provided source material. Do not fill it from Stage 1 visual omissions or hallucinated additions.

```text
Coverage lock for Stage 2:

Must-cover mechanism content:
1. [entity / state / branch / outcome]
2. [entity / state / branch / outcome]
3. [...]

Carrier assignment:
- Image2 cutout visual units: [objects or state icons that must become PNG modules]
- Native PPT text: [labels, low/high states, assay names, pathway names]
- Native PPT arrows/boxes: [connectors, inhibition bars, lanes, panels]
- Excluded: [items intentionally omitted]

Stage 2 must include all Image2 cutout visual units. Do not omit any listed unit. Do not let Image2 choose only the most visually salient objects. If the list is too long for one clean grid, split it into multiple asset boards and generate Board A, Board B, etc.
```

## Stage 2 Cutout-Ready Asset Board

Use this for the second Image2 generation. Stage 2 must be generated with Image2 unless the user explicitly authorizes a fallback. Provide the Stage 1 Image2 image and the coverage lock as references.

```text
Use the completed diagram as the visual reference for style and object design.

Create a cutout-ready asset board, not a final diagram.

Extract and redraw the must-cover visual units listed in the coverage lock. Keep the same illustration style, color palette, shading, line quality, and visual identity from the completed diagram.

Do not preserve the original composition. Do not include readable text, labels, captions, arrows, connectors, flow lines, panels, cards, containers, plain rectangles, timelines, UI boxes, legends, axes, or diagram layout scaffolding. Do not include cropped fragments of text.

Place each visual unit in its own separate thin rectangular guide box. Use one complete unit per box. Use a crisp visible border around every guide box. Keep at least 15 percent empty margin on all sides inside each box. Every unit must be complete, centered, isolated, and fully visible. No unit may touch or cross the guide border. No overlapping units.

Arrange the boxes in the exact row-major order provided in the coverage lock. Leave empty guide boxes if fewer units are needed. Keep high contrast and complete object boundaries. Avoid shadows, glow, blur, or background effects that merge with the object edge.

Do not omit any listed unit. If the list is too long for one clean image, generate only the requested board range, for example Board A units 1-12, then wait for Board B.

Return a single high-resolution image suitable for automated cropping, background removal, and conversion into a PowerPoint asset library.
```

Save the exact Stage 2 prompt as `analysis/stage2_prompt.txt`. Run the Stage 2 prompt audit before calling Image2.

## Missing Content Warning

Do not repeat this failure pattern: an asset board that contains only the prettiest foreground objects but loses state changes, loss-of-function branches, validation outcomes, pathway statuses, or final phenotypes. Those items must appear in the coverage lock and be assigned to either cutout visual units or native PPT text/shapes.

## Stronger Extraction Variant

Append this when prior crops were incomplete:

```text
Make every object smaller inside its guide box, with at least 20 percent empty margin on all sides. Use rectangular guide boxes that are clearly separated and perfectly detectable. Each object must be whole, centered, and isolated. Avoid any object touching the guide border or another object. Do not crop or truncate any part of the object.
```
