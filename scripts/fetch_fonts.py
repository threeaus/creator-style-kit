#!/usr/bin/env python3
"""Download the fonts that the repo can't redistribute (free for commercial use, but not re-hostable).

usage: fetch_fonts.py

MiSans (dark-keynote, isometric-stack, lookbook intro) and 优设标题黑 (poster-kinetic) go into fonts/src.
Files already present are skipped, and each download is checked against the sha256 of the file the kit was built with.
Licenses: MiSans 字体知识产权许可协议 (https://hyperos.mi.com/font/), 优设标题黑 free-commercial statement (https://www.uisdc.com/).
"""
import hashlib, subprocess
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "fonts" / "src"
FONTS = {
    "MiSans-Heavy.otf": ("https://cdn.jsdelivr.net/npm/@fontpkg/mi-sans@4.3.0/MiSans-Heavy.otf",
                         "2b8eb30ed34487f60b24cff0f6390ff347f4a07bab122a3a6ed2b805ac6638d9"),
    "MiSans-Medium.otf": ("https://cdn.jsdelivr.net/npm/@fontpkg/mi-sans@4.3.0/MiSans-Medium.otf",
                          "d42b498b7ed9b5bf66a2f5c545839c43f39d6a81efc10eeb83fd63a959629c65"),
    "YouSheBiaoTiHei.ttf": ("https://cdn.jsdelivr.net/npm/@fontpkg/you-she-biao-ti-hei@1.0.0/%E4%BC%98%E8%AE%BE%E6%A0%87%E9%A2%98%E9%BB%91.ttf",
                            "dab883d69fb713233ea5d9aff8d1f27ccc2b71e249143edf6ea08367784c5dba"),
}


def main():
    SRC.mkdir(parents=True, exist_ok=True)
    for name, (url, sha) in FONTS.items():
        dst = SRC / name
        if dst.exists():
            print(f"have  {name}"); continue
        data = subprocess.run(["curl", "-fsSL", "--max-time", "300", url], capture_output=True, check=True).stdout  # curl: system certs
        if hashlib.sha256(data).hexdigest() != sha:
            raise SystemExit(f"{name}: checksum mismatch from {url}")
        dst.write_bytes(data)
        print(f"got   {name} ({len(data) // 1024} KB)")


if __name__ == "__main__":
    main()
