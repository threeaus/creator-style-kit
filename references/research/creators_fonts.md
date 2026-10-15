# Creator visual language + free Chinese fonts: research for 9:16 tech/knowledge video presets

Researched 2026-10-08. Network from this machine was flaky: GitHub API and jsDelivr timed out intermittently, so every URL below was retried until it gave a definite answer.

**Evidence labels used throughout**
- **[V]** verified this session, either from a cited source or by downloading the file and reading its name table with fontTools.
- **[S]** secondary source: a blog, a fan analysis or a community style pack. Plausible, but not from the creator.
- **[I]** inferred from general familiarity with the channel's output. Not checked against footage in this session. Treat as a hypothesis and confirm by watching 2–3 recent videos.

Hex codes are never presented as a creator's official values. Each one is marked as fan-derived **[S]** or as my own design proposal **[P]**.

---

## Part A: Creator style analysis

### A1. Creator style table

| Creator | Typefaces | Color | Text motion / graphics | Transitions | Sound | Pacing |
|---|---|---|---|---|---|---|
| **影视飓风 MediaStorm** | Bold Chinese grotesque titles with small English labels **[I]**. They made a survey video of creator subtitle practice: 14 of 54 creators used 思源黑体 **[V]**. White, low-stroke subtitles with a soft shadow **[I]**. | Every clip is individually graded **[V]**. Cinematic contrast, deep blacks, one accent **[I]**. | A dedicated animator builds custom AE scripts and plugins **[V]**. Text is motion-tracked to footage (they publish 字幕追踪 tutorials **[V]**). Thin-line spec callouts and big type layered with footage **[I]**. | Camera-move transitions (whip, push), speed ramps, match cuts **[I]**. | Whoosh + hit on transitions, risers into reveals, beat-synced cuts **[I]**. | Fast but structured, dense with breathing room; Bilibili cuts slightly slower than Douyin **[S]** (fan SKILL.md). |
| **亿点点不一样** (MediaStorm sub-channel) | Minimal on-screen text **[I]** | Footage-led, natural grade **[I]** | Shoots on high-speed, macro and probe lenses **[V]**. Graphics limited to labels and callouts **[I]**. | Slow-motion holds, ramp in and out **[I]** | Heavily sweetened foley (impacts, whooshes) over slow motion **[I]** | Spectacle beats with long holds **[I]** |
| **何同学** | Subtitles and effects mostly in 苹方 (PingFang), occasionally SF; thumbnails in 阿里巴巴普惠体 **[V]** (ifeng). Free substitutes: HarmonyOS Sans SC, MiSans, 普惠体 3.0. | Neutral, bright, clean desk; product colors carry the frame **[I]** | Minimal graphics. Text fades or slides softly. The memorable effects are practical or hand-made (e.g. the 36万行备忘录 animation) **[V/I]**. | Rich camera moves and seamless transitions, every shot planned against a word-for-word script **[V]** | "Comfortable, natural music" **[V]**: light piano or ambient. Uses silence and room tone **[I]**. | Calm and emotional. 2 weeks to 6 months per video **[V]**. |
| **极客湾 Geekerwan** | Went from 苹方, to SF Compact/SF Pro, to **Manrope + MiSans** recently. Uses HarmonyOS Sans for Huawei topics and MiSans for Xiaomi topics. **Bahnschrift** for chart numerals **[V]** (ifeng). | Dark chart backgrounds; one hue per chip or brand **[I]** | Data-first. Performance-vs-power efficiency curves (focus moved from peak performance to efficiency in 2022 **[V]**). Leaderboard (天梯图) bar charts **[V]**. Numeric counters **[I]**. | Mostly hard cuts and chart builds **[I]** | Synth bed, few SFX **[I]** | Dense, information-first **[I]** |
| **小Lin说** | Bold keyword captions with a color highlight **[I]** | Plain light-gray or beige wall, later a branded "Lin" set **[V]** | Talking head in a stable medium close-up, camera at or slightly above eye level **[V]**. Inserts animation for dry concepts **[V]**. Pop-in flat doodles and meme stickers **[I]**. | Clean, sharp cuts and inserts **[S]** | "Well-timed SFX" **[S]**: pops and dings on sticker entrances **[I]** | Brisk. Expressive delivery; editors note a 3-second segment can take 30 minutes to edit **[S]**. |
| **回形针 PaperClip** | Cover Chinese in **方正俊黑** (commercial font; use a free substitute), white text with a dark-gray drop shadow **[S]** (jianshu cover breakdown via search) | Covers use one bright key color plus transparency-derived secondaries, white border, color mask **[S]** | 3D animation and information/technical visualization storyboards. Real news, papers and documents shown with a textured treatment **[V]**. Isometric 3D, HUD-like leader-line labels, monospaced data **[I]**. | Motion rhythm comes from the motion designer **[V]**. Grid slides and hard cuts **[I]**. | Electronic, minimal; UI ticks **[I]** | Very high information density, 3–4 weeks per episode **[V]** |
| **半佛仙人** | Large plain subtitles **[I]** | Plain background; the stickers carry the color **[I]** | 100+ odd memes per video, rarely repeated **[V]** | Hard cuts **[V/I]** | Cartoon SFX, almost no silence **[I]** | Very fast, built on jokes **[V]** |
| **差评** | n/a | n/a | Moved from "reading the article aloud" to motion graphics, 3D models by an in-house modeler, and live action **[V]** | n/a | n/a | 7–15 min, humorous, hard-core science **[V]** |
| **MKBHD** | Clean neo-grotesque in white, small relative to the frame **[S]** | Matte black, deep grays, one accent (signature red or a color taken from the product) **[S]** | Product shot like advertising photography: shallow depth of field, controlled reflections **[S]**. No burned-in captions **[S]**. Robot-arm (MRMC) product moves **[I]**. | Cuts alternate between talking head (~48%) and b-roll (~43%) **[S]** | Restrained music, very few SFX **[I]** | Conversational. One 32–55 s static "verdict" hold at 72–92% of runtime **[S]** (writepanda measurement; the source page failed to load, figures come from the search snippet). |
| **Apple keynote / product films** | SF Pro, optical sizes: SF Text below 20 pt, SF Display above **[S]** | Pure black or white grounds **[S]**. Recent keynotes do use gradient text for hero words, so treat "no gradients" as only mostly true **[I]**. | Very large type, tight tracking, blur/opacity fade-ins, slow product rotation **[I]** | Slow dissolves, push-ins, black frames between beats **[I]** | Music-led; SFX nearly absent **[I]** | Unhurried and confident **[I]** |
| **Vox** | Brand typefaces (website): Balto, Harriet, Alright Sans **[V]** (Fonts In Use). Video: bold condensed sans punches in on the spoken word **[S]**. | A community HyperFrames pack approximates it as paper `#f2ecdf`, ink `#161513`, highlighter `#ffd200`, red `#e5483f`, cobalt `#2f5fe8` **[S]** | Paper collage, halftone B/W cutouts, torn edges, thick arrows, yellow highlighter sweep over quotes, 2.5D parallax on archival photos **[S]**. 12 fps stutter on textures only, never on hero type **[S]**. | Camera travels across a grid of panels; sheet wipes **[S]** | Paper and archival texture sounds **[I]** | Driven by the narration: each visual answers the line just spoken **[S]** |
| **Kurzgesagt** | Rounded geometric sans **[I]** | Fan palettes: deep blue backgrounds `#141535` / `#1a1d43`, accents `#ff3fa7`, `#fad53c`, `#00d8fc`, `#51fbdc` **[S]** | Flat vector, rounded shapes, bold color fields, recurring birds. Illustrator for drawing, After Effects for animation **[V]**. Gradient shading, idle motion everywhere, glows **[I]**. | Zooms through objects and scale changes **[I]** | Rich ambient score and sound design (Epic Mountain) **[I]** | Calm and dense |
| **Johnny Harris** | Typewriter/serif labels on maps **[I]** | Warm paper, red markers **[I]** | Maps built in After Effects + GEOlayers 3. Textured overlays, film burns, light leaks, grain on most graphics **[S]**. | Match cuts on text that start slow and accelerate **[S]** | **Camera-click SFX at the start of each clip, timed to the cut** **[S]** | Momentum builds toward reveals **[S]** |
| **Wendover** | Clean sans **[I]** | Muted land colors, one accent color for routes **[I]** | Custom maps, infographics, animated diagrams **[V]** | Map pans and zooms **[I]** | Steady music bed, little SFX **[I]** | Driven by the voiceover **[V/I]** |

