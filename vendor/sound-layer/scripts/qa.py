# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "soundfile", "pyloudnorm", "matplotlib"]
# ///
"""Check the finished video's sound with measurements, because you cannot
hear it. Needs ffmpeg on PATH. Exit code 1 if any check fails.

  qa.py out/final.mp4 [--audio audio]

Reads audio/mix.wav, audio/stems/*.wav, audio/mix-report.json and
audio/cues.json (written by mix.py). Writes audio/qa-report.json and
audio/qa.png (waveform, spectrogram and picture motion, every cue marked).

Checks
  picture   each cue's "visual" (cut | move | land) matches the picture:
            cut = a hard frame change within 1 frame, move = a motion peak
            within 3 frames, land = motion settling within 2 frames.
            Hero cues fail, support cues warn.
  offset    the MP4's audio lines up with mix.wav within 1 ms
  loudness  integrated loudness within 1 LU of target, true peak <= -1 dBTP,
            measured on the encoded MP4
  sync      each sound's peak sits within 1 frame (hero) / 2 frames
            (support) of where it was placed
  audible   each sound lifts its own band over music+voice by >= 1.5 dB
  voice     music at least 8 LU under the voice while it speaks
  music     no dip 12 LU below the music's median, except planned stops
  silence   no silence of 0.5 s or more outside "silence_ok"
"""
import argparse, json, os, re, subprocess, sys
import numpy as np
from scipy import signal
import soundfile as sf
import pyloudnorm as pyln

SR = 48000
BANDS = [(125, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]


def decode_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "2", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2)


def motion_curve(path, fps):
    w, h = 160, 90
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-an", "-vf", f"fps={fps},scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    m = np.zeros(len(fr)); m[1:] = np.mean(np.abs(np.diff(fr, axis=0)), axis=(1, 2))
    return m


def picture_check(kind, f, m):
    n = len(m)
    if f < 1 or f >= n: return False, "cue outside the video"
    if kind == "cut":
        lo, hi = max(1, f - 1), min(n, f + 2)
        i = lo + int(np.argmax(m[lo:hi]))
        base = np.median(m[max(1, f - 15):min(n, f + 15)]) + 1.0
        return m[i] > 4 * base and m[i] > 6.0, f"largest change at frame {i} ({m[i]:.1f} vs local {base:.1f})"
    if kind == "move":
        lo, hi = max(1, f - 3), min(n, f + 4)
        i = lo + int(np.argmax(m[lo:hi]))
        ok = m[i] >= m[max(1, i - 1)] and m[i] >= m[min(n - 1, i + 1)] and m[i] > 0.5
        return ok and abs(i - f) <= 3, f"motion peak at frame {i}"
    if kind == "land":
        pre = m[max(1, f - 15):max(2, f - 1)]
        if len(pre) == 0 or pre.max() < 0.5: return False, "no motion before the landing"
        thr = max(0.25, 0.05 * pre.max())            # moving has effectively stopped
        for i in range(max(1, f - 6), min(n, f + 7)):
            if m[i] <= thr and m[i - 1] > thr:
                return abs(i - f) <= 2, f"motion stops at frame {i}"
        return False, "motion does not stop near the cue"
    if kind == "appear":
        lo, hi = max(1, f - 1), min(n, f + 2)
        i = lo + int(np.argmax(m[lo:hi]))
        base = np.median(m[max(1, f - 15):min(n, f + 15)])
        return m[i] >= 0.3 and m[i] >= 3 * (base + 0.1), f"change at frame {i} ({m[i]:.2f} vs local {base:.2f})"
    return True, "no visual check"


def band_rms(x, lo, hi):
    lo = max(20.0, lo); hi = min(SR / 2 - 100, hi)
    if len(x) < 64 or hi <= lo * 1.05: return 0.0
    return float(np.sqrt(np.mean(signal.sosfilt(signal.butter(4, [lo, hi], "bandpass", fs=SR, output="sos"), x) ** 2)))


