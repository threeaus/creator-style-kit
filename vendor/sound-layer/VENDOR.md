# Vendored: opus-sound-layer

- Source: https://github.com/Bodila51/opus-sound-layer
- Commit: e9bdf5cbf2986ac73179d7a0fb1ada7f41302f1b (2026-10-10), reviewed before vendoring: network access is limited to kenney.nl, freesound.org (CDN) and api.openverse.org, used only by `sfx.py kit/search`; zip extraction uses basenames only.
- Licence: MIT (code); downloaded sounds are CC0 and credited in audio/kit/CREDITS.md.
- Files are unmodified. Per its own rules: never edit the scripts and never loosen a QA threshold to make a check pass.
- The kit drives it through `scripts/sound_pass.py`, which feeds our per-style SFX files as plain paths, so `sfx.py kit` (the 1,139-sound library download) is optional — use it only when a style kit lacks a sound.
- Update: re-clone, review the diff, copy the four files in `scripts/`, bump the commit above.
