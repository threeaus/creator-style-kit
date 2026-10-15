#!/usr/bin/env python3
"""Scaffold a styled HyperFrames composition from a small beat list.

usage: scaffold.py <style_id> <project_dir> --content beats.json [--init] [--no-build]

beats.json:
{
  "name": "opus-scores",                       # composition id → compositions/<name>.html
  "beats": [
    {"type": "chapter", "num": "01", "title": "Opus 5.5 实测", "sub": "Case Study"},
    {"type": "list", "kick": "Benchmark notes", "head": "拉开差距的 <em>3</em> 个能力",
     "items": [["长上下文检索", 92], ["多步工具调用", 78], ["代码重构", 64]]},   # value optional (bar/readout styles use it)
    {"type": "stat", "value": 87.6, "suffix": "%", "unit": "一次通过", "note": "200 道任务 · <em>零样本</em>"}   # "max": 100 sets the bar/gauge scale
  ],
  "source": "Anthropic 技术报告, 2026",        # data-journal footer (cite the real source)
  "caption": "<b>Figure 1:</b> …"               # paper-figure caption
}
Optional per beat: "dur" (seconds) — a minimum, e.g. the narration length; the beat is never shorter than
its entrance + reading hold (see compose.py). <em>…</em> marks the one emphasised word per beat.
Timing, sequencing and sound cues come from scripts/compose.py; the printout shows each beat's hold and the cues kept.

--init     also write <project>/index.html hosting this composition (fresh projects)
--no-build skip build_style.py (fonts are subset from every .html in the project, so build after all scenes exist)
Prints the host <div> to paste into an existing index.html, plus the scripts index.html must load.
"""
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT / "scripts"))
from compose import composition  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("style"); ap.add_argument("project"); ap.add_argument("--content", required=True)
    ap.add_argument("--init", action="store_true"); ap.add_argument("--no-build", action="store_true")
    a = ap.parse_args()
    project = Path(a.project)
    spec_path = KIT / "styles" / a.style / "style.yaml"
    if not spec_path.exists():
        sys.exit(f"unknown style '{a.style}' — run scripts/list_styles.py")
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    content = json.loads(Path(a.content).read_text(encoding="utf-8"))
    name, beats = content["name"], content["beats"]
    sid, r = spec["id"], f"sc-{content['name']}"
    sfx_dir = KIT / "sfx" / sid
    style_json = project / "csk" / f"{sid}.json"
    html, plan, cues = composition(spec, content, r, {}, sfx_dir)
    total = plan["total"]

    (project / "compositions").mkdir(parents=True, exist_ok=True)
    out = project / "compositions" / f"{name}.html"
    out.write_text(html, encoding="utf-8")  # first pass so the build sees this text for font subsetting

    if a.init:
        (project / "index.html").write_text(f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="csk/gsap.min.js"></script><script src="csk/kit.js"></script>
<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; background:#000; overflow:hidden; }} #main {{ position:relative; width:100%; height:100%; }}</style></head>
<body><div id="main" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
<div id="h-{name}" data-composition-id="{r}" data-composition-src="compositions/{name}.html" data-start="0" data-duration="{total:.2f}" data-track-index="2" data-width="1080" data-height="1920"></div>
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script></body></html>
""", encoding="utf-8")
        for f in ("hyperframes.json", "package.json"):
            src = KIT / "lookbook" / f
            if src.exists() and not (project / f).exists():
                (project / f).write_text(src.read_text(encoding="utf-8").replace("opus55-tutorial", project.name), encoding="utf-8")

    if not a.no_build:
        subprocess.run([sys.executable, str(KIT / "scripts/build_style.py"), sid, str(project)], check=True)
    if style_json.exists():
        html, plan, cues = composition(spec, content, r, json.loads(style_json.read_text()), sfx_dir)
        out.write_text(html, encoding="utf-8")
    else:
        print("! csk/%s.json missing — run build_style.py, then re-run scaffold" % sid)

    print(f"wrote {out}  ({len(beats)} beats, {total:.2f}s, style {sid})")
    for k, p in enumerate(plan["beats"]):
        print(f"  beat {k + 1} {p['type']:7s} {p['t0']:6.2f}–{p['t1']:6.2f}s  settled {p['settled'] - p['t0']:4.2f}s  hold {p['exit'] - p['settled']:4.2f}s")
    print(f"  sound: {len(cues)} cues ({len(cues) / total:.2f}/s) — " + ", ".join(f"{c['role']}@{c['at']:.2f}" for c in cues))
    if not a.init:
        print("host it in index.html (index must load csk/gsap.min.js and csk/kit.js in <head>):")
        print(f'  <div id="h-{name}" data-composition-id="{r}" data-composition-src="compositions/{name}.html" data-start="<t>" data-duration="{total:.2f}" data-track-index="<n>" data-width="1080" data-height="1920"></div>')


if __name__ == "__main__":
    main()
