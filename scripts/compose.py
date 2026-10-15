"""Shared beat planner for scaffold.py and lookbook.py.

Turns a beat list + a style into one composition: every action time is derived from the
style's own motion tokens (so slow styles get longer beats instead of being cut short),
actions run in sequence (one thing moves at a time), each beat holds still long enough to
read, and sound cues are placed on real visual events and thinned to the style's
`sound.rules` (maxPerSecond, silentShare) — with each file's peak aligned to its event.

    plan = plan_beats(spec, beats)          # times for every action, beat spans, total
    cues = plan_sound(spec, plan, sfx_dir)  # thinned, peak-aligned sound cues
    html = composition(spec, content, comp_id, style_json, ...)
"""
import json, re, sys, wave
from pathlib import Path
import numpy as np

KIT = Path(__file__).resolve().parent.parent
CN_NUM = "一二三四五六七八九十"

# ---------------------------------------------------------------- reading
CPS = 7.0                                              # comfortable on-screen reading speed (CJK chars / s)
HOLD_MIN = {"chapter": 1.2, "list": 1.6, "stat": 1.4}  # still time after everything has settled
NUMBER_HOLD = 2.2                                      # the key figure stays locked at least this long ("huh" moment)
LEAD = {"chapter": 0.25, "list": 0.2, "stat": 0.55}    # stillness after the cut; the stat pause is the anticipation


def plain(s):
    return re.sub(r"<[^>]+>", "", str(s or ""))


def glyphs(s):
    return len(plain(s))


def read_s(*texts):
    """Seconds to read: CJK chars count 1, a Latin word counts ~1.5."""
    s = " ".join(plain(t) for t in texts)
    cjk = len(re.findall(r"[㐀-鿿]", s))
    words = len(re.findall(r"[A-Za-z0-9.%]+", s))
    return (cjk + 1.5 * words) / CPS


# ---------------------------------------------------------------- settle times (mirror runtime/kit.js)
def text_settle(M, mode, n):
    D = M["dur"]; i, cs = D["in"], D.get("charStagger", 0) or 0; k = max(0, n - 1)
    sp = min(cs * k, 0.4)                       # kit.js stg(): a line's stagger is capped at 0.4 s
    return {
        "clip-rise": i, "paper-slap": i, "slide-block": i + 0.02, "scan-in": i + 0.07,
        "type-scramble": cs * k + 0.1, "segment-on": sp + 0.08,
        "write": 1.1 * i + sp, "draft-in": 0.16 + i, "converge": i + 0.28,
    }.get(mode, i + sp)  # blur-rise, fade-up, ink-bleed, spring-pop, drop-letters


def number_settle(M, mode, value):
    i, s = M["dur"]["in"], str(value)
    return {
        "scramble-lock": 0.35 + 0.1 * (len(s) - 1), "step-climb": max(i, 0.9), "stamp": 0.44, "bubble-count": 1.1,
        "odometer": 1.1 + 0.15 * (len(s) - 1), "decimal-tracker": 1.3, "soft-count": 1.4, "bar-grow": 1.2, "gauge": 1.3,
        "particle-form": 1.55, "segment": 1.32, "ink-count": 1.15, "geo-count": max(i, 0.8),
    }.get(mode, 1.2)


# GSAP eases used by the count modes (GSAP powerN = polynomial of degree N+1)
EASES = {
    "none": lambda x: x,
    "power2.out": lambda x: 1 - (1 - x) ** 3, "power3.out": lambda x: 1 - (1 - x) ** 4,
    "power2.inOut": lambda x: 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2,
    "expo.out": lambda x: 1.0 if x >= 1 else 1 - 2 ** (-10 * x),
}
# (delay, duration, ease, fps) of each mode's countSets call in kit.js
COUNTS = {"step-climb": (0, 0.9, "none", 13), "bubble-count": (0, 1.1, "expo.out", 30), "decimal-tracker": (0, 1.3, "power2.inOut", 30),
          "soft-count": (0, 1.4, "expo.out", 30), "bar-grow": (0, 1.2, "power3.out", 30), "gauge": (0, 1.3, "power3.out", 30),
          "segment": (0.32, 1.0, "power2.out", 12), "ink-count": (0.15, 1.0, "expo.out", 30), "geo-count": (0, 0.8, "power2.out", 15)}


