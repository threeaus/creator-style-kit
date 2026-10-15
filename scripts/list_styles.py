#!/usr/bin/env python3
"""Print the style catalog straight from styles/*/style.yaml (always current).

usage: list_styles.py                 one line per style: id, name, best_for, essence
       list_styles.py <id> [<id>...]  full brief for each style: essence, not-rules, motion, colours, fonts, sound
"""
import sys
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent


def load():
    specs = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in (KIT / "styles").glob("*/style.yaml")]
    return sorted(specs, key=lambda s: (s.get("order", 99), s["id"]))


def brief(s):
    m, c = s["motion"], s["colors"]
    print(f"## {s['id']} — {s['name']['zh']} / {s['name']['en']}")
    print(f"essence: {s['essence']}")
    print("best_for: " + "、".join(s.get("best_for", [])))
    print("not (hard rules):")
    for n in s.get("not", []):
        print(f"  - {n}")
    print("motion: " + ", ".join(f"{k}={m[k]}" for k in ("textIn", "textOut", "emphasis", "number", "list", "transition", "camera") if k in m))
    print("colors: " + ", ".join(f"{k}={v}" for k, v in c.items() if isinstance(v, str)))
    print("fonts: " + ", ".join(f"{k}={f['family']} {f['weight']}" for k, f in s["fonts"].items()))
    print(f"sound: {s['sound']['character']}  rules={s['sound'].get('rules')}")
    print(f"sfx roles: {', '.join(s['sound']['kit'])}")
    print()


if __name__ == "__main__":
    specs = load()
    if len(sys.argv) > 1:
        by = {s["id"]: s for s in specs}
        for sid in sys.argv[1:]:
            if sid not in by:
                sys.exit(f"unknown style '{sid}'. known: {', '.join(by)}")
            brief(by[sid])
    else:
        for s in specs:
            print(f"{s['id']:<18} {s['name']['zh']:<6} | {'、'.join(s.get('best_for', [])[:3])} | {s['essence'][:46]}…")
