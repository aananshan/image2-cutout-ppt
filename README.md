# Image2 Cutout PPT

## 痛点 / Why This Exists

**中文**  
现在用 Image2 做科研机制图、技术路线图和流程图时，最尴尬的地方不是“画不漂亮”，而是“漂亮之后不好用”：整张图是一张扁平图片，PPT 里改不了；直接抠原图容易裁切不完整、把文字和箭头一起抠进去；让 AI 再生成一版抠图素材时，又容易漏模块、改错内容，甚至把第二阶段的提示词污染到第一张参考图里。

`image2-cutout-ppt` 就是为了解决这个断点：保留 Image2 最强的审美和构图能力，同时把最终结果变成可检查、可拆分、可复用、可在 PowerPoint 里继续编辑的科研绘图资产。

**English**  
Image2 can make scientific diagrams look great, but the hard part starts after the image is generated. A polished diagram is still a flat screenshot: hard to edit in PowerPoint, easy to crop incorrectly, and prone to carrying unwanted text, arrows, or broken fragments into downstream assets. A second AI generation can also omit key modules or contaminate the first creative prompt with extraction rules.

`image2-cutout-ppt` bridges that gap. It preserves Image2's visual strengths while turning the result into auditable, reusable, PowerPoint-friendly figure assets.

## 简介 / Overview

**English**  
`image2-cutout-ppt` is an Image2-first Codex skill that turns beautiful scientific diagrams into reusable PowerPoint-ready assets. It lets Image2 do what it does best first: freely design a polished mechanism figure, technical roadmap, process diagram, or flowchart. After the user approves the visual direction, the skill generates a clean cutout board, extracts isolated transparent PNG modules, checks crop completeness, and packages everything into an editable PPTX asset library. Instead of fighting with a flat screenshot, you get a reusable figure-building kit.

**中文**  
`image2-cutout-ppt` 是一套 Image2-first 的 Codex skill，用来把 Image2 精美科研图变成 PowerPoint 可复用素材库。它先让 Image2 自由发挥，生成一张完整、美观的科研机制图、技术路线图、流程图或过程图；在用户确认满意后，再把同一套视觉风格拆成干净、独立、便于抠图的模块，自动提取透明 PNG，并打包成可在 PPT 中自由组合、标注和复用的资产库。它不是把一张截图硬塞进幻灯片，而是把一张漂亮图变成一套可编辑、可复用的科研绘图积木。

## 工作流程 / Workflow

**中文流程**  

1. 根据用户的主题、论文、草图或笔记，整理任务本地的 Stage 0 source brief，不把具体领域内容写进 skill 本体。
2. 第一阶段只把用户内容或 Stage 0 source brief 发给 Image2，让它自由生成完整、美观的参考图，不加入排版、无文字、抠图或素材板约束。
3. 展示第一版参考图，并停下来等用户确认整体风格和完整度。
4. 用户确认后，记录第一版值得保留的视觉语言，例如对象风格、模块形状、配色、质感和构图密度。
5. 从用户材料中写 coverage lock，明确哪些实体、状态、分支、验证结果和结论必须保留，而不是从第一版图的遗漏或幻觉里反推内容。
6. 第二阶段用已确认的第一版图作为风格参考，用 coverage lock 锁定内容，生成干净的可抠图 asset board：一个复杂图案一个框，不要文字、箭头、普通框线或流程布局。
7. 从 asset board 中提取透明 PNG 模块，检查是否有裁切不完整、边缘丢失、混入文字或遗漏模块。
8. 生成 cutout-only PPTX 资产库，让每个图案都成为独立图片对象，后续文字、箭头和流程关系用 PowerPoint 原生元素编辑。

**English Workflow**  

1. Create a task-local Stage 0 source brief from the user's topic, paper, sketch, or notes, without storing domain-specific content in the skill itself.
2. Send only the user content or Stage 0 source brief to Image2 for Stage 1, letting it freely generate a complete and polished reference diagram without layout, no-text, cutout, or asset-board constraints.
3. Show the Stage 1 reference image and stop until the user approves the overall style and completeness.
4. After approval, record the visual language worth preserving: object style, module shapes, palette, texture, and layout density.
5. Write the coverage lock from the user's source material, listing the entities, states, branches, validation results, and outcomes that must survive. Do not infer required content from Stage 1 omissions or hallucinations.
6. Use the approved Stage 1 image for style and the coverage lock for content to generate a clean Stage 2 cutout-ready asset board: one complex pictorial unit per box, with no text, arrows, plain boxes, or final flow layout.
7. Extract transparent PNG modules from the asset board and inspect crop completeness, edge loss, text fragments, and missing modules.
8. Build a cutout-only PPTX asset library where each visual unit is an independent picture object, while text, arrows, and process structure stay editable with native PowerPoint elements.

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