def number_lock(M, mode, value):
    """When the figure visibly stops: the first frame the displayed count shows the final value."""
    if mode in COUNTS:
        d, dur, e, fps = COUNTS[mode]; fn = EASES[e]
        dec = len(str(value).split(".")[1]) if "." in str(value) else 0
        n = max(2, round(dur * fps)); final = f"{float(value):.{dec}f}"
        # the eye reads it as landed once it is within 0.2 % (the last tenths creep in an ease-out tail)
        # (per-mode thresholds were measured against renders with sound_pass.py's reveal check)
        # stepped counts (< 30 fps) visibly tick to the end: wait for the exact final value
        near = 1.01 if fps < 30 else {"soft-count": 0.995, "bubble-count": 0.995}.get(mode, 0.998)
        k = next(k for k in range(n + 1) if f"{float(value) * fn(k / n):.{dec}f}" == final or fn(k / n) >= near)
        return d + k / fps
    return {"odometer": 0.85 + 0.15 * (len(str(value)) - 1), "particle-form": 1.0, "stamp": 0.28}.get(mode, number_settle(M, mode, value))


def item_settle(M, mode, n):
    D = M["dur"]; i, cs = D["in"], D.get("charStagger", 0) or 0
    return {
        "index-snap": 0.61, "slam-alternate": 0.58, "terminal-lines": 0.18 + cs * max(0, n - 1), "bar-chart": 1.0,
        "leader-lines": 0.28 + i, "readout": max(0.8, 0.12 + i), "glass-cards": max(i, 1.2), "geo-blocks": 0.12 + i, "key-press": 0.48,
    }.get(mode, i)  # rise-dim, index-cards, sticker-cards, fade-rows, grow-in, converge-rows, iso-stack, ink-rows


EMPH_SETTLE = {"accent-glint": 0.35, "knife-underline": 0.32, "highlighter": 0.45, "selection": 0.3, "scribble": 0.42, "recolor-char": 0.3,
               "circumscribe": 0.6, "boxed": 0.6, "dimension": 0.45, "bracket-lock": 0.37, "halo": 0.6, "seal-stamp": 0.6,
               "gradient-sweep": 0.9, "underline-soft": 0.5, "shape-mark": 0.45, "led-tag": 0.1}

# time from transition start to full cover (mirror runtime/kit.js `trans`)
COVER = {"light-sweep": 0.3, "column-wipe": 0.495, "sheet-wipe": 0.4, "card-zoom": 0.5, "ground-slats": 0.54, "glitch-slice": 0.05,
         "edge-wipe": 0.38, "draft-wipe": 0.42, "particle-warp": 0.4, "frost": 0.4, "iso-slide": 0.42, "shape-iris": 0.42,
         "ink-spread": 0.55, "shutter": 0.435}
OPEN_TRANSITIONS = {"light-sweep", "glitch-slice"}  # these don't hide the frame: text must leave on its own first


def cover_len(M):
    return max(0.3, M["dur"]["out"]) if M["transition"] == "dip" else COVER.get(M["transition"], 0.4)


