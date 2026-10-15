#!/usr/bin/env python3
"""Build each style's SFX kit from its style.yaml.

Sources (all CC0): uisfx (npm uisfx@0.4.0), Kenney interface / impact / rpg packs,
plus deterministic ffmpeg synth recipes. Every cue is trimmed short, high-passed to
keep the voice band clear, peak-normalised to -3 dBFS and then offset by the role gain.

usage: build_sfx.py <sources_dir> [style_id ...]
"""
import json, subprocess, sys, tempfile
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent
MAXLEN = {"outro": 2.0, "reveal": 1.6, "title": 1.4}
SYNTH = {
    "air-whoosh-short": "anoisesrc=c=pink:d=0.42:a=0.6:seed=7,highpass=f=400,lowpass=f=5000,afade=t=in:st=0:d=0.26:curve=exp,afade=t=out:st=0.26:d=0.16:curve=qsin",
    "air-whoosh": "anoisesrc=c=pink:d=0.7:a=0.6:seed=7,highpass=f=300,lowpass=f=4000,afade=t=in:st=0:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.25:curve=qsin",
    "subboom": "aevalsrc='0.8*sin(2*PI*(55*t-20*t*t))*exp(-t*3.5)':d=1.2:s=48000,lowpass=f=180,afade=t=in:d=0.005",
    "tick": "aevalsrc='0.5*sin(2*PI*2400*t)*exp(-t*90)':d=0.06:s=48000",
    "bitburst": "anoisesrc=c=white:d=0.12:a=0.5:seed=11,acrusher=bits=5:samples=12:mix=1,highpass=f=600,afade=t=out:st=0.08:d=0.04",
}


def resolve(src_dir: Path, ref: str):
    kind, name = ref.split(":", 1)
    if kind == "uisfx":
        return src_dir / "uisfx/package/sounds" / f"{name}.ogg"
    folder = {"kenney-if": "kenney_interface-sounds", "kenney-imp": "kenney_impact-sounds", "kenney-rpg": "kenney_rpg-audio"}.get(kind)
    if folder:
        return src_dir / folder / "Audio" / f"{name}.ogg"
    return None


def peak_db(path: Path) -> float:
    out = subprocess.run(["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "max_volume" in line:
            return float(line.split("max_volume:")[1].split("dB")[0])
    return 0.0


def render(src_dir: Path, ref: str, role: str, gain: float, pitch: float, out: Path):
    tmp = Path(tempfile.mkdtemp())
    raw = tmp / "raw.wav"
    kind, name = ref.split(":", 1)
    if kind == "synth":
        if name == "stutter":
            g = src_dir / "kenney_interface-sounds/Audio/glitch_003.ogg"
            b = src_dir / "uisfx/package/sounds/scifi/select.ogg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(g), "-i", str(b), "-filter_complex",
                            "[0]aresample=48000[g];[1]aresample=48000,acrusher=bits=6:samples=8:mix=1,atrim=0:0.12[b];[g][b]concat=n=2:v=0:a=1,aloop=loop=2:size=4000",
                            str(raw)], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", SYNTH[name], str(raw)], check=True)
    else:
        f = resolve(src_dir, ref)
        if not f or not f.exists():
            raise FileNotFoundError(ref)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-ac", "2", "-ar", "48000", str(raw)], check=True)
    norm = -3.0 - peak_db(raw) + gain
    maxlen = MAXLEN.get(role, 1.0)
    chain = []
    if pitch:
        chain.append(f"asetrate=48000*{2 ** (pitch / 12):.5f},aresample=48000")
    if name != "subboom":
        chain.append("highpass=f=140")
    chain += [f"volume={norm:.2f}dB", f"atrim=0:{maxlen}", f"afade=t=out:st={max(0, maxlen - 0.12)}:d=0.12"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", ",".join(chain), "-ar", "48000", "-ac", "2", str(out)], check=True)


def build(src_dir: Path, style_id: str):
    spec = yaml.safe_load((KIT / "styles" / style_id / "style.yaml").read_text())
    out_dir = KIT / "sfx" / style_id
    out_dir.mkdir(parents=True, exist_ok=True)
    kit = {}
    for role, entries in spec["sound"]["kit"].items():
        files = []
        for i, e in enumerate(entries):
            pitches = e.get("pitch", [0])
            for p in pitches:
                fn = f"{role}_{len(files) + 1}.wav"
                render(src_dir, e["src"], role, e.get("gain", -8), p, out_dir / fn)
                files.append(fn)
        kit[role] = files
    (out_dir / "kit.json").write_text(json.dumps({"style": style_id, "roles": kit, "license": "CC0-1.0 (uisfx, Kenney) + generated"}, indent=1))
    print(style_id, {k: len(v) for k, v in kit.items()})


if __name__ == "__main__":
    src = Path(sys.argv[1])
    ids = sys.argv[2:] or sorted(p.name for p in (KIT / "styles").iterdir() if (p / "style.yaml").exists())
    for sid in ids:
        build(src, sid)
