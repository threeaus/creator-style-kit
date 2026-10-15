# SFX research: per-style sound kits for vertical tech explainers

Date: 2026-10-08. Every URL status below comes from `curl` run during this research. `000` means the request timed out, or the host refused a HEAD request. `403` means Cloudflare or a bot wall blocked it.

## TL;DR

- **The best find is UI SFX (`uisfx`), which is CC0.** It contains 12 coherent sonic "personalities" (minimal, soft, glass, arcade, mechanical, organic, dreamy, scifi, rubber, cinematic, studio, zen). Each personality covers the same 78 semantic cues. The audio is rendered from deterministic synthesis recipes and ships in the npm tarball as ogg and mp3. This is almost exactly the "one coherent kit per style" structure we want. It is downloaded locally.
- **Kenney packs (CC0) cover foley and texture.** These are paper and book sounds, wood, metal latches, cloth, glitch blips, switches and impacts. Three packs are downloaded locally.
- **Long whooshes, risers, sub-booms, tape-stops, room tone and shutters are missing from CC0 packs we can fetch by script.** Synthesize them deterministically with ffmpeg; the recipes are tested and listed below. Sonniss GDC has great cinematic material and a no-attribution license, but it can't be downloaded by script (403 behind Cloudflare). Fetch it by hand if you need it.
- **Avoid BBC (non-commercial only).** Pixabay and Mixkit are fine to use by hand but have no SFX API and forbid redistributing the files themselves. ZapSplat requires attribution unless you pay.
- **The current `assets/sfx/*.m4a` kit is long and generic.** The riser is 10 s, the whoosh-cinematic is 5.5 s, the glitch is 3.5 s and the chime is 2.5 s. The proposed kits use short cues (0.1–1.2 s), and each cue is tied to a visual event.

---

## 1. Sources

