# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "soundfile", "pyloudnorm"]
# ///
"""Build the whole sound layer from one cue sheet. Needs ffmpeg on PATH.

  mix.py audio/cues.json [--out audio]

Writes audio/mix.wav (48 kHz stereo master), audio/stems/{music,voice,sfx}.wav
at master scale, and audio/mix-report.json (every event: file, time, gain,
what limited it). Run `mix.py --schema` to print the cue sheet format.

What it does, in order:
  music: loop or trim to length, 5 ms fade-in, fade-out, a 2 s high-pass build
         before cues with "build", a 0.4 s dead stop before cues with
         "stop_before", ducking under the voice (default 10 dB, 80/250 ms)
  voice: placed and levelled
  sfx:   each cue's sound is placed so its peak lands on the cue. A sound is
         a library type ("hit": rotates through that type's defaults), a
         library id you picked with `sfx.py browse` ("hit/kenney-impact-
         metal-heavy-2"), a path to any audio file you chose yourself,
         "a+b" layers (peaks aligned, later layers -4 dB), or synth:pluck /
         synth:bell tuned by "note" (musical accents only, never for hits,
         clicks or whooshes). "pitch" shifts a cue by semitones.
         ("align": "peak"; "end" ends on the cue; "start" starts on it).
         Repeats rotate through the kit's files with seeded +-2% pitch.
         Gain is solved per event against the music+voice bed, in the
         sound's own band: +3.5 dB (hero +5), the 2-8 kHz lift capped at
         4 dB, the peak capped at 6 dB over the local bed peak (hero 8).
         Same sound and weight: gains within 2 dB of their median.
         Sounds within 0.15 s of the previous one: x0.6 (not hero hits,
         so a riser can peak on its hit).
  room:  every sound effect goes through one short shared room (0.6 s,
         -16 dB wet) so recordings from different places share a space.
  master: integrated loudness to the target (punchy -14, calm -18 LUFS),
         look-ahead true-peak limiter at -2 dBTP so the AAC encode stays
         under -1 dBTP.
"""
import argparse, json, os, subprocess, sys, zlib
import numpy as np
from scipy import signal
from scipy.ndimage import minimum_filter1d, uniform_filter1d
import soundfile as sf
import pyloudnorm as pyln

SR = 48000
SCHEMA = """{
  "fps": 30,                       // picture frame rate
  "duration_s": 15.0,              // film length
  "energy": "punchy",              // punchy | calm (sets loudness and lifts)
  "lufs": -14,                     // optional override of the master target
  "kit": "audio/kit",              // library built by sfx.py kit (catalog.json)
  "room": {"decay_s": 0.6, "wet_db": -16},   // optional; false = dry
  "music": {"file": "audio/music.wav", "start_s": 0, "loop": true,
            "fade_out_s": 1.0},    // optional
  "voice": [{"file": "audio/vo.wav", "start_s": 0.5}],   // optional
  "duck_db": 10,                   // optional
  "silence_ok": [[14.2, 15.0]],    // optional: planned silence, for qa.py
  "cues": [
    {"id": "logo", "frame": 120, "sound": "thump+tap", "weight": "hero",
     "align": "peak", "pan": 0.0, "visual": "land",
     "stop_before": true, "build": true},
    {"id": "build", "frame": 120, "sound": "riser/fs-123-tension-riser-1",
     "align": "peak", "weight": "support"},
    {"id": "push", "frame": 64, "sound": "whoosh", "weight": "support",
     "align": "peak", "pan": -0.3, "visual": "move"},
    {"id": "own", "t": 7.2, "sound": "audio/candidates/glitch/ov-1a2b3c4d.wav",
     "pitch": -2},
    {"id": "accent", "t": 9.5, "sound": "synth:pluck", "note": 64}
  ]
}
sound: type | type/id from sfx.py browse | file path | "a+b" layers.
Choose each sound yourself with `sfx.py browse --type <type> --like "..."`;
heroes: "hit+boom" (or "thump+tap" for soft), a "riser" or "reverse"
peaking on the same frame. Types: hit boom riser reverse transition whoosh
swish glitch ui click key tick tap pop thump paper chime shimmer zap.
frame or t (seconds); weight hero|support (default support); align
peak|end|start (default peak); pan -1..1 (clamped to +-0.6); visual
cut|move|land is what qa.py checks against the picture."""


def load(path, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, ch)


def lufs(x):
    x = np.atleast_2d(x.T).T
    if len(x) < int(0.5 * SR): return -70.0
    v = pyln.Meter(SR).integrated_loudness(x)
    return float(v) if np.isfinite(v) else -70.0