# ---------------------------------------------------------------- beat plan
def plan_beats(spec, beats):
    """Absolute times for every action. Each beat: t0 (scene visible) … exit (hold ends) → cover (next t0)."""
    M = spec["motion"]; D = M["dur"]
    em = lambda s: "<em>" in str(s or "")
    emph = EMPH_SETTLE.get(M["emphasis"], 0.5)
    open_tr = M["transition"] in OPEN_TRANSITIONS
    plans, t = [], 0.0
    for k, b in enumerate(beats):
        ty, p = b["type"], {"type": b["type"], "t0": t}
        t0 = t + LEAD[ty]
        if ty == "chapter":
            p["num"] = t0; num_end = t0 + text_settle(M, M["textIn"], glyphs(b.get("num")))
            p["ttl"] = t0 + 0.15; ttl_end = p["ttl"] + text_settle(M, M["textIn"], glyphs(b["title"]))
            p["rule"] = p["ttl"] + 0.2; p["rule_dur"] = max(0.6, D["in"])
            p["sub"] = max(p["ttl"] + 0.3, ttl_end - 0.35); sub_end = p["sub"] + text_settle(M, M["textIn"], glyphs(b.get("sub")))
            settled = max(num_end, ttl_end, p["rule"] + p["rule_dur"], sub_end)
            hold = max(HOLD_MIN[ty], read_s(b["title"], b.get("sub")) - 0.5 * (settled - p["ttl"]))
            p["events"] = [("title", p["ttl"] + 0.05, "appear")]
        elif ty == "list":
            items = [x if isinstance(x, list) else [x] for x in b.get("items", [])]
            p["kick"] = t0; p["ttl"] = t0 + 0.12
            ttl_end = p["ttl"] + text_settle(M, M["textIn"], glyphs(b["head"]))
            nxt = ttl_end
            if em(b["head"]):
                p["emph"] = ttl_end + 0.1; nxt = p["emph"] + emph
            st = [item_settle(M, M["list"], glyphs(it[0])) for it in items] or [0]
            gap = min(0.75, max(0.4, 0.6 * max(st)))
            p["items"] = [nxt + 0.1 + gap * i for i in range(len(items))]
            settled = max([ttl_end, nxt] + [a + s for a, s in zip(p["items"], st)])
            hold = max(HOLD_MIN[ty], read_s(b["head"], *[it[0] for it in items]) - 0.5 * (settled - p["ttl"]))
            p["events"] = ([("hit", p["emph"], "appear")] if "emph" in p else []) + ([("list", p["items"][0] + 0.05, "appear")] if items else [])
        elif ty == "stat":
            p["num"] = t0; p["lock"] = t0 + number_lock(M, M["number"], b["value"])
            num_end = t0 + number_settle(M, M["number"], b["value"])
            p["unit"] = p["lock"] + 0.12; unit_end = p["unit"] + text_settle(M, M["textIn"], glyphs(b.get("unit")))
            p["note"] = p["unit"] + 0.3; note_end = p["note"] + text_settle(M, M["textIn"], glyphs(b.get("note")))
            settled = max(num_end, unit_end, note_end)
            if em(b.get("note")):
                p["emph"] = note_end + 0.1; settled = p["emph"] + emph
            hold = max(HOLD_MIN[ty], read_s(b.get("unit"), b.get("note")) - 0.5 * (settled - p["unit"]), p["lock"] + NUMBER_HOLD - settled)
            # qa.py's "land" probe can't see a lock through ambient motion + follow-through; sound_pass.py checks reveals itself
            p["events"] = [("reveal", p["lock"], "lock")] + ([("highlight", p["emph"], "appear")] if "emph" in p else [])
        else:
            sys.exit(f"unknown beat type {ty!r} (chapter | list | stat)")
        p["settled"] = settled
        exit_t = settled + hold
        if b.get("dur"):                                       # narration-driven length wins if longer
            exit_t = max(exit_t, p["t0"] + float(b["dur"]) - cover_len(M))
        p["exit"] = exit_t
        p["text_out"] = exit_t if open_tr else None            # covering transitions hide the text themselves
        p["trans"] = exit_t + (D["out"] * 0.5 if open_tr else 0.0)
        p["cover"] = p["trans"] + cover_len(M)
        p["t1"] = p["cover"]
        plans.append(p); t = p["t1"]
    return {"beats": plans, "total": round(t + 0.1, 2)}


# ---------------------------------------------------------------- sound
_meta = {}


def sfx_meta(path):
    """(peak offset s, audible length s, file length s) of a wav — peak of a 2 ms RMS envelope, tail until -40 dB."""
    path = str(path)
    if path not in _meta:
        with wave.open(path) as w:
            sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
            x = np.frombuffer(w.readframes(n), np.int16).astype(np.float64).reshape(-1, ch).mean(axis=1) / 32768
        win = max(1, int(0.002 * sr)); env = np.sqrt(np.convolve(x * x, np.ones(win) / win, mode="same"))
        pk = int(np.argmax(env)); loud = np.where(env > env[pk] * 0.01)[0]
        _meta[path] = (pk / sr, (loud[-1] if len(loud) else pk) / sr, n / sr)
    return _meta[path]


