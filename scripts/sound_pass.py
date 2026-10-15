#!/usr/bin/env python3
"""Final sound pass for a HyperFrames project built with the kit (uses vendor/sound-layer).

usage: sound_pass.py <project> <rendered.mp4> [--voice vo.wav[@start_s]] [--music bed.wav]
                     [--energy calm|punchy] [--out <project>/out/final.mp4] [--no-visual]

1. Reads every <audio> cue the kit placed (compositions/*.html: data-peak, data-role,
   data-visual, data-weight) and the host offsets in index.html → <project>/audio/cues.json.
2. mix.py: peak-aligned placement, per-event gain against voice + music, ducking, a shared
   room, loudness to target (calm −18 / punchy −14 LUFS) with a true-peak limiter.
3. Muxes the mix onto the picture (video stream copied), then qa.py checks sync, audibility,
   loudness, true peak, voice/music balance and the cue ↔ picture match → audio/qa.png.
4. Writes <project>/LISTEN.md: timecodes a human should check by ear.

Rules (from sound-layer): never edit vendor/sound-layer, never loosen a threshold. Fix a
FAIL by changing cues (style sound.rules, scaffold timing) or sounds, at most 2 rounds.
Needs ffmpeg and uv.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SL = KIT / "vendor" / "sound-layer" / "scripts"


def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def collect(project):
    idx = (project / "index.html").read_text(encoding="utf-8")
    cues = []
    for host in re.findall(r"<div[^>]*data-composition-src=[^>]*>", idx):
        h = attrs(host); t0 = float(h.get("data-start", 0))
        comp = project / h["data-composition-src"]
        for tag in re.findall(r"<audio[^>]*>", comp.read_text(encoding="utf-8")):
            a = attrs(tag)
            if "data-peak" not in a:          # hand-placed audio (music, VO) is not a cue
                continue
            cues.append({"id": a["id"], "t": round(t0 + float(a["data-peak"]), 3), "sound": str((project / a["src"]).resolve()),
                         "align": "peak", "weight": a.get("data-weight", "support"), "visual": a.get("data-visual"),
                         "role": a.get("data-role"), "volume": float(a.get("data-volume", 1)),
                         "roi": [int(v) for v in a["data-roi"].split(",")] if a.get("data-roi") else [520, 940]})
    return sorted(cues, key=lambda c: c["t"])


def reveal_check(video, cues, fps, tol=3):
    """Kit check for hero reveals (qa.py's `land` probe is fooled by ambient motion): crop to the stat figure
    (its band comes from the style's layout, data-roi on the cue) and find the last frame the figure still
    changes; the reveal sound should sit within `tol` frames of it."""
    if not cues: return 0
    import numpy as np
    fails = 0
    print("\nreveal sync (kit check: figure region, ±%d frames)" % tol)
    for c in cues:
        a0 = max(0.0, c["t"] - 1.6)
        y0, y1 = c["roi"]; hh = (y1 - y0) // 4
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0:.3f}", "-i", str(video), "-t", "2.4", "-an", "-vf",
                              f"fps={fps},crop=1000:{y1 - y0}:40:{y0},scale=250:{hh},format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, hh, 250).astype(np.float32)
        m = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)); ts = a0 + (np.arange(len(m)) + 1) / fps
        win = (ts > c["t"] - 1.5) & (ts < c["t"] + 0.25)
        if not win.any() or m[win].max() <= 0:
            print(f"warn  {c['id']:26s} no figure motion found"); continue
        last = ts[win][np.where(m[win] > 0.12 * m[win].max())[0][-1]]
        d = round((c["t"] - last) * fps, 1)
        hit = abs(ts[win][int(np.argmax(m[win]))] - c["t"]) * fps <= 2      # impact modes (stamp): sound on the biggest change
        ok = abs(d) <= tol or hit; fails += not ok
        why = "on the impact frame" if hit and abs(d) > tol else f"figure stops {last:.2f}s ({d:+.1f} frames)"
        print(f"{'pass' if ok else 'FAIL'}  {c['id']:26s} sound {c['t']:.2f}s, {why}")
    return 1 if fails else 0


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("video")
    ap.add_argument("--voice", action="append", default=[], help="file[@start_s], repeatable")
    ap.add_argument("--music"); ap.add_argument("--energy", default="calm", choices=["calm", "punchy"])
    ap.add_argument("--out"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--no-visual", action="store_true", help="don't ask qa.py to match cues to picture motion")
    a = ap.parse_args()
    project, video = Path(a.project).resolve(), Path(a.video).resolve()
    out = Path(a.out).resolve() if a.out else project / "out" / "final.mp4"
    audio = project / "audio"; audio.mkdir(exist_ok=True); out.parent.mkdir(parents=True, exist_ok=True)

    cues, T = collect(project), duration(video)
    if not cues:
        sys.exit("no kit cues found (audio tags need data-peak — regenerate with scaffold.py)")
    sheet = {"fps": a.fps, "duration_s": round(T, 3), "energy": a.energy, "kit": str(audio / "kit"), "cues": []}
    for c in cues:
        e = {k: c[k] for k in ("id", "t", "sound", "align", "weight")}
        if c["visual"] in ("cut", "move", "land") and not a.no_visual:
            e["visual"] = c["visual"]
        sheet["cues"].append(e)
    voices = []
    for v in a.voice:
        f, _, st = v.partition("@"); voices.append({"file": str(Path(f).resolve()), "start_s": float(st or 0)})
    if voices: sheet["voice"] = voices
    if a.music: sheet["music"] = {"file": str(Path(a.music).resolve()), "start_s": 0, "loop": True, "fade_out_s": 1.0}
    if not voices and not a.music:
        # an SFX-only film is mostly silence by design (style sound.rules silentShare); declare it planned
        sheet["silence_ok"] = [[0, round(T, 3)]]
        print("note: no voice or music bed — silence check covers the whole film as planned silence")
    (audio / "cues.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"cues.json: {len(cues)} cues over {T:.1f}s ({len(cues) / T:.2f}/s)")

    uv = lambda script, *args: subprocess.run(["uv", "run", "-q", str(SL / script), *args], cwd=project)
    if uv("mix.py", str(audio / "cues.json"), "--out", str(audio)).returncode:
        sys.exit("mix.py failed")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(audio / "mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)], check=True)
    qa = uv("qa.py", str(out), "--audio", str(audio))
    lock_fail = reveal_check(out, [c for c in cues if c["visual"] == "lock"], a.fps)

    heroes = [c for c in cues if c["weight"] == "hero"]
    rest = [c for c in cues if c["weight"] != "hero"]
    gaps = sorted(rest, key=lambda c: min([abs(c["t"] - o["t"]) for o in cues if o is not c] or [99]))
    pick = (heroes[:3] + gaps[:5])[:5]
    lines = ["# Listen", "", f"`{out.name}` — the checks measure, they don't hear. Check these by ear:", ""]
    for c in sorted(pick, key=lambda c: c["t"]):
        why = "hero: lands with the number locking?" if c["weight"] == "hero" else "closest to another cue: two sounds smearing?"
        lines.append(f"- **{int(c['t'] // 60)}:{c['t'] % 60:05.2f}** {c['role']} — {why}")
    lines += ["", "QA: `audio/qa-report.json` · picture: `audio/qa.png`"]
    (project / "LISTEN.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n→ {out}\n→ {project / 'LISTEN.md'}")
    sys.exit(qa.returncode or lock_fail)


if __name__ == "__main__":
    main()
