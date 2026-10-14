"""Build the per-package Python cheatsheets: one landscape PDF per package.

    python scripts/build_package_cheatsheets.py            # every package
    python scripts/build_package_cheatsheets.py pandas     # one package

Why this exists
---------------
The session cheatsheets (PYTHON-CHEATSHEET.pdf, one per session) list every name
taught so far, one line each. They answer "what did we type?". These answer a
different question — "what does this function do, and what does its result look
like?" — one package at a time, in the spirit of the RStudio cheatsheets: boxed
sections, a plain sentence per function, a line of code, and small pictures of
what the operation does or produces, drawn on the course data.

Only the functions this course uses, or that a student of it will want next.

How it works
------------
Each package's content is a Python module in python-cheatsheets/src/sheet_<pkg>.py with
two names: META (title, colour, import line, sessions) and SECTIONS (boxes of
entries; a box may carry a figure — a matplotlib function or an SVG string). This
script lays them out as HTML in three columns on landscape US Letter pages, then
prints the HTML to PDF with the Chrome already on the machine (no new Python
package). Figures are embedded, so each PDF stands alone.

Output: python-cheatsheets/<pkg>.pdf. scripts/build_docs.py publishes them.
"""

import base64
import html
import os
import importlib.util
import io
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")   # draw off-screen: never open a window

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "python-cheatsheets" / "src"
OUT = ROOT / "python-cheatsheets"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "slides"))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

SITE = "https://warint.github.io/quantitative-methods/"

CSS = """
@page { size: 11in 8.5in; margin: 0.32in 0.34in 0.36in 0.34in; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 7.6pt;
       line-height: 1.28; color: #222; margin: 0; }
header { display: flex; align-items: center; gap: 14px; padding: 0 0 6px 0;
         border-bottom: 3px solid var(--accent); margin-bottom: 7px; }
header .logo { background: var(--accent); color: #fff; font-weight: 800; font-size: 22pt;
               padding: 4px 12px 6px; border-radius: 6px; letter-spacing: -0.5px; }
header .tag { font-size: 10.5pt; font-weight: 600; color: #222; }
header .sub { font-size: 7.5pt; color: #6b6b67; margin-top: 2px; }
header .imp { margin-left: auto; text-align: right; }
header .imp code { background: #f2efe8; border: 1px solid #ddd6c8; padding: 3px 7px;
                   border-radius: 4px; font-size: 8.5pt; display: block; margin-bottom: 2px; }
header .imp span { font-size: 6.8pt; color: #6b6b67; }
.cols { column-count: 3; column-gap: 9px; column-fill: auto; height: 6.86in; overflow: hidden; }
.page2 .cols { height: 7.5in; }
section { height: 7.78in; position: relative; }
.box { break-inside: avoid; border: 1.4px solid var(--accent); border-radius: 6px;
       margin: 0 0 8px 0; background: #fff; overflow: hidden; }
.box h2 { margin: 0; background: var(--accent); color: #fff; font-size: 9pt; padding: 3px 8px;
          font-weight: 700; letter-spacing: 0.1px; }
.box .intro { padding: 4px 8px 2px; color: #444; font-style: italic; }
.box .fig { text-align: center; padding: 3px 6px 0; }
.box .fig img, .box .fig svg { max-width: 100%; }
.entry { padding: 3px 8px 3px; border-top: 1px dotted #d9d4c7; }
.entry:first-of-type { border-top: none; }
.entry .code { font-family: Menlo, Consolas, monospace; font-size: 7.6pt; font-weight: 700;
               color: var(--accent); }
.entry .text { margin-top: 1px; }
.entry .ex { font-family: Menlo, Consolas, monospace; font-size: 6.9pt; color: #333;
             background: #f7f4ed; border-left: 2px solid var(--accent); padding: 2px 5px;
             margin-top: 2px; white-space: pre-wrap; }
.warn { margin: 3px 8px 5px; padding: 3px 6px; background: #fdecea; border-left: 3px solid #e3120b;
        font-size: 7.2pt; }
.tip { margin: 3px 8px 5px; padding: 3px 6px; background: #e8f3ee; border-left: 3px solid #2e8b57;
       font-size: 7.2pt; }
.foot { position: absolute; bottom: 0; left: 0; right: 0; font-size: 6.5pt; color: #6b6b67;
         display: flex; justify-content: space-between; border-top: 1px solid #ddd6c8; padding-top: 2px; }
.page2 { break-before: page; }
"""


def chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    raise SystemExit("Chrome or Chromium not found: install one to print the cheatsheets to PDF.")


def png(fig):
    import matplotlib.pyplot as plt
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def inline(text):
    """`code`, **bold** and *italic* in the prose."""
    t = html.escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)
    return t


def figure(spec, width):
    if spec is None:
        return ""
    if callable(spec):
        spec = spec()                          # a diagram (SVG string) or a matplotlib figure
    if isinstance(spec, str):
        return f'<div class="fig">{spec}</div>'
    return f'<div class="fig"><img src="{png(spec)}" style="width:{width}"></div>'


def box(sec):
    parts = [f'<div class="box"><h2>{inline(sec["title"])}</h2>']
    if sec.get("intro"):
        parts.append(f'<div class="intro">{inline(sec["intro"])}</div>')
    if sec.get("figure_top") is not None:
        parts.append(figure(sec["figure_top"], sec.get("fig_width", "96%")))
    for e in sec.get("items", []):
        ex = f'<div class="ex">{html.escape(e["ex"])}</div>' if e.get("ex") else ""
        parts.append(f'<div class="entry"><div class="code">{html.escape(e["code"])}</div>'
                     f'<div class="text">{inline(e["text"])}</div>{ex}</div>')
    if sec.get("figure") is not None:
        parts.append(figure(sec["figure"], sec.get("fig_width", "96%")))
    if sec.get("tip"):
        parts.append(f'<div class="tip">{inline(sec["tip"])}</div>')
    if sec.get("warn"):
        parts.append(f'<div class="warn">{inline(sec["warn"])}</div>')
    parts.append("</div>")
    return "\n".join(parts)


def page(meta, sections, first):
    head = ""
    if first:
        head = f"""<header>
  <div class="logo">{html.escape(meta['title'])}</div>
  <div><div class="tag">{inline(meta['tagline'])}</div>
       <div class="sub">Python cheatsheet · MATH60033A · Quantitative Methods in IB · used in
       {'session' if str(meta['sessions']).strip().isdigit() else 'sessions'} {meta['sessions']}</div></div>
  <div class="imp"><code>{html.escape(meta['import'])}</code>
       <span>{inline(meta.get('version_note', ''))}</span></div>
</header>"""
    body = "\n".join(box(s) for s in sections)
    cls = "" if first else ' class="page2"'
    foot = (f'<div class="foot"><span>{html.escape(meta["title"])} · MATH60033A · Quantitative Methods in IB · '
            f'Thierry Warin, PhD · HEC Montréal</span><span>All the cheatsheets: {SITE}python-cheatsheets/</span></div>')
    return f'<section{cls}>{head}<div class="cols">{body}</div>{foot}</section>'


def build(pkg):
    spec = importlib.util.spec_from_file_location(f"sheet_{pkg}", SRC / f"sheet_{pkg}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    meta = mod.META
    pages = mod.PAGES                     # a list of pages, each a list of sections
    body = "\n".join(page(meta, secs, i == 0) for i, secs in enumerate(pages))
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>{meta['title']} cheatsheet</title>
<style>:root {{ --accent: {meta['color']}; }} {CSS}</style></head><body>
{body}
</body></html>"""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"{pkg}.html"
        src.write_text(doc, encoding="utf-8")
        out = OUT / f"{pkg}.pdf"
        subprocess.run([chrome(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf-no-header", f"--print-to-pdf={out}", src.as_uri()],
                       check=True, capture_output=True)
        (OUT / "html").mkdir(exist_ok=True)
        shutil.copy2(src, OUT / "html" / f"{pkg}.html")   # for review; git-ignored
    print(f"  {out.relative_to(ROOT)}")


def main():
    wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    pkgs = wanted or sorted(p.stem.removeprefix("sheet_") for p in SRC.glob("sheet_*.py"))
    for p in pkgs:
        build(p)


if __name__ == "__main__":
    main()