PRIORITY = {"reveal": 0, "transition": 1, "title": 2, "hit": 3, "list": 4, "highlight": 5}


def plan_sound(spec, plan, sfx_dir):
    """Candidate cues on visual events, thinned to the style's sound.rules, then peak-aligned."""
    roles = json.loads((Path(sfx_dir) / "kit.json").read_text())["roles"]
    rules = (spec.get("sound") or {}).get("rules") or {}
    rate, silent = rules.get("maxPerSecond", 0.6), rules.get("silentShare", 0.7)
    cap3 = max(1, round(3 * rate))                      # cues allowed in any 3 s window
    total = plan["total"]
    cand = []
    for k, p in enumerate(plan["beats"]):
        for role, at, visual in p["events"]:
            cand.append({"role": role, "at": at, "visual": visual, "weight": "hero" if role == "reveal" else "support"})
        if k < len(plan["beats"]) - 1 and k % 2 == 0:  # every other cut gets a sound
            cand.append({"role": "transition", "at": p["cover"] - 0.1, "visual": "move", "weight": "support"})  # peak speed is ~3 frames before full cover
    use = {}
    for c in cand:                                      # resolve role → file (highlight falls back to hit, quieter)
        files = roles.get(c["role"]) or (roles.get("hit") if c["role"] == "highlight" else None)
        if files:
            n = use.get(c["role"], 0); use[c["role"]] = n + 1
            c["file"] = files[n % len(files)]; c["vol"] = 0.7 if c["role"] == "highlight" else 1.0
            c["peak"], c["len"], c["file_len"] = sfx_meta(Path(sfx_dir) / c["file"])
    cand = [c for c in cand if "file" in c]
    heroes = [c["at"] for c in cand if c["weight"] == "hero"]
    kept, busy = [], 0.0
    for c in sorted(cand, key=lambda c: (PRIORITY[c["role"]], c["at"])):
        if any(abs(c["at"] - o["at"]) < 0.5 for o in kept): continue
        if sum(1 for o in kept if abs(c["at"] - o["at"]) < 1.5) + 1 > cap3: continue
        if c["weight"] != "hero" and any(0 < h - c["at"] < 0.6 for h in heroes): continue   # silence before the reveal
        audible = min(c["len"] - c["peak"] + 0.15, 1.2)
        if busy + audible > (1 - silent) * total: continue
        kept.append(c); busy += audible
    for c in kept:
        c["start"] = max(0.0, c["at"] - c["peak"])
    return sorted(kept, key=lambda c: c["at"])


def figure_band(spec):
    """Vertical band (px) the stat figure occupies for this style's layout — used by sound_pass.py's reveal check."""
    h = spec["type"]["hero"] * 0.9
    top = {"top-left": 380, "center": 640, "left": 600}.get((spec.get("layout") or {}).get("stat", "left"))
    if top is None:                                   # low-left: the block is anchored 560 px from the bottom
        top = 1920 - 560 - (h + 260)
    return int(max(0, top - 40)), int(min(1920, top + h + 30))


def audio_tags(cues, comp_id, sid, roi=None):
    return "".join(
        f'<audio id="{comp_id}-a{i}" src="csk/sfx/{sid}/{c["file"]}" data-start="{c["start"]:.3f}" data-duration="{c["file_len"]:.3f}" '
        f'data-track-index="{20 + i % 3}" data-volume="{c["vol"]}" data-role="{c["role"]}" data-peak="{c["at"]:.3f}"{f' data-visual="{c["visual"]}"' if c["visual"] else ""} data-weight="{c["weight"]}"'
        f'{f' data-roi="{roi[0]},{roi[1]}"' if roi and c["visual"] == "lock" else ""}></audio>'
        for i, c in enumerate(cues))


# ---------------------------------------------------------------- markup
def idx_label(fmt, i):
    return fmt.replace("{n}", str(i + 1)).replace("{cn}", CN_NUM[i % 10])


