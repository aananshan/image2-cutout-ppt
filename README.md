# Image2 Cutout PPT

## Overview

**English**  
`image2-cutout-ppt` is an Image2-first Codex skill that turns beautiful scientific diagrams into reusable PowerPoint-ready assets. It lets Image2 do what it does best first: freely design a polished mechanism figure, technical roadmap, process diagram, or flowchart. After the user approves the visual direction, the skill generates a clean cutout board, extracts isolated transparent PNG modules, checks crop completeness, and packages everything into an editable PPTX asset library. Instead of fighting with a flat screenshot, you get a reusable figure-building kit.

**中文**  
`image2-cutout-ppt` 是一套 Image2-first 的 Codex skill，用来把 Image2 精美科研图变成 PowerPoint 可复用素材库。它先让 Image2 自由发挥，生成一张完整、美观的科研机制图、技术路线图、流程图或过程图；在用户确认满意后，再把同一套视觉风格拆成干净、独立、便于抠图的模块，自动提取透明 PNG，并打包成可在 PPT 中自由组合、标注和复用的资产库。它不是把一张截图硬塞进幻灯片，而是把一张漂亮图变成一套可编辑、可复用的科研绘图积木。

The workflow is intentionally two-stage:

1. Create a task-local source brief from the user's material; never store domain-specific mechanism content in the skill.
2. Generate a polished Image2 style master first with a source-only prompt: the user's content or the Stage 0 source brief as the entire prompt.
3. Show the Stage 1 image to the user and stop until the user approves the overall style and completeness.
4. After approval, inspect the first image for reusable visual style and save Stage 1 aftercare notes.
5. Write a coverage lock from the user's material, not from Image2's omissions or hallucinations.
6. Generate a clean Image2 asset board from the approved style master and coverage lock, with one complex pictorial object per guide box.
7. Extract each framed object as a transparent PNG cutout and inspect crop completeness.
8. Build a PPTX library containing independent picture objects and editable text labels.

This repository does not include API keys or private Image2 credentials. The intended workflow requires Image2 for both the polished reference diagram and the cutout-ready asset board unless the user explicitly authorizes a fallback. Configure your own Image2/OpenAI-compatible environment, then run the extraction and PPT scripts locally.

## Install

Clone the repository, then copy the skill folder into your Codex skills directory.

```powershell
git clone https://github.com/<owner>/image2-cutout-ppt.git
Copy-Item -Recurse .\image2-cutout-ppt "$env:USERPROFILE\.codex\skills\image2-cutout-ppt"
```

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Usage

Read `image2-cutout-ppt/SKILL.md` for the complete workflow and `image2-cutout-ppt/references/prompts.md` for Image2 prompt templates.

Extract framed cutouts:

```powershell
$SKILL_DIR = ".\image2-cutout-ppt"
python "$SKILL_DIR\scripts\extract_framed_cutouts.py" `
  --source path\to\asset_sheet.png `
  --cut-dir path\to\cutouts `
  --analysis-dir path\to\analysis `
  --asset-ids asset_01,asset_02,asset_03
```

Build a cutout-only PPTX library:

```powershell
$SKILL_DIR = ".\image2-cutout-ppt"
python "$SKILL_DIR\scripts\build_cutout_only_ppt.py" `
  --manifest path\to\cutouts\manifest.json `
  --project-root path\to\project `
  --out path\to\exports\cutout_assets.pptx `
  --preview path\to\analysis\cutout_assets_preview.png
```

Validate stored generation gates:

```powershell
python "$SKILL_DIR\scripts\validate_generation_flow.py" --project-root path\to\project
```

## Test

```powershell
python -m unittest discover -s image2-cutout-ppt\scripts -p "test_*.py"
```

If you have Codex's skill creator validator installed, also run:

```powershell
python path\to\skill-creator\scripts\quick_validate.py image2-cutout-ppt
```

## License

MIT
