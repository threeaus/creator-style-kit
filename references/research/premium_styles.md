# Premium visual languages for 9:16 AI-evaluation / tutorial / explainer videos

Researched 2026-10-09 for HyperFrames (HTML + GSAP), 1080×1920. Builds on `creators_fonts.md` (Part C). Fonts already in the kit are not repeated except as pairings.

**Legend.**
- **[F]**: the value was read from a primary source fetched in this session: the official site or CSS, the official GitHub source, or the font file's own name table.
- **[S]**: secondary source (a third-party reconstruction).
- **(unverified)**: not fetched. It comes from general knowledge or is a design recommendation. Treat it as a starting point.
- "Rec." marks a recommendation of mine, not a claim about the brand.

WebSearch/WebFetch hit a session limit partway through, so most verification was done with `curl` / `gh api` against primary sources. The font licences were read from each downloaded file's `name` table (IDs 0/13/14) using fontTools 4.62.1.

---

## 0. Quick picker

| Direction | Best for | Background | Accent | Latin / 中文 |
|---|---|---|---|---|
| 1 Data Journalism (FT paper) | Benchmark charts, rankings, price/perf | `#FFF1E5` | `#0F5499` oxford, `#990F3D` claret | Newsreader / Source Serif 4 + Noto Serif SC; numbers in Inter Tight tabular |
| 2 arXiv Figure | Paper explainers, method diagrams | `#FFFFFF` / `#FCFCFA` | matplotlib tab10 `#1F77B4` `#FF7F0E` | CMU Serif / Latin Modern + Noto Serif SC (宋) |
| 3 3B1B / Manim | Math intuition, attention, embeddings | `#000000` (3b1b's own) or `#1C1C1C` | `#58C4DD` BLUE, `#F7D96F` YELLOW | CMU Serif + LXGW WenKai / Noto Serif SC |
| 4 Warm Ivory (Anthropic-inspired) | Opus/Claude reviews, "thinking" topics | `#FAF9F5` / `#F0EEE6` | `#D97757` clay | Fraunces / Newsreader + Noto Serif SC / LXGW ZhenKai |
| 5 Aurora Launch | Model launch hype, feature reveals | `#08090A` / `#000` | gradient `#FFAA40→#9C40FF`; `#FF6363` | Inter Tight / Geist + MiSans |
| 6 Instrument (TE / Rams) | Spec sheets, token/latency/price tables | `#E5E5E5` / `#F1F2F2` | signal orange (rec. `#FF5A1F`), `#ED2024` | Space Mono / DM Mono / Doto / DSEG7 + MiSans |
| 7 Blueprint | Architecture diagrams, agent pipelines | `#003153` Prussian blue | `#FFFFFF` hairlines, `#7FD3FF` | IBM Plex Mono / Space Mono + Sarasa / Noto Sans SC Light |
| 8 Ink Wash 国风 | Openers, philosophical takes, CN-culture topics | `#F2ECDE` 缟 / `#FFFBF0` | 胭脂 `#9D2933`, 朱红 `#FF4C00`, ink `#161823` | LXGW ZhenKai / 演示春风楷 / Ma Shan Zheng |
| 9 Isometric + Particles | System overviews, "how it works", data flow | dark `#0B0D12` or light `#F4F5F8` | 1 hue + greys | Inter Tight / Space Grotesk + HarmonyOS / MiSans |

---

## 1. 数据新闻 Data Journalism: FT · Economist · Pudding · OWID

**Why it works for 评测.** Its credibility comes from restraint. One salient colour carries the story, everything else is grey context, the axes are honest, and every chart has a source line. Benchmark charts look authoritative instead of "marketing".

### Palette
FT Origami `o-colors` v6.7.1 `_palette.scss` **[F]**:

| Token | Hex | Use |
|---|---|---|
| paper | `#FFF1E5` | page background (the salmon) |
| wheat | `#F2DFCE` | panels, alternate rows |
| black-80-ish ink / slate | `#262A33` | body text |
| ft-grey | `#333333` | dark text alt |
| oxford | `#0F5499` | primary data series |
| claret | `#990F3D` | brand kicker or highlight series |
| teal | `#0D7680` | secondary series |
| mandarin | `#FF8833` | callout |
| crimson / jade | `#CC0000` / `#00994D` | down / up |
| ft-pink | `#FCD0B1` | soft highlight |

FT graphics `g-chartcolour` (npm 0.8.26) **[F]**:
- line-web series: `#0F5499 #EB5E8D #70DCE6 #9DBF57 #208FCE #7F062E #C2B7AF`
- muted-first variant: puts `#B3A9A0` first, for "everything else" lines.
- categorical bar: `#1E558C #94D2E6 #1E8FCC #B3325D #FF75A3 #D9CCC3 #AECC70 #F34D5B`
- **backgrounds:** web `#FFF1E5`, social `#333`, **video `#335`**, print `#FEE`, clean `#FFF`.
- Rec.: for a dark FT-video variant, use `#333355` with paper-coloured text.

The Economist:
- Red `#E3120B` and ink `#0D0D0D` appear in the HTML of design-system.economist.com **[F]**.
- Chart palette often quoted **[S] (unverified)**: blue `#006BA2`, cyan `#3EBCD2`, green `#379A8B`, yellow `#EBB434`, gridlines `#B7C6CF`.
- Signature: a red rectangle tag at top-left plus a thin red rule across the top of each chart (unverified as an official spec).

Our World in Data, owid-grapher `CustomSchemes.ts` **[F]**:
- OwidDistinctLines order: Denim `#4C6A9C`, RustyOrange `#B13507`, CamelDarker `#996D39`, LightTealDarker `#2C8465`, Purple `#6D3E91`, Maroon `#883039`, MidnightBlue `#00295B`, Mauve `#A2559C`, DarkCopper `#9A5129`, TurquoiseDarker `#008291`, Cherry `#970046`, LimeDarker `#338711`, PeachDarker `#C4523E`, Blue `#286BBB`.
- These are deliberately darkish and mid-saturation, so they stay readable on white.

The Pudding:
- Per-story background colour via `--story-bg` (e.g. `#FDE300`, `#33B9DE`, `#F9E4FF`, `#B51670`) **[F]**.

### Type
| Role | Original | Free alternative (rec.) | 中文 |
|---|---|---|---|
| Headline serif | FT *Financier Display* (Klim; drawn from Gill/Perpetua) | **Newsreader** Display opsz (OFL), or **Source Serif 4** Display opsz | 思源宋体 Noto Serif SC 700–900 |
| Text / labels | FT *Metric* (Klim grotesk) | **Inter Tight** or **Archivo** (already in kit) | MiSans / Noto Sans SC |
| Numbers | — | Inter Tight with `font-variant-numeric: tabular-nums` | — |

Other sites, all **[F]**:
- The Pudding: Tiempos Text + Atlas Grotesk + Atlas Typewriter.
- OWID: `Playfair Display` for headings and `Lato` for body (owid.css: 94 vs 365 declarations).
- Economist: "EconMilo Display" / Econ Sans, per webdesignhot **[S]**.

Typewolf has a "closest free alternative" for Financier but it is paywalled. The Newsreader and Source Serif picks are mine.

### Motion signature (rec.)
- Bars grow from the baseline: `scaleY 0→1`, `transformOrigin: bottom`, `duration 0.9`, `ease "power3.out"`, `stagger 0.06`.
- Numbers count up in sync, snapped with `Math.round`.
- The highlight series (your model) draws last and in colour. Competitors draw first, in `#B3A9A0` grey (FT "muted-first").
- Line charts use stroke-dashoffset draw, `1.2s`, `"power2.inOut"`. Then a dot pops on the end value (`back.out(2)`, `0.35s`) with a direct label. **No legend boxes.**
- Annotation callouts come last: a thin leader line draws, then the text fades up 12px.

### Texture and layout
- No grain on FT paper. It is flat colour with 1px hairline gridlines `rgba(0,0,0,.12)`.
- Layout: top-left kicker (claret, caps, letter-spacing .08em) → headline (serif, 2 lines max) → subtitle "Score, %, higher is better" → chart → source line at the bottom, e.g. `Source: SWE-bench Verified, Anthropic; as of 2026-10`.
- 9:16 tip: use horizontal bar charts. Model names fit on the left and bars grow right. Vertical bars cramp at 1080 px wide.

### Transition
- Rec.: hard cut or "chart-to-chart morph". Keep axes fixed and tween the bar lengths and labels to the next benchmark, which reads like a newsroom flipping data; Page turn: avoid.

### Sound (rec.)
- Soft paper/pencil ticks on bar landings; Muted piano or pizzicato bed at 85–100 BPM; No risers.

### Pitfalls (cheap tells)
- Rainbow series; 3D bars; Gradient fills on bars; Truncated y-axis that exaggerates a 1-point lead. Always show 0, or explicitly mark a broken axis; Legend instead of direct labels; Missing source line or eval date; Drop shadows on the paper; Using FT pink `#FCD0B1` as the background. The paper is `#FFF1E5`, which is much paler.

---

## 2. 论文图表 arXiv / Academic figure · Distill

**Look.** A white page, Computer Modern type, "Figure 1:" captions, thin black axes, and matplotlib default colours. Its authority comes from "this is literally how papers look." Distill adds a clean web layer: system sans body, grey captions, and a thin left rule.

### Palette
matplotlib tab10, the default `axes.prop_cycle` per matplotlibrc **[F]**; hex values from `_color_data.py` **[F]**:
- `#1F77B4` blue, `#FF7F0E` orange, `#2CA02C` green, `#D62728` red, `#9467BD` purple, `#8C564B` brown, `#E377C2` pink, `#7F7F7F` grey, `#BCBD22` olive, `#17BECF` cyan.

Colour-blind-safe alternative, matplotlib `seaborn-v0_8-colorblind` **[F]**:
- `#0072B2 #009E73 #D55E00 #CC79A7 #F0E442 #56B4E9`

matplotlib defaults **[F]**:
- `lines.linewidth 1.5`, `axes.linewidth 0.8`, `font.size 10`.
- Scaled to 1080 px video, rec. axes 2px, lines 4–5px, tick labels 28–32px.

Distill template CSS **[F]**:
- links `#004276`
- figcaption `rgba(0,0,0,.6)` at 12–13px, with **bold lead-in at 600 in pure black**
- rules `rgba(0,0,0,.1)`
- blockquote: Georgia italic with a 2px left border `rgba(0,0,0,.2)`

### Type
- **CMU Serif** (Computer Modern Unicode, OFL) is the font 3b1b also uses.
- **Latin Modern Roman** (GUST Font License, LPPL-like; free use; renaming is required if you modify it).
- Math: **KaTeX**. CSS `https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css` returned 200 **[F]**. Its KaTeX_Main font is CM-derived, so equations match the CMU text.
- 中文: 思源宋体 Noto Serif SC Regular for the body, matching the "paper" feel. Mixed Chinese and English captions in 宋 + CMU look like a Chinese thesis.
- Captions: `Figure 1:` in bold-ish CMU, then sentence text. Chinese: `图 1：`.

### Motion signature (rec.)
- "Typeset" reveal: equations write in symbol by symbol (KaTeX spans, `stagger 0.04`, `opacity` + `y 6px`, `power1.out`).
- Figures appear as a whole (`opacity` over 0.4s), then a **highlight box** (`#D62728`, 3px, rounded 2px) draws around the relevant region.
- Camera push-in on the figure region: `scale 1→1.6`, `2.4s`, `power2.inOut`. This mimics "zooming into a PDF".
- Paper texture moment: an optional PDF-page frame (white with drop shadow `0 2px 24px rgba(0,0,0,.12)` on `#E9E9E6`) scrolls up like a reader.

### Texture
- None on the page itself. The surround can be a neutral desk grey `#E9E9E6`.
- Optional: a faint scanline-free "print" look, using a 0.5% noise overlay at `opacity .04`.

### Transition
- Rec.: vertical scroll between "pages", or cut to the next figure with the caption persisting; Footnote-number callouts (`[1]` superscripts in `#1F77B4`) can link segments.

### Sound (rec.)
- Very quiet: page-flip foley, a soft keyboard or pen scratch when an equation writes; Lo-fi ambient or none.

### Pitfalls
- Using Times New Roman instead of CM. It instantly reads as "Word doc"; Mixing tab10 with brand colours; Equations as screenshots. Blurry raster equations are a cheap tell. Render with KaTeX/SVG; Over-animating figures that should feel static and factual; Forgetting the paper citation: arXiv ID, authors, year.

---

## 3. 数学动画 3Blue1Brown / Manim

### Palette
- 3b1b's own `videos/custom_config.yml` **[F]**: `background_color: "#000000"`, text font `"CMU Serif"`, `file_writer.saturation: 1.5`, resolution 3840×2160 @ 30fps.
- ManimGL default config **[F]**: background `#333333`, default stroke `#DDDDDD` (GREY_A), fill `#888888`, mobject `#FFFFFF`.
- The commonly cited "#1C1C1C-ish" look is not in either config. Rec.: use `#000` like 3b1b, or `#1C1C1C` if you want softer blacks on phone OLED.

ManimCommunity `manim_colors.py` **[F]** (A = lightest → E = darkest; the bare name equals C):

| Family | A | B | C (= bare) | D | E |
|---|---|---|---|---|---|
| BLUE | `#C7E9F1` | `#9CDCEB` | `#58C4DD` | `#29ABCA` | `#236B8E` |
| TEAL | `#ACEAD7` | `#76DDC0` | `#5CD0B3` | `#55C1A7` | `#49A88F` |
| GREEN | `#C9E2AE` | `#A6CF8C` | `#83C167` | `#77B05D` | `#699C52` |
| YELLOW | `#FFF1B6` | `#FFEA94` | `#F7D96F` | `#F4D345` | `#E8C11C` |
| GOLD | `#F7C797` | `#F9B775` | `#F0AC5F` | `#E1A158` | `#C78D46` |
| RED | `#F7A1A3` | `#FF8080` | `#FC6255` | `#E65A4C` | `#CF5044` |
| MAROON | `#ECABC1` | `#EC92AB` | `#C55F73` | `#A24D61` | `#94424F` |
| PURPLE | `#CAA3E8` | `#B189C6` | `#9A72AC` | `#715582` | `#644172` |
| GREY | `#DDDDDD` | `#BBBBBB` | `#888888` | `#444444` | `#222222` |

Also **[F]**:
- PINK `#D147BD`, ORANGE `#FF862F`, DARK_BROWN `#8B4513`, GREY_BROWN `#736357`.
- LOGO colours: white `#ECE7E2`, green `#87C2A5`, blue `#525893`, red `#E07A5F`, black `#343434`.
- Note: `BLUE_E` is `#236B8E`, not `#1C758A` as one search summary claimed.

### Type
- CMU Serif (Latin and math). 中文: **LXGW WenKai** (already in kit; this is the friendly "3b1b-CN" choice) or Noto Serif SC.
- Variables in CMU Serif Italic.
- Colour-code the variables consistently: e.g. Q = `#58C4DD`, K = `#F7D96F`, V = `#FC6255` for attention.

### Motion signature (from manimlib source [F])
- **Default rate func `smooth`**: `t³(10s² + 5st + t²)` with `s = 1−t`, i.e. `6t⁵ − 15t⁴ + 10t³` (zero 1st/2nd derivative at both ends). Default `run_time` = 1s.
  - GSAP: `ease: t => t*t*t*(t*(6*t-15)+10)`. `"power2.inOut"` is a close substitute.
- `Write`:
  - run_time is 1s if the object has fewer than 15 sub-parts, else 2s.
  - lag_ratio = `min(4/(n+1), 0.2)`, linear rate.
  - Every glyph draws its border (stroke width 2), then fills (DrawBorderThenFill uses `double_smooth`, 2s).
- `ShowCreation`: `lag_ratio 1.0` (sub-paths draw sequentially).
- `Transform`: interpolates points of matched sub-paths. Its signature is that it bends with `path_arc` (0 by default; π/2 for the "swing over" look).
  - In HTML, use GSAP MorphSVG on matched SVG paths. For text, use per-glyph FLIP: matching glyphs fly to new positions and unmatched ones fade (= `TransformMatchingTex`).
- Also available: `there_and_back` for pulses/highlights, `running_start` (bezier `[0,0,-.5,-.5,1,1,1]`) for an anticipation pull-back.

### Texture
- Pure flat black. Strokes have **no glow**.
- 3b1b gets punch from `saturation 1.5` at render time, so colours look richer than the hex values. Rec.: `filter: saturate(1.15)` on the stage if the colours look dull.

### Transition
- No cuts within a concept. Objects transform into the next idea; the camera (`frame`) pans and zooms with `smooth`; Section breaks: fade everything out (`FadeOut`, 1s).

### Sound (rec.)
- Calm piano/strings (Vincent Rubinetti-style); Almost no SFX. Silence while equations write is part of the brand.

### Pitfalls
- Neon glow; Default HTML sans for maths; Linear easing. Manim's smooth is quintic; linear looks robotic; Changing a variable's colour mid-video; Too many simultaneous moves. 3b1b moves one idea at a time; Pi creature imitation. Don't use his mascot.

---

## 4. Warm Ivory: Anthropic/Claude-inspired (no logos)

Official colour values, from two sources:
- (a) `anthropics/skills` → `skills/brand-guidelines/SKILL.md` (Anthropic's own GitHub) **[F]**:
  - Dark `#141413`, Light `#FAF9F5`, Mid Gray `#B0AEA5`, Light Gray `#E8E6DC`
  - Orange `#D97757`, Blue `#6A9BCC`, Green `#788C5D`
  - Fonts it recommends: **Poppins** for headings and **Lora** for body.
- (b) anthropic.com's live stylesheet `ant-brand.shared.775d58967.min.css` **[F]** (the full swatch set):

| Swatch | Hex | Swatch | Hex |
|---|---|---|---|
| slate-dark | `#141413` | ivory-light | `#FAF9F5` |
| slate-medium | `#3D3D3A` | ivory-medium | `#F0EEE6` |
| slate-light | `#5E5D59` | ivory-dark | `#E8E6DC` |
| cloud-dark | `#87867F` | oat | `#E3DACC` |
| cloud-medium | `#B0AEA5` | manilla | `#EBDBBC` |
| cloud-light | `#D1CFC5` | kraft | `#D4A27F` |
| **clay** | `#D97757` | **accent** | `#C6613F` |
| pencil | `#F0AC54` | peach | `#EBC9B7` |
| sky | `#6A9BCC` | cloud (blue) | `#C5D3E0` |
| olive | `#788C5D` | matcha | `#CED6BF` |
| mineral | `#629987` | cactus | `#BCD1CA` |
| fig | `#C46686` | orchid | `#E5CADA` |
| plum | `#827DBD` | heather | `#CBCADB` |
| poppy | `#DE6262` | coral | `#EBCECE` |

More from the same CSS **[F]**:
- Site fonts are proprietary "Anthropic Sans" / "Anthropic Serif"; "Tiempos Text" also appears.
- UI transitions are a uniform `.2s` on color/background/border. Calm, nothing bouncy.

### Type (free alternatives, rec.)
- Headline serif (Tiempos / Anthropic Serif feel): **Fraunces** (OFL, opsz 9–144, SOFT and WONK axes). Set `SOFT 50–100`, `opsz 72+`, weight 400–500 for a warm, slightly inky display. Or use **Newsreader**, more neutral. Lora is the brand-skill fallback.
- Sans for UI labels: Inter Tight / Instrument Sans. The brand skill suggests Poppins.
- 中文:
  - Headlines in **思源宋体 Noto Serif SC 600**.
  - Human or "thinking" quotes in **LXGW ZhenKai 霞鹜臻楷** (new; OFL) or LXGW WenKai.
  - Body in Noto Sans SC 400.
- Text colour `#141413` on `#FAF9F5`. Secondary text `#5E5D59`.

### Motion signature (rec.)
- Slow and confident: `duration 0.8–1.2`, `ease "power2.out"` / `"expo.out"` for entrances; text line-by-line `stagger 0.08`.
- No bounce, no overshoot.
- "Thinking" motif: a small clay asterisk/spark (draw your own, not the logo) breathing at `scale 1↔1.06`, `2.4s`, `sine.inOut`, yoyo.
- Spot illustrations draw on with DrawSVG at `1.6s` `power1.inOut`. The stroke is `#141413` at 3–4px with round caps and a slightly wobbly path, then fills with flat clay/oat/sky/olive blocks.

### Texture
- Paper grain: SVG `feTurbulence` noise at `opacity .05–.08`, `mix-blend-mode: multiply` on `#F0EEE6`.
- Illustrations: hand-drawn black outline, flat fills, slight misregistration (fill offset by 4–6px from the outline).

### Transition
- Soft wipe: an `#E3DACC` oat panel slides over in `0.6s` `power3.inOut`. Or a cross-dissolve over a clay full-bleed card.

### Sound (rec.)
- Warm acoustic: felt piano, soft marimba, paper and pencil foley; 70–90 BPM. No sub-drops.

### Pitfalls
- Using the Claude/Anthropic logo or "spark" mark, or official-looking lockups. This is "inspired by", so avoid impersonation; Pure white `#FFF` background. It kills the warmth; Saturated orange `#FF6600`. Clay is a dusty `#D97757`; Sans-only typography; Glossy 3D renders mixed with flat drawings; Gradients. The brand is flat.

---

## 5. Aurora / Glow Dark Launch: Linear · Vercel · Raycast

### Palette
- Linear brand page **[F]**:
  - Mercury White `#F4F5F8`, Nordic Gray `#222326`. The primary brand colour is described as "a subtle desaturated blue" (its hex was not in the page text).
  - The site also uses `#08090A` and `#0F1012` near-blacks and `#9C9DA1` grey text.
- Raycast homepage **[F]**:
  - Brand red `#FF6363`.
  - Aurora stops: deep indigo `#070D4F`, `#030F81`, `#043F96`, violet `#330381`, `#523091`, magenta `#550062`, `#1A0B33`.
- Vercel Geist **(unverified)**: background `#000` / `#0A0A0A`, text `#EDEDED`, gray scale with P3 colours. The colors page confirms 10 scales: Gray, Gray-alpha, Blue, Red, Amber, Green, Teal, Purple, Pink, plus backgrounds **[F]**.
- MagicUI `border-beam` defaults **[F]**: `colorFrom #FFAA40` → `colorTo #9C40FF`, size 50, `duration 6s`, linear, infinite.

### Type
- **Inter Tight** (already in kit) or **Geist** (in C3), tracking −0.02em at display sizes, weight 500–600.
- 中文: **MiSans** 500/600, or HarmonyOS Sans.
- Mono labels: Geist Mono / JetBrains Mono.

### Techniques
- **Border beam**: an element on `offset-path: rect(0 auto auto 0 round R)` animates `offset-distance 0→100%` with a linear ease. It sits inside a 1px border masked by `mask: linear-gradient(transparent,transparent), linear-gradient(#000,#000); mask-composite: intersect; mask-clip: padding-box, border-box`. Source: magicui `border-beam.tsx` **[F]**; MDN `mask-composite` (200).
- **Aurora / mesh**: 3–5 large blurred radial gradients (`filter: blur(80–120px)`) with 20–40s slow drift on `x`/`y` (`sine.inOut`, yoyo), plus a **noise overlay**. Keep the luminance below 25%.
- **Frosted glass**:
  - `backdrop-filter: blur(24px) saturate(140%)`, `background: rgba(255,255,255,.04–.06)`.
  - 1px top highlight `inset 0 1px 0 rgba(255,255,255,.08)`; 1px border `rgba(255,255,255,.08)`.
  - Optional inner gradient stroke.
- **Spotlight / hero glow**: a radial gradient centred behind the product at `opacity .35`, plus a thin horizontal "horizon" line glow.

### Motion signature (rec.)
- Titles: blur-to-sharp reveal (`filter: blur(12px)→0`, `opacity`, `y 20→0`), `0.9s`, `expo.out`, per-word stagger `0.05`.
- Numbers flip like a split-flap or roll.
- Camera: slow 3D tilt of UI cards (`rotateX 12°→0`, `perspective 1200px`, `1.4s`, `power3.out`).
- Hold everything still for a beat after big reveals.

### Transition
- Light sweep across the frame (a 30° skewed white gradient at 0.15 opacity, `0.6s`), or a dissolve through black with the aurora persisting underneath.

### Sound (rec.)
- Airy synth pads, sub-bass "whoom" on reveals, crisp glassy UI clicks; 100–120 BPM; minimal techno/house.

### What keeps it premium vs cheap
- **One** hue family per video. For an Opus video, rec. warm amber→clay or cool indigo, not both.
- Glow luminance is low; text sits on near-black, not on the gradient.
- Always add a noise/grain overlay (`opacity .03–.06`) to kill gradient banding. This matters even more after H.264 compression at 9:16.
- Borders are 1px at alpha .06–.12. Radii are consistent (rec. 16/24px).
- **Cheap tells:**
  - full-saturation rainbow gradients; glassmorphism over busy photos; neon text glow (`text-shadow` spread); lens flares; multiple simultaneous beams; gradient text on body copy; visible banding.

---

## 6. Industrial Instrument: Teenage Engineering × Dieter Rams

### Palette
- teenage.engineering homepage **[F]**:
  - Greys `#E5E5E5`, `#F1F2F2`, `#C5C6CD`; inks `#121114`, `#231F20`, `#000`.
  - One red `#ED2024`.
  - Web font: Univers Next Pro (Thin seen).
- Signal orange (OP-1/Braun-style) **(unverified)**. Rec. `#FF5A1F` for the single "active" accent, with LCD yellow-green `#C8FF3D` for readout text on dark.
- Rams "less but better" **(unverified)**: warm greys `#D9D6CF`/`#EDEBE6`, black controls `#1A1A1A`, one functional colour (orange or green) for the primary control.

### Type
- Mono spec text: **Space Mono** (OFL) for character, **DM Mono** (OFL) for neutral.
- Dot-matrix: **Doto** (OFL variable, has a ROND axis).
- 7-segment numerals: **DSEG7 Classic** (OFL).
- Pixel UI: **Departure Mono** (OFL).
- Labels: Archivo / Inter Tight at small sizes in caps with +0.08em tracking, to mimic Univers-like panel labels.
- 中文: **MiSans** 400/500 for labels. Avoid serif. For chips, use small caps-like Chinese at 0.9em with tracking +0.05em.

### Layout
- Spec-sheet grid: 12-column, 48px gutter, every value in a cell with a hairline `#121114` at 1px.
- Index numbers `01 / 02` and units in grey `#87867F`-ish.
- Big numerals in DSEG7 or Doto showing "tokens/s", "$ / Mtok", "latency ms".
- Knob/fader graphics are pure circles and rectangles, no gradients.

### Motion signature (rec.)
- Mechanical and stepped: `ease "steps(8)"` for counters.
- Toggles snap: `0.12s`, `power4.out`, with a 2px overshoot via `back.out(3)`.
- LED indicators blink at 2Hz.
- Panels slide in like drawers (`x`, `0.35s`, `power3.out`).
- Seven-segment digits roll by switching glyphs, not by tweening opacity.

### Texture
- Matte plastic: very subtle noise `opacity .03`.
- Bead-blasted aluminium: a light linear gradient `#F1F2F2→#E5E5E5` with 0.5% noise.
- No shadows except a 1px drop `rgba(0,0,0,.15)` under "buttons".

### Transition
- Hard cuts on beat, or a "screen-off" collapse to a horizontal line (CRT-ish, `scaleY 1→0.005`, `0.18s`), then expand.

### Sound (rec.)
- Synth blips, button clicks, sample-and-hold arps, OP-1-style tape stops; Dry, no reverb.

### Pitfalls
- Too many accent colours; Skeuomorphic gradients and bevels; Fake "techy" HUD clutter (random hex dumps, sci-fi brackets everywhere); Using the dot-matrix font for long Chinese text. Doto, DSEG and VT323 have **no hanzi**; Mixing rounded and sharp corners.

---

## 7. Blueprint / Technical Line Drawing

### Palette
- Prussian blue `#003153` (Wikipedia infobox) **[F]**. Blueprints are "white lines on a blue background, a negative of the original" (Wikipedia: Blueprint) **[F]**. Cyanotype chemistry yields Prussian blue (Wikipedia: Cyanotype) **[F]**.
- Rec. stack:
  - background `#0B3A66` (lighter, phone-friendly) with vignette to `#062744`
  - major gridlines `rgba(255,255,255,.14)` every 120px, minor `rgba(255,255,255,.06)` every 24px
  - lines `#F4F8FF`
  - highlight cyan `#7FD3FF`
  - redline `#FF6B5A` for annotations / "changed parts"
- Light inverse ("whiteprint"): paper `#F4F1E8`, lines `#1D3B6E`.

### Type
- **IBM Plex Mono** (in kit) or **Space Mono** for dimensions.
- Rec. **osifont** (ISO 3098 technical lettering) **(unverified licence/URL; not fetched)**.
- Title block in Archivo caps.
- 中文: Noto Sans SC Light/Regular or **Sarasa Mono SC** (from C2) for aligned annotations. Hairline Chinese works only at ≥32px.

### Motion signature (rec.)
- **Stroke-draw everything**: `stroke-dasharray = length`, tween `stroke-dashoffset length→0` (GSAP DrawSVG: `drawSVG "0% 100%"`).
  - Outlines `1.2s` `power1.inOut`; then dimension lines `0.5s` each; arrowheads pop `0.15s`; numbers type in (`steps`).
- Construction lines first (dashed, 30% alpha), then solid geometry over them, then the construction lines fade to 10%.
- Camera: slow pans along the drawing; zoom to a "detail circle" callout (circle draws, then a magnified inset).

### Texture
- Paper fibre noise at `opacity .06`.
- Slight line bleed: `filter: blur(.3px)` and a duplicate line at `opacity .25`, `blur(2px)`.
- Optional folded-paper creases as a faint lighter diagonal band.

### Transition
- Rec.: grid persists. The old drawing "erases" in reverse stroke-draw, `0.6s`, while the new one draws; Or pan to an adjacent sheet with a title-block change (`SHEET 2/5`).

### Sound (rec.)
- Pencil and technical-pen scratches, ruler clicks, a quiet room tone; Minimal ambient/ticking clock music.

### Pitfalls
- Saturated electric blue `#0000FF`; Thick lines. Keep hairlines at 1.5–2px, with heavier 3px only for outlines; Fake dimensions that don't add up; Using blueprint for everything. It suits architecture, pipelines and hardware; it is wrong for leaderboards; Gridlines so strong that they compete with content.

---

## 8. 国风水墨 Ink Wash (premium, not 古装-kitsch)

### Palette
Chinese traditional colours, from the zerosoul/chinese-colors dataset (a community compilation) **[F]**:
- **Paper:**
  - 缟 `#F2ECDE` (rec. default rice-paper)
  - 象牙白 `#FFFBF0`
  - 鱼肚白 `#FCEFE8`
  - 牙色 `#EEDEB0` (aged)
- **Ink:**
  - 漆黑 `#161823` (rec. main ink)
  - 乌黑 `#392F41`
  - 玄青 `#3D3B4F`
  - 墨色 `#50616D` (wash mid-tone)
  - 墨灰 `#758A99` (light wash)
  - 苍 `#75878A`
- **Seal / cinnabar:**
  - 胭脂 `#9D2933` (deep seal; rec. for 印章)
  - 朱红 `#FF4C00` and 丹 `#FF4E20`. These are bright, so use them small.
  - Wikipedia vermilion infobox `#FF4000`/`#E34234`-family **[F]**.
  - Rec. seal red `#B7352B` as the compromise.
- **Mineral accent** (sparingly): 石青 `#7BCFA6`, 藏青 `#2E4E7E`, 黛 `#4A4266`.

### Fonts (free-commercial, verified this session)
- **LXGW ZhenKai GB 霞鹜臻楷** (OFL; 20,992 hanzi) is the elegant formal kai. It is the most "premium" free 楷 for headlines.
- **演示春风楷** (author statement: free commercial for companies and individuals; GB2312 6,763 hanzi). Neat, readable brush kai.
- **Ma Shan Zheng 马善政楷书** and **Zhi Mang Xing 钟齐志莽行书** (OFL, on Google Fonts; 6,763 hanzi each). Ma Shan Zheng for bold brush titles; Zhi Mang Xing for running-script accents.
- **江西拙楷** (author statement free commercial; **only 6,055 hanzi**, below GB2312, so lint glyphs).
- 演示悠然小楷 and 霞鹜文楷 are already in the kit.
- Licence listed as author-statement free commercial on maoken.com, no download URL tested (login wall):
  - 千图纤墨体 (calligraphy-style handwriting)
  - 仓耳与墨 (seal-carving "knife" strokes, 5 weights)
  - 仓耳非白
  - 演示秋鸿楷
  - iSlide 云犹体 (brush)
- 字魂: most are paid. **字魂扁桃体** is OFL per maoken but is a playful display font, not ink.
- Latin pairing: **Cormorant / EB Garamond** (OFL, unverified this session) or Newsreader Italic; small caps for romanisation.

### Ink-bleed reveal techniques (CSS/SVG)
1. **Displacement mask.** Text or brush SVG sits under `mask-image` of a large radial gradient whose radius tweens from 0→150%. The mask passes through an SVG filter `feTurbulence (type="fractalNoise", baseFrequency .012–.03, numOctaves 3–4)` → `feDisplacementMap scale 30–60`, so the edge looks like ink wicking into paper. Tween `scale` 60→0 to "settle". MDN feTurbulence / feDisplacementMap (200) **[F]**.
2. **Blur-threshold "gooey" bleed.** A blurred white mask (`feGaussianBlur stdDeviation 8`) followed by `feComponentTransfer` alpha table `0 0 1 1` (or `feColorMatrix` alpha `×20 −8`) gives organic blob edges. Animate the blob circles' radius.
3. **Brush-stroke draw.** Calligraphy as SVG paths with variable width: build the shape as a filled outline and reveal it with a mask path drawn via DrawSVG along the stroke's skeleton.
4. **Wash layers.** 3–4 large ink-wash PNGs/SVG blobs in `#50616D`→`#758A99` at `opacity .15–.35`, `mix-blend-mode: multiply`, drifting `x ±30px` over 20s.
5. **Seal stamp.** A square `#B7352B` seal with white carved text (仓耳与墨 or Ma Shan Zheng), a rough edge via `feTurbulence` + `feDisplacementMap scale 4`. Enters with `scale 1.4→1`, `0.18s`, `power4.in`, then a 2-frame 2px shake. Add a thud SFX.

### Motion signature (rec.)
- Slow: entrances `1.6–2.4s`, `sine.inOut` / `power1.out`.
- Text appears stroke-by-stroke or by ink bleed, never by sliding.
- Lots of 留白 (negative space). One vertical title column (`writing-mode: vertical-rl`) on the right, seal under it.
- Mist layers parallax at different speeds.

### Texture
- Xuan paper: fibre noise (`feTurbulence baseFrequency .9`, `numOctaves 1`, alpha .06) plus 2–3 faint large stains.
- Edge vignette `rgba(57,47,65,.12)`.

### Transition
- Ink drop expands to fill the frame (`#161823`), then recedes to reveal the next scene. Or a slow cross-dissolve through a wash layer.

### Sound (rec.)
- Guqin, xiao, or sparse pipa; Brush-on-paper foley, a water drip at the ink-drop, a deep seal "thud"; Reverb: large hall at low mix.

### Pitfalls
- Over-ornamentation: clouds, dragons and gold gradients together read as 页游 ads; Bright 朱红 everywhere; Simulating calligraphy with a non-calligraphy font plus `skew`; Mixing ink wash with neon or glass; Using 草书 (Liu Jian Mao Cao) for anything that must be read; Missing glyphs. Most brush fonts are GB2312-only, so set the fallback to `"LXGW ZhenKai GB","Noto Serif SC"`.

---

## 9. Isometric 2.5D Diagrams + Particle Fields

### Isometric
- **True isometric math:** view elevation = arctan(1/√2) = 35.264°.
  - CSS: `transform: rotateX(54.7356deg) rotateZ(-45deg)` on the ground plane, or skew-based faces: top `rotate(30deg) skewX(-30deg) scaleY(.864)`, left `skewY(30deg)`, right `skewY(-30deg)`.
  - The "2:1 pixel isometric" variant uses 26.565° (arctan 0.5) for crisp pixel edges.
  - (math; rec.)
- **Reference tools and libraries [F, via GitHub API]:**
  - **Isoflow** (`markmanx/isoflow`, MIT, ★1.7k): open-source isometric network/infra diagrams; its look is a good spec for "AI system architecture".
  - **Isomer** (`jdan/isomer`, MIT, ★2.9k): isometric canvas library.
  - Visual references (unverified): Stripe's and Kurzgesagt-style isometric explainers; AWS/Azure isometric architecture icon sets.
- Style tokens (rec.):
  - Face shading from one light source: top 100%, left 82%, right 64% of the base colour (e.g. `#5E6AD2` / `#4D58B0` / `#3C4590`).
  - Edges 1.5px at 20% darker.
  - Ground grid `rgba(255,255,255,.06)` on dark.
  - Max 2 accent hues; data packets are small glowing cubes or dots travelling along iso paths.
- Motion (rec.):
  - Blocks drop in from `y −80` with `back.out(1.4)`, `0.5s`, stagger 0.05 by depth (back-to-front).
  - Packets travel paths with MotionPath, `linear`, looping.
  - Camera dolly is a pure `scale` + translate; never rotate the iso camera.

### Particle fields (dots forming shapes)
- Technique:
  - Sample N target points from a text/SVG/logo shape (draw to an offscreen canvas, read alpha > 0.5 at a grid step of 6–10px), giving 2k–8k points.
  - Tween each particle from its random/noise position to its target with a per-particle delay = distance-based stagger, `1.6s`, `expo.inOut`. Add curl/simplex noise drift at idle (amplitude 1–3px).
- Deterministic rendering for HyperFrames: drive positions only from timeline progress `t` and a **seeded** RNG. Never `Math.random()` per frame. Canvas 2D handles ~10k dots at 1080×1920. For more, use three.js `Points` with the morph in a shader keyed to `uProgress`.
- References:
  - **tsParticles** (`tsparticles/tsparticles`, MIT, ★9k) **[F]**
  - MagicUI `particles.tsx` (fetched; canvas implementation) **[F]**
  - Three.js Journey "particles morphing" lesson **(unverified)**
  - Bartosz Ciechanowski's explainers at ciechanow.ski (200), the gold standard of interactive scientific explainers.
- Tokens (rec.):
  - Dots 2–3px, round.
  - 2 colours max: main `#EDEDED` at 70% and highlight = your accent.
  - On dark, add `globalCompositeOperation='lighter'` only for the highlight cluster.
- Pitfalls:
  - Particle "dust" that never resolves into meaning; Too many particles, which turns into mush after video compression; Random jitter in renders (non-seeded); Mixing iso projection with a perspective camera; Inconsistent light direction across blocks.

---

## 10. Additional free-for-commercial fonts (verified this session)

Each file was downloaded with `curl`, then its `name` table and cmap were read with fontTools.
- `github.com/google/fonts/raw/main/...` URLs worked but were flaky: one or two retries were needed and some first attempts returned 000.
- GitHub release URLs needed `--connect-timeout 30 -m 280` and a retry.

### Primary recommendations (6)

| Font | Licence (from file) | Hanzi | Serves | Direct download URL | GF css2 |
|---|---|---|---|---|---|
| **CMU Serif** (Computer Modern Unicode) | SIL OFL 1.1 | 0 | 2 arXiv, 3 Manim | `https://mirrors.ctan.org/fonts/cm-unicode/fonts/otf/cmunrm.otf` (200, 330 KB, v0.7.0). Same dir: `cmunti.otf` italic (200), `cmunbi.otf` bold italic (200), `cmunbx.otf` bold (timed out; name unverified) | No |
| **Newsreader** (variable opsz 6–72, wght 200–800) | OFL 1.1 | 0 | 1 Data journalism, 4 Warm Ivory | `https://github.com/google/fonts/raw/main/ofl/newsreader/Newsreader%5Bopsz,wght%5D.ttf` (200, 452 KB, v1.003) | Yes (200) |
| **Fraunces** (variable SOFT, WONK, opsz 9–144, wght) | OFL 1.1 | 0 | 4 Warm Ivory (Tiempos-ish warmth), 8 Latin pairing | `https://github.com/google/fonts/raw/main/ofl/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf` (200, 360 KB) | Yes (200) |
| **LXGW ZhenKai GB 霞鹜臻楷** | OFL 1.1 (file name table) | **20,992** | 8 Ink wash, 4 quotes | `https://github.com/lxgw/LxgwZhenKai/releases/download/v0.825/LXGWZhenKaiGB-Regular.ttf` (200, 17.5 MB, v0.825, 2026-03-17) | No |
| **Doto** (dot-matrix, variable ROND, wght) | OFL 1.1 | 0 | 6 Instrument, 9 particles titles | `https://github.com/google/fonts/raw/main/ofl/doto/Doto%5BROND,wght%5D.ttf` (200, 457 KB) | Yes (200) |
| **DSEG7 Classic** (7-segment; also DSEG14, Modern, MINI) | OFL 1.1 (RFN "DSEG") | 0 | 6 Instrument numerals (latency, tokens/s) | `https://github.com/keshikan/DSEG/releases/download/v0.46/fonts-DSEG_v046.zip` (200, 1.1 MB; ttf + woff2 inside) | No |

### Also verified (alternates)

| Font | Licence | Hanzi | Serves | URL (status) |
|---|---|---|---|---|
| Source Serif 4 (var opsz 8–60) | OFL 1.1 (RFN "Source") | 0 | 1, 2 | `https://github.com/google/fonts/raw/main/ofl/sourceserif4/SourceSerif4%5Bopsz,wght%5D.ttf` (200, 1.2 MB) |
| Latin Modern Roman 10 | GUST Font License (file copyright string; name ID 13 empty). fsType=12, i.e. editable-embedding bits set | 0 | 2 | `https://mirrors.ctan.org/fonts/lm/fonts/opentype/public/lm/lmroman10-regular.otf` (200, 112 KB) |
| DM Mono | OFL 1.1 | 0 | 6, 7 | `https://github.com/google/fonts/raw/main/ofl/dmmono/DMMono-Regular.ttf` (200) |
| Space Mono | OFL 1.1 | 0 | 6, 7 | `https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Regular.ttf` (200) |
| VT323 | OFL 1.1 | 0 | 6 (CRT/terminal) | `https://github.com/google/fonts/raw/main/ofl/vt323/VT323-Regular.ttf` (200) |
| Departure Mono | OFL 1.1 | 0 | 6 (pixel UI) | `https://github.com/rektdeckard/departure-mono/releases/download/v1.500/DepartureMono-1.500.zip` (200, otf + woff2) |
| Ma Shan Zheng 马善政楷书 | OFL 1.1 | 6,763 | 8 brush titles | `https://github.com/google/fonts/raw/main/ofl/mashanzheng/MaShanZheng-Regular.ttf` (200, 5.9 MB) |
| Zhi Mang Xing 钟齐志莽行书 | OFL 1.1 | 6,763 | 8 running-script accents | `https://github.com/google/fonts/raw/main/ofl/zhimangxing/ZhiMangXing-Regular.ttf` (200, 4.1 MB) |
| 演示春风楷 Slidechunfeng | Author statement: "面向全社会提供全媒体免费可商用" (maoken 6073). File copyright "keynoteart, All rights reserved" | 6,763 | 8 | `https://cdn.jsdelivr.net/gh/wordshub/free-font@master/assets/font/%E4%B8%AD%E6%96%87/%E5%85%B6%E4%BB%96%E5%AD%97%E4%BD%93/%E6%BC%94%E7%A4%BA%E6%98%A5%E9%A3%8E%E6%A5%B7.ttf` (200, 9.7 MB, third-party mirror) |
| 江西拙楷 | Author statement (企业、个人均可免费商用), per maoken 1438 | **6,055** ⚠ | 8 | `.../%E5%85%B6%E4%BB%96%E5%AD%97%E4%BD%93/%E6%B1%9F%E8%A5%BF%E6%8B%99%E6%A5%B7.ttf` (same jsDelivr base; 200, 9.9 MB) |
| 寒蝉全圆体 ChillRound M | OFL 1.1 (derived from Zen Maru Gothic) | 11,172 | soft-rounded UI for 4/9 | `https://github.com/Warren2060/ChillRound/releases/download/v1.805/ChillRoundM_v1.805.zip` (200, 7 MB) |
| 江城斜宋体 | OFL (derived from Source Han; 7 weights; 12° slant), per maoken 4679 | — | 1 editorial italic Chinese | maoken.com/freefonts/4679.html (login-walled; **not downloaded**) |
| Long Cang, Liu Jian Mao Cao | OFL (GF) | — | 8 accents only | GF css2 200 |

**Not recommended / unresolved.**
- "975 Maru" was not researched (search quota exhausted).
- osifont: licence and URL unverified.
- 令东齐伋体: the jsDelivr mirror returned 403.
- Typewolf's Financier "free alternative" is paywalled.
- Vercel Geist colour hex values: their CSS chunks returned 404.
- Bloomberg graphics: 403, so no tokens were taken.

**Coverage reminder.** Latin display fonts (Doto, DSEG, VT323, CMU, Fraunces…) have **zero hanzi**, so always declare a Chinese family next in the stack. Brush fonts other than ZhenKai cover only about GB2312.

---

## 11. Copy-paste snippets (rec.)

```css
/* FT paper chart frame */
:root{--paper:#FFF1E5;--wheat:#F2DFCE;--ink:#262A33;--oxford:#0F5499;--claret:#990F3D;--muted:#B3A9A0;}
.kicker{color:var(--claret);font:600 28px/1 "Inter Tight","MiSans";letter-spacing:.08em;text-transform:uppercase}
.headline{font:500 72px/1.08 "Newsreader","Noto Serif SC";font-variation-settings:"opsz" 72}
.num{font-variant-numeric:tabular-nums lining-nums}

/* Warm ivory grain */
.grain{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.06;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
```

```html
<!-- Ink-bleed filter (animate #disp scale 60->0 and mask radius 0->150%) -->
<svg width="0" height="0"><filter id="ink"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="4" seed="7"/>
<feDisplacementMap id="disp" in="SourceGraphic" scale="60" xChannelSelector="R" yChannelSelector="G"/></filter></svg>
```

```js
// Manim "smooth" for GSAP (quintic smoothstep = 6t^5-15t^4+10t^3)
const smooth = t => t*t*t*(t*(6*t-15)+10);
gsap.to(el, {x: 400, duration: 1, ease: smooth});
```

---

## Sources (fetched unless marked)
- FT o-colors palette: https://cdn.jsdelivr.net/npm/@financial-times/o-colors@6.7.1/src/scss/_palette.scss
- FT g-chartcolour: https://cdn.jsdelivr.net/npm/g-chartcolour@0.8.26/src/line-web.js , …/src/categorical_bar.js , …/src/backgrounds.js , …/src/muted-first-line-web.js
- FT Chart Doctor / Visual Vocabulary repo (metadata): https://github.com/Financial-Times/chart-doctor
- Financier background (search summary): https://klim.co.nz/blog/financier-design-information/ , https://www.typewolf.com/financier-display
- Economist design system (red `#E3120B`, `#0D0D0D` in HTML): https://design-system.economist.com/foundations/colours
- Economist homage tokens [S]: https://www.webdesignhot.com/design.md/theeconomist/
- Economist red via brand-colour site [S]: https://www.brandcolorcode.com/the-economist
- OWID colour schemes: https://raw.githubusercontent.com/owid/owid-grapher/master/packages/@ourworldindata/grapher/src/color/CustomSchemes.ts
- OWID fonts: https://ourworldindata.org/assets/owid.css
- The Pudding fonts and story colours: https://pudding.cool/
- Distill template CSS: https://github.com/distillpub/template/tree/master/src/styles (styles-base.css, d-article.css)
- matplotlib: https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/mpl-data/matplotlibrc , …/_color_data.py , …/stylelib/seaborn-v0_8-colorblind.mplstyle
- KaTeX CDN: https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css
- Manim CE colours: https://github.com/ManimCommunity/manim/blob/main/manim/utils/color/manim_colors.py
- ManimGL defaults, rate functions, animations: https://github.com/3b1b/manim/blob/master/manimlib/default_config.yml , …/manimlib/utils/rate_functions.py , …/manimlib/animation/creation.py , …/animation/animation.py , …/animation/transform.py
- 3b1b's own config (black background, CMU Serif, saturation 1.5): https://github.com/3b1b/videos/blob/master/custom_config.yml
- Anthropic brand skill (official repo): https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md
- anthropic.com swatches and fonts: https://www.anthropic.com/ → https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/css/ant-brand.shared.775d58967.min.css
- Third-party Anthropic palette pages [S], consistent with the above: https://www.designpieces.com/palette/anthropic-color-palette-hex-and-rgb/ , https://www.webdesignhot.com/design.md/anthropic/
- Linear brand: https://linear.app/brand
- Raycast: https://www.raycast.com/
- Vercel Geist colours (scale names only): https://vercel.com/geist/colors
- MagicUI border-beam and particles: https://github.com/magicuidesign/magicui/blob/main/apps/www/registry/magicui/border-beam.tsx , …/particles.tsx
- MDN: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence , …/feDisplacementMap , https://developer.mozilla.org/en-US/docs/Web/CSS/mask-composite
- GSAP DrawSVG / MorphSVG docs (pages reachable; "free for all" status unverified in fetched text): https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/ , https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
- Teenage Engineering: https://teenage.engineering/ , https://teenage.engineering/products/op-1
- Wikipedia: https://en.wikipedia.org/wiki/Prussian_blue , https://en.wikipedia.org/wiki/Blueprint , https://en.wikipedia.org/wiki/Cyanotype , https://en.wikipedia.org/wiki/Vermilion , https://en.wikipedia.org/wiki/Cinnabar
- Chinese traditional colours dataset: https://github.com/zerosoul/chinese-colors (src/assets/colors.json)
- Isometric / particles repos (GitHub API metadata): https://github.com/markmanx/isoflow , https://github.com/jdan/isomer , https://github.com/tsparticles/tsparticles ; explainer reference https://ciechanow.ski/
- Font licence pages (maoken.com aggregator; licence field read from page):
  - 演示春风楷 https://www.maoken.com/freefonts/6073.html; 江西拙楷 https://www.maoken.com/freefonts/1438.html; 江城斜宋体 https://www.maoken.com/freefonts/4679.html; 站酷仓耳渔阳体 https://www.maoken.com/freefonts/6665.html; 仓耳与墨 https://www.maoken.com/freefonts/6929.html; 仓耳非白 https://www.maoken.com/freefonts/6919.html; 千图纤墨体 https://www.maoken.com/freefonts/11323.html; 字魂扁桃体 https://www.maoken.com/freefonts/18575.html; 演示秋鸿楷 https://www.maoken.com/freefonts/6094.html; iSlide 云犹体 https://www.maoken.com/freefonts/6025.html.
- Font files: URLs as listed in §10, plus https://github.com/Warren2060/ChillRound , https://github.com/lxgw/LxgwZhenKai , https://github.com/keshikan/DSEG , https://github.com/rektdeckard/departure-mono