def beat_html(b, fmt, caret):
    t = b["type"]
    if t == "chapter":
        return (f'<div class="csk-chapter"><div class="num">{b.get("num", "")}</div><div class="ttl t-display">{b["title"]}</div>'
                f'<div class="rule"></div><div class="sub t-label">{b.get("sub", "")}</div></div>')
    if t == "list":
        lis = "".join(f'<li{f" data-v={chr(34)}{it[1]}{chr(34)}" if len(it) > 1 else ""}><span class="idx">{idx_label(fmt, i)}</span><span class="txt">{it[0]}</span><i class="rule"></i></li>'
                      for i, it in enumerate([x if isinstance(x, list) else [x] for x in b.get("items", [])]))
        return (f'<div class="csk-head"><div class="kick t-label">{b.get("kick", "")}</div><div class="ttl t-display">{b["head"]}{caret}</div></div>'
                f'<ol class="csk-list">{lis}</ol>')
    mx = f' data-max="{b["max"]}"' if "max" in b else ""
    sf = f' data-suffix="{b["suffix"]}"' if b.get("suffix") else ""
    return f'<div class="csk-stat"><div class="val"{mx}{sf}>{b["value"]}</div><div class="unit">{b.get("unit", "")}</div><div class="note t-note">{b.get("note", "")}</div></div>'


def beat_js(b, k, p):
    s = f".csk-s{k}"
    L = [f"  // beat {k + 1} — {b['type']}  [{p['t0']:.2f}s – {p['t1']:.2f}s]  settled {p['settled']:.2f}s, holds until {p['exit']:.2f}s"]
    if b["type"] == "chapter":
        L += [f'  kit.textIn($("{s} .csk-chapter .num"), {p["num"]:.2f});',
              f'  kit.textIn($("{s} .csk-chapter .ttl"), {p["ttl"]:.2f});',
              f'  tl.fromTo($("{s} .csk-chapter .rule"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: {p["rule_dur"]:.2f}, ease: kit.ease.snap }}, {p["rule"]:.2f});',
              f'  kit.textIn($("{s} .csk-chapter .sub"), {p["sub"]:.2f});']
        if p["text_out"] is not None:
            L += [f'  kit.textOut($("{s} .csk-chapter .num, {s} .csk-chapter .ttl, {s} .csk-chapter .sub"), {p["text_out"]:.2f});',
                  f'  tl.to($("{s} .csk-chapter .rule"), {{ scaleX: 0, transformOrigin: "100% 50%", duration: 0.3, ease: kit.ease.exit }}, {p["text_out"]:.2f});']
    elif b["type"] == "list":
        L += [f'  kit.textIn($("{s} .csk-head .kick"), {p["kick"]:.2f});',
              f'  kit.textIn($("{s} .csk-head .ttl"), {p["ttl"]:.2f});']
        if "emph" in p: L.append(f'  kit.emphasis($("{s} .csk-head em"), {p["emph"]:.2f});')
        L.append(f'  kit.list($("{s} .csk-list li"), [{", ".join(f"{x:.2f}" for x in p["items"])}]);')
        if p["text_out"] is not None:
            L.append(f'  kit.textOut($("{s} .csk-head .kick, {s} .csk-head .ttl, {s} .csk-list li"), {p["text_out"]:.2f});')
    else:
        L += [f'  kit.number($("{s} .csk-stat .val"), {p["num"]:.2f}, {b["value"]});',
              f'  kit.textIn($("{s} .csk-stat .unit"), {p["unit"]:.2f});',
              f'  kit.textIn($("{s} .csk-stat .note"), {p["note"]:.2f});']
        if "emph" in p: L.append(f'  kit.emphasis($("{s} .csk-stat .note em"), {p["emph"]:.2f});')
        if p["text_out"] is not None:
            L.append(f'  kit.textOut($("{s} .csk-stat .val, {s} .csk-stat .unit, {s} .csk-stat .note"), {p["text_out"]:.2f});')
    return "\n".join(L)


