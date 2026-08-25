"""Assemble docs/ — the GitHub Pages site that serves the lecture slides.

GitHub will not render an HTML file stored in a repository: clicking one shows
the source, and the raw URL is served as text/plain. Pages is the way round
that, and it needs the rendered HTML committed under docs/.

Run after rendering the decks:

    scripts/render_session_lectures.sh
    python scripts/build_docs.py

Then in the repository: Settings -> Pages -> Deploy from a branch -> main /docs.

Each deck is already self-contained (`embed-resources: true`), so copying the
file is the whole deployment step. There is no build system to maintain.
"""

import glob
import html
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/warint/quantitative-methods"

# Session number -> (title, one-line description) for the landing page.
SESSIONS = {
    "02": ("Exploratory Data Analysis",
           "Centre, spread and shape — mean, median, trimmed mean, variance, IQR, "
           "skewness, kurtosis"),
    "03": ("Adequacy, Validity and Robustness",
           "Residual diagnostics, goodness of fit, influence, information criteria"),
    "04": ("Logistic Regression",
           "Binary, ordinal and multinomial outcomes in international business research"),
    "05": ("Ridge, Lasso and the Elastic Net",
           "Regularisation: shrinkage, sparsity and the grouping effect"),
    "06": ("Regression: Advanced Considerations",
           "Panel data, non-linearity, categorical variables and interactions"),
    "07": ("Principal Component and Factor Analyses",
           "Dimension reduction, and when to use which"),
    "08": ("KNN and Friends",
           "The Bayes classifier, k-nearest neighbours and the bias–variance trade-off"),
    "09": ("Structural Equation Modelling",
           "Measurement models, structural models and mediation"),
    "10": ("Causal Inference (1/2)",
           "Counterfactuals, randomised trials, matching and propensity scores"),
    "11": ("Causal Inference (2/2)",
           "Difference-in-differences and instrumental variables"),
}

STYLE = """
  :root { --bg:#F7F6F3; --ink:#16181A; --muted:#6E7275; --line:#DEDCD6; --accent:#1C73C5; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#16181A; --ink:#F7F6F3; --muted:#9AA0A6; --line:#2C2F33; --accent:#8FB2FF; }
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.6 "IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
  .wrap { max-width:820px; margin:0 auto; padding:4rem 1.5rem 5rem; }
  h1 { font-size:1.9rem; line-height:1.25; margin:0 0 .4rem; letter-spacing:-.01em; }
  .sub { color:var(--muted); margin:0 0 .4rem; }
  .by { color:var(--muted); font-size:.92rem; margin:0 0 2.5rem; }
  .card { display:flex; gap:1rem; align-items:flex-start; text-decoration:none; color:inherit;
    padding:1rem 1.1rem; border:1px solid var(--line); border-radius:10px; margin-bottom:.6rem;
    transition:border-color .15s, transform .15s; }
  .card:hover { border-color:var(--accent); transform:translateY(-1px); }
  .num { font-variant-numeric:tabular-nums; font-weight:700; color:var(--accent);
    min-width:2.1rem; font-size:1.05rem; padding-top:.05rem; }
  .body { display:flex; flex-direction:column; flex:1; }
  .blurb { color:var(--muted); font-size:.9rem; margin-top:.15rem; }
  .go { color:var(--muted); font-size:.85rem; white-space:nowrap; padding-top:.15rem; }
  .card:hover .go { color:var(--accent); }
  footer { margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--line);
    color:var(--muted); font-size:.88rem; }
  a.plain { color:var(--accent); }
"""


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").touch()   # skip Jekyll: nothing here needs processing

    pattern = str(ROOT / "[0-9][0-9]-*/01-lecture/MATH60033A-S*-Lecture.html")
    decks = sorted(glob.glob(pattern))
    if not decks:
        raise SystemExit("No rendered decks found — run scripts/render_session_lectures.sh first.")

    rows = []
    for src in decks:
        num = re.search(r"-S(\d\d)-", os.path.basename(src)).group(1)
        if num not in SESSIONS:
            print(f"  skipping unknown session {num}")
            continue
        dest = DOCS / f"session-{num}-lecture.html"
        shutil.copy2(src, dest)
        title, blurb = SESSIONS[num]
        rows.append((num, title, blurb, dest.name, dest.stat().st_size))

    cards = "\n".join(
        f'''    <a class="card" href="{fn}">
      <span class="num">{num}</span>
      <span class="body"><strong>{html.escape(title)}</strong>'''
        f'''<span class="blurb">{html.escape(blurb)}</span></span>
      <span class="go">Open →</span>
    </a>'''
        for num, title, blurb, fn, _ in rows)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quantitative Methods in International Business — Lecture slides</title>
<style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    <h1>Quantitative Methods in International Business</h1>
    <p class="sub">Lecture slides — MATH60033A</p>
    <p class="by">Thierry Warin, PhD · HEC Montréal</p>
{cards}
    <footer>
      Slides open in the browser; press <strong>F</strong> for full screen, <strong>S</strong> for
      speaker notes, <strong>Esc</strong> for the overview.<br>
      Course materials, notes and practice briefs:
      <a class="plain" href="{REPO_URL}">github.com/warint/quantitative-methods</a>
    </footer>
  </div>
</body>
</html>
"""
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    total = sum(size for *_, size in rows) / 1e6
    print(f"docs/ built: {len(rows)} decks + index, {total:.0f} MB")
    for num, title, _, fn, size in rows:
        print(f"   {num}  {size/1e6:5.1f} MB  {fn:26s} {title}")


if __name__ == "__main__":
    main()