def true_peak(x):
    os4 = signal.resample_poly(x, 4, 1, axis=0)
    return float(20 * np.log10(np.max(np.abs(os4)) + 1e-12))


def db(v): return 20 * np.log10(v + 1e-12)
def undb(d): return 10 ** (d / 20)


def band_rms(x, lo, hi):
    lo = max(20.0, lo); hi = min(SR / 2 - 100, hi)
    if len(x) < 64 or hi <= lo * 1.05: return 0.0
    sos = signal.butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
    return float(np.sqrt(np.mean(signal.sosfilt(sos, x) ** 2)))


BANDS = [(125, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]


def band_levels(x):
    return np.array([band_rms(x, lo, hi) for lo, hi in BANDS])


def active_window(xs, pk):
    """Window over the sound's own body: from 10 ms before its peak until it
    falls 20 dB, kept between 40 and 150 ms. Short clicks are judged on
    their own length, not diluted over 150 ms."""
    n = max(1, int(0.005 * SR)); seg = xs[pk: pk + int(0.3 * SR)]
    env = np.sqrt(np.convolve(seg * seg, np.ones(n) / n, mode="same"))
    below = np.where(env < env.max() * 0.1)[0] if len(env) else []
    below = [i for i in below if i > np.argmax(env)]
    dur = np.clip((below[0] if below else len(env)) / SR, 0.04, 0.15)
    return max(0, pk - int(0.01 * SR)), pk + int(dur * SR)


def centroid(x):
    s = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return float((f * s).sum() / (s.sum() + 1e-20))


def peak_offset(x):
    n = max(1, int(0.002 * SR))
    env = np.sqrt(np.convolve(x * x, np.ones(n) / n, mode="same"))
    return int(np.argmax(env))


def synth(kind, note, seed):
    f = 440.0 * 2 ** ((note - 69) / 12)
    rng = np.random.default_rng(seed)
    if kind == "pluck":          # Karplus-Strong string
        n = int(0.9 * SR); d = max(2, int(round(SR / f)))
        buf = rng.uniform(-1, 1, d); out = np.zeros(n)
        for i in range(n):
            out[i] = buf[i % d]
            buf[i % d] = 0.996 * 0.5 * (buf[i % d] + buf[(i + 1) % d])
        out = signal.sosfilt(signal.butter(2, 6000, "lowpass", fs=SR, output="sos"), out)
    elif kind == "bell":         # two-operator FM bell
        t = np.arange(int(1.6 * SR)) / SR
        idx = 2.0 * np.exp(-t / 0.4)
        out = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 3.5 * f * t)) * np.exp(-t / 0.55)
    else:
        raise SystemExit(f"unknown synth sound: {kind}")
    out[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return out / (np.max(np.abs(out)) + 1e-12) * undb(-3)


class Kit:
    """Sounds from the library built by sfx.py. A cue's sound can be
    a type ("hit": rotates through that type's defaults in catalog.json, or
    all its files), a library id ("hit/kenney-impact-metal-heavy-2"), or a
    path to any audio file."""
    def __init__(self, root):
        self.root, self.count, self.cache = root, {}, {}
        p = os.path.join(root, "catalog.json")
        self.catalog = json.load(open(p)) if os.path.exists(p) else None

    def files(self, typ):
        if self.catalog and self.catalog["types"].get(typ, {}).get("defaults"):
            return [os.path.join(self.root, i + ".wav") for i in self.catalog["types"][typ]["defaults"]]
        d = os.path.join(self.root, typ)
        if not os.path.isdir(d): raise SystemExit(f"kit has no type '{typ}' in {self.root}")
        fs = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".wav"))
        if not fs: raise SystemExit(f"kit type '{typ}' is empty")
        return fs

    def resolve(self, token):
        if os.path.isfile(token): return [token]
        if "/" in token:
            f = os.path.join(self.root, token if token.endswith(".wav") else token + ".wav")
            if not os.path.isfile(f): raise SystemExit(f"no sound '{token}' in {self.root} (see sfx.py browse)")
            return [f]
        return self.files(token)

    def next(self, token, seed):
        fs = self.resolve(token)
        k = self.count.get(token, 0); self.count[token] = k + 1
        f = fs[k % len(fs)]
        if f not in self.cache:
            self.cache[f] = sf.read(f)[0].astype(np.float64) if f.endswith(".wav") else load(f, 1)[:, 0]
            if self.cache[f].ndim > 1: self.cache[f] = self.cache[f].mean(axis=1)
        x = self.cache[f]
        ratio = 1 + np.random.default_rng(seed).uniform(-0.02, 0.02)   # +-2% pitch
        n = int(len(x) / ratio)
        return np.interp(np.arange(n) * ratio, np.arange(len(x)), x), f


