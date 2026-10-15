# Opus 5.5 style ecosystem: candidate premium directions for AI 评测 / 教程 / 科普 (9:16)

Researched 2026-10-09. This extends `github.md` section (a). It does not repeat what is already there: lemo-opuscar `swiss-motion` / `dark-keynote`, kinetic-reel, vox-style-animation, motion-video-kit, bang-motion and so on.

Unless marked otherwise, every value below was read from a file fetched in this session, through raw.githubusercontent.com or the `gh api` contents endpoint. jsDelivr's flat listing for lemo-opuscar returns **403 "Package size exceeded 50 MB"**, so the GitHub contents API was used to enumerate the styles. WebSearch hit its session limit after 3 queries, so the remaining discovery used `gh search repos`. Anything not opened is marked *(unverified)*.

The lemo-opuscar films are **1920×1080, 24 fps**, with hold rules in seconds. The pixel sizes quoted here are theirs. For 1080×1920, scale type by about 1.0–1.15 (the frame width drops from 1920 to 1080, but phone viewing distance is shorter) and re-place the subtitle zones yourself.

---

## 1. Sources

| # | Source | License | What is useful |
|---|---|---|---|
| S1 | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) `styles/<x>/STYLE.md` + `DEMO.md` (1,469★, pushed 2026-10-09) | MIT (LICENSE file "Copyright (c) 2026 LemoLab"; API says NOASSERTION) | 43 styles, all on the same 11-section schema. **Read in full for this report:** blueprint, dataviz, hologram-hud, iso-infographic, glass-product, ink-wash, one-line, pictogram-motion, living-screencast, engraving. **Sections 3–5 skimmed:** whiteboard, art-deco, spy-titles, risograph, tilt-shift, paper-popup, silkscreen-poster, game-show. The `DEMO.md` files hold the real hex values and timings (only the `hud.js` theme was read from source code). |
| S2 | [chenyuxiaojin/opus55-video-style-prompts](https://github.com/chenyuxiaojin/opus55-video-style-prompts) | **No LICENSE file**, so all rights are reserved by default. Take ideas only. | 15 content-agnostic style prompts (CN + EN). A sub-agent derived them frame by frame from @VincentWei93's Opus 5.5 showcase. Directly relevant: 02 等轴2.5D, 04 线条动画, 06 形变动画, 08 赛博朋克HUD, 10 弥散渐变玻璃拟态, 11 几何构成包豪斯, 14 液态流动. Online gallery: chenyuxiaojin.github.io/opus55-video-style-prompts *(page not opened)*. |
| S3 | [PHY041/claude-motion-playbook](https://github.com/PHY041/claude-motion-playbook) | CC BY 4.0 (docs), CC0 (templates) | A statistical study of the 233 entries on prompt-motion.com. `docs/techniques.md` lists 137 moves; its **Data viz** and **Particles** sections are the best catalogue found for evaluation-video moves. There is also a HyperFrames SaaS launch-film template. |
| S4 | [HiAPIAI/awesome-opus-5-5-video-styles](https://github.com/HiAPIAI/awesome-opus-5-5-video-styles) | CC-BY-4.0 | 425 prompts sorted into 12 styles: cartoon, cinematic3d, collage, explainer (38), generative (34), handdrawn, lowpoly, photoreal, pixel, productui (80), retro, typography. Each style has a one-paragraph "style recipe" (quoted below). |
| S5 | [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) `data/videos.json` | MIT | 513 prompts. Keyword statistics are in §4. |
| S6 | [joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts) | No license in the API | 18 CN-annotated prompts, including the `16-high-end-product-video` "high-end minimal" prompt with a **banned list** (quoted in §3.13). The README shows that CN users most often ask for **线稿** (line-art) explainers: 中华五千年, 大气环流. |
| S7 | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) (1,152★) | MIT | `manim-composer/references/visual-techniques.md` has 3b1b palettes, colour-as-meaning rules and a timing table. |
| S8 | [dot-Justin/teenage-engineering-ui-ux-skill](https://github.com/dot-Justin/teenage-engineering-ui-ux-skill) (0★) | **No LICENSE file**; reverse-engineered brand tokens | `references/DESIGN.md` gives TE neutrals and accents, a thin type scale, hairline borders and "near-zero ornament". |
| — | athemeroy/awesome-opus-5-5-videos (510★, CC-BY-4.0) | — | Contents listed, but the data files timed out *(unverified)*. |
| — | eastling/awesome-opus-5.5-video-prompts, jinhanbuilds/opus-5-5-motion-gallery, haiy/opus55-video-guide-zh, joefedna/Claude-Opus-5.5-Motion-Video-Skill | — | Found by `gh search` only, not opened *(unverified)*. |
| — | christopherabey/3brown1blue (72★), iart-ai/manim-skills (MIT), Wamikmk/interactive-educator | — | 3b1b-style generators found by search, not opened *(unverified)*. |

### 1.1 lemo-opuscar: all 43 `styles/<x>/STYLE.md` (enumerated via the GitHub contents API)

`art-deco, ascii-crt, backrooms, blueprint, brick-toy, cel-anime-80s, crayon-book, dark-keynote, dataviz, engraving, game-show, glass-product, halftone-dossier, hd-2d, hologram-hud, impasto, ink-wash, iso-infographic, living-screencast, lowpoly-island, microgame, midcentury-toon, one-line, paper-lantern, paper-popup, papercut-red, pictogram-motion, pixel-rpg, risograph, rubber-hose, scifi-toon, shadow-puppet, silent-film, silkscreen-poster, spy-titles, stained-glass, swiss-motion, tilt-shift, ukiyoe, urban-sketch, watercolor, whiteboard, woodcut` (plus `_template` and `README.md`).

The repo's own categories (from `styles/README.md`):
- **Information & Keynote (信息与发布):** dataviz 数据叙事, iso-infographic 等距信息图, dark-keynote 暗色科技发布, living-screencast 活体实机录屏, hologram-hud 科幻全息界面.
- **Graphic & Type (图形与排版):** swiss-motion, spy-titles, art-deco, blueprint 蓝图/工程制图, stained-glass, pictogram-motion 象形运动图形, ascii-crt.
- **Materials & 3D (材质与3D):** glass-product 玻璃质感产品, tilt-shift, paper-popup, lowpoly-island, brick-toy.
- **Print (印刷):** risograph, halftone-dossier, woodcut, engraving 铜版画, silkscreen-poster.
- **Hand-drawn (手绘):** one-line 一笔画, whiteboard 白板讲解, ink-wash 中国水墨, and others.

**Gaps in lemo-opuscar for our list:** there is no particles style, no bauhaus, no glassmorphism UI, no aurora or liquid gradient, no 3b1b/math morph, no academic-paper style and no TE/Braun instrument style. Those come from S2, S3, S7 and S8 below.

**Shared rules across lemo-opuscar** (they appear in every STYLE.md read):
- Subtitle hold ≥ max(1.8 s, speech + 0.6 s).
- Final mix at −14 LUFS.
- Music ducks under the voice, and foley ducks too.
- "True digital silence" (reverb tails cut as well) before the key reveal.
- **No dissolves.** Each style names its own transition.
- One accent colour, spent on one meaning.
- Key subject at least 1/3 of frame height at key moments.
- Every key event on the beat grid, verified by a `cuecheck` tool to 0 ms.

---

## 2. Spec blocks per candidate direction

### 2.1 蓝图 / Blueprint (engineering drawing): S1 `blueprint`

Good for: architecture explainers ("how an Agent/RAG pipeline is built"), model teardown, version history (REV.1→REV.n = model versions).

- **Colour:** blue and white only. Sheet `#18336B → #2A58A6` (fbm noise), lines `#E7F0F9`, table/cloth `#0D1116`. Alternatives: a faded sheet `#3A6DA8 → #5B8CC4`, a deep sheet `#0F2350 → #1D3F80`. **One stamp red `#C23B2E`, used exactly once**, to carry the verdict ("APPROVED" / "REJECTED"). That fits an evaluation conclusion well.
- **Lines:** four weights in sheet units: 3.2 / 2.0 / 1.25 / 0.9. **Screen width = sheet width × zoom^0.65**, so close-ups never turn into sausages. Dash patterns: centre `[34,7,6,7]`, hidden `[11,7]`, phantom `[30,6,5,6,5,6]`. Hatching at 45°, spacing 8–14.
- **Type (all OFL):** Architects Daughter for hand lettering, **B612** for title-block fields, Allura for the signature only. Text is written on left to right with a glowing nib. Subtitles are "NOTE / n" boxes with double rules, lettered on in about 0.35 s, wrapped at about 880 px and placed in empty sky (never at the bottom). For CN, pair with 霞鹜文楷 or a mono *(our suggestion)*.
- **Motion:** draw-on is truncated by arc length with a glowing nib at the head. Drafting order is centre lines → outlines → detail → hatching → dimensions → balloons → labels, **one layer per beat**. In the exploded view, parts leave one every ~0.055 of progress on 8th notes and return one 8th per group with a click. Gears advance one tooth (7.5°) per 8th note with a 0.35-beat ease-out. Failure plays as a slow wind-down over ~1.5 s; joy is a needle overshoot (back-ease). Camera on ones, hard cuts on downbeats.
- **Signature moves:**
  - "FIG. 1" struck through and rewritten "FIG. 2 · EXPLODED VIEW" as a transition.
  - Live dimension lines whose numbers change. Good for latency, params and benchmark deltas.
  - The title block as story: the status field is the verdict, and the revision rows are the history.
  - The oblique depth factor animating 0 → 0.5 makes the flat drawing gain thickness.
- **Camera:** whole sheet only at open and close. Medium shots with the figure at about 80% of height. A 2× close-up cut on a downbeat. A lateral pan Fig.1 → Fig.2 → Fig.3.
- **Sound:** contrapuntal and mechanical: harpsichord, bassoon, spiccato strings, celesta. The demo is a 108 BPM baroque invention in G. Foley: technical-pen scratch (2–6 kHz), T-square slide, part clicks at 3–5 kHz, escapement ticks, a rubber-stamp thump. Music ducks to about 0.36× under the voice.
- **Pitfalls:**
  - Explosions upward hit the header. Explode sideways.
  - Subtitles drawn into the ink buffer vanish. Use a separate overlay.
  - Line weights that do not scale with zoom.

### 2.2 数据叙事 / Data journalism: S1 `dataviz` + S3 data-viz moves

Good for: benchmark charts, price/perf, "model X over time". **This is the closest match to 评测.**

- **Colour (demo):**
  - Paper `#F6F3EC`, with a 24 px dot grid in `#E4DDCF`.
  - Ink `#2B2723`: axes 1.4–1.6 px, series line 2.4 px. Gridlines `#DDD6C9` 1 px. Zero line `#BDB4A5` 1.3 px.
  - Ticks in IBM Plex Mono 17–20 px, `#6E665C`.
  - Diverging ramp (ColorBrewer RdBu): `#2166AC → #4393C3 → #92C5DE → #D1E5F0 → #F2EEE8 (centre) → #FDDBC7 → #F4A582 → #D6604D → #B2182B → #7A0F1E`.
  - Pencil leads: **blue `#2F5D8A` for memories and human notes, red `#A8283A` for records and warnings**. Changing lead marks a turn.
  - **Colour encodes one thing only: the value.** "Never stretch a ramp to make a change look bigger."
- **Type:** the figure caption is the subtitle: **Newsreader** 42 px, left-aligned with the chart, ≤ 2 lines, a hairline rule above, a mono kicker for the range so far (e.g. `1926–1958`), a 3-frame rise. Title: Newsreader 66 px in world space. Notes: Caveat 30 px with per-glyph ±1.7° rotation, ±2.5% baseline jitter, 16% pixel knock-out.
- **Marks:** dots r = 6 px with a 1.5 px ink ring. Landing pop 0.25 s (×1.55) with a thin ripple, suppressed when marks arrive < 0.1 s apart.
- **Motion:** the rhythm of the data is the rhythm of the film. To speed up, divide the beat instead of changing tempo. Pick a tempo whose finest subdivision lands on whole frames (demo: 90 BPM).
  - A rescale plays as stepped ratchet clicks.
  - A morph is a staggered sweep.
  - **No fades or dissolves.** Transitions are chart operations: axis growth, pull-back, rescale, morph.
- **Signature moves:**
  - One mark = one fact.
  - **The axis arrives when the narration first names the unit.**
  - Pinned annotations live in data space.
  - "Breaking the frame": the outlier tears through the plot box and leaves a scar. Hold the pierced state ≥ half a beat.
  - Encoding morph, e.g. bars → waffle.
  - **"The empty next cell":** a dashed slot for the unknown value. Good for "the next model?".
- **Camera:** 2D `{x,y,zoom,roll}` over one sheet, as one take. Track the newest mark at about 60% of width. Punch in over 2 frames with a decaying shake on an outlier. When the axis scrolls off, pin its ticks to a frozen-pane strip.
- **Sound (optional, distinctive):** sonification. Pitch = value. A low-pass-gate "plonk" (sine + FM, index rising with value). Music ducked about −11 dB. True silence before the key mark.
- **Evaluation-ready moves from S3** (*seen in the catalogue table; the videos themselves were not watched*):
  - **Comparison bars with confidence-interval whiskers** (Claude/Copilot/Gemini, #106).
  - **Race bars** with scrambling digits, one falling behind (0.114 s vs 7.133 s, #48).
  - Ring gauge: stroke-dashoffset and the centre number reach the target together.
  - Hero number with a one-line grey footnote for source and unit.
  - Odometer with a growth line and a bright tip dot.
  - Waffle / dot matrix that reflows into a histogram.
  - Threshold line ("your line").
  - **Synced multi-view:** gauge + number + event log + playhead chart, all from one `state(t)`.
  - Persistent meter as storyline.
  - Counters appear in 67 of 233 entries, making them the most common data move.

### 2.3 全息遥测 / Hologram HUD / telemetry: S1 `hologram-hud` + S2 08 FUI

Good for: spec walkthroughs of a model ("context 1M · price · speed"), upgrade comparisons (old value dim → new value accent).

- **Colour (S1 `hud.js theme(hue=190, accent=38)`; demo hue 188 cyan / accent 38 amber, alternate 204/18 blue/orange):**
  - `line hsla(h,100%,72%,a)`, `hi hsla(h,60%,93%,a)`, `dim hsla(h,70%,52%,a)`, `acc hsla(acc,100%,64%,a)`.
  - Stage `bg0 hsl(h+12,70%,2.4%)` with a radial lift `bg1 hsl(h+6,65%,7%)`. Vignette 0.5.
  - Text plates `rgba(1,8,12,.72)` with a 28% border and 10 px corner ticks.
  - **The accent is spent only on a value at the frame it becomes true.** White = heat (what is active now).
- **S2 variant:** near-black with a cool vignette. One cyan ranked by brightness, near-white for focus. **At the critical moment the whole screen turns amber as an alert.**
- **Type:** **Rajdhani** 300 for big numbers and names (26 px tracking), 500/600 for labels (2–3 px tracking). **Share Tech Mono** 20–22 px for micro data. Numbers are monospaced; the decimal point is drawn as a small square. Subtitles: plate `rgba(1,8,12,.62)` with two diagonal brackets, 4 "voiceprint" bars, Rajdhani Medium 38 px, in 0.1 s before the voice.
- **Motion (demo numbers):**
  - Target box starts at 1.9× the rest bounding box, 30% alpha, rotated 45°. It **snaps in 0.22 s** (cubic ease-out) and flashes white for 3 frames on the downbeat.
  - Leader: anchor ring → diagonal → horizontal in ~0.5 s.
  - **Rolling value 0.5 s, characters locking right-to-left**, turning accent on the downbeat.
  - Chip dock: the card fades in 0.35 s and the chip slides x 140 → 110 into a side rail (step `min(112, 410/(n−1))`).
  - Whip: 0.5 s cubic in-out, starting 0.45 s before the next lock, with 5 motion-blur sub-frames.
  - A 3-frame glitch at most once.
  - **No cuts or fades inside a scene**, only a scan plane and a loupe iris.
- **S2 motion:** power-on (a bright line opens into a crosshair), arcs draw along their ticks, text types out line by line, rings turn slowly, a slice-offset glitch on a state change.
- **Use cases with holds (S1 §11):**
  - Spec walkthrough: title ≥ 5 s, each value ≥ 2.5 s then docked, final sheet ≥ 3 s, 30–40 s total.
  - Upgrade: 3 s per upgrade, old value dim → new value accent. **Maps directly to "v1 → v2 model" comparisons.**
- **Sound:** 120 BPM (1 bar = 2 s). D minor/Dorian: Dm9 → B♭maj7 → Fmaj9 → G6. In-key sine/FM blips. A lock = thump + clack + two-tone beep. Rolls tick at the frame rate. Projector hum at 40/80/120 Hz. Add a layer per part. One beat of true silence before the drop. Hold the duck envelope through word gaps.
- **Caveat (S3):** HUD chrome appears in 72 of 233 gallery entries and some prompts explicitly ban it. It is overused, so keep it diegetic (it measures something real), not decorative.

### 2.4 粒子 / Particles & generative: S3 §7 + S4 "generative"

No STYLE.md for this direction. Rule from S3: **"the ones that work give the particles a job: they become a word, a logo, a cluster or a line."**

- **Moves (S3):**
  - **Dot-to-line ignition:** one dot on black → a horizontal light line → it opens into the panel/UI.
  - **Particles converge into a word:** sample target points from the text's pixels (`getImageData`), lerp by t, hold, scatter. About 6,000 particles in #172.
  - **Flow field → recolour → clusters:** one particle system for the whole film: a ribbon, recoloured by source, regrouped into labelled clusters, then settled as spikes on a timeline. **Ideal for "tokens / embeddings / training data".**
  - Implode into a core.
  - Fibonacci point-cloud sphere (1,200 dots) with live readouts.
  - Dot-grid ripple.
  - **Dot matrix as the only motif** (one visual language for everything).
  - Halftone/Truchet waves.
  - Metaballs via SVG `feGaussianBlur` + alpha-threshold `feColorMatrix`.
  - Oscilloscope waveform thread that evolves by chapter.
  - Path draw with a travelling glow dot.
- **S4 recipe (verbatim):** "Everything is procedural: particles, flow fields, shaders or tiling geometric patterns driven by time and audio. Dark background with neon or a bold 3–4 colour palette; motion locked to the beat."
- **Premium guard (S6 banned list):** "shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds, bouncy easing". Particles therefore need to be *structural* (tokens → clusters), never bursts.
- **HyperFrames note:** seeded PRNG, positions as a pure function of t (closed-form noise, no integration state). This matches the S5 convention "one `draw(t)`, no state between frames".

### 2.5 等距 2.5D / Isometric infographic: S1 `iso-infographic` + S2 02

Good for: "how an inference cluster / data centre / agent workflow works", supply-chain-style system diagrams.

- **Projection:** axes at 30°. `sx=(x−y)·cos30°·k`, `sy=((x+y)·½−z)·k`. Painter depth = x+y+z. **The projection never rotates or tilts.** No outlines on solids.
- **Three tones per face:** top light / left (+y) mid / right (+x) dark. Derive them with `tri(c)`: mix toward warm white 20% for the top and toward `#231A2C` 22% for the dark side (shadows slightly cool).
  - coffee red `#CF5140/#B3352B/#8C2620`
  - leaf `#7BA75F/#5E8C4A/#476F37`
  - sea blue `#5A9BCB/#3C7FB1/#2D6390`
  - cream `#FBF4E6/#F2E6D0/#D9C8A9`
  - soil `#A77850/#8A5B3A/#6A432A`
  - mustard `#E9BE5C/#D9A53A/#B0832A`
  - ink `#2E2522`
  - Example sets for a data centre: electric blue, amber, graphite, mint on off-white.
- **Colour logic:** a pale neutral ground plus 5–7 flat hues, **one hue per role and never reused**. **Focus + context:** everything desaturates toward warm grey except the subject.
- **S2 variant ("clay-block miniature", more premium):** rounded matte clay blocks on one square unit, soft diffuse light, a **lavender haze background deepening toward the bottom**, off-white and low-saturation pastels, **one small deep-indigo mass** anchoring the eye. Forms drop or rise cell by cell (quick ease-out, slight bounce). The camera only pans or dollies.
- **Type:** one geometric sans (Jost). Titles 600, all caps, ~0.12 em tracking. Numbers 400 at ~44 px with units at half size. **~7 px halo in the ground colour** on all text. Label pins: dot (ink ring, pale fill) → vertical leader → horizontal rule → text. Ink lines 2 px, only for infographic furniture. The subtitle is a map-label card ~42 px with a tiny iso-cube chip. Keep the bottom ~170 px clear.
- **Motion:**
  - Cutaway: cut line 0.3 s → skin slides out 0.35 s (ease-out, alpha 1→0 between 10% and 75%) → hatched rims fade in over the last 40%.
  - **Isotype fill:** icons pop with back-ease (overshoot 2.2), one per 16th note.
  - Accumulation = acceleration: quarters → 8ths → 16th-note waves.
  - Squash 18% on landing.
  - **Solids arrive by motion, never by alpha.**
  - "Nothing moves without a line leading it."
  - Dive: three pushes through nested cutaways, 0.9 s / 0.6 s / 0.6 s. Snap-out ×470 in 1.2 s, eased in log zoom.
- **Sound:** acoustic and light: kalimba, marimba, nylon guitar, pizzicato, or a clean electronic pulse for technical systems. Demo at about 100 BPM, with a 3-note motif for the subject. Music ducked about 8 dB.

### 2.6 玻璃 / 弥散 / 液态: Glass, frosted, aurora, liquid. S1 `glass-product` + S2 10 + S2 14

Good for: a premium model-launch/评测 opener and a "product as object" hero. **Highest 质感 potential, highest kitsch risk.**

- **S1 glass-product (dark-field studio, Three.js):**
  - **Accent family reserved for light:** ice blue `#62DCFF` → soft violet `#A98BFF`. Everything else is neutral.
  - Background sweep `#34383d → #16181b → #000`, no horizon line. Light-guide acrylic `#15181b`.
  - Clear glass: roughness 0.015, IOR 1.52, thickness 3–4.5, dispersion 5. Frosted: transmission 0.82–0.9, roughness 0.4, tint `#eef2f5`, plus something bright behind or inside it, otherwise it reads as grey plastic.
  - Neutral tone mapping (**AgX washes accents to white**). Bloom only above ~1.1. Grain 0.
- **Frosted subtitle bar (portable to CSS):** 76 px tall, radius 38, `backdrop/filter: blur(18px) brightness(1.25)` + 10% cool white, a 1.2 px gradient stroke, a blue → violet top line, **Inter Tight 300, 40 px, tracking 1 px**. Held ≥ 1.9 s and ≥ speech + 0.7 s.
- **Titles:** the same grotesk at weight **200**, 100–140 px, very wide tracking, centred in the upper third. **A diagonal glint sweeps across the letters in sync with the light sweep.** Kickers are tracked caps at 18–20 px.
- **Motion:**
  - Everything eased, on ones. **The camera always drifts**, never locked, never handheld. Orbits 0.2–0.4 rad per shot.
  - **Exploded view:** 3 s ease-out apart → 0.75 s hover (drifting +3%) → **0.25 s ease-in snap exactly on the downbeat**, then a ~40% push-in over 0.9 s and 2 frames of micro-shake.
  - Cuts only on beats or a sweep through black. **Never dissolves or wipes.**
- **Sound:** "minimal electronic, never piano-and-strings". Bowed glass, granular crystal, FM glass plucks, a filtered tick grid, an 808. The demo is 120 BPM minor with half a bar of total silence before the drop. The snap = 6 clicks 15 ms apart + an inharmonic glass chord (partials ×2.76, ×5.4). Music −12 dB / foley −6 dB under the voice.
- **S2 10 Aurora glassmorphism (2D-friendly; best HyperFrames fit):**
  - Large-radius frosted panes with a **hairline bright highlight** on the outline, staggered depth and a slight perspective tilt.
  - **A thick clear lens glides slowly across, magnifying and bending what is under it, with rainbow-fringed edges.**
  - Ground: near-black, cool, darkened corners. **Huge soft-focus glows (blue leading, violet and cyan supporting)** blend like mist. **The foreground is only white and translucent white.**
  - Motion: smooth throughout, the aurora morphing slowly, panes floating with parallax. Elements **resolve from blur to sharp** and exit by defocusing and receding.
- **S2 14 Liquid jelly:** translucent jelly with white specular highlights and rim light. Deep-violet ground. Orange → magenta → violet liquids. Metaball merge and pinch-off, crown splashes, damped wobble. *Probably too playful for 评测. Keep it for one transition at most.*

### 2.7 包豪斯 / Bauhaus geometric construction: S2 11 (+ S1 `pictogram-motion` as a cousin)

- **S2 11:**
  - Build everything from circles, semicircles, quarter-circles, squares, triangles and **thick black bars**, with razor-sharp flat fills.
  - **Thin black construction lines, registration crosshairs and pivot dots stay visible.** The paper carries a very faint module grid.
  - Warm off-white paper, empty space dominating, **pure red/yellow/blue primaries + black**, asymmetric balance.
  - Motion: on a steady beat, **one piece moves at a time**. The crosshair appears first, then the shape unfolds from that point, slides in or swings about a pivot. **Fast start, fast stop, with motion blur.** Between sections the composition shatters into small tiles that flip, scatter and reassemble.
- **S1 `pictogram-motion` (premium broadcast identity; good for "Top N models" list videos):**
  - A square grid (cell ≈ 1/6 of frame height) of discs, half-discs and motifs in **5 tones of one hue**, with **whole rows cut and shifted sideways** as the signature.
  - Title in a **900-weight grotesk (Inter Tight) at 150–330 px**, a heavy second-language line ~0.08 s after it, **DM Mono ~22 px** meta in the corners.
  - **A progress bar of N ticks** (current tall, done dimmed, rest faint) and an "07 / N" index.
  - Exponential ease-out for entrances, exponential in-out for whips; back-ease once at most. Type enters by **mask slide-up**.
  - Every shot starts on a beat. A card that must be read holds ≥ 1.6 s.
  - Never dissolves, 3D camera moves, handheld shake or DoF.
  - Pace ladder: normal cards last one bar, related sub-items run at half length.

### 2.8 水墨 / Chinese ink wash: S1 `ink-wash`

Good for: CN-flavoured 科普 openers and "AI × 东方" chapter cards. Use sparingly. It makes a strong 留白 premium look but fights data.

- **Colour:**
  - Paper `#F2ECDE` to `#F3EBDD`, cloud mottling ±7%, vignette ~0.22.
  - Ink from cool grey `rgb(.52,.55,.58)` to warm black `rgb(.075,.068,.062)`, in five tones by opacity: 焦 .96 / 浓 .82 / 重 .60 / 淡 .34 / 清 .16.
  - **One vermilion `#B02E22`** for the seal and at most one tiny accent. Never a red wash, never red type.
  - **60–80% empty paper.** "If a frame gets busy, remove ink rather than add tone."
- **Type:** subtitles are inscriptions (题跋) in **Cormorant Garamond italic**, no box, ≤ 2 lines, placed in empty paper, with a small vermilion square before each line. Titles are vertical columns plus a code-drawn 白文 seal. For CN, use a brush or Kai face such as 霞鹜文楷 *(our suggestion)* traced as a skeleton in stroke order.
- **Motion:** figures on twos (12 fps); camera, blooms and ripples on ones. Strokes appear in drawing order. **"Stillness before action":** a slow 5% push-in, then the decisive stroke crosses the frame in ~4 frames. Wet bleed is a 12-tap Poisson blur of ~5 px. Edge pigment = small blur − large blur.
- **Transitions:** **ink bloom** (noisy radial mask with a dark tide-line), handscroll pan from right to left, mist. Never a generic dissolve or wipe.
- **Sound:** guqin-led (open and stopped strings, harmonics), xiao, big drum for mass. The demo uses F-gong pentatonic at 60 BPM (landscape) and 90 BPM (travel). Literal digital silence with at most one drip. Music ducked ~8 dB.
- **Pitfalls:** dry brush looking like dashed lines; parallel semi-transparent strokes reading as "organ pipes"; clipping a font outline (use the font as a skeleton only).

### 2.9 数学形变 / Morph & math (3Blue1Brown-like): S7 + S2 06 + S1 `one-line`

No lemo-opuscar style exists for this. Assembled from three sources.

- **3b1b palette (S7):** bg `#1C1C1C`, primary blue `#58C4DD`, green `#83C167`, accent yellow `#FFFF00`, warning `#FF6666`. "Soft academic" variant: bg `#2D2D2D`, `#6ECFFF`, `#98E898`, `#FFE66D`.
- **Colour-as-meaning (S7):** inputs BLUE, outputs GREEN, the term under discussion YELLOW, errors RED, support WHITE/GREY. Held for the whole video.
- **Rules (S7):**
  - **"Transform, don't replace":** `TransformMatchingTex` rather than fade-out/fade-in.
  - Progressive disclosure, term by term.
  - Left→right = causation, top→bottom = derivation.
- **Timing (S7):** shape creation 0.5–1 s, equation writing 1–2 s, transform 1–2 s, camera 2–3 s, absorption pause 0.5–1 s. Rhythm **fast-fast-SLOW-fast-fast-SLOW**. Default rate function `smooth` (≈ `power2.inOut`; manim's `smooth` is a sigmoid *(GSAP equivalence is our approximation)*).
- **S2 06 Shape morph:**
  - One centred bold round-cornered silhouette for the whole piece, with **one diagonal lighter fold facet** and fine paper grain.
  - Full-bleed saturated flat ground in 3–4 rotating colours. **At each section change the new ground blooms out from the silhouette as a soft-edged circle.**
  - Shapes stretch, split and merge. Each holds briefly, then squashes and rebounds on landing.
- **S1 `one-line` (premium variant of the morph idea):**
  - Paper `#F4EFE4`, ink `#1D1A17`, one accent used once.
  - Ink is a filled polygon around the path. Width = base × pressure, with `pressure = 0.66 + 0.8·exp(−v/300)` (fast = thin), ±8% noise, and bleed at ~20%.
  - Speeds ~300–700 units/s travelling, 50–150 for detail. **"The most important stroke is usually the slowest."**
  - **No cuts: the last stroke of one image is the first stroke of the next.**
  - Handwriting subtitles (Caveat), written on in ~0.2 s + ~17 ms per char; fade out 0.45 s.
  - Music: one solo instrument, no pads. The pen sound is synthesised from speed.
  - "**Line as graph**" is a native move.
- **S2 04 gold single-line (dark premium variant):** one thin desaturated warm-gold line on deep navy/near-black, **with a white-hot spark at the tip**. Closing a shape floods it gold with a ring of light. The camera pans with the tip and pulls back only for the reveal. *Fits a dark kit well.*
- **CN popularity:** CN prompts in S6 repeatedly ask for "动画格式为线稿" (中华五千年, 大气环流), so line art is the de facto CN 科普 style.

### 2.10 学术论文 / Scientific paper & academic plate: S1 `engraving` + `dataviz` caption system

No dedicated "arXiv paper" style was found. The nearest grammar is the natural-history plate.

- **S1 engraving:**
  - Laid paper `#f1e8d2`, ink `#1c1510`.
  - **Tone made only of line density**, never grey fill. Hatch families switch on at tone thresholds ~0.14 / 0.5 / 0.75.
  - **Swell law** for every line: `width × (0.2 + 0.8·sin(πu)^0.7)`, tapered over the first and last 22%. Spacing ≈ 1/180 of figure height.
  - One light direction (upper left).
  - **Roundels:** double-ruled circular magnified insets, with hairline leaders to the part and small italic figure numbers. **Good for "zoom into one attention head".**
  - Lettering: **Bodoni Moda** roman caps (title 44–56 px, wide tracking; labels 15–19 px), italics 20–24 px for names, Pinyon Script for notes. Roman letters are cut glyph by glyph. Nothing fades in.
  - An engraved note stays ≥ chars ÷ 12 + 1 s.
  - Colour arrives late as a transparent wash in muted earth/mineral pigments, one stronger pigment at most. **Colour arriving is an event.**
  - Transitions: proof pulled, tissue guard laid over, new sheet. **No dissolves or wipes.**
- **Paper-figure system (our synthesis from `dataviz` §4, *not a fetched style*):**
  - Newsreader caption with "Fig. n" kicker in mono.
  - Hairline rule.
  - Cream `#F6F3EC` page.
  - IBM Plex Mono ticks.
  - The equation as a typeset object that transforms (S7).
  - Citation threads drawn to `[n]` (cf. github.md HUD "threads drawn to citations").
  - The S3 gallery has an "Engraving-style Claude ad" (#8, @LexnLin), which is a top pick *(video not watched)*.

### 2.11 仪器 / Instrument & industrial (Teenage Engineering, Braun): S8, tokens only

No video style pack exists for this. The tokens are reverse-engineered from TE's website; the repo has no license. **Use them as inspiration and re-pick the hex values.**

- **Neutrals:** te-white `#F5F5F5`, te-black `#0F0E12`, greys `#E5E5E5 / #CCCCCC / #B2B2B2 / #A1A7AF / #767676 / #4D4D4D / #272727`, inverted surface `#000000`.
- **Accents:** blue `#0071BB`, green `#006837`, **orange `#F05A24`**, red `#B81D13`, yellow `#FAB413`.
- **Type:** thin weights only. Display 53 px/300, −0.015 em; 40 px/300; body 26 px at 300 or **100**; small 19 px/100. Their face is TE's own (Univers-Next-like), falling back to Inter.
  - **Lowercase-only voice.** Product codes in UPPERCASE with an **en-dash** (`EP–133`, `OP–1`). Model names could follow the same convention (`GPT–5`, `OPUS–5.5`; *our idea*).
- **Surfaces:** hairline 1 px borders (`#E5E5E5`/`#B2B2B2`, never 2 px, never black, never accent). CTA radius ~1.5 px, "almost rectangular". **"Shadows, gradients, parallax, hover-scale, bounce, spring and colour-wash transitions are absent."**
- **Implied motion** *(our translation, unverified against any TE video)*:
  - Linear or `power1.out` only, at 120–200 ms.
  - Values step like an LCD (`steps(n)`).
  - Knob and slider indicators rotate with no overshoot.
  - A single orange element per scene.
- Sound idea *(unverified)*: dry sampler clicks, an OP-1-style synth arpeggio, tape-stop.

### 2.12 Other premium candidates worth stealing from

- **活体实机录屏 / Living Screencast (S1 `living-screencast`): the strongest match for 教程.**
  - The real UI is **redrawn in HTML/CSS** so the camera can go anywhere and text stays sharp. Labels, modes and shortcuts must match the product's docs.
  - 30 fps, zoom ≥ 1 (never show beyond the monitor).
  - **Two actors, never a hand:** the cursor is the user, a pixel mascot is the software.
  - Overlays limited to:
    - a chapter pill (01–04)
    - a **KeyCastr-style keystroke HUD**
    - **frosted-glass caption pills** at the bottom, never over the element being discussed
    - an optional "▶▶ 4×" time-lapse tag
  - Camera vocabulary:
    - push-in to the caret
    - **rack focus between panes** (never blur text the viewer must read)
    - whip between panes, with anisotropic blur on an untransformed wrapper and only on whips
    - push-in + vignette "spotlight freeze" on the one promise
    - split-window for parallel sessions
  - Music: a hi-fi band plus a chiptune voice for the mascot. **A short drop to room tone before the key promise.**
  - Pitfalls: invented features, and foley landing on product names (verify with whisper).
- **白板 / Whiteboard (S1 `whiteboard`):**
  - Three markers max, each with a fixed meaning: black `#23262c` / blue `#2a5cb3` / orange `#d97757`; or black / green `#2e8b57` / red `#c8363a`; or navy `#1f2a44` / teal `#1f8a8a` / purple `#7a4fb3`.
  - Stroke easing `u − sin(2πu)/2π × 0.8` (slow-fast-slow), solved per time window so writing finishes on the spoken word. A label takes 0.3–0.8 s, a title ~3 s.
  - An eraser at ~90% strength leaves a ghost.
  - Subtitles ≤ 44 chars per line in the bottom ~12%.
- **Risograph (S1):** inks `#0078BF` + `#FFE800` + `#FF48B0`, or `#3D5588` + `#FF665E` + `#FFB511`, on paper `#F4EEE2`. Registration offsets are **fixed per shot** (±1–3 px), with a kick of 8–14 px decaying over ~0.25 s on accents.
- **Silkscreen poster (S1):**
  - 6-ink palettes, e.g. winter `#EEF1F4 #B8C9D9 #8B9BB0 #4A5D78 #1F2A3C` with accent `#F2B134`.
  - Squeegee pulls are **linear** ("a squeegee does not ease"). **No fade anywhere.**
  - Reading rule: chars/12 + 1 s after the last item lands, rounded up to the beat.
- **Spy titles (S1):** 4-ink sets such as `#1b1714 / #efe4c9 / #d23a22 / #e2a52a`, or ink `#161a22` / bone `#ece6d6` / teal `#1f8a8a` / orange `#f07a28`. Credits slide in along grid lines and **stop dead on the beat** (subtitles in ~0.18 s). The "stop-time" freeze plays in total silence.
- **Art deco (S1):** everything unfolds from the centre axis. Fonts Limelight / Poiret One / Josefin Sans / Italiana. Bulb ignition overshoots ~1.6× and settles in ~0.18 s. *Too ornamental for 评测.*
- **S6 "High-end minimal" direction (a premium recipe worth copying):**
  - "One idea per shot, lots of empty space, one accent color, one clean sans (Geist or Inter) with tight tracking. Masked type reveals, match cuts, one smooth camera language… No full stops in on-screen text."
  - Banned: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds, bouncy easing.
  - Build: 10 bars at 120 BPM (2 s each). Every cut on a downbeat. 3 sub-frames at t ± 1/240 s blended for motion blur. Sound effects placed by their measured peak. −14 LUFS. Probe 20+ stills before the full render.
  - Gotcha: "never set opacity or filter on a preserve-3d element; fade its wrapper".

---

## 3. Popularity data (S5 yihui `videos.json`, 513 entries; word-boundary regex over prompts)

- **Categories:** motion 317, interactive 70, explainer 67, 3d 59.
- **Tech tags:** canvas 351, svg 219, threejs 147, shader 104, **gsap 100**, css 68, audio 36, particles 26.

| Keyword | All | Explainer (67) | Keyword | All | Explainer |
|---|---|---|---|---|---|
| beat | 36 | 4 | one take / single shot / never cut | 17 | 2 |
| particle(s) | 25 | 1 | spring | 17 | 2 |
| glow | 19 | 1 | morph | 16 | 1 |
| gradient | 19 | 0 | cream/paper | 15 | 2 |
| glass | 13 | 4 | tokens | 12 | 3 |
| dark | 11 | 0 | terminal | 9 | 0 |
| hand-drawn | 8 | 4 | hud | 6 | 0 |
| apple | 6 | 0 | attention | 5 | 1 |
| editorial | 4 | 0 | halftone | 3 | 2 |
| 3blue1brown/manim | 2 | 2 | benchmark | 2 | 1 |
| whiteboard / blueprint / risograph / vox | 1 each | — | isometric / swiss / kurzgesagt / bauhaus / aurora / TE·Braun | **0** | 0 |

**Reading:**
- Explainer prompts are short and rarely name a style. The ones that do lean **hand-drawn / glass / halftone / 3b1b**.
- "Swiss / isometric / bauhaus / aurora / instrument" are absent from prompts, so none of them is a crowded look.
- S3 found that **the "go all out" one-liner is 44% of the 230 prompts**. Pressure phrases score higher (4.05 vs 3.73, p ≈ 0.001), and longer specs buy control, not looks.
- The S4 category counts are explainer 38, generative 34, productui 80.

---

## 4. Takeaways for the kit (premium, AI 评测 / 教程 / 科普)

1. **Best new presets, in priority order:**
   1. **数据叙事 dataviz-paper** (S1 dataviz palette + S3 whisker/race/ring moves).
   2. **全息遥测 telemetry** (S1 hologram-hud with the hue/accent tokens; accent only on locked values; upgrade use-case).
   3. **实机录屏 screencast** for tutorials (S1 living-screencast without the mascot, or with a tiny one).
   4. **蓝图 blueprint** (stamp verdict).
   5. **玻璃弥散 aurora-glass** (S2 10 + the S1 frosted subtitle bar).
   6. **线稿 line-art / 3b1b morph** (S1 one-line + S7 palette).
   7. **仪器 instrument** (TE tokens).
   8. **等距 iso** (S2 clay variant).
   - Ink-wash and bauhaus are better as chapter-card skins than as full presets.
2. **Every lemo-opuscar style names its own transition and forbids dissolves.** Each preset should carry one `transition` token: blueprint = fig-number rewrite, dataviz = chart operation, hud = scan plane / loupe iris, glass = sweep through black, ink = ink bloom, screencast = chapter-pill or pixel wipe.
3. **Spend the accent on one meaning.** Examples: HUD = locked value, blueprint = verdict stamp, dataviz = red pencil for records, glass = light only.
4. **Reading holds:** ≥ max(1.8 s, speech + 0.6 s). For text that must be read, chars/12 + 1 s. HUD values ≥ 2.5 s before docking.
5. **Audio constants:** −14 LUFS, music ducked 8–12 dB under the voice, true digital silence (tails cut) before the verdict, sound effects aligned by measured peak.
