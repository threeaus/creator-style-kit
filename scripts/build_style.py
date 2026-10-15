#!/usr/bin/env python3
"""Compile a style.yaml into what a HyperFrames project needs:

  <out>/csk/<id>.css      CSS variables scoped to [data-csk="<id>"] + @font-face rules + styles/<id>/skin.css
  <out>/csk/<id>.json     motion / colour tokens for runtime/kit.js
  <out>/csk/fonts/*.woff2 fonts subset to exactly the glyphs your compositions use
  <out>/csk/sfx/<id>/     the style's SFX kit (copied from the kit)
  <out>/csk/kit.css, kit.js, gsap.min.js

usage: build_style.py <style_id> <project_dir> [--text-from <glob>...]
Text for subsetting is collected from every .html under the project unless globs are given.
"""
import argparse, glob, json, shutil, subprocess, sys
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent
FONT_SRC = KIT / "fonts" / "src"
ASCII = "".join(chr(c) for c in range(32, 127))
EXTRA = "，。、？！：；“”‘’《》（）【】—…·✳↗→←✓×"


def collect_text(project: Path, globs):
    files = [Path(p) for g in globs for p in glob.glob(str(project / g), recursive=True)] if globs else list(project.rglob("*.html"))
    s = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in files)
    return "".join(sorted(set(s) | set(ASCII) | set(EXTRA)))


def build(style_id: str, project: Path, globs=None):
    spec = yaml.safe_load((KIT / "styles" / style_id / "style.yaml").read_text())
    out = project / "csk"
    (out / "fonts").mkdir(parents=True, exist_ok=True)
    text = collect_text(project, globs)
    tf = out / f".chars-{style_id}.txt"
    tf.write_text(text, encoding="utf-8")

    faces, fam = [], {}
    for role, f in spec["fonts"].items():
        fam[role] = f["family"]
        if f.get("bundled"):
            continue
        woff = out / "fonts" / f"{Path(f['file']).stem}.woff2"
        if not (FONT_SRC / f["file"]).exists():
            sys.exit(f"missing fonts/src/{f['file']} — run: python3 scripts/fetch_fonts.py")
        if not woff.exists() or woff.stat().st_mtime < tf.stat().st_mtime:
            subprocess.run(["pyftsubset", str(FONT_SRC / f["file"]), f"--text-file={tf}", f"--output-file={woff}", "--flavor=woff2", "--layout-features=*"], check=True)
        style = f.get("style", "normal")
        faces.append(f'@font-face {{ font-family: "{f["family"]}"; src: url("fonts/{woff.name}") format("woff2"); font-weight: {f["weight"]}; font-style: {style}; }}')

    c, ty = spec["colors"], spec["type"]
    tex = spec.get("texture", {})
    var = {
        "--c-bg": c["bg"], "--c-surface": c["surface"], "--c-line": c["line"], "--c-text": c["text"], "--c-muted": c["muted"],
        "--c-accent": c["accent"], "--c-accent-ink": c.get("accentInk", c["bg"]),
        "--f-display": f'"{fam["display"]}"', "--f-body": f'"{fam["body"]}"', "--f-latin": f'"{fam["latin"]}"', "--f-mono": f'"{fam["mono"]}"',
        "--f-note": f'"{fam.get("note", fam["body"])}"',
        "--w-display": spec["fonts"]["display"]["weight"], "--w-body": spec["fonts"]["body"]["weight"], "--w-latin": spec["fonts"]["latin"]["weight"], "--w-mono": spec["fonts"]["mono"]["weight"],
        "--s-latin": spec["fonts"]["latin"].get("style", "normal"),
        "--fs-hero": f'{ty["hero"]}px', "--fs-h1": f'{ty["h1"]}px', "--fs-h2": f'{ty["h2"]}px', "--fs-body": f'{ty["body"]}px', "--fs-label": f'{ty["label"]}px',
        "--tr-display": f'{ty["displayTracking"]}em', "--tr-label": f'{ty["labelTracking"]}em',
        "--grid": f'{tex["grid"]}px' if isinstance(tex.get("grid"), int) and tex["grid"] else "0px",
        "--grid-op": tex.get("gridOpacity", 1), "--grain": tex.get("grain", 0), "--vig": tex.get("vignette", 0),
        "--halftone": tex.get("halftone", 0), "--dots": f'{tex.get("dots", 36)}px', "--dots-op": tex.get("dotsOpacity", 0.12), "--scan": tex.get("scanlines", 0.03),
    }
    for k, v in c.items():
        if k not in ("bg", "surface", "line", "text", "muted", "accent", "accentInk") and isinstance(v, str):
            var[f"--c-{k}"] = v
    css = "\n".join(faces) + f'\n[data-csk="{style_id}"] {{\n' + "\n".join(f"  {k}: {v};" for k, v in var.items()) + "\n}\n"
    skin = KIT / "styles" / style_id / "skin.css"   # per-style component skin, scoped to .csk[data-csk="<id>"]
    if skin.exists():
        css += "\n" + skin.read_text(encoding="utf-8")
    (out / f"{style_id}.css").write_text(css, encoding="utf-8")

    runtime = {k: spec[k] for k in ("id", "name", "colors", "type", "motion", "texture") if k in spec}
    (out / f"{style_id}.json").write_text(json.dumps(runtime, ensure_ascii=False, indent=1), encoding="utf-8")

    for f in ("kit.css", "kit.js", "gsap.min.js"):
        shutil.copy(KIT / "runtime" / f, out / f)
    sfx_src = KIT / "sfx" / style_id
    if sfx_src.exists():
        shutil.copytree(sfx_src, out / "sfx" / style_id, dirs_exist_ok=True)
    print(f"built {style_id} → {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("style"); ap.add_argument("project"); ap.add_argument("--text-from", nargs="*")
    a = ap.parse_args()
    ids = sorted(p.name for p in (KIT / "styles").iterdir() if (p / "style.yaml").exists()) if a.style == "all" else [a.style]
    for sid in ids:
        build(sid, Path(a.project), a.text_from)
