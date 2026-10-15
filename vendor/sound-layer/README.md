# opus-sound-layer

A sound layer for motion videos made by Claude Opus 5.5 (Remotion, HyperFrames or any renderer that can export frame timings).

Opus can't hear its own audio, so its sound effects come out synthetic and off the picture. This repo gives it real recordings, a mixer that places every sound from the timeline, and a QA script that measures what a sound designer would listen for.

The prompt to paste into Claude Code is in [PROMPT.md](PROMPT.md).

## What's inside

| Script | Does |
|---|---|
| `scripts/sfx.py kit` | Builds the sound library: 1,139 CC0 sounds in 19 types (hit, boom, riser, reverse, transition, whoosh, swish, glitch, ui, click, key, tick, tap, pop, thump, paper, chime, shimmer, zap). Downloads 7 Kenney packs and hand-checked Freesound recordings, cuts each to clean events, filters and judges them, writes `catalog.json` and `CREDITS.md` |
| `scripts/sfx.py browse` | Lets Claude pick each sound: ranks one type by tags, length and brightness, prints the shortlist and draws its waveforms and spectrograms |
| `scripts/sfx.py search` / `add` | When nothing fits: finds more CC0 recordings through the Openverse API (no key), or takes any file Claude found, judges it and adds it to the library with its credit |
| `scripts/sfx.py sheet` | Waveform and spectrogram per sound, so Claude can look at what it can't hear |
| `scripts/mix.py` | Builds the mix from one cue sheet: peak-aligned placement, a library type, a picked id or any file per cue, layered hero hits, per-event gain in each sound's own band against music and voice, pitch to the music's key, one shared room for every effect, ducking, dead stop and filter build before hero hits, −14 LUFS master with a true-peak limiter |
| `scripts/qa.py` | Checks the encoded MP4: each cue against the real picture motion, sync, loudness, true peak, audibility of every sound, music under the voice, dips, silence. Exits 1 on failure |

## Requirements

- [ffmpeg](https://ffmpeg.org) on PATH
- [uv](https://docs.astral.sh/uv/) (installs Python and the packages for each script)

If uv fails with `invalid peer certificate`, set `UV_NATIVE_TLS=1` (common behind antivirus or corporate proxies).

## Run by hand

```bash
uv run scripts/sfx.py kit
uv run scripts/sfx.py browse --type hit --like "metal heavy"
uv run scripts/mix.py --schema           # cue sheet format
uv run scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out/final.mp4
uv run scripts/qa.py out/final.mp4
```

## Licence

Code: MIT. Sounds are not stored here: `sfx.py kit` downloads CC0 (public domain) packs from [Kenney](https://kenney.nl) and recordings from Freesound, and lists every source in `audio/kit/CREDITS.md`. Sounds added with `sfx.py add` keep the credit you give them.
