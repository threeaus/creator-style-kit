```
SOUND LAYER · Opus 5.5
You can't hear. Use real recordings, pick each one yourself, place them from
the timeline, look at every sound, and let the QA decide. A human does the
final ear check.

SETUP  git clone https://github.com/Bodila51/opus-sound-layer sound-layer
Use its scripts (needs ffmpeg and uv). Never rewrite them and never loosen a
threshold to make a check pass.

1 CUES  Export audio/cues.json from the picture's own timing (springs,
easings, data-start). Never type frames. Format: uv run
sound-layer/scripts/mix.py --schema. Sound only on real actions; tag each:
cut (full-frame change) · move (frame of peak speed) · land (frame motion
stops) · appear (element pops in). One hero per ~4 s (logo, reveal):
"hit+boom" with stop_before and build, a riser or reverse peaking on it.

2 SOUNDS  uv run sound-layer/scripts/sfx.py kit  (1,139 CC0 sounds, 19
types: hit boom riser reverse transition whoosh swish glitch ui click key
tick tap pop thump paper chime shimmer zap). The first run downloads the
library: give it a 10-minute timeout or run it in the background. Choose
every sound yourself:
sfx.py browse --type <type> --like "<material, weight, mood>", LOOK at
audio/browse.png, put the chosen id in the cue. Keep one sonic family per
film (e.g. glass + air, or metal + sub); vary repeats. A bare type uses
the defaults.
Nothing fits? Find it yourself: sfx.py search "<material action>" --type
<type>, or any recording whose licence allows it; check it with sfx.py
sheet, then sfx.py add FILE --type <type> --credit "<source, licence>".
Never synthesize hits, clicks or whooshes; no meme sounds. Music: my
track, or a CC0 loop.

3 BUILD  Render the picture muted, then:
uv run sound-layer/scripts/mix.py audio/cues.json
ffmpeg -i video.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac
-b:a 256k -shortest out/final.mp4
uv run sound-layer/scripts/qa.py out/final.mp4

4 VERIFY  Fix every FAIL by changing cues or sounds, at most 2 rounds.
Open audio/qa.png and describe what you see at each hero cue.

5 DELIVER  final.mp4 · audio/kit/CREDITS.md · LISTEN.md: 5 timecodes to
check by ear. Don't call the sound good; report what the checks show.
```