### A2. Patterns that separate premium work from generic AI output

All of these are drawn from the table above.

1. **One accent color with one job.** MKBHD's red and Vox's yellow-only-for-emphasis are the two clearest cases. Generic output spreads 4–5 saturated colors evenly.
2. **Brand-matched type.** 极客湾 switches fonts by subject (MiSans for Xiaomi, HarmonyOS Sans for Huawei) and keeps tabular numerals in charts. Generic output uses one default font everywhere.
3. **Each graphic answers the line being spoken** (Vox, 回形针). Decorative motion that isn't tied to the voiceover is the main "slop" tell.
4. **Restraint in sound.** Apple, MKBHD and 何同学 lean on music and silence. Johnny Harris uses exactly one signature cue: the camera click on the cut. Constant whooshes on every transition read as template work.
5. **Texture and physicality.** Paper, grain, halftone, light leaks and real documents (Vox, Johnny Harris, 回形针) keep frames from looking vector-clean and synthetic.
6. **Planned camera movement:** a word-for-word script with shots planned to match (何同学, MediaStorm).
7. **A deliberate pause:** MKBHD's static verdict hold. Uniform pacing feels machine-made.

---

## Part B: Recommended style directions (8 presets)

All palettes below are **[P]**, my own design proposals, unless marked [S]. Motion values are starting points for HyperFrames/GSAP at 30 fps. Font names refer to the table in Part C.

