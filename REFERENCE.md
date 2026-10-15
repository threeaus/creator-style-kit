# Creator Style Kit — reference

## Files

```
styles/<id>/style.yaml   tokens: fonts, colors, type, motion (modes), texture, sound, not-rules, order, lookbook.{textures, idx}
styles/<id>/skin.css     component layout/looks, scoped .csk[data-csk="<id>"]; appended to csk/<id>.css at build
runtime/kit.js           motion runtime (CSK.create) — one call renders differently per style
runtime/kit.css          shared components, emphasis/number/list helpers, transition parts, textures
sfx/<id>/                per-style cue WAVs + kit.json {roles: {title, list, transition, hit, reveal, outro, tick?, highlight?}}
fonts/src/               source fonts (all free for commercial use; see each style.yaml for licence). MiSans + 优设标题黑 are not redistributable: scripts/fetch_fonts.py downloads them
scripts/list_styles.py   catalog / per-style brief          scripts/scaffold.py   beats → composition
scripts/compose.py       pacing + sound planner (shared)    scripts/sound_pass.py mix + QA after render
scripts/build_style.py   compile a style into <project>/csk  scripts/lookbook.py   preview of every style
vendor/sound-layer/      opus-sound-layer @ e9bdf5c (MIT, unmodified; see VENDOR.md)
scripts/build_sfx.py     rebuild SFX kits from CC0 sources (/Volumes/ORICO/Opus/opus55-tutorial/.work/research/sfx)
STYLES.md                human-facing catalog (Chinese)     references/research/  research notes behind the styles
```

`build_style.py <id> <project>` writes `<project>/csk/`: `<id>.css` (vars + @font-face + skin), `<id>.json` (runtime tokens), `fonts/*.woff2` subset to the glyphs in the project's .html files, `sfx/<id>/`, and `kit.css`, `kit.js`, `gsap.min.js`.

## beats.json (scaffold)

```json
{
  "name": "scores",
  "source": "Anthropic system card, 2026",
  "caption": "<b>Figure 1:</b> …",
  "beats": [
    {"type": "chapter", "num": "01", "title": "三模型横评", "sub": "Benchmark"},
    {"type": "list", "kick": "SWE 通过率", "head": "差距在 <em>工具调用</em>", "items": [["模型 A", 81], ["模型 B", 72]]},
    {"type": "stat", "value": 3.2, "suffix": "×", "max": 5, "unit": "速度", "note": "同一硬件 · <em>同一提示词</em>", "dur": 6.5}
  ]
}
```

- Item values (0–100) feed the `bar-chart` and `readout` lists. Other styles ignore them.
- `max` sets the bar/gauge scale. It defaults to 100 for values ≤ 100.
- Decimals work in every number mode.

- `suffix` (%, ×) is drawn on the figure itself, small and top-aligned — don't put it in `unit`.
- `dur` is a **minimum** (use the narration length). Beats are never shorter than the plan below.

## Pacing (compose.py) — why beats are as long as they are

Every time is derived from the style's own `motion.dur` / modes, so slow styles get longer beats instead of being cut off:

