#!/usr/bin/env python3
"""Generate a HyperFrames lookbook: the same three beats rendered in every style.

usage: lookbook.py <project_dir> [--only id,id,...] [--from-order N] [--title TEXT]
  --only        render just these style ids (in the given order)
  --from-order  render styles whose `order` >= N (e.g. 7 = the styles added after the first six)
Then: cd <project_dir> && npx hyperframes render

Everything per style comes from styles/<id>/: style.yaml (`order`, `lookbook.textures`, `lookbook.idx`)
and skin.css (compiled into csk/<id>.css by build_style.py).
"""
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT / "scripts"))
from compose import composition  # noqa: E402
INTRO = 2.4

# Sample content. The figures are illustrative only and are labelled 示例数据 on screen.
CONTENT = {
    "source": "示例数据 · Creator Style Kit",
    "caption": "<b>Figure 1:</b> 风格样张。数值为示例数据，仅演示排版。",
    "beats": [
        {"type": "chapter", "num": "01", "title": "Opus 5.5 实测", "sub": "Case Study · 风格样张"},
        {"type": "list", "kick": "Benchmark notes", "head": "拉开差距的 <em>3</em> 个能力",
         "items": [["长上下文检索", 92], ["多步工具调用", 78], ["代码重构 · 自测", 64]]},
        {"type": "stat", "value": 87.6, "suffix": "%", "unit": "一次通过", "note": "示例数据 · <em>200</em> 道任务"},
    ],
}


def load_styles():
    specs = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted((KIT / "styles").glob("*/style.yaml"))]
    return sorted(specs, key=lambda s: (s.get("order", 99), s["id"]))


def comp(spec, idx, total):
    sid = spec["id"]
    c = spec["colors"]
    extra = [v for k, v in c.items() if k not in ("bg", "surface", "line", "text", "muted", "accent", "accentInk") and isinstance(v, str) and v.startswith("#")]
    swatches = "".join(f'<i style="background:{c[k]}"></i>' for k in ("bg", "text", "accent")) + "".join(f'<i style="background:{v}"></i>' for v in extra[:3])
    tag = f'<div class="csk-tag"><div class="k">STYLE {idx + 1:02d} / {total:02d}</div><div class="n">{spec["name"]["zh"]}<small>{spec["name"]["en"]}</small></div><div class="sw">{swatches}</div></div>'
    js = json.loads((PROJECT / "csk" / f"{sid}.json").read_text())
    return composition(spec, CONTENT, f"lb-{sid}", js, KIT / "sfx" / sid, overlay=tag, seed=11 + idx)


def main(project: Path, only=None, from_order=None, title=None):
    global PROJECT
    PROJECT = project
    specs = load_styles()
    if only:
        by = {s["id"]: s for s in specs}
        specs = [by[i] for i in only]
    elif from_order:
        specs = [s for s in specs if s.get("order", 99) >= from_order]
    n = len(specs)
    (project / "compositions").mkdir(parents=True, exist_ok=True)
    for old in (project / "compositions").glob("*.html"):
        old.unlink()
    build = lambda: subprocess.run([sys.executable, str(KIT / "scripts/build_style.py"), "all", str(project)], check=True)
    build()
    hosts, t = [], INTRO
    for i, spec in enumerate(specs):
        sid = spec["id"]
        html, plan, cues = comp(spec, i, n)
        (project / "compositions" / f"{sid}.html").write_text(html, encoding="utf-8")
        seg = plan["total"]
        hosts.append(f'<div id="h-{sid}" data-composition-id="lb-{sid}" data-composition-src="compositions/{sid}.html" data-start="{t:.2f}" data-duration="{seg:.2f}" data-track-index="{i + 2}" data-width="1080" data-height="1920"></div>')
        print(f"  {sid:17s} {seg:5.2f}s  " + " · ".join(f"{p['type']} {p['t1'] - p['t0']:.1f}s (hold {p['exit'] - p['settled']:.1f})" for p in plan["beats"]) + f"  · {len(cues)} sounds")
        t += seg
    total = t
    title = title or f"{n} 套风格"
    (project / "index.html").write_text(f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>Creator Style Kit · Lookbook</title>
<script src="csk/gsap.min.js"></script><script src="csk/kit.js"></script>
<link rel="stylesheet" href="csk/kit.css" /><link rel="stylesheet" href="csk/dark-keynote.css" />
<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; background:#000; overflow:hidden; }}
#main {{ position:relative; width:100%; height:100%; background:#000; }}
#intro {{ position:absolute; inset:0; display:flex; flex-direction:column; justify-content:center; padding:0 90px; color:#F5F5F7; }}
#intro .k {{ font-family:"JetBrains Mono"; font-size:24px; letter-spacing:0.3em; color:#8E8E93; }}
#intro .t {{ font-family:"CSK MiSans"; font-weight:900; font-size:150px; line-height:1.05; margin-top:26px; }}
#intro .s {{ font-family:"CSK MiSans"; font-weight:500; font-size:40px; color:#8E8E93; margin-top:30px; }}</style></head>
<body><div id="main" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
<section id="intro" class="clip" data-start="0" data-duration="{INTRO}" data-track-index="1"><div class="k">CREATOR STYLE KIT · LOOKBOOK</div><div class="t">{title}</div><div class="s">同一段内容 · 不同的字体、配色、动效与音效</div></section>
{chr(10).join(hosts)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#intro .k, #intro .t, #intro .s", {{ opacity: 0, y: 30, filter: "blur(12px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.8, stagger: 0.12, ease: "expo.out" }}, 0.15);
tl.to("#intro .k, #intro .t, #intro .s", {{ opacity: 0, y: -20, duration: 0.35, ease: "power2.in" }}, 2.0);
window.__timelines["main"] = tl;
</script></body></html>
""", encoding="utf-8")
    build()  # re-subset fonts now that the compositions exist
    print("lookbook written:", project, f"{n} styles, {total:.1f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--only"); ap.add_argument("--from-order", type=int); ap.add_argument("--title")
    a = ap.parse_args()
    main(Path(a.project), a.only.split(",") if a.only else None, a.from_order, a.title)
