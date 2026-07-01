#!/usr/bin/env python3
"""
Regenerates sitemap.xml from the .html files in the repo root.

- lastmod: pulled from the file's last git commit date (falls back to today).
- priority: from PRIORITY_MAP below; anything not listed gets DEFAULT_PRIORITY.
- Excludes files in EXCLUDE.

Run from the repo root: python generate_sitemap.py
"""
import subprocess
import sys
from datetime import date
from pathlib import Path

DOMAIN = "https://www.timespancalculator.com"
CHANGEFREQ = "monthly"
DEFAULT_PRIORITY = "0.6"

PRIORITY_MAP = {
    "index.html": "1.0",
    "calculator.html": "0.9",
    "about.html": "0.7",
    "contact.html": "0.5",
}

EXCLUDE = {"404.html"}

REPO_ROOT = Path(__file__).resolve().parent


def git_lastmod(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=format:%Y-%m-%d", "--", str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return date.today().isoformat()


def url_for(path: Path) -> str:
    if path.name == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{path.name}"


def main() -> None:
    html_files = sorted(
        p for p in REPO_ROOT.glob("*.html") if p.name not in EXCLUDE
    )
    if not html_files:
        print("No .html files found - aborting.", file=sys.stderr)
        sys.exit(1)

    # index.html first, then by priority (desc), then alphabetical
    html_files.sort(
        key=lambda p: (
            p.name != "index.html",
            -float(PRIORITY_MAP.get(p.name, DEFAULT_PRIORITY)),
            p.name,
        )
    )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "",
    ]
    for f in html_files:
        lines.append("  <url>")
        lines.append(f"    <loc>{url_for(f)}</loc>")
        lines.append(f"    <lastmod>{git_lastmod(f)}</lastmod>")
        lines.append(f"    <changefreq>{CHANGEFREQ}</changefreq>")
        lines.append(f"    <priority>{PRIORITY_MAP.get(f.name, DEFAULT_PRIORITY)}</priority>")
        lines.append("  </url>")
        lines.append("")
    lines.append("</urlset>")

    out_path = REPO_ROOT / "sitemap.xml"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} with {len(html_files)} URLs.")


if __name__ == "__main__":
    main()
