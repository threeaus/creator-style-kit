# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "soundfile", "matplotlib"]
# ///
"""Build, browse and extend the sound library. Needs ffmpeg on PATH.

  sfx.py kit [--manifest library.json] [--out audio/kit]
      Download the pinned CC0 library (Kenney packs + hand-checked Freesound
      recordings), prepare every sound and write <out>/catalog.json and
      <out>/CREDITS.md. Sounds land in <out>/<type>/<id>.wav.
  sfx.py browse --type hit [--like "metal heavy"] [--short|--long]
                [--bright|--dark] [--n 12] [--kit audio/kit]
      Pick sounds yourself: ranks the catalog for one type, prints one line
      per sound (id, length, attack, brightness, tags) and writes a
      waveform + spectrogram sheet of the shortlist to audio/browse.png.
      Put the id you choose in a cue: "sound": "hit/kenney-impact-metal-heavy-2".
  sfx.py search "laptop key press" --type key [--n 6] [--out audio/candidates]
      Nothing in the library fits: search CC0 recordings on Freesound
      through Openverse (no key), download, prepare and judge them.
  sfx.py add FILE [FILE ...] --type key [--tags "soft wood"] [--credit "..."]
      Add prepared or raw files (your own, or ones from search) to the
      library so mix.py, browse and CREDITS.md know them.
  sfx.py analyze FILE [FILE ...] --type key [--out audio/sfx]
      Prepare and judge local files without adding them.
  sfx.py sheet FILE [FILE ...] [--png audio/sheet.png]

Prepare = cut to the strongest event(s), high-pass, low-pass, 5 ms fades,
mono, 48 kHz, peak at -3 dBFS. Judge = reject boomy (>50% energy below
150 Hz), hissy, noise-like (spectral flatness), soft attacks on hits,
steady noise or clicks inside whooshes, risers that don't build. Every
prepared file gets a .json sidecar with its measurements.
"""
import argparse, concurrent.futures, io, json, os, re, shutil, subprocess, sys, urllib.parse, urllib.request, zipfile
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
UA = "sound-layer/1.0 (motion video sound design)"
HERE = os.path.dirname(os.path.abspath(__file__))

# win: (min_s, max_s) length of the kept event.
# kind: transient | swell | tonal | riser (builds into its peak) | glitch
TYPES = {
    "click":      dict(kind="transient", win=(0.03, 0.20), hp=200, lp=12000, hi_max=0.5, about="mouse, switch, button, latch"),
    "key":        dict(kind="transient", win=(0.05, 0.15), hp=200, lp=11000, about="keyboard key"),
    "tick":       dict(kind="transient", win=(0.03, 0.15), hp=300, lp=12000, hi_max=0.55, about="small counter tick, scroll notch"),
    "tap":        dict(kind="transient", win=(0.06, 0.60), hp=100, lp=12000, hi_max=0.55, about="light impact: glass, wood, metal, plastic, chip"),
    "pop":        dict(kind="transient", win=(0.05, 0.40), hp=150, lp=12000, about="element pops in, bubble, cork"),
    "thump":      dict(kind="transient", win=(0.12, 1.00), hp=35,  lp=8000, allow_low=True, about="soft heavy landing, body"),
    "hit":        dict(kind="transient", win=(0.20, 4.00), hp=28,  lp=15000, allow_low=True, allow_sub=True, rise_max=60, layered=True, min_s=0.35, about="hero impact: cinematic hit, metal, punch, explosion"),
    "boom":       dict(kind="transient", win=(0.40, 4.00), hp=22,  lp=9000, allow_low=True, allow_sub=True, rise_max=80, layered=True, min_s=0.4, about="sub drop, low boom under a hit"),
    "paper":      dict(kind="swell",     win=(0.12, 0.70), hp=200, lp=12000, noise_ok=True, about="page, card, book"),
    "swish":      dict(kind="swell",     win=(0.15, 0.70), hp=150, lp=12000, noise_ok=True, about="cloth, card slide, blade, small fast move"),
    "whoosh":     dict(kind="swell",     win=(0.25, 1.20), hp=100, lp=14000, noise_ok=True, about="object flies past"),
    "transition": dict(kind="swell",     win=(0.60, 3.00), hp=50,  lp=15000, noise_ok=True, allow_low=True, spiky_max=4.0, about="full-frame scene change, deep whoosh"),
    "riser":      dict(kind="riser",     win=(1.00, 6.00), hp=40,  lp=15000, noise_ok=True, allow_low=True, about="tension build that peaks on the hit"),
    "reverse":    dict(kind="riser",     win=(0.40, 3.00), hp=60,  lp=15000, noise_ok=True, allow_low=True, about="reverse cymbal / suck-in that ends on the cue"),
    "glitch":     dict(kind="glitch",    win=(0.06, 1.50), hp=80,  lp=16000, noise_ok=True, hi_max=0.7, designed_end=True, about="digital stutter, data, static burst"),
    "ui":         dict(kind="tonal",     win=(0.04, 0.90), hp=200, lp=15000, hi_max=0.6, designed_end=True, about="interface blip: confirm, select, toggle, error, open"),
    "zap":        dict(kind="tonal",     win=(0.06, 1.50), hp=120, lp=15000, noise_ok=True, hi_max=0.6, designed_end=True, about="sci-fi laser, power-up, phaser"),
    "chime":      dict(kind="tonal",     win=(0.25, 2.50), hp=200, lp=14000, hi_max=0.6, about="bell, ding, glass ping"),
    "shimmer":    dict(kind="tonal",     win=(0.40, 3.50), hp=300, lp=16000, hi_max=0.75, noise_ok=True, about="sparkle, magic, twinkle on a reveal"),
}