- **One thing moves at a time.** Chapter: number → title → rule → sub. List: kicker + headline → emphasis → items (gap = 60 % of an item's entrance, 0.4–0.75 s). Stat: figure counts and **locks**, then the unit and note follow (follow-through), then the emphasis.
- **Hold to read.** After the last entrance settles: max(minimum, reading time at 7 CJK chars/s − half the build time). Minimums: chapter 1.2 s, list 1.6 s, stat 1.4 s; the locked figure stays ≥ 2.2 s.
- **Anticipation by stillness.** A stat beat starts with 0.55 s of nothing after the cut, and no sound plays in the 0.6 s before the reveal.
- **One exit.** Covering transitions hide the text; only `light-sweep` / `glitch-slice` (open) run a text exit first.
- Long lines don't crawl: per-char stagger is capped so a line is in within `dur.in + 0.4 s`.

## Sound (compose.py → sound_pass.py)

- Cues sit on visual events: title appears, headline emphasis, first list item (one sound per list, not per item), **reveal on the figure's lock** (hero), every other cut.
- They are thinned by priority (reveal > transition > title > hit > list > highlight) to the style's `sound.rules`: ≥ 0.5 s apart, ≤ round(3 × maxPerSecond) in any 3 s, audible time ≤ (1 − silentShare) of the film.
- Each file's **peak** is aligned to its event (`data-start` = event − peak offset). Tags carry `data-peak/role/visual/weight` for the sound pass.
- After rendering: `python3 scripts/sound_pass.py <project> renders/x.mp4 [--voice vo.wav] [--music bed.wav]` → `out/final.mp4`, `audio/qa.png`, `LISTEN.md`. Fix FAILs by changing cues or sounds (≤ 2 rounds), never by editing vendor/ or loosening thresholds.
- Reveal cues are tagged `lock`, not `land`: qa.py's land probe reads the whole frame and is fooled by our ambient motion (grain, drift) and the unit/note follow-through. sound_pass.py checks them itself on the figure region (±3 frames, or on the impact frame for stamp-type modes). `number_lock()` in compose.py computes the lock from the count's ease; it was calibrated against renders. Known exception: `bauhaus-geometry` (geo-count) reports the figure stopping early — the landing circle dominates the region and the last 15 fps ticks are below the probe's threshold. Frames confirm the count runs to the sound; stepped counts (< 30 fps) lock on the exact final value.
- Known false alarm: qa.py `offset` can FAIL by one period on a tonal, periodic sound (a chime) because its 1 s cross-correlation has two near-equal peaks. Confirm with a whole-file cross-correlation (lag 0) before touching anything.

## Markup contract (custom scenes)

Index `<head>` loads `csk/gsap.min.js` and `csk/kit.js`. Each composition `<template>` links `csk/kit.css` and `csk/<id>.css`:

```html
<div id="root" class="csk" data-csk="<id>" data-l-chapter="center" data-l-list="head-top" data-l-stat="center" data-composition-id="<comp-id>" data-width="1080" data-height="1920">
  <div class="csk-bg"></div>
  <!-- style textures: copy lookbook.textures from style.yaml (fill {source} {caption} {tape} {lines}) -->
  <div class="csk-scene csk-s0"><div class="csk-chapter"><div class="num">01</div><div class="ttl t-display">标题</div><div class="rule"></div><div class="sub t-label">副标</div></div></div>
  <div class="csk-scene csk-s1"><div class="csk-head"><div class="kick t-label">Kicker</div><div class="ttl t-display">标题 <em>重点</em></div></div>
    <ol class="csk-list"><li data-v="81"><span class="idx">01</span><span class="txt">条目</span><i class="rule"></i></li></ol></div>
  <div class="csk-scene csk-s2"><div class="csk-stat"><div class="val" data-max="100">87.6</div><div class="unit">单位</div><div class="note t-note">注释 <em>重点</em></div></div></div>
</div>
```

Layout: copy the style's `layout:` from style.yaml onto the root as `data-l-chapter / data-l-list / data-l-stat` (compose.py does this). Archetypes live in kit.css:

| Slot | Archetypes |
|---|---|
| chapter | `left-mid` (default) · `center` · `top` · `low-left` · `split` (number at the top, title low) · `right-mid` |
| list | `head-top` (default) · `center` · `article` (higher, denser) · `low` |
| stat | `left` (default) · `center` · `low-left` · `top-left` |

Titles break between words only (glyphs of a word sit in a nowrap `.wd` box; runs > 8 chars may wrap) and balance their lines.

Type roles: `t-display`, `t-latin`, `t-body`, `t-label`, `t-note`. Colour vars: `--c-bg --c-surface --c-line --c-text --c-muted --c-accent` plus style extras (`--c-claret`, `--c-cyan`, `--c-seal`…).

**Root selector:** on mount, HyperFrames strips the inner root's `id` and `data-composition-id`. Select the root from the host instead: `'[data-composition-id="<comp-id>"] .csk[data-csk]'`. A bare `#id` returns null.

## Runtime API

```js
const kit = CSK.create({ tl, root: R, style: STYLE_JSON /* csk/<id>.json, add seed */ });
kit.ambient(0, total);              // camera drift/push, particles, blobs, tape, caret, grid pan
kit.transition(0, "in");            // reveal half only at start; (t, "out") cover only at end
const c = kit.transition(t);        // full transition; returns the time the frame is covered → swap scenes there
kit.textIn(sel, t[, mode]);  kit.textOut(sel, t);
kit.emphasis(sel, t[, mode]);  kit.number(sel, t, value[, mode]);  kit.list(sel, [t1, t2, …][, mode]);
kit.punch(t);                       // 4-frame zoom hit (poster)
```

Everything is `tl.set`/`tl.to` with a seeded PRNG: seek-safe and deterministic, with no callbacks. Pass a `mode` only to borrow another style's move deliberately.

| Slot | Modes |
|---|---|
| textIn | blur-rise, clip-rise, paper-slap, spring-pop, drop-letters, type-scramble, write, draft-in, scan-in, converge, ink-bleed, segment-on, fade-up, slide-block |
| textOut (`motion.textOut`) | cut, fade, sink, lift, disperse (default derives from textIn) |
| emphasis | accent-glint, knife-underline, highlighter, selection, scribble, recolor-char, circumscribe, boxed, dimension, bracket-lock, halo, seal-stamp, gradient-sweep, underline-soft, shape-mark, led-tag |
| number | scramble-lock, step-climb, stamp, bubble-count, odometer, decimal-tracker, soft-count, bar-grow, gauge, particle-form, segment, ink-count, geo-count |
| list | rise-dim, index-snap, index-cards, sticker-cards, slam-alternate, terminal-lines, bar-chart, fade-rows, grow-in, leader-lines, readout, converge-rows, glass-cards, iso-stack, geo-blocks, key-press, ink-rows |
| transition | light-sweep, column-wipe, sheet-wipe, card-zoom, ground-slats, glitch-slice, dip, edge-wipe, draft-wipe, particle-warp, frost, iso-slide, shape-iris, ink-spread, shutter |

## Gotchas

- **Hide a finished scene when the next one starts** (`tl.set(prev, {opacity: 0}, cover)`). Slow entrances can otherwise finish after their exit tween and reappear.
- Custom scenes: keep compose.py's settle tables (`text_settle`, `number_settle`, `item_settle`) in step with kit.js when you add or change a mode — they are how beat lengths are computed.
- Keep information text ≥ 26 px (labels, source lines) and out of the bottom 400 px and the right-hand 120 px from y 900–1500 (platform captions and buttons).
- `particle-form` hides the typeset number and draws 5×7 dots. It supports digits, `.` and `%` only.
- `poster-kinetic` changes ground colour on every cut. Use `grounds`, `groundText` and `groundAccent` together, or emphasis can match the background.
- `ink-wash` titles stay horizontal; vertical text works only for pure-Chinese titles (`style="writing-mode:vertical-rl"` on `.ttl`).
- `isometric-stack` lists look best with 3–4 items and short labels (≤ 8 characters).
- `hyperframes check` reports `content_overlap` between a big number and its unit line. It is a bounding-box artefact and is not visible in renders. Confirm with a snapshot.

## Adding a style

1. Copy a close `styles/<id>/` and set `id`, `order` (next number), `name`, `essence`, `not`, `best_for`, fonts, colors, type, motion modes, `layout` (pick archetypes that fit the style's character — don't default everything to left), texture, `lookbook.textures`/`idx`, and `sound.kit` (refs: `uisfx:<pack>/<cue>`, `kenney-if:`, `kenney-imp:`, `kenney-rpg:`, `synth:`).
2. Put new fonts in `fonts/src/`. For variable fonts, instance a static weight first with `python3 -m fontTools.varLib.instancer`.
3. Write `skin.css` scoped to `.csk[data-csk="<id>"]`. If a move is missing, add it to `runtime/kit.js` and `kit.css`, seek-safe.
4. Build the sound kit: `python3 scripts/build_sfx.py /Volumes/ORICO/Opus/opus55-tutorial/.work/research/sfx <id>`.
5. Preview it: `python3 scripts/lookbook.py <dir> --only <id>`, then snapshot. Add a row to STYLES.md.