def build_event(cue, kit):
    seed = zlib.crc32(str(cue["id"]).encode())
    snd = cue["sound"]
    if snd.startswith("synth:"):
        x = synth(snd.split(":")[1], cue.get("note", 64), seed); return x, [snd]
    layers, used = [], []
    for i, typ in enumerate(snd.split("+")):
        y, f = kit.next(typ.strip(), seed + i)
        layers.append((y * (1.0 if i == 0 else undb(-4)), peak_offset(y))); used.append(f)
    pk = max(p for _, p in layers)
    n = max(pk - p + len(y) for y, p in layers)
    x = np.zeros(n)
    for y, p in layers: x[pk - p: pk - p + len(y)] += y      # peaks coincide
    if cue.get("pitch"):                                      # semitones, e.g. to sit in the music's key
        r = 2 ** (float(cue["pitch"]) / 12)
        x = np.interp(np.arange(int(len(x) / r)) * r, np.arange(len(x)), x)
    return x, used


def room(sfx, decay_s, wet_db, seed=7):
    """One short shared room for every sound effect, so recordings from
    different places sound like one scene: decorrelated stereo tail,
    12 ms pre-delay, 250 Hz-7 kHz, RT60 = decay_s."""
    rng = np.random.default_rng(seed)
    n = int(decay_s * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-6.91 * t / decay_s)[:, None]
    ir = signal.sosfilt(signal.butter(2, [250, 7000], "bandpass", fs=SR, output="sos"), ir, axis=0)
    ir = np.vstack([np.zeros((int(0.012 * SR), 2)), ir / np.sqrt(np.sum(ir ** 2, axis=0))])
    wet = np.stack([signal.fftconvolve(sfx.mean(axis=1), ir[:, ch])[: len(sfx)] for ch in (0, 1)], axis=1)
    return sfx + wet * undb(wet_db)


def one_pole(target, att_s, rel_s, rate=1000):
    """Smooth a control-rate gain curve: falls with att_s, rises with rel_s."""
    a_att, a_rel = np.exp(-1 / (att_s * rate)), np.exp(-1 / (rel_s * rate))
    out = np.empty_like(target); g = target[0]
    for i, v in enumerate(target):
        a = a_att if v < g else a_rel
        g = a * g + (1 - a) * v; out[i] = g
    return out


def to_audio_rate(ctrl, n, rate=1000):
    return np.interp(np.arange(n) / SR, np.arange(len(ctrl)) / rate, ctrl)


def hp_build(seg):
    """High-pass rising 40 -> 300 Hz across the segment, morphing smoothly."""
    cuts = np.geomspace(40, 300, 16)
    vers = [signal.sosfilt(signal.butter(2, c, "highpass", fs=SR, output="sos"), seg, axis=0) for c in cuts]
    pos = np.linspace(0, len(cuts) - 1, len(seg))
    k = np.minimum(pos.astype(int), len(cuts) - 2); w = (pos - k)[:, None]
    out = np.empty_like(seg)
    for j in range(len(cuts) - 1):
        m = k == j
        out[m] = (1 - w[m]) * vers[j][m] + w[m] * vers[j + 1][m]
    return out