def load(path):
    """Decode any audio file to mono float32 at 48 kHz with ffmpeg."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def envelope(y, win_s=0.004):
    n = max(1, int(win_s * SR))
    return np.sqrt(np.convolve(y * y, np.ones(n) / n, mode="same"))


def event_span(y, t):
    """(a, b) of the strongest event. Never pad into neighbouring audio: a
    short real sound stays short."""
    hi_len = int(t["win"][1] * SR)
    if t["kind"] == "riser":
        env = envelope(y, 0.03)
        p = int(np.argmax(env)); thr = env[p] * 10 ** (-30 / 20)
        a = p
        while a > 0 and env[a - 1] > thr and p - a < hi_len - int(0.4 * SR): a -= 1
        b = p
        while b < len(y) - 1 and env[b + 1] > env[p] * 0.1 and b - p < int(0.6 * SR): b += 1
        return a, b
    if t["kind"] == "swell":
        env = envelope(y, 0.02)
        p = int(np.argmax(env)); thr = env[p] * 0.1
        a = b = p
        # grow towards the louder side until both edges are 20 dB down
        while b - a < hi_len:
            left = env[a - 1] if a > 0 else 0.0
            right = env[b + 1] if b < len(y) - 1 else 0.0
            if left <= thr and right <= thr: break
            if left >= right: a -= 1
            else: b += 1
        return a, b
    fine = envelope(y, 0.002)      # onset
    smooth = envelope(y, 0.015)    # tail and second hits, smooth over low cycles
    p = int(np.argmax(fine)); ps = smooth[p]
    a = p
    while a > 0 and fine[a] > fine[p] * 0.1 and p - a < int(0.05 * SR): a -= 1
    a = max(0, a - int(0.005 * SR))
    tail = ps * 10 ** (-40 / 20)
    b, low = p, ps
    while b < len(y) - 1 and smooth[b] > tail and b - a < hi_len:
        low = min(low, smooth[b])
        # a second hit: the level climbs well above the lowest point reached
        # since the peak. Stop at that dip. Glitches are many hits by design.
        if t["kind"] != "glitch" and not t.get("layered") and b - p > int(0.01 * SR) and smooth[b] > max(4 * low, 0.1 * ps):
            b = p + int(np.argmin(smooth[p:b])); break
        b += 1
    return a, b


def cut_events(y, t, k=1):
    """Up to k separate events of one file, in time order. Each must reach
    a quarter (-12 dB) of the strongest one's peak."""
    y = y.copy(); out = []; first = None
    for _ in range(k):
        pk = np.max(np.abs(y)) if len(y) else 0.0
        if pk <= 1e-6 or (first is not None and pk < first * 0.25): break
        a, b = event_span(y, t)
        if b - a < int(0.01 * SR): break
        out.append((a, y[a:b].copy()))
        first = first or pk
        m = int(0.05 * SR); y[max(0, a - m):b + m] = 0.0
    return sorted(out, key=lambda e: e[0])


