# Prompt Patterns

## Stage 1 Complete Polished Diagram

Use this for the first Image2 generation. Stage 1 must be generated with Image2 unless the user explicitly authorizes a fallback. The goal is a beautiful complete diagram, not cutouts.

```text
Create a complete polished scientific mechanism diagram / technical route map / process flow figure.

Design the full composition with strong visual hierarchy, coherent scientific storytelling, balanced spacing, professional color palette, and high-end publication-style illustration quality. Make the diagram visually beautiful and internally consistent. Use elegant pictorial modules, clean spatial grouping, clear directional flow, and polished biomedical / engineering / software / technical illustration style as appropriate for the subject.

Text may be omitted or kept as simple placeholders if exact wording is uncertain. Prioritize visual style, module design, composition, and complete object appearance. Avoid clutter. Keep all important objects fully visible and avoid excessive overlap.

Return one complete high-resolution diagram image.
```

## Coverage Lock

Write this checklist before Stage 2. The agent should fill it from the paper, user notes, or Stage 1 diagram.

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

## Missing Content Warning

Do not repeat this failure pattern: an asset board that contains only the prettiest foreground objects but loses state changes, loss-of-function branches, validation outcomes, pathway statuses, or final phenotypes. Those items must appear in the coverage lock and be assigned to either cutout visual units or native PPT text/shapes.

## Stronger Extraction Variant

Append this when prior crops were incomplete:

```text
Make every object smaller inside its guide box, with at least 20 percent empty margin on all sides. Use rectangular guide boxes that are clearly separated and perfectly detectable. Each object must be whole, centered, and isolated. Avoid any object touching the guide border or another object. Do not crop or truncate any part of the object.
```