| Source | License | Commercial | Attribution | Format / size | Programmatic URL (status) | Verdict |
|---|---|---|---|---|---|---|
| **UI SFX** (`romainsimon/uisfx`, npm `uisfx@0.4.0`) | Audio **CC0-1.0** (`LICENSE-AUDIO`), code MIT | Yes | No | ogg + mp3, 12 packs × 78 cues = 936 assets; tgz 7.9 MB | `https://registry.npmjs.org/uisfx/-/uisfx-0.4.0.tgz` (**200**) | **Downloaded.** Primary UI layer. |
| Kenney Interface Sounds | **CC0** (`License.txt`) | Yes | No (appreciated) | 100 ogg, 0.8 MB zip | `https://kenney.nl/media/pages/assets/interface-sounds/fa43c1dd4d-1677589452/kenney_interface-sounds.zip` (**200**) | **Downloaded** |
| Kenney Impact Sounds | **CC0** | Yes | No | 130 ogg, 0.8 MB | `https://kenney.nl/media/pages/assets/impact-sounds/87b4ddecda-1677589768/kenney_impact-sounds.zip` (**200**) | **Downloaded** |
| Kenney RPG Audio (foley) | **CC0** | Yes | No | 50 ogg, 0.96 MB | `https://kenney.nl/media/pages/assets/rpg-audio/8e99002d76-1677590336/kenney_rpg-audio.zip` (**200**) | **Downloaded** (book, paper, cloth, latch) |
| Kenney Digital Audio | **CC0** | Yes | No | 0.88 MB | `https://kenney.nl/media/pages/assets/digital-audio/216eac4753-1677590265/kenney_digital-audio.zip` (**200**) | Not downloaded. Optional source of sci-fi/cyber zaps. |
| Kenney UI Audio, Casino Audio | **CC0** | Yes | No | 0.4 MB / 0.99 MB | `.../ui-audio/490d233f68-1677590494/kenney_ui-audio.zip` (**200**), `.../casino-audio/2472606a04-1721639069/kenney_casino-audio.zip` (**200**) | Optional (chips and cards give a "pop" texture) |
| Material Design sound resources (Google) | **CC-BY 4.0** per Google. The archive.org item metadata says **BY-SA 4.0**. | Yes | **Required** ("Sound by Google, CC BY 4.0") | 40 ogg/mp3, a few KB each; includes `ui_camera-shutter`, `ui_tap-variant-01..04`, `navigation_transition-left/right` | `https://archive.org/download/material-design-sound-resources/<path>` (**200** per file). `archive.org/metadata/material-design-sound-resources` lists the files. | Usable with credit. Not downloaded, because of the BY vs BY-SA ambiguity. Treat it as BY-SA to be safe. |
| SND (snd.dev, Dentsu; npm `snd-lib@1.2.4`) | Custom terms. Free for commercial use. Banned: redistributing unmodified files, and use as a sound logo or trademark. | Yes | No | 3 kits: SND01 sine, SND02 piano, SND03 industrial | `https://cdn.jsdelivr.net/npm/snd-lib@1.2.4/dist/snd.js` (**200**). The sprite folder listing timed out. | Good Apple-like "sine" kit. The terms are custom rather than CC0. Not downloaded. |
| Sonniss GDC Game Audio Bundles | Royalty-free, commercial, **no attribution**, unlimited projects. You can't resell or redistribute the raw files. | Yes | No | WAV, 7+ GB per year, ~200 GB archive | `https://gdc.sonniss.com/` (**403**), `sonniss.com/gameaudiogdc` (**403**). Cloudflare blocks it. | **Manual or torrent only.** Best source of real whooshes, risers and film foley. Curate a few files by hand. |
| Freesound | Per-sound: CC0, CC-BY, or CC-BY-NC | Depends on the sound | Depends on the license | wav/flac originals; mp3/ogg previews | `https://freesound.org/apiv2/search/text/?filter=license:"Creative Commons 0"` (**401** without a key). Docs **200**. | Needs an API key (token) to search and get previews. Downloading originals needs OAuth2. Filter to CC0 only. |
| Pixabay sound effects | Pixabay Content License: commercial use, no attribution. Can't redistribute standalone. | Yes | No | mp3 | `pixabay.com/sound-effects/` (**403** to curl). The API (`/api/docs/` **200**) covers **images and videos only**. It says "Systematic mass downloads are not allowed." | Manual, hand-picked only. |
| Mixkit SFX | Mixkit SFX Free License: commercial use, no attribution. Can't redistribute "on its own, as stock, in a tool or template". | Yes | No | wav/mp3 | `mixkit.co/free-sound-effects/` (**200**). No API. | Manual only. **Don't bundle Mixkit files inside a reusable preset or template** (the license forbids "in a tool or template"). |
| ZapSplat | Standard (free) license **requires credit to "ZapSplat"**. Gold (paid) removes it. | Yes | **Required** | mp3/wav | `zapsplat.com` (**403**) | Skip, because of the attribution and the login wall. |
| BBC Sound Effects | **RemArc: personal, educational or research use only.** Commercial use goes through Pro Sound Effects. | **No** | n/a | wav/mp3 | `sound-effects.bbcrewind.co.uk/licensing` (**200**) | **Do not use.** |
| OpenGameArt | Per asset (CC0, CC-BY, GPL…) | Varies | Varies | various | `opengameart.org/content/cc0-resources` (**200**) | Only assets tagged CC0. Low priority. |
| soundcn (`kapishdima/soundcn`) | Code MIT; per-sound license unclear | ? | ? | 700+ UI sounds | GitHub | **Unclear license, not used.** |
| **Procedural** | | | | | | |
| ffmpeg `aevalsrc` / `anoisesrc` | Our own output | Yes | No | wav | local | **Used for the gaps** (recipes in §4) |
| ZzFX (`zzfx@1.4.0`) | MIT | Yes | No | JS → wav (`wav.js` included) | `https://cdn.jsdelivr.net/npm/zzfx@1.4.0/ZzFX.js` (**200**) | Deterministic 8-bit/UI blips; 20-parameter arrays |
| jsfxr (`jsfxr@1.4.1`) | Unlicense/MIT | Yes | No | JS → wav (riffwave) | `https://cdn.jsdelivr.net/npm/jsfxr@1.4.1/sfxr.js` (**200**) | Retro/arcade blips |
| Tone.js (`tone@15.1.22`) | MIT | Yes | No | Web Audio; `Tone.Offline` renders a buffer | `https://cdn.jsdelivr.net/npm/tone@15.1.22/build/Tone.js` (**200**) | Musical swells and FM chimes. Rendering needs a browser (HyperFrames' Chromium works). |

GitHub search note: `ui sounds cc0` and `sound effects cc0` mostly return tiny repos and MCP wrappers with no curated content. Of the GitHub results, only uisfx has a large, clearly licensed audio set.

---

## 2. Downloaded inventory

Location: `/Volumes/ORICO/Opus/opus55-tutorial/.work/research/sfx/`. The full per-file list with durations is in `inventory.tsv` (1,218 rows, all CC0-1.0). The zip files were deleted after unzipping, and the uisfx tgz was kept.

### 2a. `uisfx/package/sounds/<pack>/<cue>.{ogg,mp3}` (CC0)

There are 78 cues in each of the 12 packs. The cues used most in the kits below are `select, deselect, hover, focus, press, release, open, close, expand, collapse, swipe, snap, drop, drag-start, progress-step, check, complete, success, achievement, level-up, reward, notification, info, warning, error, typing, copy, paste, send, receive, start, stop, wake, sleep, unlock, lock, scanning, processing, loading`.

Durations of key cues (seconds):

| pack | select | swipe | open | snap | progress-step | success | complete | typing | notification | drop |
|---|---|---|---|---|---|---|---|---|---|---|
| minimal | .25 | .33 | .32 | .16 | .21 | .59 | .65 | .09 | .47 | .26 |
| glass | .52 | .61 | .59 | .37 | .46 | 1.04 | 1.13 | .12 | .83 | .54 |
| soft | .42 | .50 | .49 | .27 | .34 | .91 | .98 | .11 | .72 | .42 |
| cinematic | .58 | .69 | .68 | .41 | .50 | 1.14 | 1.23 | .12 | .95 | .59 |
| dreamy | .60 | .69 | .69 | .43 | .51 | 1.14 | 1.22 | .11 | .92 | .59 |
| studio | .30 | .34 | .34 | .20 | .26 | .60 | .66 | .10 | .48 | .31 |
| zen | .26 | .33 | .33 | .16 | .22 | .58 | .64 | .09 | .46 | .28 |
| organic | .43 | .53 | .51 | .30 | .38 | .92 | 1.01 | .11 | .74 | .45 |
| mechanical | .25 | .26 | .29 | .17 | .22 | .50 | .57 | .09 | .39 | .26 |
| scifi | .32 | .34 | .36 | .22 | .28 | .62 | .70 | .10 | .49 | .33 |
| rubber | .30 | .34 | .35 | .19 | .25 | .65 | .71 | .10 | .50 | .31 |
| arcade | .31 | .36 | .39 | .21 | .27 | .63 | .74 | .12 | .53 | .32 |

Levels: the files are pre-normalized. Peaks sit around **−7.5 dBFS**, and the mean is −17 to −23 dBFS.

Character by pack:
- **minimal, glass, soft**: clean and premium.
- **cinematic, dreamy**: tails and blooms.
- **studio, zen, organic**: tactile, paper and wood.
- **mechanical**: relays and detents.
- **scifi**: holographic and digital.
- **rubber, arcade**: playful.

### 2b. `kenney_interface-sounds/Audio/` (CC0, 100 files)

Peaks are near **0 dBFS**, so pad them about −8 dB to match uisfx.

| group | files | dur (s) | character |
|---|---|---|---|
| tick | tick_001/002/004 | .02–.05 | micro-click, very clean (Apple, editorial) |
| click | click_001–005 | .01–.10 | dry clicks |
| select | select_001–008 | .04–1.94 | soft pings (005 is a long 1.9 s chime tail) |
| toggle / switch | toggle_001–004, switch_001–007 | .07–.62 | plastic/mechanical switches (retro) |
| pluck / bong / drop | pluck_001–002, bong_001, drop_001–004 | .10–.29 | rounded, playful |
| glass | glass_001–006 | .11–.69 | crystalline taps |
| open / close / maximize / minimize | ×4 / ×4 / ×9 / ×9 | .15–.53 | UI swells, short whoosh-like |
| confirmation / question / error | ×4 / ×4 / ×8 | .10–.54 | earcons (use sparingly) |
| glitch | glitch_001–004 | .01–.03 | digital micro-bursts (cyber; chain them into stutters) |
| scratch | scratch_001–005 | .12–.33 | vinyl-ish scratch (retro, glitch) |
| scroll | scroll_001–005 | 1.00 | ratchet/scroll texture |

### 2c. `kenney_impact-sounds/Audio/` (CC0, 130 files, 5 variants each)

| group | dur (s) | character / use |
|---|---|---|
| impactSoft_medium/heavy | .12–.57 | **soft thud**, the best general "emphasis hit" (low-pass it for docu) |
| impactPunch_medium/heavy | .40–.65 | punchy body hit (pop, docu stingers) |
| impactWood_light/medium/heavy, impactPlank_medium | .27–.78 | wooden knock or stamp (editorial, retro) |
| impactBell_heavy | .30–1.74 | bell/gong tail (docu outro, low-pass it) |
| impactGlass_light/medium/heavy | .17–.54 | glass clink (Apple accent) |
| impactMetal_*, impactTin_medium, impactPlate_* | .11–.66 | metallic (retro, mechanical) |
| impactGeneric_light | .12–.14 | neutral tap |
| impactMining | .80–.99 | gritty (rarely useful) |
| footstep_* (carpet, concrete, grass, snow, wood) | .11–.78 | foley. Skip, except snow/grass as soft "crunch" textures |

### 2d. `kenney_rpg-audio/Audio/` (CC0, 50 files): foley and paper

| group | dur (s) | use |
|---|---|---|
| bookFlip1–3 | .23–.77 | **page turn** (editorial transition) |
| bookOpen / bookClose / bookPlace1–3 | .15–.35 | **paper/board set-down**, stamp-like (editorial list item) |
| cloth1–4, clothBelt, clothBelt2 | .38–.75 | soft fabric swish (an organic micro-whoosh) |
| metalClick, metalLatch | .26–.45 | **shutter/latch** body (retro camera) |
| creak1–3, doorOpen/Close | .34–1.41 | wooden creak (retro) |
| drawKnife1–3, knifeSlice1–2 | .40–.60 | metallic swipe ("blade" transition, use carefully) |
| handleCoins, handleSmallLeather, dropLeather, beltHandle, chop, metalPot, footstep00–09 | .22–1.46 | mostly too game-like for explainers |

---

## 3. Per-style kits

Naming: `uisfx:<pack>/<cue>`, `kenney-if:<file>` (interface), `kenney-imp:<file>`, `kenney-rpg:<file>`, `synth:<recipe>` (§4).

**Variation rule for every kit:** each role has 2–4 interchangeable sources or variants. Pick them round-robin from a seeded RNG, add ±1–2 semitones of pitch jitter (`asetrate` + `aresample`) and ±1.5 dB of gain jitter, and never use the same file twice in a row.

### Style A: Apple-clean (minimal, airy, premium)
Sonic idea: almost invisible, high-mid, dry, short. Sine and glass, no low-end booms. Silence is the default.

| role | source | notes |
|---|---|---|
| title-in | `uisfx:glass/open` (+ `synth:air-whoosh` 0.4 s at −8 dB under it) | Land the glass bloom on the frame where the title settles |
| text-tick | `kenney-if:tick_002`, `tick_004`, `uisfx:minimal/typing` | Only on key words or numbers, never on every word |
| transition | `synth:air-whoosh` (0.35–0.5 s, high-passed at 400 Hz), alternating with `uisfx:glass/swipe` | One per scene change at most |
| emphasis-hit | `uisfx:glass/snap`, `kenney-imp:impactGlass_light_00x` | A highlight or underline lands |
| list-item | `uisfx:minimal/progress-step` pitched +0/+2/+4/+5 st per item | The ascending ladder gives a sense of progress without repeating |
| reveal | `uisfx:glass/complete` | Number or product reveal |
| outro | `uisfx:glass/success` → 1 s of silence | |
| bed | none (or very quiet `synth:roomtone`) | |

### Style B: Cinematic documentary
Sonic idea: weight and air. Low sub-booms, long tails, risers into reveals. There are few events, but each one is bigger.

| role | source | notes |
|---|---|---|
| title-in | `synth:subboom` + `uisfx:cinematic/open` | The boom lands on the cut; the open tail carries the title |
| text-tick | `uisfx:studio/typing` at −6 dB, or nothing | Docs mostly skip ticks |
| transition | `synth:air-whoosh` 0.7–0.9 s, low-passed at 3 kHz; Sonniss whoosh (manual) | Whoosh peak on the cut frame, not the start |
| emphasis-hit | `kenney-imp:impactSoft_heavy_00x` low-passed at 900 Hz + `synth:subboom` at −10 dB | Max 2 per minute |
| list-item | `uisfx:cinematic/progress-step` | |
| reveal | `synth:riser` (1.5–2 s, hard stop) → 120 ms silence → `uisfx:cinematic/complete` | The pre-hit silence (the "suck-out") is what sells it |
| outro | `kenney-imp:impactBell_heavy_000` low-passed at 1.5 kHz + reverb tail, or `uisfx:cinematic/success` | |
| bed | `synth:roomtone` at −50 dBFS under the voice | Stops dead-air "holes" |

### Style C: Playful / pop
Sonic idea: rounded, bouncy, mid-range, pitched. Fits the color and bounce easing.

| role | source | notes |
|---|---|---|
| title-in | `uisfx:rubber/open` + `kenney-if:pluck_002` | |
| text-tick | `kenney-if:drop_001–004` (round-robin) | Pop-in words only |
| transition | `uisfx:rubber/swipe`, `kenney-rpg:cloth2` | Short |
| emphasis-hit | `uisfx:rubber/snap`, `kenney-imp:impactSoft_medium_00x` | Sync with a squash/scale-bounce |
| list-item | `kenney-if:pluck_001`, then `uisfx:rubber/select` pitched up per item | |
| reveal | `uisfx:arcade/reward` (sparingly) or `uisfx:soft/complete` | arcade only at peak moments, or it gets childish |
| outro | `uisfx:rubber/achievement` | |
| bed | music does the work; no room tone | |

### Style D: Retro / analog (film, tape, hardware)
Sonic idea: mechanical detents, latches, tape hiss and wow, typewriter.

| role | source | notes |
|---|---|---|
| title-in | `synth:shutter` (metalLatch + mechanical/snap) + `kenney-if:switch_00x` | Camera clack plus power-on |
| text-tick | `uisfx:mechanical/typing`, `kenney-if:click_001–005` | A typewriter feel for typed-on text |
| transition | `kenney-if:scratch_00x` or `synth:tapestop` (pitch-dive the outgoing audio over 0.3 s) | |
| emphasis-hit | `kenney-imp:impactWood_medium_00x`, `kenney-imp:impactMetal_light_00x` | Stamp or rivet |
| list-item | `kenney-if:switch_001–007` (round-robin), `uisfx:mechanical/progress-step` | Relay clicks |
| reveal | `kenney-rpg:metalLatch` → `uisfx:mechanical/complete` | |
| camera/snapshot | `synth:shutter`, or Material `ui_camera-shutter` (needs CC-BY credit) | |
| outro | `kenney-rpg:creak2` (short) or `uisfx:mechanical/stop` | |
| bed | `synth:roomtone` brown noise + 3 kHz low-pass "hiss" at −48 dBFS | Gives the tape texture |

### Style E: Editorial / print (magazine, paper, ink)
Sonic idea: paper, wood and pencil. Dry, close-miked and tactile. No synth tones.

| role | source | notes |
|---|---|---|
| title-in | `kenney-rpg:bookPlace1–3` + `uisfx:zen/open` | A sheet set down on a desk |
| text-tick | `uisfx:studio/typing`, `kenney-if:tick_001` | A pencil-like tick |
| transition | `kenney-rpg:bookFlip1–3` (page turn) | The signature sound of this style; keep it under 0.5 s with a fade |
| emphasis-hit | `kenney-imp:impactWood_light_00x` (stamp), `uisfx:zen/snap` | Marker or stamp hits |
| list-item | `uisfx:organic/select`, `kenney-rpg:bookOpen` | |
| highlight/underline | `uisfx:zen/swipe`, `kenney-rpg:cloth3` (very quiet) | Marker swipe |
| reveal | `uisfx:zen/complete` | |
| outro | `kenney-rpg:bookClose` | Literally closing the magazine |

### Style F: Glitch / cyber
Sonic idea: digital artifacts, bitcrush, short bursts, hard cuts and the silence between them.

| role | source | notes |
|---|---|---|
| title-in | `synth:stutter` (glitch_003 + bitcrushed scifi/select ×3) | |
| text-tick | `kenney-if:glitch_001–004` (10–30 ms) | Decoding or scramble text |
| transition | `kenney-if:scratch_00x` + `synth:bitburst` (120 ms of noise through acrusher) | A cut, not a whoosh |
| emphasis-hit | `uisfx:scifi/snap` + `synth:subboom` at −12 dB | |
| list-item | `uisfx:scifi/select`, `uisfx:scifi/progress-step` | |
| reveal | `uisfx:scifi/scanning` (trimmed 0.6 s) → `uisfx:scifi/complete` | |
| error/warning beat | `kenney-if:error_00x`, `uisfx:scifi/warning` | Only when the script says "fails" or "wrong" |
| outro | `uisfx:scifi/sleep` (power-down) | |

The packs left over (`dreamy`, `soft`, `organic`) map naturally to a future "calm / wellness / 治愈" preset.

---

## 4. Deterministic synth recipes (ffmpeg, tested)

All of these ran successfully on 2026-10-08. They are deterministic because the seeds are fixed.

```bash
# synth:air-whoosh  (0.7s; shorten d / fades for Apple)
ffmpeg -f lavfi -i "anoisesrc=c=pink:d=0.7:a=0.6:seed=7" -af "highpass=f=300,lowpass=f=4000,afade=t=in:st=0:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.25:curve=qsin" whoosh.wav
# synth:riser  (2s chirp 200→1200Hz + hiss, exp fade-in, hard stop)
ffmpeg -f lavfi -i "aevalsrc='0.3*sin(2*PI*(200*t+250*t*t))':d=2:s=48000" -f lavfi -i "anoisesrc=c=white:d=2:a=0.15:seed=3" -filter_complex "[1]highpass=f=2000[n];[0][n]amix=inputs=2:normalize=0,afade=t=in:st=0:d=1.9:curve=exp,afade=t=out:st=1.95:d=0.05" riser.wav
# synth:subboom  (1.2s, 55Hz downward sweep, exp decay)
ffmpeg -f lavfi -i "aevalsrc='0.8*sin(2*PI*(55*t-20*t*t))*exp(-t*3.5)':d=1.2:s=48000" -af "lowpass=f=180,afade=t=in:d=0.005" subboom.wav
# synth:tick  (60ms 2.4kHz sine ping)
ffmpeg -f lavfi -i "aevalsrc='0.5*sin(2*PI*2400*t)*exp(-t*90)':d=0.06:s=48000" tick.wav
# synth:stutter  (glitch + bitcrushed blip, looped)
ffmpeg -i kenney_interface-sounds/Audio/glitch_003.ogg -i uisfx/package/sounds/scifi/select.ogg -filter_complex "[1]acrusher=bits=6:samples=8:mix=1,atrim=0:0.12[b];[0][b]concat=n=2:v=0:a=1,aloop=loop=2:size=4000" stutter.wav
# synth:shutter  (latch + snap, 25ms offset)
ffmpeg -i kenney_rpg-audio/Audio/metalLatch.ogg -i uisfx/package/sounds/mechanical/snap.ogg -filter_complex "[1]adelay=25|25[s];[0][s]amix=inputs=2:normalize=0,highpass=f=200" shutter.wav
# synth:roomtone  (brown noise bed; set level at mix time, ~-50 dBFS)
ffmpeg -f lavfi -i "anoisesrc=c=brown:d=10:a=0.02:seed=1" -af "highpass=f=80,lowpass=f=6000" roomtone.wav
# synth:tapestop  (apply to the outgoing 0.3s of music/VO)
#   asetrate=48000*0.5,aresample=48000 with afade out, or a pitch envelope via rubberband if available
# variation jitter (±2 semitones, ±1.5 dB)
ffmpeg -i in.ogg -af "asetrate=48000*1.122,aresample=48000,volume=-1.5dB" out.wav   # 1.122 = +2 st; 0.891 = -2 st
```

For musical swells and FM chimes (Apple or dreamy), use `Tone.Offline` inside the HyperFrames Chromium and save the buffer as WAV. For 8-bit or arcade sounds, ZzFX parameter arrays are deterministic and fit in a single line.

---

## 5. Mixing and placement rules for 60–180 s vertical explainers

### Density (the "sparingly" rule)
- **Budget: about 1 SFX event per 3–5 s on average, and at most 1 per 1.5 s locally.** A 90 s video should have roughly 15–25 events, not 60. The SFX track should be **silent for 60–75% of the runtime**.
- **SFX follow visual events, not words.** Use one only when something *enters, lands, changes state or is revealed*. If nothing visibly lands, don't add a sound.
- **Hero moments (at most 2–3 per video)** get the big layered treatment: riser → silence → hit. Everything else stays at the "texture" level.
- **No two consecutive transitions should use the same sound.** Alternate whoosh / cut / page-turn, or use a different variant.
- **Text tick only on key nouns or numbers.** Typing on every word is the #1 thing that makes a video sound cheap.
- **Keep 3–5 s with no SFX at all** during the densest explanation, so the listener can focus on the content.

### Silence as a tool
- **Pre-hit gap:** cut music and SFX 80–150 ms before a hero reveal or punchline (the "suck-out"), then hit. That gap is louder than any boom.
- **Drop music for one key sentence** (the thesis or the number), then bring it back at the next scene. MKBHD, Johnny Harris and Vox all use this.
- **End clean:** the outro sting plus a 0.5–1 s tail, with no SFX under the final CTA voice line.

### Levels (target the delivered file, not the timeline)
- **Master: −14 LUFS integrated (YouTube, Shorts and TikTok normalize to this), true peak ≤ −1.5 dBTP.** Douyin, Bilibili and 视频号 don't publish a target. −14 to −16 LUFS with TP −1.5 is safe, and keeps AAC transcodes from clipping.
- **Voice is the anchor:** VO at about −16 to −14 LUFS short-term while speaking.
- **SFX under the voice:** UI ticks and list items sit **10–15 dB below the VO**; transitions and whooshes 6–10 dB below. Hero hits may peak at **VO level, but never above it**, and only in gaps between words.
- **Music bed:** −18 to −24 dB below the VO while speaking, ducking 6–10 dB with about 80 ms attack and 300–500 ms release. In gaps it comes back up to roughly 8–12 dB below the VO. Use `/hyperframes-audio` (voiceover carve, `<hf-audio-group>` buses).
- **Normalize sources first.** uisfx peaks around −7.5 dBFS and Kenney around 0 dBFS. Trim Kenney by about −8 dB, or loudness-match all one-shots to a common short-term target (for example −20 LUFS-S) before applying per-role offsets.

### Layering and frequency rules
- **Two layers maximum per event:** body (the transient) plus air/tail. A third layer only on hero moments (sub + body + air).
- **Keep 1–4 kHz clear for the voice.** High-pass every SFX at 150–250 Hz, except sub-booms, which go low-pass < 180 Hz and only in VO gaps. Cut 2–3 dB at about 2.5 kHz on whooshes that run under speech.
- **Most viewers listen on a phone speaker.** Sub-booms below 80 Hz are inaudible there, so make sure every hit also has a 200 Hz–2 kHz body component.
- **Sync on the landing frame:** the transient goes on the frame the element *settles*, not the frame it starts moving. Whoosh peaks go on the cut, so whoosh audio starts 150–300 ms *before* the cut.
- **One reverb space per style:** dry for Apple, editorial and glitch; a short plate for pop; a long hall tail only on docu hero hits.
- **Variation:** round-robin plus pitch jitter (±2 st) plus gain jitter (±1.5 dB) on every repeated role. Ascending pitch ladders on list items (+2 st per item, reset per list).

### How top creators handle it (patterns)
- **Apple keynotes and product films:** almost no SFX. The music carries the edit, and the rare sounds are tiny glass or sine ticks on UI state changes.
- **Vox and Johnny Harris docu style:** paper, map and film foley as the texture signature, plus silence drops before key facts and risers into the thesis.
- **MKBHD and tech reviewers:** clean whooshes only on actual camera or graphic moves, with a lot of silence. The sound follows the motion design, never decorates the speech.
- **Chinese tech creators (影视飓风, 何同学 style):** strong music-driven rhythm, SFX only on graphic landings, and a deliberate music cut on the key sentence. Dense meme SFX (综艺音效) stay out of the "premium" presets.

---

## 6. Recommended next steps
1. Build `presets/<style>/sfx/` by copying the selected CC0 files out of `.work/research/sfx` and rendering the `synth:*` recipes. Add a `kit.json` that maps role → [variants], gain offset and pitch-jitter range. Remove the generic `assets/sfx/*.m4a` from presets (the 10 s riser and 5.5 s whoosh are too long for short-form).
2. Add a placement linter: one SFX per 1.5 s at most, no same file back-to-back, at most 3 hero events, and the SFX track silent ≥ 60%.
3. If you need real cinematic whooshes or foley, hand-pick 10–20 files from Sonniss GDC (no attribution). Don't put Mixkit or Pixabay files inside presets, because of their template/redistribution clauses.
4. Get a Freesound API key only if specific textures are still missing. Filter on `license:"Creative Commons 0"`.