def limiter(x, ceiling_db):
    os4 = signal.resample_poly(x, 4, 1, axis=0)
    pk = np.max(np.abs(os4), axis=1)
    pk = pk[: len(x) * 4].reshape(-1, 4).max(axis=1) if len(pk) >= len(x) * 4 else np.pad(pk, (0, len(x) * 4 - len(pk))).reshape(-1, 4).max(axis=1)
    need = np.minimum(1.0, undb(ceiling_db) / (pk + 1e-12))
    g = minimum_filter1d(need, size=int(0.010 * SR))
    g = uniform_filter1d(g, size=int(0.005 * SR))
    return x * g[:, None]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cues", nargs="?"); ap.add_argument("--out", default="audio")
    ap.add_argument("--schema", action="store_true")
    a = ap.parse_args()
    if a.schema or not a.cues: print(SCHEMA); return
    C = json.load(open(a.cues))
    fps, T = C["fps"], float(C["duration_s"]); N = int(round(T * SR))
    calm = C.get("energy", "punchy") == "calm"
    target = C.get("lufs", -18 if calm else -14)
    lift = {"support": 3.0 if calm else 3.5, "hero": 4.0 if calm else 5.0}
    cues = sorted(C["cues"], key=lambda c: c.get("t", c.get("frame", 0) / fps))
    for c in cues: c["time"] = float(c.get("t", c.get("frame", 0) / fps))

    # voice
    voice = np.zeros((N, 2))
    for v in C.get("voice", []):
        y = load(v["file"], 1)[:, 0]; s = int(v.get("start_s", 0) * SR)
        y = y[: max(0, N - s)]; voice[s:s + len(y)] += y[:, None]
    if np.any(voice): voice *= undb(-16 - lufs(voice))

    # music
    music = np.zeros((N, 2))
    ctrl = np.ones(int(T * 1000) + 1)                        # music gain, 1 kHz control rate
    if C.get("music"):
        m = C["music"]; y = load(m["file"], 2); s = int(m.get("start_s", 0) * SR)
        need = N - s
        if m.get("loop", False) and len(y) < need: y = np.tile(y, (need // len(y) + 1, 1))
        y = y[:need].copy(); music[s:s + len(y)] = y
        fi = int(0.005 * SR); music[s:s + fi] *= np.linspace(0, 1, fi)[:, None]
        fo = int(m.get("fade_out_s", 1.0) * SR)
        if fo: music[N - fo:] *= np.linspace(1, 0, fo)[:, None]
        music *= undb((-23 if calm else -20) - lufs(music))
        for c in cues:
            t = c["time"]
            if c.get("build"):
                a0, a1 = int(max(0, t - 2.0) * SR), int(t * SR)
                if a1 - a0 > SR // 10: music[a0:a1] = hp_build(music[a0:a1])
            if c.get("stop_before"):
                ctrl[int(max(0, t - 0.4) * 1000): int(t * 1000)] = np.minimum(ctrl[int(max(0, t - 0.4) * 1000): int(t * 1000)], undb(-24))
        if np.any(voice):
            r = SR // 1000
            vv = np.pad(voice[:, 0], (0, max(0, len(ctrl) * r - N)))[: len(ctrl) * r]
            vr = uniform_filter1d(np.sqrt(np.mean(vv.reshape(-1, r) ** 2, axis=1)), 50)   # 50 ms
            active = db(vr) > -45
            duck = np.where(active, undb(-C.get("duck_db", 10)), 1.0)
            ctrl = np.minimum(ctrl, one_pole(duck, 0.08, 0.25))
        ctrl = one_pole(ctrl, 0.02, 0.02)
        music *= to_audio_rate(ctrl, N)[:, None]
    bed = music + voice
    bed_mono = bed.mean(axis=1)

    # sound effects
    kit = Kit(C.get("kit", "audio/kit"))
    events = []
    for c in cues:
        x, used = build_event(c, kit)
        p = peak_offset(x)
        al = c.get("align", "peak")
        start = c["time"] - (p / SR if al == "peak" else len(x) / SR if al == "end" else 0.0)
        s = int(round(start * SR)); pkt = s + p
        xs = np.zeros(N); a0, a1 = max(0, s), min(N, s + len(x))
        if a1 <= a0:
            print(f"warning: cue {c['id']} falls outside the film, skipped", file=sys.stderr); continue
        xs[a0:a1] = x[a0 - s:a1 - s]
        w0, w1 = active_window(xs, pkt); w1 = min(N, w1)
        # audible = it stands out in at least one band that carries >= 10% of
        # its energy (partial masking). Solve the smallest gain that lifts the
        # easiest such band by the target.
        e_b = band_levels(xs[w0:w1]); m_b = np.maximum(band_levels(bed_mono[w0:w1]), undb(-60))
        share = e_b ** 2 / (np.sum(e_b ** 2) + 1e-20)
        weight = c.get("weight", "support")
        need = np.where(share >= 0.1, m_b * np.sqrt(10 ** (lift[weight] / 10) - 1) / (e_b + 1e-12), np.inf)
        if weight == "hero":     # a hero hit must stand out where most of its energy is
            k = int(np.argmax(share)); why = "main-band target (hero)"
        else:                    # support sounds: just clearly audible, in their easiest band
            k = int(np.argmin(need)); why = "best-band target"
        g = float(m_b[k] * np.sqrt(10 ** (lift[weight] / 10) - 1) / (e_b[k] + 1e-12))
        lo, hi = BANDS[k]
        bed_rms = float(np.sqrt(np.mean(bed_mono[w0:w1] ** 2))) if w1 > w0 else 0.0
        e28 = band_rms(xs[w0:w1], 2000, 8000)
        m28 = max(band_rms(bed_mono[w0:w1], 2000, 8000), bed_rms * undb(-20), undb(-60))
        if e28 > 0:
            cap = 9 if weight == "hero" else 6                       # 2-8 kHz lift cap, dB
            g28 = m28 * np.sqrt(10 ** (cap / 10) - 1) / e28
            if g28 < g: g, why = g28, "2-8 kHz cap"
        # local bed peak: +-0.15 s, or +-1 s for hero hits so a dead stop
        # before the hit doesn't clamp the hit it is there to set up
        reach = int((1.0 if weight == "hero" else 0.15) * SR)
        lw0, lw1 = max(0, pkt - reach), min(N, pkt + reach)
        bed_pk = max(np.max(np.abs(bed_mono[lw0:lw1])) if lw1 > lw0 else 0.0, undb(-26))
        gp = bed_pk * undb(8 if weight == "hero" else 6) / (np.max(np.abs(x)) + 1e-12)
        if gp < g: g, why = gp, "peak cap"
        events.append(dict(id=c["id"], sound=c["sound"], files=used, weight=weight, align=al,
                           cue_s=round(c["time"], 4), peak_s=round(pkt / SR, 4), start=s, x=x,
                           pan=float(np.clip(c.get("pan", 0.0), -0.6, 0.6)), gain_db=float(db(g)), limited_by=why,
                           band_hz=[int(lo), int(hi)], win_s=[round(w0 / SR, 4), round(w1 / SR, 4)],
                           visual=c.get("visual")))
    groups = {}
    for ev in events: groups.setdefault((ev["sound"], ev["weight"]), []).append(ev["gain_db"])
    last_peak = -9.0
    for ev in sorted(events, key=lambda e: e["peak_s"]):
        med = float(np.median(groups[(ev["sound"], ev["weight"])]))
        ev["gain_db"] = float(np.clip(ev["gain_db"], med - 2, med + 2))
        if ev["peak_s"] - last_peak < 0.15 and ev["weight"] != "hero": ev["gain_db"] += db(0.6); ev["limited_by"] += " + cluster x0.6"
        last_peak = ev["peak_s"]
    sfx = np.zeros((N, 2))
    for ev in events:
        x = ev.pop("x") * undb(ev["gain_db"]); s = ev.pop("start")
        a0, a1 = max(0, s), min(N, s + len(x))
        th = (ev["pan"] + 1) * np.pi / 4
        sfx[a0:a1, 0] += x[a0 - s:a1 - s] * np.cos(th); sfx[a0:a1, 1] += x[a0 - s:a1 - s] * np.sin(th)
        ev["gain_db"] = round(ev["gain_db"], 2)
    rm = C.get("room", {})
    if rm is not False and np.any(sfx):
        sfx = room(sfx, float(rm.get("decay_s", 0.6)), float(rm.get("wet_db", -16)))

    # master
    mix = music + voice + sfx
    gain = undb(target - lufs(mix)); out = mix * gain
    for _ in range(6):
        out = limiter(out, -2.0)
        L = lufs(out)
        if abs(L - target) <= 0.3 and true_peak(out) <= -1.95: break
        gain *= undb(target - L); out = mix * gain
    else:
        # never converged (e.g. a few short sounds and no music can't reach
        # the target): never ship unlimited audio, qa.py reports the loudness
        out = limiter(limiter(out, -2.0), -2.0)
    os.makedirs(os.path.join(a.out, "stems"), exist_ok=True)
    sf.write(os.path.join(a.out, "mix.wav"), out.astype(np.float32), SR, subtype="PCM_24")
    for name, st in (("music", music), ("voice", voice), ("sfx", sfx)):
        sf.write(os.path.join(a.out, "stems", name + ".wav"), (st * gain).astype(np.float32), SR, subtype="FLOAT")
    rep = dict(cues_file=os.path.abspath(a.cues), fps=fps, duration_s=T, target_lufs=target, master_lufs=round(lufs(out), 2),
               master_true_peak_db=round(true_peak(out), 2), master_gain_db=round(float(db(gain)), 2),
               events=events)
    json.dump(rep, open(os.path.join(a.out, "mix-report.json"), "w"), indent=1)
    print(f"mix.wav  {rep['master_lufs']} LUFS  TP {rep['master_true_peak_db']} dBTP  events {len(events)}")
    for ev in events:
        print(f"  {ev['id']:12s} {ev['sound']:14s} {ev['weight']:7s} peak {ev['peak_s']:7.3f}s  gain {ev['gain_db']:6.1f} dB  ({ev['limited_by']})")


if __name__ == "__main__":
    main()