**9:16 safe zone [I]:** at 1080×1920, keep key text out of the top ~200 px and the bottom ~380 px, where the Douyin/Bilibili/视频号 UI overlays sit. Treat 1080×1300 in the center as the safe band.

### 1. Studio Noir (MKBHD × Apple × 何同学)
- **Type:** titles in MiSans Heavy or HarmonyOS Sans SC Black. Latin in Geist or Inter (tabular numerals for specs). Subtitles in MiSans Medium.
- **Palette:** bg `#0B0B0C`, surface `#161618`, text `#F5F5F7`, secondary `#8E8E93`, one accent `#FF3B30`, used once per scene at most.
- **Text motion:** blur 12px→0 + y 24→0 + opacity, 600 ms, `expo.out` (`cubic-bezier(.16,1,.3,1)`), lines staggered 70 ms. Exit at 0.6× the entry duration. Spec numbers count up with tabular-nums.
- **Graphics:** 1px hairlines at 20% white, oversized numerals (240–320 px), product cutouts with a soft floor reflection, no icons.
- **Transitions:** hard cuts on downbeats, 8-frame dissolves between sections, constant 2–3% push-in on stills.
- **SFX:** mostly silence and room tone. A soft sub "thump" (−18 LUFS-ish) on the hero reveal only. A music bed ducks under the voiceover.
- **Best for:** talking-head intros and outros, product or feature showcases, "verdict" moments.

### 2. Swiss Data Lab (回形针 × 极客湾)
- **Type:** titles in Noto Sans SC Black or 思源黑体 Heavy. Data in JetBrains Mono or IBM Plex Mono. Latin labels in Space Grotesk or Manrope (Manrope is what 极客湾 uses **[V]**).
- **Palette:** bg `#0E0F11`, grid `#23262B`, text `#E8E8E6`, muted `#7A7F87`, signal `#3DDC97`, warning `#FFB020`, compare `#5B8CFF`.
- **Text motion:** linear mask wipes left→right, 220 ms, `power2.out`. Mono labels type on at 40 chars/s. Numbers roll like a counter. Index tags ("01 /", "02 /") snap in.
- **Graphics:** 12-column grid at 64 px gutters, visible at 6% opacity. Leader-line callouts (1.5 px line + 6 px dot). Bar and line charts with direct labels instead of legends. Isometric diagrams.
- **Transitions:** grid-panel slides (whole layout shifts 1 column), shutter wipes, hard cuts.
- **SFX:** soft UI ticks on each data point (−24 dB), a low sine pulse on the key finding, no whooshes.
- **Best for:** benchmarks, mechanism explainers, "how it works" screen-share annotation.

### 3. Editorial Paper (Vox × Johnny Harris)
- **Type:** headlines in Noto Serif SC Black or 思源宋体 Heavy. Latin accents in Instrument Serif italic. Labels in IBM Plex Mono, typewriter feel.
- **Palette:** paper `#F2ECDF`, ink `#161513`, highlighter `#FFD200`, red `#E5483F`, cobalt `#2F5FE8`. These are [S], from the community Vox pack; one meaning per color.
- **Text motion:** paper slap-in. Scale 1.08→1, rotate ±2°, 220 ms, `back.out(1.6)`, hard offset shadow `10px 12px 0 rgba(22,21,19,.16)`. Highlighter wipe 450 ms, `power1.inOut`, behind one key phrase. Texture layers stutter at 12 fps; hero type stays at full frame rate.
- **Graphics:** halftone cutouts of screenshots and people, torn edges, hand-drawn circles and arrows (SVG stroke draw), map snippets, real documents.
- **Transitions:** sheet-wipe (a paper layer slides across), match cuts on text that start slow and accelerate.
- **SFX:** paper rustle on slap-ins, a **camera-shutter click on each cut** (the Johnny Harris signature [S]), marker squeak on highlights. Keep the music sparse.
- **Best for:** industry stories, AI-history narratives, "why X happened."

