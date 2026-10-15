---
name: creator-style-kit
description: Pick and apply one of 18 premium visual styles (fonts, palette, motion grammar, SFX kit) for the user's 9:16 HyperFrames videos — AI model evaluation (评测), tutorials (教程) and science explainers (科普). Use when making, designing or restyling a video or composition for this user, when choosing a 视频风格/画面风格/样式, or when they mention the style kit, 风格样张, or a style by name (数据新闻, 评测仪表, 暗场发布会, 终端控制台, 水墨留白…).
---

# Creator Style Kit

The kit lives in this skill's folder: `KIT=/Volumes/ORICO/Opus/creator-style-kit` (on the ORICO drive — if the path is missing, ask the user to mount it). It is a **design system on top of HyperFrames**: the /hyperframes workflow still owns project setup, narration and rendering; this skill decides how every scene looks, moves and sounds.

## Workflow

1. **Pick the style** (skip if the user named one).
   - `python3 $KIT/scripts/list_styles.py` prints the live catalog (id · name · best_for · essence).
   - Use the table below; recommend **one main style + at most one accent style** for hooks/code segments, with a one-line reason each.
   - Offer the previews: `/Volumes/ORICO/Opus/风格样张_18套_一览.jpg` (stills) and `风格样张_18套.mp4` (motion + sound).
2. **Read the brief before building**: `python3 $KIT/scripts/list_styles.py <id>`. Its `not:` lines are hard rules (one accent, no glow, etc.) — 高级感 comes from obeying them.
3. **Build scenes.** Standard beats (chapter card / headline + list / big number) → write a beats file and run
   `python3 $KIT/scripts/scaffold.py <id> <project> --content beats.json [--init]`
   (`--init` only for a fresh project; otherwise paste the printed host `<div>` into index.html). Custom scenes → follow the markup contract and `kit.*` API in [REFERENCE.md](REFERENCE.md).
   Beat lengths come from the style's pacing (see REFERENCE.md "Pacing"); pass `"dur"` only to stretch a beat to its narration — never to squeeze it.
4. **Re-subset fonts after all text is final**: `python3 $KIT/scripts/build_style.py <id> <project>` (once per style used). Fonts only contain glyphs present in the project's .html at build time — stale builds show tofu/fallback glyphs.
5. **Verify the picture**: `npx hyperframes check` then `npx hyperframes snapshot --at …` at each beat's "holds until" time (in the generated script comments) — everything should be settled there (emphasis visible, nothing overflowing, accent used once).
6. **Sound pass** after rendering: `python3 $KIT/scripts/sound_pass.py <project> renders/<x>.mp4 [--voice vo.wav] [--music bed.wav]`. Fix every FAIL by changing cues or sounds (≤ 2 rounds), look at `audio/qa.png`, and hand over `out/final.mp4` + `LISTEN.md`. Report what the checks show; don't call the sound good — the user listens.

## Which style

| Scene | Main | Alternative |
|---|---|---|
| Benchmark results, score reveal | `data-journal` 数据新闻 | `benchmark-hud` 评测仪表 |
| Model A vs B, version upgrades | `data-journal` | `instrument-panel` 仪器面板 |
| Specs: price / speed / context | `instrument-panel` | `swiss-grid` 瑞士网格 |
| Launch opener, title card | `frosted-aurora` 弥散玻璃 | `dark-keynote` 暗场发布会, `particle-field` 粒子星云 |
| Paper / tech-report explainer | `paper-figure` 论文图表 | `manim-morph` 数学动画 |
| How it works (attention, reasoning) | `manim-morph` | `particle-field` |
| Architecture, agent workflow | `blueprint` 蓝图线稿 | `isometric-stack` 等轴架构 |
| Layers (tech stack, context makeup) | `isometric-stack` | `blueprint` |
| Concept frameworks, "3 elements" | `bauhaus-geometry` 包豪斯构成 | `swiss-grid` |
| Claude / Opus topics, opinion pieces | `clay-serif` 暖陶书卷 | `editorial-paper` 报刊纸感 |
| Screen recordings, prompts, code | `dev-console` 终端控制台 | `instrument-panel` |
| Beginner tutorial, friendly tone | `warm-notebook` 暖调手账 | `clay-serif` |
| History / culture / festival specials | `ink-wash` 水墨留白 | `editorial-paper` |
| First-3-second hook, chapter stings | `poster-kinetic` 海报撞色 | `bauhaus-geometry` |

Typical pairing: an evaluation video in `data-journal`, opened with `frosted-aurora`, with code segments cut to `dev-console`. Don't use `poster-kinetic` or `benchmark-hud` for a whole video (they tire fast; HUD looks are common in AI videos).

## Rules that always apply

- **Never invent benchmark numbers.** Use figures the user supplies or that you can cite; put the citation in the beats file's `source` (data-journal footer) or `caption` (paper-figure). Placeholder figures must be labelled 示例数据 on screen.
- **No logos or brand marks.** `clay-serif` borrows Anthropic's public palette only.
- One `<em>` per beat: it marks the single emphasised word and drives the emphasis effect.
- Sound stays sparse: each style's `sound.rules` (maxPerSecond, silentShare) caps the density, enforced by compose.py. Don't add cues by hand on top; one sound per list, the reveal on the lock.
- Pace for reading, not for speed: one thing moves at a time, the key figure holds ≥ 2 s. If a video feels slow, cut content — don't shorten holds.
- All layouts are 1080×1920 (9:16). A 16:9 video needs new layouts — say so instead of stretching.

## Extending

To add a style, change a palette, or fix a layout, see "Adding a style" in [REFERENCE.md](REFERENCE.md). Then regenerate the previews with `python3 $KIT/scripts/lookbook.py $KIT/lookbook` and render.
