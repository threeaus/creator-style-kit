# GitHub research: video style presets for 9:16 Chinese tech-creator videos (HyperFrames)

Researched 2026-10-08. The GitHub search API supplied stars, license and last-push dates. Files were read through jsDelivr. **Every repo cited below was fetched**, at least its README. Items marked *(unverified)* were not opened or could not be confirmed. The core GitHub API rate limit ran out partway through, so a few license values come from the repo's LICENSE file and not from the API. Those are noted.

---

## (a) Top 15 finds

| # | Repo | Stars | License | Last push | What is reusable | Maps to |
|---|---|---|---|---|---|---|
| 1 | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 1.4k | MIT (LICENSE file; API says NOASSERTION) | 2026-10-05 | **43 `styles/<x>/STYLE.md` style prompts, all tuned for Opus 5.5 and all following one 11-section schema**: Essence & what it is not, Materials, Colour logic, Type & subtitles, Motion quality, Camera grammar, Sound palette, Native moves, Pitfalls, Engine, Variation space. I read `swiss-motion` and `dark-keynote`. Both give exact eases, hex values, font choices and foley lists. | Best template for the *shape* of a preset. Swiss Grid, Dark Keynote, Hologram HUD, ASCII/CRT, Risograph, Halftone Dossier, Blueprint, Dataviz |
| 2 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 58.9k | Apache-2.0 | 2026-10-08 | `packages/shader-transitions` registry contains 14 WebGL transitions: `domain-warp, ridged-burn, whip-pan, sdf-iris, ripple-waves, gravitational-lens, cinematic-zoom, chromatic-split, glitch, swirl-vortex, thermal-distortion, flash-through-white, cross-warp-morph, light-leak`. Also `frame.md`, a DESIGN.md superset for the camera, with named design templates (Biennale Yellow, BlockFrame, Bold Poster, Broadside, Capsule, Cartesian, Cobalt Grid…), plus `npx hyperframes add` catalog blocks. A cached file listing showed `skills/hyperframes/palettes/*.md` (dark-premium, neon-electric, warm-editorial…), but those paths return 404 on current `main` *(moved; unverified)*. | Transition vocabulary for every preset. Use frame.md as the token layer |
| 3 | [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills) (`kinetic-reel`) | 131 | MIT | 2026-09-27 | One skill per style, made with Opus 5.5. `references/style-guide.md` contains palette tokens (`ink #0E0F0E, cream #F1EEE6, lime #DDF53D, blue #2F3CFF, red #E8412F`), type roles (cond / wide / serif / mono / zh), named motion helpers (`dropWord` expo-out stagger, `odometer`, `tape`, `glitchIn`, `hud`, `texWindow`) and a **transition map `TR`** (`trZoom, trIris, trPush, trWipe, trSlats, trGrid`) with the rule "0.45–0.6 s, never three of one kind in a row". `references/sound.md` has rules: **no noise whooshes**, about half the cuts get no transition sound, `impact()` only about 5 times per piece. | Poster Kinetic, HUD |
| 4 | [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) | 1.1k | MIT | 2026-09-28 | `references/motion-grammar.md` gives 6 rules drawn from 28 launch films (foreground becomes the transition, one persistent actor, density through hierarchy, change speed, hard cuts are OK when motion continues, cause → effect), a catalog of 16 mechanisms and pacing numbers (beats of 1.4–3.5 s, no stretch without motion longer than ~0.6 s, frame 0 must be a finished composition). Built for HyperFrames. | Rules shared by all presets |
| 5 | [Cele-san/vox-style-animation](https://github.com/Cele-san/vox-style-animation) | 2 | MIT | 2026-07-14 | **A HyperFrames-native style pack with tuned GSAP defaults.** Text entrance 0.55–0.75 s `expo.out`/`power3.out` with y 36–50→0. Card slap-in 0.5–0.6 s `back.out(1.15)` at most. Hero lockup blur 14→0. Dot field `steps(12fps)`. Pen strokes `steps(6–7)`. Highlighter `scaleX` 0.45 s `power2.out`. The sheet-wipe is the only transition. Also `capture-your-own-style.md`, a 7-step method for turning any style into a pack, and `brand-tokens.css`. | Editorial Paper. Method for writing new presets |
| 6 | [ojuliocouto/video-ads-machine-2](https://github.com/ojuliocouto/video-ads-machine-2) | 1 | MIT | 2026-09-01 | **A 9:16 HyperFrames preset system** in 6 independent dimensions (`caption, lettering, transition, grade, hook, endcard`). Each preset is a file in `presets/<dim>/<name>.css|.js` marked `validated` or `unvalidated`, and `brief.json` selects them. `references/style.md` has exact numbers for 1080×1920: captions Montserrat 600 60 px with Playfair italic 66 px keyword at bottom 330 px; a warm soft-light grade; a 9×16 grid-wipe with stagger 0.28; a z-order ladder. | Warm Talking-head. Schema dimensions |
| 7 | [bangtutorial/bang-motion](https://github.com/bangtutorial/bang-motion) | 583 | MIT | 2026-09-15 | A table of **10 style directions** (background / type / signature motion / good for): Cinematic dark, Poster color-block, Editorial light, Paper & print, Retro/analog, Brutalist mono, Pastel playful, Luxury dark, Flat pop with photos, Grainy gradient. Also 19 opener concepts and 6 explainer styles. Supports 9:16. | Names and signature-motion pairs for most directions |
| 8 | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 10.8k | Apache-2.0 | 2026-10-05 | `template/THEMES.md` and `src/themes/palettes.json` define **7 semantic colour roles** (background, card surface, text, secondary text, accent, subtle fill, border) across 9 presets (Ink Press, Modern Light, Midnight, Sage, Coral, Iris, Deep Ocean, Obsidian Violet, Vintage Kraft). Props resolve in the order schema → preset → project palette → per-clip edit. Ships 152 shot recipe cards and 209 Remotion motion previews driven by a normalized `t`, plus JianYing (CapCut CN) draft export. Built on Remotion. | Colour-role schema. Precedence rules |
| 9 | [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | 3.0k | MIT | 2026-10-08 | `data/videos.json` holds 513 Opus 5.5 video prompts (317 motion, 67 explainer). Common conventions: "one HTML file, one `draw(t)`, no timers, no state between frames", "120 BPM grid, something on every beat", "closed-form springs, tiny overshoot", "three colours + site fonts, one idea per shot", "content enters after its container starts morphing". Mentions: remotion 89, hyperframes 38, beat 36, swiss 0, Chinese 1. | Prompt phrasing for the skill |
| 10 | [gl-transitions/gl-transitions](https://github.com/gl-transitions/gl-transitions) | 2.1k | MIT (LICENSE file) | 2026-06-22 | **125 GLSL transitions** following one spec (`progress`, `ratio`, `getFromColor/getToColor`, params with `// = default`). Relevant ones: `GlitchDisplace, StripDatamoshGlitch, DoomScreenTransition, FilmBurn, CrossZoom, directionalwarp, Directional, windowslice, GridFlip, pixelize, luma, static_wipe, tangentMotionBlur, LinearBlur, Overexposure`. | Glitch/terminal and documentary transitions |
| 11 | [scriptituk/xfade-easing](https://github.com/scriptituk/xfade-easing) | 124 | MIT | 2026-09-09 | Ports standard and CSS `cubic-bezier` easings plus GLSL transitions to ffmpeg `xfade`. Useful for joining HyperFrames sub-renders in post with eased transitions. | Post-assembly fallback |
| 12 | [greensock/GSAP](https://github.com/greensock/GSAP) | 28.9k | GSAP "standard no-charge" license (not OSI) | 2026-04-13 | The README states GSAP is now 100% free, **including SplitText, MorphSVG and all bonus plugins**. SplitText (chars/words/lines and masks) and ScrambleText are the standard toolkit for text effects. | Text engine for every preset |
| 13 | [shshaw/Splitting](https://github.com/shshaw/Splitting) | 1.8k | MIT | 2024-06-19 | Splits text into chars and words as `<span>`s with CSS variables (`--char-index`, `--word-index`), so you can do CSS-only staggers like `animation-delay: calc(var(--char-index)*30ms)`. | Lightweight fallback for text splitting |
| 14 | [Remocn/remocn](https://github.com/Remocn/remocn) | 1.6k | MIT | 2026-10-08 | A shadcn-style registry for Remotion (`npx shadcn add @remocn/blur-reveal`) of transitions, kinetic titles and backgrounds. Its components are deterministic: no `Math.random`, and they use `spring()`/`interpolate()`. They are React, so porting is needed, but they make a good catalogue of effect names. *(The component list was not enumerated because the request timed out.)* | Effect naming. Porting candidates |
| 15 | [style-dictionary/style-dictionary](https://github.com/style-dictionary/style-dictionary) (4.9k, Apache-2.0, 2026-10-03) and [design-tokens/community-group](https://github.com/design-tokens/community-group) (2.1k, W3C DTCG format, 2026-09-08) | — | — | — | The DTCG token format (`$value`, `$type`: color, fontFamily, duration, cubicBezier, …). Style Dictionary compiles tokens to CSS variables and JS. Both repo READMEs were confirmed. The DTCG field names come from prior knowledge of the spec. | Token layer of the preset file |

**Worth knowing but not reusable as code** (restrictive licenses; take ideas only):
- [feitangyuan/onetake](https://github.com/feitangyuan/onetake): 1.9k stars, **PolyForm Noncommercial**. Continuous single-take films where "something on screen survives every boundary". It measures continuity with a "carry score" (it rejects 0.00–0.40 and accepts 0.75+), uses real 180° shutter motion blur, and has about 38 measured moves.
- [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft): 1.4k stars, **PolyForm NC**. Narration-locked motion with 78 recipe cards. A 2026-09 note says they *reduced* motion to one very slow camera push per scene, with idle and breathing loops off by default. [anything2explainer](https://github.com/Vincentwei1021/anything2explainer): 2.3k stars, noncommercial "Required Notice" license. Black canvas, white line art, purple accent, ultra-bold headlines, top capsule HUD, bottom chapter progress bar, 44 px subtitles. Chinese voiceover at about 5.5 chars/s.
- [op7418/guizang-product-video-skill](https://github.com/op7418/guizang-product-video-skill): 720 stars, **AGPL-3.0**. A Chinese product-promo skill. It **assigns separate fonts to English titles (for rhythm) and Chinese explanation (for clarity)**, offers `repo/default/hybrid` style modes and uses a warm-white/charcoal default.
- [kurbaitaev/ghost-editor](https://github.com/kurbaitaev/ghost-editor): 66 stars, MIT. Seven talking-head styles (`clean, editorial, meme, cinematic, launch, kinetic, pop`) plus named recipes (Clean OS, RESULT, POV montage). It also offers "show it a reel → save the look as your style".
- [feicaiclub/video-spec-builder](https://github.com/feicaiclub/video-spec-builder): 1.0k stars, MIT, Chinese. It refuses vague words like "premium" or "high-impact" until the brief describes concrete shots, then writes a per-second `video-spec.md` for HyperFrames.
- [ARTHONG1/Opus-promo-Director](https://github.com/ARTHONG1/Opus-promo-Director): MIT, Remotion. Look-first style frames, every cut on beat-unit frames, and an honest strong/weak style table.
- [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo): 1.9k stars, no license. An Opus 5.5 music video in which Opus wrote `ANIMATION_GUIDE.md` to brief parallel subagents.
- [moritzkremb/framejam](https://github.com/moritzkremb/framejam): 22 stars, MIT. Has 30 styles, each a recipe of "palette, fonts, easing, transitions, text animations, pacing + template". The styles are streamed from framejam.ai and are not in the repo *(unverified)*.
- Others confirmed but less relevant: `iart-ai/motion-skills` (742 stars, MIT, an index of 17 skill packs including `kinetic-typography-skills`), `nexu-io/html-video` (Apache-2.0), `latent-spaces/brag` (MIT), `notivn/AIEV` (MIT, 14 colour-grade presets plus brand kits), `juliangarnier/anime` (73k stars, MIT, `stagger(…, {from:'center'})`), `motion-canvas/motion-canvas` (MIT), `midrender/revideo` (MIT), `theatre-js/theatre` (Apache-2.0), `bradley/Blotter` (3k stars, **no LICENSE file found**), `animate-css/animate.css` (**Hippocratic License 2.1**, not permissive), `lxgw/LxgwWenKai` (26k stars, **OFL-1.1**, Chinese font), `adobe-fonts/source-han-sans` (17k stars; OFL by common knowledge, API says NOASSERTION).

---

## (b) Recommended style directions (8)

Each direction assumes 1080×1920 at 30 fps and GSAP on a single paused timeline. "Beat" means the BGM beat; at 120 BPM, one beat is 0.5 s. CN fonts are suggestions (OFL where marked).

### 1. 终端黑客 / Terminal Mono
- **Borrows from:** bang-motion "Brutalist mono"; lemo-opuscar `ascii-crt`; kinetic-reel `glitchIn`; gl-transitions `GlitchDisplace`/`StripDatamoshGlitch`; HyperFrames `glitch`/`chromatic-split`.
- **Look:** a #0B0D0C ground and one phosphor accent (#7CFF6B or amber #FFB000). Type is JetBrains Mono / IBM Plex Mono with 思源黑体 Heavy for CN. Scanlines at ≤4% opacity.
- **Text:** a typewriter reveal using `steps(n)` at about 28 ms per char; a block cursor blinking every 530 ms; ScrambleText decode on keywords (0.6–0.9 s, chars `01#_/`); and a hard-cut entrance with a 2-frame RGB split of ±6 px.
- **Graphics:** blocks shift on the grid with `power4.out` in 0.25 s; progress bars drawn in `steps()`; "redacted" bars instead of fake text (kinetic-reel `redacted`).
- **Transitions:** hard cuts. On section breaks only, a 3–4-frame slice glitch. Never a dissolve.
- **Sound:** key ticks for each char, square-wave "crumbs" on glitches, a sub drop on the reveal, digital silence before the punchline.

### 2. 瑞士网格 / Swiss Grid
- **Borrows from:** lemo-opuscar `swiss-motion`, nearly verbatim in its grammar.
- **Look:** paper #EAE9E5, ink #111111, and one signal colour (#E30613, #FF5A00 or #1F3FFF), never a second. Use a 6-column grid with 72 px margins and 24 px gutters at 1080 wide. Type is one neo-grotesque (Inter/Archivo, −2% tracking at ≥90 px) with 思源黑体 for CN. Flush left, plus giant numerals beside tiny notes.
- **Motion:** **only two curves**: `cubic-bezier(.7,0,.2,1)` for snaps and `linear` for lines and playheads. No overshoot, spring or bounce. Durations are note values, and a snap starts one note early and lands on the beat.
- **Text:** words clip-reveal up from below the baseline and exit upward. Deletion is a "knife cut": a line crosses the word, then it collapses to its midline.
- **Transitions:** wipes, knife cuts, a hard pan by one column, re-flow. Never dissolves.
- **Sound:** dry print foley (letterpress clack, guillotine snick, paper slap) over a motorik or marimba pulse. Hard stop on the downbeat.

### 3. 暗场发布会 / Dark Keynote
- **Borrows from:** lemo-opuscar `dark-keynote`; bang-motion "Cinematic dark"; motion-video-kit rule 1 (foreground becomes the transition).
- **Look:** a near-black stage with a radial lift, a hairline grid (white 3%, every 4th line 6%, 48 px module), three dark surface steps with 1 px borders at 8% white, and **one accent** (lime #B7F34A or violet #8B7CFF). Type is Inter / Inter Tight 600 for big numbers (−4.5%) and JetBrains Mono for labels. CN: 思源黑体 Medium/Heavy.
- **Motion:** a fast-out ease with one small overshoot (`back.out(1.3)`) that settles immediately. Spawns take 0.2–0.3 s, and each element type gets one motion. Nothing fades out; elements retract or do a CRT-off squash.
- **Text:** one line per screen. The big number gets its own screen, and its digits scramble then lock one per 1/16 note. Captions are a UI toast (a pill, rising ~0.16 s).
- **Graphics:** a light-sweep reveal (soft front, glint ≤20%, ≤1.3 s) and a snap-grid "everything flies into place in one beat".
- **Transitions:** UI expand/collapse, plus HyperFrames `cinematic-zoom` or `sdf-iris`. When an expansion lands on a beat, start it one frame early.
- **Sound:** tuned mallets (marimba, vibes, glockenspiel). The product's sounds are one in-key family. Digital zero before the reveal. Mix at −14 LUFS.

### 4. 海报撞色 / Poster Kinetic
- **Borrows from:** bang-motion "Poster color-block"; kinetic-reel palette, `dropWord`, slams and `tape`.
- **Look:** rotate the full-bleed ground on every cut (ink → lime → ink → cream → blue) so each cut is visible. Huge cropped condensed type, with outlined echo copies stacked above and below a one-word slam. CN: 得意黑 Smiley Sans *(unverified repo)* or 思源黑体 Heavy, with a lime-coloured key character.
- **Text:** letters drop in with `expo.out` 0.5–0.7 s and a 0.03–0.05 s stagger per char. Recolour one char (`fillAt`). Numbers roll with expo `count()` or flip with `odometer()`.
- **Graphics:** diagonal scrolling tapes with ✳/↗ separators, starbursts, asterisks.
- **Transitions:** `trSlats / trPush / trZoom-through-element / trGrid` at 0.45–0.6 s, **never three of one kind in a row**.
- **Sound:** a beat-locked groove with the music ducked by the kick. `impact` about 5 times per piece and `softImpact` elsewhere. **No noise whooshes**. Use a reversed-pad swell into chapter cuts, and about half the cuts get no sound at all.

### 5. 报刊纸感 / Editorial Paper (Vox-like)
- **Borrows from:** Cele-san/vox-style-animation (all numbers below); lemo-opuscar `halftone-dossier`; bang-motion "Paper & print".
- **Look:** cream paper, halftone dots, heavy ink type, **one yellow highlighter**, hand-drawn annotations. CN: 思源宋体 Heavy for display, 思源黑体 for body, and 霞鹜文楷 (OFL) for handwritten notes.
- **Motion:** paper slap-in from `scale 1.18, rot −1.2°, blur 14px` to rest over 0.55 s with `power3.out`. Cards settle about 0.6° crooked. `back.out` max 1.15.
- **Text:** entrance 0.55–0.75 s `expo.out`, y 36–50 → 0. The highlighter swipe is `scaleX 0→1` from the left, 0.45 s `power2.out`, on one word per scene. A red strike-through carries all negation.
- **Graphics:** a dot field panning at a 12 fps `steps()` stutter (only there). Pen strokes are dash-offset draws with `steps(6–7)`.
- **Transitions:** a sheet-wipe as the **only** transition: 0.4 s `power3.in`, starting at slot −0.2 s.
- **Sound:** paper slap, marker squeak, pen scratch, a light typewriter, an upright-bass or piano bed.

### 6. 全息数据 / HUD Data
- **Borrows from:** lemo-opuscar `hologram-hud` / `dataviz`; kinetic-reel `hud()` corners, segmented progress bar and `odometer`; anything2explainer's black canvas, capsule HUD and chapter progress bar.
- **Look:** a black or deep-navy ground with a thin cyan/purple line art, corner brackets, micro-type in the four corners and a segmented chapter bar at the bottom. Mono labels with 4–8 px tracking; CN labels in 思源黑体 at 20–34 px with 4–14 px spacing (kinetic-reel).
- **Motion:** counters use `expo.out` rolls. Scan lines and target-box locks are `linear`, with a 2-frame overshoot on the lock.
- **Text:** chips wipe in and labels type on.
- **Graphics:** target boxes that lock onto parts, spec values rolling into place, and threads drawn to their citations.
- **Transitions:** `trIris` from a lit node (HyperFrames `sdf-iris`) and a `trWipe` that follows an existing scan line.
- **Sound:** in-key sine blips on chips, an "odo" tick burst under counters, a bell bloom on the iris, a low buzz on errors.

### 7. 一镜到底 / Continuous Morph
- **Borrows from (ideas only):** onetake (NC), plus motion-video-kit rules 1–2, plus the awesome-opus5-5 "one shape, never cut" prompt.
- **Look:** neutral light or dark. **One persistent actor** (a pill, card or cursor) changes size, radius and colour while its content swaps.
- **Motion:** closed-form springs with a tiny overshoot. If the target changes, sum one spring per change. Content enters after its container starts morphing and leaves before the next morph. Use a short blur only on fast moves.
- **Camera:** pushes through an element into the next "scene" and holds dead still between moves. Rests are what make the moves land.
- **Transitions:** none. Every boundary carries something. As a QA idea, count how many elements survive each boundary.
- **Sound:** foley placed from events in one shared reverb, with music ducked under hits.

### 8. 暖调口播 / Warm Talking-Head
- **Borrows from:** video-ads-machine-2 (validated 9:16 numbers); ghost-editor `editorial`/`clean`; guizang's EN/CN font split.
- **Look:** a warm soft-light radial grade plus a vignette. Captions use 思源黑体 Bold at about 60 px, with keywords in a contrasting face (霞鹜文楷 or 思源宋体 Italic-like, about 66 px), anchored around bottom 330 px. Letterings sit at the chest and keep the face clear.
- **Motion:** the hook stagger is eyebrow at 0.2 s, line at 0.42 s, accent at 0.64 s, then a 1.04 scale push over 1.7 s. B-roll cards scale 0.985 → 1 over 0.4 s and fade out over 0.24 s.
- **Transitions:** a 9×16 grid-wipe (cells scale 0 → 1 with stagger 0.28 from the start, then 1 → 0 from the end), or a hard cut.
- **Sound:** soft clicks on caption keywords, a light riser into the hook, the BGM ducked about 10 dB under the voice.

---

## (c) Proposed preset file schema (YAML)

This merges lemo-opuscar's STYLE.md sections, video-ads-machine-2's dimensions and validation status, shotcraft's semantic colour roles and precedence, kinetic-reel's transition map and sound rules, and DTCG-style typed tokens.

```yaml
# presets/<id>/preset.yaml
id: swiss-grid                 # kebab-case
name: { zh: 瑞士网格, en: Swiss Grid }
version: 1
status: validated              # validated | unvalidated (only rendered+audited presets are 'validated')
essence: "Grid-locked flat type, one signal colour, every move lands on a beat."
not: ["no gradients/glow", "no bounce/spring", "no dissolves"]   # anti-patterns (lemo 'what it is not')
references: [lemo-opuscar/styles/swiss-motion]                  # provenance

canvas: { width: 1080, height: 1920, fps: 30,
          safe: { top: 220, bottom: 420, side: 72 } }            # Douyin/Shorts UI zones — tune empirically
grid:   { columns: 6, margin: 72, gutter: 24, baseline: 24 }

tokens:                        # DTCG-style: {$type, $value}; compiled to CSS vars --c-*, --f-*, --e-*, --d-*
  color:                       # semantic roles (shotcraft) + accent discipline
    bg:        { $type: color, $value: "#EAE9E5" }
    surface:   { $type: color, $value: "#FFFFFF" }
    text:      { $type: color, $value: "#111111" }
    textMuted: { $type: color, $value: "#6B6B6B" }
    accent:    { $type: color, $value: "#E30613", rule: "exactly one element per shot" }
    danger:    { $type: color, $value: "#E8412F", rule: "only for failures/negation" }
    subtle:    { $type: color, $value: "#D9D7D1" }
    grounds:   ["bg", "text", "accent"]       # optional ground rotation per cut (kinetic-reel)
  font:
    display:   { $type: fontFamily, $value: ["Archivo", "Source Han Sans SC"], weight: 800, tracking: -0.02 }
    body:      { $type: fontFamily, $value: ["Inter", "Source Han Sans SC"], weight: 500 }
    mono:      { $type: fontFamily, $value: ["JetBrains Mono"], weight: 700, tracking: 0.08 }
    zhAccent:  { $type: fontFamily, $value: ["LXGW WenKai"] }              # optional handwritten/emphasis
    scale:     { caption: 56, label: 28, body: 44, h2: 96, h1: 160, hero: 320 }
  ease:
    snap:   { $type: cubicBezier, $value: [0.7, 0, 0.2, 1] }
    draw:   { $type: cubicBezier, $value: [0, 0, 1, 1] }   # linear
    enter:  { gsap: "expo.out" }
    exit:   { gsap: "power2.in" }
    overshootMax: 0            # e.g. 1.15 for paper, 1.3 for keynote, 0 for swiss
  duration:                    # seconds, or beats: "1/8" when bpm is set
    textIn: 0.55
    textOut: 0.3
    stagger: { char: 0.03, word: 0.08, line: 0.12 }
    transition: [0.45, 0.6]
    minHold: 1.8               # caption hold >= max(1.8, speech+0.6)
  texture: { grain: 0, scanlines: 0, halftone: false, vignette: 0 }

rhythm:
  bpm: 120
  snapToBeat: true             # moves start early and land on the beat
  shotLength: [1.4, 3.5]       # motion-video-kit pacing
  maxStill: 0.6

text:                          # named effects the skill may use; each maps to a GSAP recipe file
  entrances: [clip-rise, knife-cut-out]           # e.g. drop-letters, scramble-decode, typewriter, blur-in, highlighter
  emphasis:  { device: accent-color, perShot: 1 } # highlighter | accent-color | outline-echo | strike
  captions:  { style: layout-label, position: "column-start", wordReveal: clip, keywordFont: display }
  numbers:   { device: step-climb }               # odometer | expo-roll | glyph-scramble-lock

graphics:
  allowed: [bars, rules, giant-numeral, grid-lines]
  forbidden: [particles, glow, drop-shadow]
  signatureMoves: [knife-cut, re-flow, one-exception]

camera:
  moves: [locked-spread, hard-pan-column, push-into-module, rotate-90-stop]
  ease: snap

transitions:                   # kinetic-reel TR map style; variety rule enforced by linter
  default: wipe
  pool:
    - { id: wipe,        dur: 0.5, ease: snap }
    - { id: knife-cut,   dur: 0.3, ease: snap }
    - { id: hard-cut,    dur: 0 }
    - { id: hf:cinematic-zoom, dur: 0.6 }          # hf:* = @hyperframes/shader-transitions; gl:* = gl-transitions
  rules: { maxSameInRow: 2, never: [dissolve] }

sound:
  bed: { genre: "motorik / marimba pulse", lufs: -14, duckUnderVoiceDb: 10 }
  foley: { family: print, items: [letterpress-clack, guillotine-snick, paper-slap], reverb: dry }
  transitionSfx: { policy: "~50% of cuts silent", forbidden: [noise-whoosh] }
  impacts: { max: 5 }
  silence: { beforeReveal: true }

qa:                            # checks the skill runs on contact sheets
  - "accent appears on exactly one element per shot"
  - "no element enters by pure opacity fade"
  - "no transition id repeats 3x in a row"
  - "frame 0 is a finished composition"
```

**Design notes for the skill:**
1. Keep presets small and opinionated. Every source that worked limits itself to 1 accent, 1–2 curves and 1 transition family per piece, and the restriction itself is what makes a style recognisable.
2. Pair each preset's YAML with a `recipes/*.js` file of GSAP snippets (vox-style-animation shows this works in HyperFrames).
3. Ship one rendered `demo/` per preset, and mark a preset `validated` only after a frame-by-frame audit (video-ads-machine-2).
4. Add a "capture a new style" procedure (Cele-san's 7 steps) so users can mint their own presets.