### 4. Warm Notebook (小Lin说 friendliness)
- **Type:** punch titles in 得意黑 Smiley Sans. Body and keywords in 霞鹜文楷 LXGW WenKai Medium. Subtitles in Noto Sans SC Bold.
- **Palette:** cream `#FFF8EC`, ink `#2B2A28`, tomato `#FF5A36`, sky `#3B82F6`, mint `#22C55E`, butter `#FFD166`.
- **Text motion:** spring pop. Scale 0.6→1.06→1 over 300 ms (`back.out(2)`), random tilt ±3°, 40 ms stagger per word. Keyword gets a scribble underline drawn in 350 ms.
- **Graphics:** rounded cards (radius 28, 2px ink stroke), flat doodle icons, sticker-style cutouts of the speaker with a white 8px outline.
- **Transitions:** zoom-through a card, whip pan with 6-frame motion blur.
- **SFX:** soft "pop" on stickers, a "ding" on key numbers, a pencil scratch on underlines. Use one SFX per beat at most.
- **Best for:** concept and finance-style explainers, beginner tutorials, approachable outros.

### 5. Cosmic Flat (Kurzgesagt)
- **Type:** titles in HarmonyOS Sans SC Black or OPPO Sans Heavy. Latin in Space Grotesk.
- **Palette:** night `#141535`, deep `#1A1D43` (both [S] fan-derived), accents `#FF3FA7`, `#FAD53C`, `#00D8FC`, `#51FBDC` ([S]). Limit each scene to 2 accents.
- **Text motion:** scale 0.92→1 + opacity, 500 ms, `sine.out`, with a 20px soft glow that fades out. Idle float ±3 px on a 3 s sine loop.
- **Graphics:** rounded vector shapes, two-tone gradient shading, star particles, a glow on "active" objects.
- **Transitions:** continuous zoom into an object that becomes the next scene.
- **SFX:** ambient pad bed, soft chimes on reveals, airy whooshes at low volume.
- **Best for:** AI or science concept explainers ("what is a model," "how attention works").

### 6. Cinematic Tech (影视飓风 × 亿点点不一样)
- **Type:** titles in 阿里巴巴普惠体 3.0 115 Black or MiSans Heavy. Labels in Geist Mono, uppercase, tracking +8%.
- **Palette:** black `#050505`, white `#FFFFFF`, steel `#9AA0A6`, electric accent `#2EE6FF`, or amber `#FFB000` for warm grades.
- **Text motion:** giant type placed behind the subject (needs a subject matte), tracked labels pinned to objects, 2-frame white flash on the hero word. Character cascade: y 100%→0 inside a mask, 30 ms per character, `expo.out`.
- **Graphics:** thin-line callouts with circle targets, spec labels, light leaks, anamorphic streaks at most once per video.
- **Transitions:** speed ramps, whip pan + directional blur, match cuts on motion.
- **SFX:** whoosh into hit on major transitions, short risers (1–2 s) into reveals, bass hit on the title. Save these for 3–4 moments per video.
- **Best for:** hype intros, product reveals, channel ident, outro sting.

### 7. Meme Rush (半佛仙人 × 差评 punch)
- **Type:** punch words in 优设标题黑, 庞门正道标题体, 抖音美好体 or 钉钉进步体. Subtitles in Noto Sans SC Black with a 6px dark stroke.
- **Palette:** white `#FFFFFF`, ink `#111111`, highlight `#FFE600`, red `#FF2D2D`.
- **Text motion:** snap-in within 3 frames, no easing. Scale punch 1.18→1 over 4 frames, 2-frame ±6px shake on impact words.
- **Graphics:** reaction stickers, screenshot cutouts with thick outlines, big arrows.
- **Transitions:** hard cuts, zoom punch (+12% over 4 frames), rare glitch.
- **SFX:** cartoon hits, record scratch, "叮". This is the only preset with dense SFX, and it still needs a cap (one per sentence).
- **Best for:** Douyin hooks (first 3 s), hot takes. **Do not** use it for whole long videos.

### 8. Developer Console (for screen-share and showcase segments)
- **Type:** code and UI in JetBrains Mono or Sarasa Mono SC (更纱, which handles CJK in monospace). Narration titles in HarmonyOS Sans SC Bold.
- **Palette:** bg `#0D1117`, panel `#161B22`, text `#E6EDF3`, green `#3FB950`, purple `#A371F7`, orange `#F0883E`. Inspired by GitHub's dark theme; not an official spec.
- **Text motion:** typewriter at 35–45 chars/s with a 530 ms caret blink. Line highlight sweeps 250 ms. A callout bubble springs from the cursor.
- **Graphics:** window chrome with 3 dots, the cursor drawn with a halo, zoom-to-region with a dimmed surround (60% black), keystroke chips (`⌘ K`).
- **Transitions:** camera zoom 1.0→1.6 toward the active region, 700 ms, `expo.inOut`; a pan follows the cursor.
- **SFX:** very soft key clicks under typing (−30 dB), a confirm chime on success. No whooshes.
- **Best for:** Claude/Opus tutorial screen recordings and terminal demos. It pairs as the screen-share companion to presets 1, 2 or 4.

