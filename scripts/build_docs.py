"""Assemble docs/ — the GitHub Pages site that serves the book and the slides.

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
    "01": ("The Syllabus",
           "What the course asks of you, how you are judged, and the rules on using a "
           "language model"),
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
    "12": ("What the Twelve Weeks Were For",
           "The closing address: what the term established, why it matters in private "
           "and public organisations, and Europe 2031 read with the tools you now have"),
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
  .card.book { border-color:var(--accent); background:rgba(28,115,197,.045);
               margin-bottom:2.2rem; }
  .card.book .num { font-size:1.15rem; }
  .card.book strong { font-size:1.02rem; }
  .row { margin-bottom:.6rem; }
  .row .card { margin-bottom:.25rem; }
  .also { display:block; font-size:.82rem; color:var(--muted);
    padding-left:3.2rem; }
  .also a { color:var(--muted); text-decoration:underline; }
  .also a:hover { color:var(--accent); }
"""


# Every deck links to its neighbours the way a reader browsing the repository
# would want — `../01-lecture/README.md`, `setup-git-and-github.md`. Those are
# correct on GitHub and wrong the moment the page is copied into docs/, which is
# one directory with no session folders under it. Rewriting them on the way out
# means the source keeps the relative links that work where it lives, and the
# published page gets absolute ones that work where it lands.
MD_LINK = re.compile(r'href="((?!https?:|#|mailto:|data:)[^"]{1,200}\.md)"')


def publish_deck(src, dest):
    """Copy a rendered deck into docs/, repointing its relative .md links."""
    src = Path(src)
    here = src.parent.relative_to(ROOT)
    text = src.read_text(encoding="utf-8")

    def fix(m):
        target = os.path.normpath(os.path.join(here, m.group(1)))
        if target.startswith(".."):        # escapes the repository: leave it
            return m.group(0)
        if not (ROOT / target).exists():
            print(f"    {dest.name}: link to a file that does not exist — {m.group(1)}")
        return f'href="{REPO_URL}/blob/main/{target}"'

    fixed, n = MD_LINK.subn(fix, text)
    dest.write_text(fixed, encoding="utf-8")
    shutil.copystat(src, dest)
    return n


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").touch()   # skip Jekyll: nothing here needs processing

    # Publish the data spine alongside the slides, so qmib.REMOTE works from a
    # notebook that has no clone of the repository (Colab, a student's laptop).
    data_out = DOCS / "data"
    data_out.mkdir(exist_ok=True)
    n_data = 0
    for f in sorted((ROOT / "data" / "spine").glob("*.parquet")):
        shutil.copy2(f, data_out / f.name)
        n_data += 1
    print(f"published {n_data} spine files to docs/data/")

    decks = sorted(glob.glob(str(ROOT / "[0-9][0-9]-*/0[0-2]-*/MATH60033A-S*.html")))
    if not decks:
        raise SystemExit("No rendered decks found — run scripts/render_session_lectures.sh first.")

    KINDS = {"Pre-Session": "pre-session", "Lecture": "lecture", "Practice": "practice"}
    extra = {}          # session -> {kind: filename}
    rows = []
    for src in decks:
        base = os.path.basename(src)
        num = re.search(r"-S(\d\d)", base).group(1)
        if num not in SESSIONS:
            print(f"  skipping unknown session {num}")
            continue
        kind = next((v for k, v in KINDS.items() if k in base), None)
        if kind is None:
            continue
        dest = DOCS / f"session-{num}-{kind}.html"
        publish_deck(src, dest)
        if kind == "lecture":
            title, blurb = SESSIONS[num]
            rows.append((num, title, blurb, dest.name, dest.stat().st_size))
        else:
            extra.setdefault(num, {})[kind] = dest.name

    def companions(num):
        got = extra.get(num, {})
        if not got:
            return ""
        bits = " · ".join(f'<a href="{v}">{k.replace("-", " ")}</a>'
                          for k, v in sorted(got.items()))
        return f'<span class="also">also: {bits}</span>'

    cards = "\n".join(
        f'''    <div class="row">
      <a class="card" href="{fn}">
        <span class="num">{num}</span>
        <span class="body"><strong>{html.escape(title)}</strong>'''
        f'''<span class="blurb">{html.escape(blurb)}</span></span>
        <span class="go">Open →</span>
      </a>
      {companions(num)}
    </div>'''
        for num, title, blurb, fn, _ in rows)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quantitative Methods in International Business with Python — MATH60033A</title>
<style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    <h1>Quantitative Methods in International Business with Python</h1>
    <p class="sub">The course book and the lecture slides — MATH60033A</p>
    <p class="by">Thierry Warin, PhD · HEC Montréal</p>

    <a class="card book" href="book/">
      <span class="num">&#9776;</span>
      <span class="body">
        <strong>The course book</strong>
        <span class="blurb">Twelve chapters as continuous prose — every method derived, then
        run in Python on real data. Searchable across the whole course.</span>
      </span>
      <span class="go">Read &rarr;</span>
    </a>

{cards}
    <footer>
      The book is the same material as continuous prose, searchable across every session.
      Slides open in the browser; press <strong>F</strong> for full screen, <strong>S</strong> for
      speaker notes, <strong>Esc</strong> for the overview.<br>
      The same material as a book: <a class="plain" href="book/">the course book</a>.<br>
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