def loud(x, meter):
    if len(x) < int(0.4 * SR): return -70.0
    v = meter.integrated_loudness(x)
    return float(v) if np.isfinite(v) else -70.0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--audio", default="audio")
    a = ap.parse_args(); A = a.audio
    rep = json.load(open(os.path.join(A, "mix-report.json")))
    cues = json.load(open(rep.get("cues_file") or os.path.join(A, "cues.json")))
    fps, target = rep["fps"], rep["target_lufs"]
    mix = sf.read(os.path.join(A, "mix.wav"))[0]
    st = {k: sf.read(os.path.join(A, "stems", k + ".wav"))[0] for k in ("music", "voice", "sfx")}
    final = decode_audio(a.video)
    meter = pyln.Meter(SR)
    res = []                                   # (check, status, detail)

    def add(check, ok, detail, hard=True):
        res.append(dict(check=check, status="pass" if ok else ("FAIL" if hard else "warn"), detail=detail))

    # offset of the encoded audio against mix.wav
    mono_mix, mono_fin = mix.mean(axis=1), final.mean(axis=1)
    win = SR; lags = []
    energy = [np.sum(mono_mix[i:i + win] ** 2) for i in range(SR // 2, max(SR // 2 + 1, len(mono_mix) - win - SR // 2), SR // 2)]
    for k in np.argsort(energy)[-3:]:
        s = SR // 2 + int(k) * (SR // 2); r = mono_mix[s:s + win]
        R = min(12000, s)                                   # search +-250 ms
        d = mono_fin[s - R:s + win + R]
        if len(d) < len(r) + 2 * R: continue
        c = signal.correlate(d, r, mode="valid", method="fft"); lags.append(int(np.argmax(c)) - R)
    worst = max([abs(l) for l in lags], default=0)
    add("offset", worst <= 48, f"encoded audio vs mix.wav: worst {worst} samples ({worst / SR * 1000:.2f} ms), lags {lags}")

    # loudness on the encoded file
    I = loud(final, meter)
    tp = 20 * np.log10(np.max(np.abs(signal.resample_poly(final, 4, 1, axis=0))) + 1e-12)
    add("loudness", abs(I - target) <= 1.0, f"integrated {I:.2f} LUFS, target {target}")
    add("true peak", tp <= -1.0, f"{tp:.2f} dBTP (limit -1.0)")

    # picture match
    motion = motion_curve(a.video, fps)
    for c in cues["cues"]:
        if c.get("visual"):
            f = int(round(c.get("frame", c.get("t", 0) * fps)))
            ok, why = picture_check(c["visual"], f, motion)
            add(f"picture {c['id']}", ok, f"{c['visual']} at frame {f}: {why}", hard=c.get("weight") == "hero")

    # per event: sync and audibility from the stems
    sfx = st["sfx"].mean(axis=1); bed = (st["music"] + st["voice"]).mean(axis=1)
    n = max(1, int(0.002 * SR)); env = np.sqrt(np.convolve(sfx * sfx, np.ones(n) / n, mode="same"))
    for ev in rep["events"]:
        hero = ev["weight"] == "hero"; p = int(ev["peak_s"] * SR)
        if ev["align"] == "peak":
            lo, hi = max(0, p - int(0.06 * SR)), min(len(env), p + int(0.06 * SR))
            found = lo + int(np.argmax(env[lo:hi])); err = abs(found - p) / SR * fps
            add(f"sync {ev['id']}", err <= (1 if hero else 2), f"peak {err:.2f} frames from its cue")
        w0, w1 = int(ev["win_s"][0] * SR), min(len(sfx), int(ev["win_s"][1] * SR))
        best, band = -99.0, None
        fx_b = [band_rms(sfx[w0:w1], lo, hi) for lo, hi in BANDS]
        tot = sum(v * v for v in fx_b) + 1e-20
        for (lo, hi), e in zip(BANDS, fx_b):
            if e * e / tot < 0.1: continue                 # band must carry >= 10% of the sound
            b = max(band_rms(bed[w0:w1], lo, hi), 10 ** (-60 / 20))
            lift = 20 * np.log10(band_rms(bed[w0:w1] + sfx[w0:w1], lo, hi) / b + 1e-12)
            if lift > best: best, band = lift, (lo, hi)
        add(f"audible {ev['id']}", best >= 1.5, f"stands out by {best:.1f} dB in {band[0]}-{band[1]} Hz over music+voice" if band else "no energy")
        if hero:   # a hero hit must also stand out where most of its energy is
            k = int(np.argmax(fx_b)); lo, hi = BANDS[k]
            b = max(band_rms(bed[w0:w1], lo, hi), 10 ** (-60 / 20))
            ml = 20 * np.log10(band_rms(bed[w0:w1] + sfx[w0:w1], lo, hi) / b + 1e-12)
            add(f"hero body {ev['id']}", ml >= 3.0, f"main band {lo}-{hi} Hz lifted {ml:.1f} dB (needs 3)")

    # voice clarity and music continuity, 400 ms blocks every 100 ms
    step, blk = int(0.1 * SR), int(0.4 * SR)
    starts = range(0, len(bed) - blk, step)
    if np.any(st["voice"]) and np.any(st["music"]):
        gaps = []
        for s in starts:
            lv = loud(st["voice"][s:s + blk], meter)
            if lv > -40: gaps.append(lv - loud(st["music"][s:s + blk], meter))
        if gaps:
            g = float(np.median(gaps)); add("voice", g >= 8, f"music sits {g:.1f} LU under the voice (median while speaking)")
    if np.any(st["music"]):
        stops = [(c.get("t", c.get("frame", 0) / fps) - 1.5, c.get("t", c.get("frame", 0) / fps) + 0.5) for c in cues["cues"] if c.get("stop_before")]
        L3 = [(s / SR, loud(st["music"][s:s + 3 * SR], meter)) for s in range(0, len(bed) - 3 * SR, SR // 2)]
        if L3:
            med = float(np.median([l for _, l in L3]))
            dips = [t for t, l in L3 if l < med - 12 and not any(a0 <= t + 1.5 <= a1 for a0, a1 in stops) and t + 3 < len(bed) / SR - 1.5]
            add("music", not dips, f"median {med:.1f} LUFS short-term; unplanned dips at {[round(t, 1) for t in dips]}")

    # silence
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", a.video, "-vn", "-af", "silencedetect=noise=-50dB:d=0.5", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts_s = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends_s = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)] + [len(final) / SR]
    ok_spans = cues.get("silence_ok", [])
    bad = [(round(s, 2), round(e, 2)) for s, e in zip(starts_s, ends_s)
           if not any(s >= a0 - 0.1 and e <= a1 + 0.1 for a0, a1 in ok_spans)]
    add("silence", not bad, f"unplanned silence: {bad}" if bad else "none")

    # picture for the reviewer
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    t = np.arange(len(mono_fin)) / SR
    fig, ax = plt.subplots(3, 1, figsize=(14, 7.5), sharex=True, gridspec_kw=dict(height_ratios=[1, 2, 0.8]))
    ax[0].plot(t[::20], mono_fin[::20], lw=0.4, color="k"); ax[0].set_ylabel("final")
    ax[1].specgram(mono_fin, NFFT=1024, Fs=SR, noverlap=768, cmap="magma", vmin=-130); ax[1].set_ylim(0, 12000); ax[1].set_ylabel("Hz")
    ax[2].plot(np.arange(len(motion)) / fps, motion, color="tab:blue", lw=0.8); ax[2].set_ylabel("picture motion")
    for ev in rep["events"]:
        col = "red" if ev["weight"] == "hero" else "0.55"
        for k in range(3): ax[k].axvline(ev["peak_s"], color=col, lw=0.7, alpha=0.8)
        ax[0].text(ev["peak_s"], ax[0].get_ylim()[1], ev["id"], fontsize=6, rotation=90, va="top", ha="right")
    ax[2].set_xlabel("seconds"); fig.tight_layout(); png = os.path.join(A, "qa.png"); fig.savefig(png, dpi=80); plt.close(fig)

    fails = [r for r in res if r["status"] == "FAIL"]; warns = [r for r in res if r["status"] == "warn"]
    json.dump(dict(passed=not fails, results=res), open(os.path.join(A, "qa-report.json"), "w"), indent=1)
    for r in res: print(f"{r['status']:4s}  {r['check']:22s} {r['detail']}")
    print(f"\n{'PASSED' if not fails else 'FAILED'}: {len(fails)} failed, {len(warns)} warnings. Picture: {png}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