def clean(x, t):
    sos_hp = signal.butter(4, t["hp"], "highpass", fs=SR, output="sos")
    sos_lp = signal.butter(4, min(t["lp"], SR / 2 - 100), "lowpass", fs=SR, output="sos")
    x = signal.sosfilt(sos_lp, signal.sosfilt(sos_hp, x))
    f = min(int(0.005 * SR), len(x) // 4)
    # designed blips often stop on purpose: a 20 ms fade instead of a click
    fo = min(int((0.02 if t.get("designed_end") else 0.005) * SR), len(x) // 4)
    if f > 0:
        x[:f] *= np.linspace(0, 1, f)
        x[-fo:] *= np.linspace(1, 0, fo)
    if t.get("layered"):
        # designed hits ring for seconds: a long tail is cut at the window
        # and faded over its last 30% so it still decays naturally
        e = envelope(x, 0.01); edge = max(1, len(x) // 10)
        if e[-edge:].max() > e.max() * 0.1:
            n = int(len(x) * 0.3); x[-n:] *= np.cos(np.linspace(0, np.pi / 2, n)) ** 2
    pk = np.max(np.abs(x)) + 1e-12
    return x * (10 ** (-3 / 20) / pk)


def measure(x, t):
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    tot = spec.sum() + 1e-20
    env = envelope(x, 0.002)
    p = int(np.argmax(env))
    above10 = np.where(env[:p + 1] >= 0.1 * env[p])[0]
    above90 = np.where(env[:p + 1] >= 0.9 * env[p])[0]
    rise = (above90[0] - above10[0]) / SR * 1000 if len(above10) and len(above90) else 0.0
    # flatness inside the pass band only, with a floor, so filtered-out bins
    # don't drive the geometric mean to zero
    band = spec[(fr >= max(t["hp"], 100)) & (fr <= t["lp"])]
    band = np.maximum(band, band.max() * 1e-6 + 1e-20)
    flat = float(np.exp(np.mean(np.log(band))) / np.mean(band))
    pre = env[: max(1, int(0.003 * SR))]
    env10 = envelope(x, 0.01)
    edge = max(int(0.005 * SR), len(x) // 10)
    db = lambda v: float(20 * np.log10(v / (env10.max() + 1e-12) + 1e-12))
    env30 = envelope(x, 0.03)
    # tonal sounds: strongest spectral line, as a MIDI note, for tuning to music
    peak_bin = int(np.argmax(spec * (fr > 80)))
    tonal = float(spec[peak_bin] / (np.mean(spec[max(0, peak_bin - 40):peak_bin + 40]) + 1e-20))
    note = round(69 + 12 * np.log2(fr[peak_bin] / 440.0), 1) if fr[peak_bin] > 0 and tonal > 8 else None
    q = max(1, len(x) // 4)
    build = 20 * np.log10((env30[-q:].mean() + 1e-12) / (env30[: 2 * q].mean() + 1e-12))
    return dict(
        build_db=round(float(build), 1),
        start_db=round(db(env10[:edge].max()), 1),
        end_db=round(db(env10[-edge:].max()), 1),
        spikiness=round(float(env.max() / (env30.max() + 1e-12)), 2),
        dur_s=round(len(x) / SR, 3),
        peak_offset_s=round(p / SR, 4),
        rise_ms=round(float(rise), 1),
        centroid_hz=int((fr * spec).sum() / tot),
        below150=round(float(spec[fr < 150].sum() / tot), 3),
        above6k=round(float(spec[fr > 6000].sum() / tot), 3),
        flatness=round(flat, 3),
        note=note,
        start_floor_db=round(float(20 * np.log10(np.max(pre) / (env[p] + 1e-12) + 1e-12)), 1),
    )


def judge(m, t):
    why = []
    if m["below150"] > 0.5 and not t.get("allow_low"): why.append("boomy")
    if m["below150"] > 0.85 and not t.get("allow_sub"): why.append("no body above 150 Hz (inaudible on phones)")
    if m["above6k"] > t.get("hi_max", 0.4): why.append("hissy")
    if m["flatness"] > 0.35 and not t.get("noise_ok"): why.append("noise-like")
    if t["kind"] == "transient" and m["rise_ms"] > t.get("rise_max", 25): why.append("soft attack")
    if t["kind"] == "swell":
        if max(m["start_db"], m["end_db"]) > -12: why.append("no rise and fall (steady noise)")
        if m["spikiness"] > t.get("spiky_max", 2.5): why.append("clicks inside")
    elif t["kind"] == "riser":
        if m["start_db"] > -12: why.append("starts loud (no build)")
        if m["peak_offset_s"] < 0.7 * m["dur_s"]: why.append("peak too early (no build)")
        if m["spikiness"] > 3: why.append("clicks inside")
        if m["build_db"] < 6: why.append("doesn't grow (last quarter < 6 dB over first half)")
    elif not t.get("designed_end"):
        if m["end_db"] > -20: why.append("cut before it decays")
    if m["dur_s"] < t.get("min_s", t["win"][0] * 0.5): why.append("too short")
    if t.get("layered") and m["build_db"] > -6: why.append("doesn't decay (a hit must die away)")
    return why


def prepare_audio(y, typ, dst, meta=None):
    t = TYPES[typ]
    x = clean(y, t)
    m = measure(x, t)
    why = judge(m, t)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    sf.write(dst, x.astype(np.float32), SR, subtype="PCM_24")
    side = dict(type=typ, file=dst, verdict="ok" if not why else "reject: " + ", ".join(why), **m)
    if meta: side["source"] = meta
    with open(dst[:-4] + ".json", "w") as fh: json.dump(side, fh, indent=1)
    return side


def prepare(src, typ, out_dir, name=None, meta=None, k=1):
    """Prepare up to k events of one file. Returns one sidecar per event."""
    name = name or slug(os.path.splitext(os.path.basename(src))[0])
    evs = cut_events(load(src), TYPES[typ], k)
    sides = []
    for i, (_, y) in enumerate(evs):
        nm = name if len(evs) == 1 and k == 1 else f"{name}-{i + 1}"
        sides.append(prepare_audio(y, typ, os.path.join(out_dir, nm + ".wav"), meta))
    return sides


def slug(s):
    s = re.sub(r"([a-z])([A-Z])", r"\1-\2", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def fetch(url, dst):
    """Download to dst. Writes to a .part file first, so an interrupted run
    never leaves a truncated file that a rerun would take as done."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dst + ".part", "wb") as fh:
        fh.write(r.read())
    os.replace(dst + ".part", dst)


def fetch_all(jobs, workers=16):
    """Download (url, dst) pairs in parallel, skipping files already there.
    Returns {dst: error} for the ones that failed."""
    todo = [(u, d) for u, d in jobs if not os.path.exists(d)]
    if not todo: return {}
    print(f"downloading {len(todo)} files ({len(jobs) - len(todo)} already here)", flush=True)
    errors, done = {}, 0
    def one(job):
        u, d = job
        os.makedirs(os.path.dirname(d), exist_ok=True)
        try: fetch(u, d)
        except Exception as ex: return d, ex
        return d, None
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        for d, err in ex.map(one, todo):
            done += 1
            if err is not None: errors[d] = err
            if done % 100 == 0 or done == len(todo): print(f"  {done}/{len(todo)}", flush=True)
    return errors


def openverse(query, n, page=1):
    q = urllib.parse.urlencode(dict(q=query, license="cc0", source="freesound",
                                    page_size=n, page=page, filter_dead="true"))
    req = urllib.request.Request("https://api.openverse.org/v1/audio/?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["results"]


def line(s):
    return (f"{os.path.basename(s['file']):40s} {s['dur_s']:5.2f}s rise {s['rise_ms']:5.1f}ms "
            f"centroid {s['centroid_hz']:5d}Hz <150 {s['below150']*100:3.0f}% >6k {s['above6k']*100:3.0f}% "
            f"flat {s['flatness']:.2f} -> {s['verdict']}")


def sheet(files, out_png, labels=None):
    """One row per prepared sound: waveform and spectrogram, for visual review."""
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    files = [f for f in files if f.endswith(".wav")]
    if not files: return
    fig, axes = plt.subplots(len(files), 2, figsize=(11, 1.25 * len(files) + 0.4), squeeze=False,
                             gridspec_kw=dict(width_ratios=[1, 2]))
    for i, (row, f) in enumerate(zip(axes, files)):
        x, _ = sf.read(f)
        side = json.load(open(f[:-4] + ".json")) if os.path.exists(f[:-4] + ".json") else {}
        t = np.arange(len(x)) / SR
        row[0].plot(t, x, lw=0.5, color="k"); row[0].set_xlim(0, t[-1] if len(t) else 1); row[0].set_yticks([])
        title = labels[i] if labels else f"{os.path.basename(f)}  {side.get('verdict','')}"
        row[0].set_title(title, fontsize=7, loc="left")
        row[1].specgram(x, NFFT=512, Fs=SR, noverlap=384, cmap="magma", vmin=-120)
        row[1].set_ylim(0, 12000); row[1].set_yticks([150, 2000, 6000, 12000]); row[1].tick_params(labelsize=6)
        row[1].set_title(f"{side.get('dur_s','?')} s  centroid {side.get('centroid_hz','?')} Hz  <150 {side.get('below150','?')}  >6k {side.get('above6k','?')}  flat {side.get('flatness','?')}", fontsize=7, loc="left")
    fig.tight_layout(); os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True); fig.savefig(out_png, dpi=90); plt.close(fig)
    print(out_png)


# ---------------------------------------------------------------- library

STOP = {"wav", "mp3", "aif", "aiff", "flac", "ogg", "sfx", "fx", "sound", "sounds", "the", "and", "of", "by"}


def words(s):
    return [w for w in re.split(r"[^a-z0-9]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", s or "").lower())
            if w and not w.isdigit() and len(w) > 1 and w not in STOP]


def catalog_entry(side, root, tags, credit, default=False):
    m = {k: side[k] for k in ("dur_s", "peak_offset_s", "rise_ms", "centroid_hz", "below150", "above6k", "flatness", "note")}
    rel = os.path.relpath(side["file"], root).replace(os.sep, "/")   # same ids on Windows
    return dict(id=rel[:-4], type=side["type"], file=rel, tags=sorted(set(tags)), credit=credit,
                default=default, **m)


def write_catalog(root, entries, credits_head, credit_lines):
    entries = sorted(entries, key=lambda e: e["id"])
    by_type = {}
    for e in entries: by_type.setdefault(e["type"], []).append(e)
    cat = dict(note="Built by sfx.py. Pick sounds with `sfx.py browse --type <type>`.",
               types={k: dict(about=TYPES[k]["about"], count=len(by_type.get(k, [])),
                              defaults=[e["id"] for e in by_type.get(k, []) if e["default"]]) for k in TYPES},
               sounds=entries)
    with open(os.path.join(root, "catalog.json"), "w") as fh: json.dump(cat, fh, indent=1)
    with open(os.path.join(root, "CREDITS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(credits_head + [""] + sorted(set(credit_lines))) + "\n")


def read_catalog(root):
    p = os.path.join(root, "catalog.json")
    if not os.path.exists(p): raise SystemExit(f"no {p}: run `sfx.py kit` first")
    return json.load(open(p))


def build_library(manifest, out):
    lib = json.load(open(manifest))
    raw_dir = os.path.join(out, "_raw"); os.makedirs(raw_dir, exist_ok=True)
    defaults = set(lib.get("defaults", []))
    entries, credits, total, rejected = [], [], 0, 0
    for typ in TYPES:                   # rebuild from scratch, but keep sounds added with `sfx.py add`
        d = os.path.join(out, typ)
        if os.path.isdir(d):
            for f in os.listdir(d):
                if not f.startswith("own-"): os.remove(os.path.join(d, f))
    zpath_of = lambda pack: os.path.join(raw_dir, os.path.basename(pack["url"]))
    raw_of = lambda it: os.path.join(raw_dir, "freesound", f"{it['id']}.mp3")
    failed = fetch_all([(p["url"], zpath_of(p)) for p in lib.get("packs", [])] +
                       [(it["url"], raw_of(it)) for it in lib.get("freesound", [])])
    for pack in lib.get("packs", []):
        zpath = zpath_of(pack)
        try:
            if zpath in failed: raise failed[zpath]
            z = zipfile.ZipFile(zpath)
        except Exception as ex:
            print(f"skip pack {pack['name']}: {ex}", file=sys.stderr); continue
        rules = [(re.compile(r, re.I), typ, tags) for r, typ, tags in pack["map"]]
        n_pack = 0
        for member in sorted(z.namelist()):
            if not re.search(r"\.(ogg|wav)$", member, re.I) or "/__MACOSX" in member: continue
            stem = os.path.splitext(os.path.basename(member))[0]
            rule = next(((typ, tags) for rx, typ, tags in rules if rx.search(stem)), None)
            if not rule or rule[0] == "skip": continue
            typ, tags = rule
            src = os.path.join(raw_dir, pack["name"], os.path.basename(member))
            if not os.path.exists(src):
                os.makedirs(os.path.dirname(src), exist_ok=True)
                with z.open(member) as fi, open(src, "wb") as fo: fo.write(fi.read())
            name = f"kenney-{pack['name']}-{slug(stem)}"
            for side in prepare(src, typ, os.path.join(out, typ), name, dict(pack=pack["name"], file=member)):
                total += 1
                if side["verdict"] != "ok": rejected += 1; os.remove(side["file"]); os.remove(side["file"][:-4] + ".json"); continue
                e = catalog_entry(side, out, words(stem) + tags + ["kenney", pack["name"]], pack["credit"])
                e["default"] = e["id"] in defaults; entries.append(e); n_pack += 1
        credits.append(f"- {pack['credit']}, {pack['license'].upper()}, {pack['landing']}")
        print(f"{pack['name']:18s} {n_pack} sounds")
    for it in lib.get("freesound", []):
        raw = raw_of(it)
        if raw in failed or not os.path.exists(raw):
            print("skip", it["title"], failed.get(raw, "not downloaded"), file=sys.stderr); continue
        name = f"fs-{it['id']}-{slug(it['title'])[:28]}".rstrip("-")
        try:
            sides = prepare(raw, it["type"], os.path.join(out, it["type"]), name, it, k=it.get("k", 1))
        except Exception as ex:          # e.g. the host sent an error page instead of audio
            print("skip", it["title"], ex, file=sys.stderr); os.remove(raw); continue
        keep = it.get("keep")
        for i, side in enumerate(sides):
            total += 1
            if side["verdict"] != "ok" or (keep is not None and i not in keep):
                rejected += 1; os.remove(side["file"]); os.remove(side["file"][:-4] + ".json"); continue
            credit = f"\"{it['title']}\" by {it['creator']}"
            e = catalog_entry(side, out, words(it["title"]) + it.get("tags", []) + ["freesound"], credit)
            e["default"] = e["id"] in defaults; entries.append(e)
            credits.append(f"- {e['id']}: {credit}, {it['license'].upper()}, {it['landing']}")
    for e in read_added(out):           # sounds added with `sfx.py add` survive a rebuild
        if os.path.exists(os.path.join(out, e["file"])): entries.append(e); credits.append(f"- {e['id']}: {e['credit']}")
    write_catalog(out, entries, ["# Sound credits", "",
                                 "Kenney packs and Freesound recordings are CC0 (public domain). Credit is not required but given.", ""], credits)
    print(f"library: {len(entries)} sounds in {len(set(e['type'] for e in entries))} types "
          f"({rejected} of {total} cut events rejected by the checks) -> {out}/catalog.json")
    print("\nPick every sound yourself: sfx.py browse --type <type> --like \"<material, weight, mood>\",\n"
          "look at audio/browse.png and put the chosen id in the cue (\"sound\": \"hit/<id>\").\n"
          "A bare type uses the defaults. Nothing fits? Find one yourself: sfx.py search, or any\n"
          "recording whose licence allows it, then sfx.py add FILE --type <type> --credit \"...\".\n"
          "Types: " + ", ".join(f"{k} ({sum(e['type'] == k for e in entries)})" for k in TYPES))


def read_added(root):
    p = os.path.join(root, "added.json")
    return json.load(open(p)) if os.path.exists(p) else []


def add_files(files, typ, root, tags, credit):
    added = read_added(root); cat = read_catalog(root)
    entries = cat["sounds"]; ids = {e["id"] for e in entries}
    for f in files:
        meta = None
        if f.endswith(".wav") and os.path.exists(f[:-4] + ".json"):
            meta = json.load(open(f[:-4] + ".json")).get("source")
        if not credit and meta and meta.get("creator"):
            credit_ = f"\"{meta.get('title')}\" by {meta.get('creator')}, {str(meta.get('license', '')).upper()}, {meta.get('landing', '')}"
        else:
            credit_ = credit or "added by hand (state the source and licence in --credit)"
        for side in prepare(f, typ, os.path.join(root, typ), "own-" + slug(os.path.splitext(os.path.basename(f))[0]), meta):
            print(line(side))
            e = catalog_entry(side, root, tags + words(os.path.splitext(os.path.basename(f))[0]) + ["own"], credit_)
            entries = [x for x in entries if x["id"] != e["id"]]; added = [x for x in added if x["id"] != e["id"]]
            entries.append(e); added.append(e)
            if side["verdict"] != "ok":
                print(f"  note: kept although the checks say {side['verdict']}; look at it with sfx.py sheet")
    with open(os.path.join(root, "added.json"), "w") as fh: json.dump(added, fh, indent=1)
    head = open(os.path.join(root, "CREDITS.md"), encoding="utf-8").read().split("\n\n")[0:2]
    lines = [l for l in open(os.path.join(root, "CREDITS.md"), encoding="utf-8").read().splitlines() if l.startswith("- ")]
    write_catalog(root, entries, "\n\n".join(head).splitlines(), lines + [f"- {e['id']}: {e['credit']}" for e in added])


def browse(root, typ, like, n, length, tone, png):
    cat = read_catalog(root)
    pool = [e for e in cat["sounds"] if e["type"] == typ]
    if not pool: raise SystemExit(f"no sounds of type '{typ}'. Types: " + ", ".join(k for k, v in cat["types"].items() if v["count"]))
    q = words(like or "")
    def score(e):
        hay = " ".join(e["tags"] + [e["id"]])
        s = sum(2 if w in e["tags"] else 1 if w in hay else 0 for w in q)
        if length == "short": s -= e["dur_s"]
        if length == "long": s += e["dur_s"]
        if tone == "bright": s += e["centroid_hz"] / 4000
        if tone == "dark": s -= e["centroid_hz"] / 4000
        return (s, e["default"])
    pool.sort(key=score, reverse=True)
    shown = pool[:n]
    print(f"{typ}: {TYPES[typ]['about']}  ({len(pool)} in library, showing {len(shown)})")
    print(f"{'id':52s} {'len':>5s} {'rise':>6s} {'bright':>7s} {'note':>5s}  tags")
    for e in shown:
        note = "" if e.get("note") is None else f"{e['note']:.0f}"
        mark = "*" if e["default"] else " "
        tags = " ".join(t for t in e["tags"] if t not in ("kenney", "freesound"))[:60]
        print(f"{mark}{e['id']:51s} {e['dur_s']:5.2f} {e['rise_ms']:5.0f}ms {e['centroid_hz']:6d}Hz {note:>5s}  {tags}")
    print("* = default (used when a cue names only the type)")
    sheet([os.path.join(root, e["file"]) for e in shown], png, labels=[e["id"] for e in shown])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("kit", "library"):
        k = sub.add_parser(name); k.add_argument("--manifest", default=os.path.join(HERE, "library.json")); k.add_argument("--out", default="audio/kit")
    b = sub.add_parser("browse"); b.add_argument("--type", required=True, choices=TYPES); b.add_argument("--like", default="")
    b.add_argument("--n", type=int, default=12); b.add_argument("--kit", default="audio/kit"); b.add_argument("--png", default="audio/browse.png")
    g = b.add_mutually_exclusive_group(); g.add_argument("--short", dest="length", action="store_const", const="short"); g.add_argument("--long", dest="length", action="store_const", const="long")
    g = b.add_mutually_exclusive_group(); g.add_argument("--bright", dest="tone", action="store_const", const="bright"); g.add_argument("--dark", dest="tone", action="store_const", const="dark")
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--type", required=True, choices=TYPES); s.add_argument("--n", type=int, default=6); s.add_argument("--out", default="audio/candidates")
    d = sub.add_parser("add"); d.add_argument("files", nargs="+"); d.add_argument("--type", required=True, choices=TYPES)
    d.add_argument("--tags", default=""); d.add_argument("--credit", default=""); d.add_argument("--kit", default="audio/kit")
    a = sub.add_parser("analyze"); a.add_argument("files", nargs="+"); a.add_argument("--type", required=True, choices=TYPES); a.add_argument("--out", default="audio/sfx")
    h = sub.add_parser("sheet"); h.add_argument("files", nargs="+"); h.add_argument("--png", default="audio/sheet.png")
    args = ap.parse_args()
    if args.cmd == "sheet":
        sheet(args.files, args.png)
    elif args.cmd in ("kit", "library"):
        build_library(args.manifest, args.out)
    elif args.cmd == "browse":
        browse(args.kit, args.type, args.like, args.n, args.length, args.tone, args.png)
    elif args.cmd == "add":
        add_files(args.files, args.type, args.kit, words(args.tags), args.credit)
    elif args.cmd == "search":
        res = openverse(args.query, args.n)
        if not res: print("no CC0 results; try other words"); return
        d = os.path.join(args.out, args.type, "_raw"); os.makedirs(d, exist_ok=True)
        for r in res:
            raw = os.path.join(d, f"ov-{r['id'][:8]}.mp3")
            try:
                if not os.path.exists(raw): fetch(r["url"], raw)
                meta = dict(title=r.get("title"), creator=r.get("creator"), license=r.get("license"),
                            url=r.get("url"), landing=r.get("foreign_landing_url"), openverse_id=r["id"])
                for side in prepare(raw, args.type, os.path.join(args.out, args.type), f"ov-{r['id'][:8]}", meta):
                    print(line(side), "|", r.get("title"))
            except Exception as e:
                print("skip", r.get("title"), e, file=sys.stderr)
    else:
        for f in args.files:
            for side in prepare(f, args.type, os.path.join(args.out, args.type)):
                print(line(side))


if __name__ == "__main__":
    main()