**Suggested pairings:** Studio Noir + Developer Console for a premium tech tutorial, Warm Notebook + Developer Console for beginner-friendly content, Swiss Data Lab for benchmarks, Cinematic Tech for the intro sting only.

---

## Part C: Free-for-commercial Chinese fonts and Latin pairings

### C1. Method
- **"Status 200 ✓file":** the file was fully downloaded and its name table and glyph count were read with fontTools.
- **"200 (HEAD)":** only the HTTP status was checked.
- **"GF":** confirmed present via `fonts.googleapis.com/css2?family=…` returning 200.
- raw.githubusercontent was unreliable (one file came back truncated at 31 KB). **jsDelivr `/gh/` per-file URLs worked**, even for `wordshub/free-font`, whose whole package exceeds jsDelivr's 50 MB repo limit.
- `api.github.com` mostly timed out from curl; `gh api` worked with retries.

### C2. Chinese fonts

| Font | License | Commercial | Weights | Personality | GF? | Verified source URL (status) |
|---|---|---|---|---|---|---|
| **思源黑体 Noto Sans SC** | SIL OFL 1.1 | ✅ | Variable 100–900 | Neutral workhorse; safest subtitle font | **Yes** | GF: `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900` (200). Fontsource: `https://cdn.jsdelivr.net/npm/@fontsource-variable/noto-sans-sc@5/index.css` (200 ✓css) |
| **Source Han Sans SC** (original) | OFL 1.1 | ✅ | 7 (ExtraLight–Heavy) | Same design, full OTF set | (as Noto) | `https://github.com/adobe-fonts/source-han-sans/releases/download/2.005R/09_SourceHanSansSC.zip` (200, 95 MB) |
| **思源宋体 Noto Serif SC** | OFL 1.1 | ✅ | 200–900 | Editorial, literary headlines | **Yes** | GF `Noto+Serif+SC:wght@200..900` (200). Static TTF example: `https://fonts.gstatic.com/s/notoserifsc/v36/H4cyBXePl9DZ0Xe7gG9cyOj7uK2-n-D2rd4FY7SCqyWv.ttf` (200 ✓file). Fontsource `@fontsource/noto-serif-sc@5/index.css` (200 ✓) |
| **Source Han Serif SC** | OFL 1.1 | ✅ | 7 | as above | (as Noto) | `https://github.com/adobe-fonts/source-han-serif/releases/download/2.003R/09_SourceHanSerifSC.zip` (200) |
| **Source Han Mono** | OFL 1.1 | ✅ | 7 in one TTC | CJK monospace for code and terminals | No | `https://github.com/adobe-fonts/source-han-mono/releases/download/1.002/SourceHanMono.ttc` (200, magic `ttcf` ✓) |
| **Sarasa Gothic 更纱黑体** (bonus) | OFL 1.1 | ✅ | many, incl. Mono SC | Best CJK + Latin monospace pairing | No | `https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.42/Sarasa-TTC-1.0.42.zip` (200, 414 MB). Smaller per-family `SarasaFixedSC-TTF-1.0.42.7z` is also in that release. |
| **阿里巴巴普惠体 3.0** | Alibaba's own free license (free commercial for individuals and companies; no resale or modification; see alibabafonts.com) | ✅ | 10: 35 Thin, 45 Light, 55 Regular, 65 Medium, 75 SemiBold, 85 Bold, 95 ExtraBold, 105 Heavy, 115 Black (+55 L3) | Friendly-modern commercial grotesque. 何同学 uses 普惠体 on thumbnails **[V]**. | No | Official `https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3.zip`: **403 AccessDenied** (also with Referer). Unofficial mirror that works: `https://cdn.jsdelivr.net/npm/@fontpkg/alibaba-pu-hui-ti-3-0@3.1.2/AlibabaPuHuiTi-3-85-Bold.ttf` (200 ✓file, v3.01). Swap the filename for other weights. ⚠ The mirror README says it is "not a download page." Download once from alibabafonts.com and vendor it. ⚠ **105 Heavy and 115 Black contain only 9,728 glyphs** (vs 29,296 in Bold) [V]: test rare characters. |
| **HarmonyOS Sans SC** | HarmonyOS Sans Fonts License (free commercial; no modification or standalone resale) | ✅ | 6: Thin, Light, Regular, Medium, Bold, Black | Crisp, geometric, techy | No | Official `https://developer.huawei.com/images/download/general/HarmonyOS-Sans.zip` (200, 52 MB). npm mirror of the same zip: `https://cdn.jsdelivr.net/npm/harmonyos-sans@1.0.0/HarmonyOS%20Sans.zip` (200). Per-weight mirror: `https://cdn.jsdelivr.net/npm/@fontpkg/harmony-os-sans-sc@1.0.3/HarmonyOS_Sans_SC_Bold.ttf` (200 ✓file, 29,221 glyphs) |
| **MiSans** | MiSans 字体知识产权许可协议 (free commercial, revocable; no adaptation; credit "MiSans" when embedded in software) | ✅ | 10: Thin–Heavy, + VF | Clean, neutral-tech. 极客湾 uses it **[V]**. | No | Official `https://hyperos.mi.com/font-download/MiSans.zip` (200, 228 MB). Mirror `https://cdn.jsdelivr.net/npm/@fontpkg/mi-sans@4.3.0/MiSans-Bold.otf` (200 ✓file, v4.003). Sliced webfont `https://cdn.jsdelivr.net/npm/misans-webfont@4.3.1/misans/misans-heavy/result.min.css` (200 ✓css) |
| **OPPO Sans 4.0** | OPPO free commercial terms: **no adaptation, no resale, "不向他方提供其他下载渠道" (no redistribution channels)** | ✅ use, ❌ re-hosting | 4.0 zip contents not inspected (2.0 had L/R/M/B/H) | Soft, rounded-modern grotesque | No | Official `https://openfs.oppomobile.com/open/oop/202410/18/62d51f494591f1a9040d83b597745911.zip` (200, 16 MB). Fetch from the official URL only; don't mirror. |
| **得意黑 Smiley Sans** | OFL 1.1 | ✅ | 1 (Oblique) | Narrow, italic, energetic display. Good for punchy titles. | **No** (GF returns 400) | `https://github.com/atelier-anchor/smiley-sans/releases/download/v2.0.1/smiley-sans-v2.0.1.zip` (200). TTF: `https://cdn.jsdelivr.net/npm/@fontpkg/smiley-sans@2.0.4/SmileySans-Oblique.ttf` (200 ✓file, v2.0.1). Sliced: `https://cdn.jsdelivr.net/npm/@chinese-fonts/dyh@3.0.0/dist/SmileySans-Oblique/result.css` (200 ✓css) |
| **霞鹜文楷 LXGW WenKai** | OFL 1.1 | ✅ | Light, Regular, Medium (+ Mono, + Screen) | Warm, bookish, handwritten-kai. Friendly keywords and quotes. | **SC: No** (400). Only *LXGW WenKai TC* (Traditional forms) is on GF. | `https://github.com/lxgw/LxgwWenKai/releases/download/v1.522/LXGWWenKai-Medium.ttf` (200 ✓file, 46,867 glyphs). Regular/Light use the same pattern. Screen variant: `https://github.com/lxgw/LxgwWenKai-Screen/releases/download/v1.522/LXGWWenKaiScreen.ttf` (200). Webfont `https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css` (200 ✓) |
| **站酷快乐体 ZCOOL KuaiLe** | OFL 1.1 (on GF) | ✅ | 1 | Playful, round, childlike | **Yes** | `https://fonts.gstatic.com/s/zcoolkuaile/v22/tssqApdaRQokwFjFJjvM6h2Wpg.ttf` (200, 1.5 MB) |
| **站酷庆科黄油体 ZCOOL QingKe HuangYou** | OFL 1.1 | ✅ | 1 | Chunky, geometric, poster-like | **Yes** | `https://fonts.gstatic.com/s/zcoolqingkehuangyou/v16/2Eb5L_R5IXJEWhD3AOhSvFC554MOOahI4mRIiw.ttf` (200 ✓file) |
| **站酷小薇 ZCOOL XiaoWei** | OFL 1.1 | ✅ | 1 | Elegant, slim Song-style display | **Yes** | `https://fonts.gstatic.com/s/zcoolxiaowei/v15/i7dMIFFrTRywPpUVX9_RJyM1YFI.ttf` (200 ✓file) |
| **优设标题黑** | Free commercial per 优设网 (custom statement, not OFL) | ✅ | 1 | Heavy, forward-leaning, e-commerce/title energy | No | `https://cdn.jsdelivr.net/npm/@fontpkg/you-she-biao-ti-hei@1.0.0/%E4%BC%98%E8%AE%BE%E6%A0%87%E9%A2%98%E9%BB%91.ttf` (200 ✓file, 7,194 glyphs). Sliced: `https://cdn.jsdelivr.net/npm/@chinese-fonts/ysbth@3.0.0/dist/%E4%BC%98%E8%AE%BE%E6%A0%87%E9%A2%98%E9%BB%91/result.css` (200 ✓) |
| **庞门正道标题体** | Free commercial per 庞门正道 (custom statement) | ✅ | 1 | Bold, blocky, loud headline | No | `https://cdn.jsdelivr.net/gh/wordshub/free-font@master/assets/font/%E4%B8%AD%E6%96%87/%E5%BA%9E%E9%97%A8%E6%AD%A3%E9%81%93%E5%AD%97%E4%BD%93%E7%B3%BB%E5%88%97/%E5%BA%9E%E9%97%A8%E6%AD%A3%E9%81%93%E6%A0%87%E9%A2%98%E4%BD%93.ttf` (200 ✓file, v3.12). ⚠ **Only 6,231 glyphs**, fewer than GB2312's 6,763 hanzi: check every title for missing characters. |
| **演示悠然小楷** | Free commercial (author statement, 孟祥媛/演示系列) | ✅ | 1 | Brush 小楷, rustic and calm. Quotes and endings. | No | `https://cdn.jsdelivr.net/gh/wordshub/free-font@master/assets/font/%E4%B8%AD%E6%96%87/%E5%85%B6%E4%BB%96%E5%AD%97%E4%BD%93/%E6%BC%94%E7%A4%BA%E6%82%A0%E7%84%B6%E5%B0%8F%E6%A5%B7.ttf` (200 ✓file, 12.6 MB, 6,956 glyphs). The GitHub release URL found in search (`inancoding/free-font` tag) is now **404**. |
| **抖音美好体 Douyin Sans** | **OFL 1.1** (OFL.txt in the official repo; name table confirms) | ✅ | Bold only | Rounded-bold, warm, Douyin-native | No | Official repo via jsDelivr: `https://cdn.jsdelivr.net/gh/bytedance/fonts@main/DouyinSans/DouyinSansBold.ttf` (200 ✓file, v1.01) |
| **钉钉进步体 DingTalk JinBuTi** | Free commercial (DingTalk custom license) | ✅ | 1 (7° italic) | Sporty, forward-slanted, techy-young | No | Official page: page.dingtalk.com (search result; not fetched). Mirror: `https://cdn.jsdelivr.net/npm/@fontpkg/ding-talk-jin-bu-ti@1.0.3/DingTalk%20JinBuTi.ttf` (200 ✓file, 7,526 glyphs) |
| 阿里巴巴普惠体 2.0 (fallback) | Alibaba free license | ✅ | 5 | — | No | `https://cdn.jsdelivr.net/gh/wordshub/free-font@master/assets/font/%E4%B8%AD%E6%96%87/%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E6%99%AE%E6%83%A0%E4%BD%93/Alibaba-PuHuiTi-Bold.ttf` (200 ✓file) |

