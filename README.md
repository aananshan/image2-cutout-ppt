# Image2 Cutout PPT

`image2-cutout-ppt` is an Image2-first Codex skill for turning scientific mechanism diagrams, technical route maps, process diagrams, and flowcharts into transparent cutout PNG modules plus a cutout-only editable PowerPoint asset library.

中文简介：本仓库是一个用于 Codex 的 Image2 科研机制图拆图与 PPT 资产化 skill。流程采用两阶段 Image2：第一阶段只根据用户提供的机制内容自由生成完整、美观的参考图，并在用户确认满意后，第二阶段再根据参考图风格和 coverage lock 生成便于抠图的模块平铺图。随后自动提取透明 PNG 模块，并生成可编辑 PowerPoint 资产库。仓库不包含 API key、论文原文、实验图片或本地中间产物。

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
