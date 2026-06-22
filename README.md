# Image2 Cutout PPT

`image2-cutout-ppt` is an Image2-first Codex skill for turning scientific mechanism diagrams, technical route maps, process diagrams, and flowcharts into transparent cutout PNG modules plus a cutout-only editable PowerPoint asset library.

The workflow is intentionally two-stage:

1. Generate a complete polished Image2 reference diagram first.
2. Write a coverage lock so every required mechanism point is assigned to an output carrier.
3. Generate a clean Image2 asset board from the reference image, with one complex pictorial object per guide box.
4. Extract each framed object as a transparent PNG cutout.
5. Build a PPTX library containing independent picture objects and editable text labels.

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

## Test

```powershell
python image2-cutout-ppt\scripts\test_skill_docs.py
python image2-cutout-ppt\scripts\test_framed_cutouts.py
python image2-cutout-ppt\scripts\test_cutout_only_ppt.py
```

If you have Codex's skill creator validator installed, also run:

```powershell
python path\to\skill-creator\scripts\quick_validate.py image2-cutout-ppt
```

## License

MIT