**License caveats.** OFL fonts (Noto/Source Han, Smiley, LXGW, ZCOOL, Douyin Sans, Sarasa) are safe to vendor and redistribute inside a project. The custom free-commercial fonts (普惠体, HarmonyOS, MiSans, OPPO, 优设, 庞门, 悠然, 钉钉) may be *used* commercially in videos but generally may not be modified or re-hosted. Store each license text next to the vendored file and point downloads at the official URL where one exists. The `@fontpkg/*` and `wordshub` mirrors are third-party convenience copies, not official sources.

**Coverage caveat.** The display fonts (优设, 庞门, 悠然, 钉钉, 抖音, Smiley, and 普惠体 Heavy/Black) cover only around GB2312, 6–10k glyphs. Set a fallback stack ending in `"Noto Sans SC"` so a missing character falls back instead of rendering as tofu (□). Lint titles for missing glyphs at build time.

### C3. Latin pairings

All are OFL. All are confirmed on Google Fonts (css2 returned 200) and on Fontsource via jsDelivr.

| Font | Weights | Personality | Pair with | Verified |
|---|---|---|---|---|
| **Inter** / Inter Tight | 100–900 var | Neutral UI; tabular numerals | Noto Sans SC, HarmonyOS | GF 200; `@fontsource-variable/inter@5/index.css` 200 ✓ |
| **Geist** / **Geist Mono** | 100–900 var | Vercel-crisp, techy | MiSans, HarmonyOS | GF 200; `@fontsource-variable/geist@5/index.css` 200 ✓; release zip `github.com/vercel/geist-font/releases/download/v1.7.2/geist-font-v1.7.2.zip` 200 |
| **Space Grotesk** | 300–700 | Quirky geometric, sci-fi | HarmonyOS Black, OPPO Sans | GF 200; `@fontsource-variable/space-grotesk@5/index.css` 200 ✓ |
| **Manrope** | 200–800 | Modern geometric (used by 极客湾 [V]) | MiSans | GF 200 |
| **IBM Plex Sans / Mono** | 100–700 | Engineered, editorial-tech | Noto Sans/Serif SC | GF 200; `@fontsource/ibm-plex-sans@5/index.css` 200 ✓ |
| **JetBrains Mono** | 100–800 | Code | Sarasa Mono SC, Source Han Mono | GF 200; `@fontsource-variable/jetbrains-mono@5/index.css` 200 ✓; zip `github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip` 200 |
| **Playfair Display** | 400–900 | High-contrast luxury serif | Noto Serif SC Black | GF 200; Fontsource 200 ✓ |
| **Instrument Serif** (+ Instrument Sans) | 400 + italic | Condensed editorial serif, very current | Noto Serif SC, LXGW WenKai | GF 200; `@fontsource/instrument-serif@5/index.css` 200 ✓ |
| Others confirmed on GF | — | DM Serif Display, Fraunces, Newsreader, Bricolage Grotesque, Space Mono, Archivo, Noto Sans Mono | — | GF 200 |