def layout_attrs(spec):
    """style.yaml layout → root attributes that select the archetypes in kit.css."""
    lay = spec.get("layout") or {}
    return "".join(f' data-l-{k}="{lay[k]}"' for k in ("chapter", "list", "stat") if lay.get(k))


def composition(spec, content, comp_id, style_json, sfx_dir, overlay="", seed=7):
    """Full composition HTML for one style. Returns (html, plan, cues)."""
    sid, beats = spec["id"], content["beats"]
    lb = spec.get("lookbook") or {}
    tape = (spec.get("texture") or {}).get("tape", "")
    tex = (lb.get("textures", "").replace("{tape}", tape).replace("{lines}", "<br>".join(str(n) for n in range(1, 37)))
           .replace("{source}", content.get("source", "")).replace("{caption}", content.get("caption", "")))
    caret = '<span class="csk-caret"></span>' if sid == "dev-console" else ""
    fmt = lb.get("idx", "0{n}")
    grounds, gtext = spec["colors"].get("grounds") or [], spec["colors"].get("groundText") or []
    gacc = spec["colors"].get("groundAccent") or [spec["colors"]["accent"]] * len(grounds)

    plan = plan_beats(spec, beats)
    cues = plan_sound(spec, plan, sfx_dir)
    total, P = plan["total"], plan["beats"]

    js = []
    for k, (b, p) in enumerate(zip(beats, P)):
        js.append(beat_js(b, k, p))
        if k < len(beats) - 1:
            swap = f"tl.set($('.csk-s{k}'), {{ opacity: 0 }}, c); tl.set($('.csk-s{k + 1}'), {{ opacity: 1 }}, c);"
            if grounds:
                g = (k + 1) % len(grounds)
                js.append(f"  {{ const c = kit.transition({p['trans']:.2f}, null, '{grounds[g]}'); {swap}"
                          f" tl.set($('.csk-bg'), {{ backgroundColor: '{grounds[g]}' }}, c); tl.set(R, {{ '--c-text': '{gtext[g]}', '--c-accent': '{gacc[g]}' }}, c); }}")
            else:
                js.append(f"  {{ const c = kit.transition({p['trans']:.2f}); {swap} }}")
    js.append(f'  kit.transition({P[-1]["trans"]:.2f}, "out");')
    if sid == "poster-kinetic":
        js += [f"  kit.punch({p['lock']:.2f});" for p in P if p["type"] == "stat"]

    scenes = "\n  ".join(f'<div class="csk-scene csk-s{k}">{beat_html(b, fmt, caret)}</div>' for k, b in enumerate(beats))
    st = dict(style_json or {}); st["seed"] = seed
    html = f"""<!doctype html>
<html><head><meta charset="UTF-8" /></head><body><template>
<link rel="stylesheet" href="csk/kit.css" /><link rel="stylesheet" href="csk/{sid}.css" />
<!-- style: {sid} ({spec['name']['zh']}) · generated by creator-style-kit/scripts/compose.py · {total:.2f}s -->
<div id="{comp_id}" class="csk" data-csk="{sid}"{layout_attrs(spec)} data-composition-id="{comp_id}" data-width="1080" data-height="1920">
  <div class="csk-bg"></div>
  {tex}
  {scenes}
  {overlay}
  {audio_tags(cues, comp_id, sid, figure_band(spec))}
</div>
<script>
(function () {{
  // on mount the runtime strips the inner root's id/data-composition-id; the host keeps data-composition-id
  const R = '[data-composition-id="{comp_id}"] .csk[data-csk]', tl = gsap.timeline({{ paused: true }});
  const kit = CSK.create({{ tl, root: R, style: {json.dumps(st, ensure_ascii=False)} }});
  const $ = (s) => R + " " + s;
  {"gsap.set([" + ", ".join(f'$(".csk-s{k}")' for k in range(1, len(beats))) + "], { opacity: 0 });" if len(beats) > 1 else ""}
  kit.ambient(0, {total:.2f});
  kit.transition(0, "in");
{chr(10).join(js)}
  window.__timelines["{comp_id}"] = tl;
}})();
</script>
</template></body></html>
"""
    return html, plan, cues
