#!/usr/bin/env python3
"""Fetch Google Fonts CSS, download referenced woff2 files, and write local fonts.css

Usage: run from the `prototype/` directory: `python3 scripts/fetch_fonts.py`
"""
import os
import re
import sys
from urllib.request import urlopen, Request


FONT_CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Open+Sans:wght@300;400;600;700&family=Source+Sans+3:wght@400;600&display=swap"
)


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "python-urllib/3"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def download(url: str, dest: str) -> None:
    req = Request(url, headers={"User-Agent": "python-urllib/3"})
    with urlopen(req, timeout=30) as r, open(dest, "wb") as out:
        out.write(r.read())


def main():
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(cwd)
    fonts_dir = os.path.join(cwd, "fonts")
    os.makedirs(fonts_dir, exist_ok=True)

    print("Fetching font CSS...", FONT_CSS_URL)
    css = fetch(FONT_CSS_URL)

    urls = sorted(set(re.findall(r"https://fonts\.gstatic\.com[^)\"']+", css)))
    if not urls:
        print("No font URLs found, aborting.")
        sys.exit(1)

    for url in urls:
        fname = os.path.basename(url.split("?")[0])
        dest = os.path.join(fonts_dir, fname)
        if os.path.exists(dest):
            print(f"Skipping existing: {fname}")
            continue
        print(f"Downloading {fname}...")
        download(url, dest)

    # Replace remote URLs with local relative paths
    def repl(m):
        full = m.group(0)
        basename = os.path.basename(full.split("?")[0])
        return f"fonts/{basename}"

    local_css = re.sub(r"https://fonts\.gstatic\.com[^)\"']+", repl, css)

    out_path = os.path.join(cwd, "fonts.css")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(local_css)

    print("Wrote", out_path)
    print("Downloaded files:")
    for p in sorted(os.listdir(fonts_dir)):
        print(" -", p)


if __name__ == "__main__":
    main()