### C4. Build-time fetch recommendations
1. **Fetch from Google Fonts at build time:** Noto Sans SC, Noto Serif SC, ZCOOL KuaiLe, ZCOOL QingKe HuangYou, ZCOOL XiaoWei, and all the Latin fonts above. Also on GF but less relevant: LXGW WenKai TC, Ma Shan Zheng, Long Cang, Zhi Mang Xing, Liu Jian Mao Cao, Chiron Hei/Sung HK.
2. **Fetch from jsDelivr as sliced webfonts** (cn-font-split `result.css`). These are ideal for HTML/HyperFrames rendering because only the used glyph slices load: Smiley Sans (`@chinese-fonts/dyh`), 优设标题黑 (`@chinese-fonts/ysbth`), MiSans (`misans-webfont`), LXGW WenKai (`lxgw-wenkai-webfont`), Noto SC (`@fontsource-variable/noto-sans-sc`).
3. **Vendor locally (recommended for everything).** Downloads from this machine to GitHub, jsDelivr and the API were intermittently slow or timed out. Copy the TTFs into the project, for example `assets/fonts/` with a `LICENSES/` folder, so renders are deterministic and don't depend on the network.

---

## Sources
- ifeng, on which Apple fonts Bilibili creators use (何同学, 极客湾, Manrope + MiSans, Bahnschrift): https://i.ifeng.com/c/8gC23YWnix9
- MediaStorm production workflow (Tencent News, 2020): https://news.qq.com/rain/a/20200407A0HUBZ00
- MediaStorm subtitle survey (14/54 creators use 思源黑体), via search summary. Archive note: https://moyf.github.io/p/%E5%BD%B1%E8%A7%86%E9%A3%93%E9%A3%8E%E7%9A%84%E5%AD%97%E5%B9%95%E6%A0%B7%E5%BC%8F%E5%92%8C%E6%8F%92%E4%BB%B6/
- Fan "Tim/MediaStorm" skill: https://github.com/phaseddd/PhasedddSkill/blob/master/tim-mediastorm/SKILL.md
- 何同学 style: https://www.woshipm.com/operate/4396016.html , https://www.lanjinger.com/d/111383
- 小Lin说: https://www.sohu.com/a/665819022_121124293 , https://www.zhihu.com/question/537496812
- 回形针: https://zh.wikipedia.org/wiki/%E5%9B%9E%E5%BD%A2%E9%92%88PaperClip , https://www.jianshu.com/p/5ab85a9b38c9 (now 404; content via search summary)
- 半佛仙人: https://www.zhihu.com/question/399979045 , https://miao.wondershare.cn/article/movie-tv/create-banfo-video.html
- 差评: https://www.sohu.com/a/700210447_355019
- 亿点点不一样: https://baike.baidu.com/item/%E4%BA%BF%E7%82%B9%E7%82%B9%E4%B8%8D%E4%B8%80%E6%A0%B7/64088769
- 极客湾 efficiency framework: https://sspai.com/post/90340
- MKBHD: https://www.thumix.com/thumbnail-style/mkbhd , https://www.writepanda.ai/blog/mkbhd-editing-style-measured/ (didn't load; figures from search snippet)
- Apple SF Pro: https://blakecrosley.com/blog/sf-pro-typography-system
- Vox fonts: https://fontsinuse.com/uses/6828/vox-website . Community Vox HyperFrames pack (hex tokens): https://github.com/Cele-san/vox-style-animation
- Kurzgesagt: https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt , https://github.com/black-atom-industries/black-atom/issues/47 (fan palette)
- Johnny Harris: https://motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/ , https://aescripts.com/learn/post/how-johnny-harris-makes-maps
- Wendover: https://en.wikipedia.org/wiki/Sam_Denby
- Font licenses and official pages: https://github.com/bytedance/fonts (Douyin Sans OFL), https://hyperos.mi.com/font/en/download/ , https://github.com/huawei-fonts/HarmonyOS-Sans , https://www.ithome.com/0/804/511.htm (OPPO Sans 4.0 terms), https://www.alibabafonts.com/ , https://blog.zhheo.com/p/e8a11f39.html (钉钉进步体), https://www.maoken.com/freefonts/3521.html (演示悠然小楷), https://github.com/wordshub/free-font
