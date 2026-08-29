"""Write the standard opening slides into every session deck.

    python scripts/build_deck_frontmatter.py             # every deck
    python scripts/build_deck_frontmatter.py 03          # one session
    python scripts/build_deck_frontmatter.py --check     # report, change nothing

Every deck in the course opens the same way, so that a student arriving at
session nine already knows where to look for what the hour is for:

  1. **Outline** — the sections of this deck, derived from the deck itself.
  2. **What this session is for** — the goals, in three registers side by side:
     the mathematics, the Python, and the international-business claim it
     licenses. Authored in `slides/deck-plan.yml`, so the three stay parallel
     across twelve weeks instead of drifting into whatever each deck felt like.
  3. **Your Python so far** — the functions taught in *earlier* sessions, on the
     lecture and practice decks. A cumulative toolkit, so the code on the slide
     is never the first time a name has been seen.

The slides are written between HTML markers and regenerated in place, so this
can be re-run after any edit to a deck and the block will be rebuilt rather than
duplicated. Everything outside the markers is left exactly as it was.

Two things are computed rather than authored, because authored copies of them go
stale silently:

**The outline** comes from the deck's own section slides — the `.center` divider
slides these decks already use to separate their parts. Reorder the deck and the
outline follows. `outline:` in the plan file overrides this when the derived one
reads badly.

**The toolkit** comes from TOOLKIT below, a curated registry of the Python worth
recalling, keyed to the session that introduced it. `--check` re-derives the real
API surface from every code block in the repository and reports two kinds of
drift: a registry entry the code no longer contains, and a name the code uses
often that the registry has never heard of. The registry is curated rather than
extracted because the extracted surface is 400 names wide and most of it is
`ax.set_xticklabels`.
"""

import ast
import re
import sys
from collections import OrderedDict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "slides" / "deck-plan.yml"

BEGIN = "<!-- BEGIN deck-frontmatter · scripts/build_deck_frontmatter.py -->"
END = "<!-- END deck-frontmatter -->"

# Deck kinds, in the order a student meets them within a session. `toolkit` says
# whether the cumulative Python recap belongs on that deck: it does where code
# gets written or read, and not on the pre-session deck, which is a reading and
# a download.
KINDS = OrderedDict([
    ("00-pre-session", {"label": "Pre-session", "toolkit": False}),
    ("01-lecture", {"label": "Lecture", "toolkit": True}),
    ("02-practice", {"label": "Practice", "toolkit": True}),
])

# ---------------------------------------------------------------------------
# The toolkit registry.
#
#   canonical name -> (session that introduced it, group, one-line gloss)
#
# Groups are tasks rather than libraries, because a student looking for "how do
# I get the coefficients out" does not know or care that `.params` is
# statsmodels and `.coef_` is scikit-learn — and the fact that those two exist
# side by side, spelled differently, for the same idea, is itself worth showing.
GROUPS = ["Load and shape", "Describe", "Fit", "Read the fit", "Diagnose",
          "Choose and validate", "Plot"]

TOOLKIT = {
    # ---- Session 02 · exploratory data analysis --------------------------
    "qmib.load": ("02", "Load and shape", "a course dataset, by name"),
    "pd.read_parquet": ("02", "Load and shape", "a parquet file, directly"),
    ".dropna": ("02", "Load and shape", "drop rows with missing values"),
    ".merge": ("02", "Load and shape", "join two frames on a key"),
    ".shape": ("02", "Load and shape", "rows and columns"),
    ".mean / .median": ("02", "Describe", "the two centres, and their gap"),
    ".std / .var": ("02", "Describe", "spread, dividing by $n-1$"),
    ".quantile": ("02", "Describe", "any quantile, including the median"),
    "stats.trim_mean": ("02", "Describe", "the mean after cutting both tails"),
    "smf.ols": ("02", "Fit", "least squares, from a formula"),
    ".fit()": ("02", "Fit", "estimate the model you specified"),
    ".params": ("02", "Read the fit", "the coefficients, in units of $y$"),
    ".rsquared": ("02", "Read the fit", "share of variance explained"),
    "plt.scatter": ("02", "Plot", "the data, before anything else"),
    "plt.xlabel / plt.ylabel": ("02", "Plot", "say the units, every time"),

    # ---- Session 03 · adequacy and validity ------------------------------
    ".get_influence()": ("03", "Diagnose", "the whole diagnostic bundle"),
    ".hat_matrix_diag": ("03", "Diagnose", "leverage; sums to $p$, always"),
    ".cooks_distance": ("03", "Diagnose", "influence: leverage $\\times$ residual"),
    ".resid_studentized_internal": ("03", "Diagnose", "residuals on a common scale"),
    ".resid / .fittedvalues": ("03", "Read the fit", "what is left, and what was predicted"),
    ".rsquared_adj": ("03", "Read the fit", "penalised for the extra predictor"),
    ".mse_resid": ("03", "Read the fit", "its square root is the RSE, in units"),
    ".aic / .bic": ("03", "Choose and validate", "compare non-nested models"),
    "plt.axhline / plt.axvline": ("03", "Plot", "draw the threshold you are judging against"),
    "plt.stem": ("03", "Plot", "one spike per observation"),

    # ---- Session 04 · logistic, ordinal, multinomial ---------------------
    "smf.logit": ("04", "Fit", "binary outcome, from a formula"),
    "OrderedModel": ("04", "Fit", "ordered categories, proportional odds"),
    "sm.MNLogit": ("04", "Fit", "unordered categories, one baseline"),
    "sm.add_constant": ("04", "Fit", "the intercept, when there is no formula"),
    ".predict": ("04", "Read the fit", "fitted probabilities, not classes"),
    ".get_prediction": ("04", "Read the fit", "with an interval, via `.summary_frame()`"),
    ".llf": ("04", "Choose and validate", "log-likelihood, for the LR test"),
    "np.exp": ("04", "Read the fit", "a log-odds becomes an odds ratio"),
    "stats.chi2.sf": ("04", "Choose and validate", "the $p$-value of that test"),
    "pd.get_dummies": ("04", "Load and shape", "categories to indicator columns"),
    "pd.crosstab": ("04", "Describe", "a contingency table in one call"),
    ".value_counts": ("04", "Describe", "how unbalanced is the outcome"),
    "plt.subplots": ("04", "Plot", "several panels, one figure"),

    # ---- Session 05 · regularisation -------------------------------------
    "StandardScaler": ("05", "Load and shape", "standardise before you penalise"),
    "make_pipeline": ("05", "Load and shape", "so the scaler is fitted on train only"),
    "Ridge / Lasso / ElasticNet": ("05", "Fit", "the three penalties"),
    "RidgeCV / LassoCV / ElasticNetCV": ("05", "Choose and validate", "$\\lambda$ by cross-validation"),
    "lasso_path": ("05", "Choose and validate", "the whole coefficient path"),
    "train_test_split": ("05", "Choose and validate", "hold something back"),
    "KFold": ("05", "Choose and validate", "and do it $k$ times"),
    "mean_squared_error": ("05", "Choose and validate", "score it on the held-out part"),
    ".coef_ / .alpha_": ("05", "Read the fit", "scikit-learn's spelling of `.params`"),
    "np.logspace": ("05", "Choose and validate", "a grid that is even in $\\log\\lambda$"),

    # ---- Session 09 · structural equation modelling ----------------------
    "semopy.Model": ("09", "Fit", "from a model description string"),
    ".inspect()": ("09", "Read the fit", "loadings and paths, estimated"),
    "semopy.calc_stats": ("09", "Choose and validate", "CFI, TLI, RMSEA — report all three"),
    "np.cov": ("09", "Describe", "the matrix the model is trying to reproduce"),

    # ---- Session 10 · causal foundations ---------------------------------
    "expit": ("10", "Fit", "the inverse logit, when you need it directly"),
    "NearestNeighbors": ("10", "Choose and validate", "match treated to control"),
    ".kneighbors": ("10", "Choose and validate", "who got matched to whom"),
    "pd.concat": ("10", "Load and shape", "stack the matched sample back together"),
    ".boxplot": ("10", "Plot", "balance, before and after matching"),
}


# ---------------------------------------------------------------------------
# Reading decks

FENCE = re.compile(
    r"^```\{python\}\n(.*?)^```$"                 # a live cell
    r"|^``` \{\.sourceCode[^\n]*\n(.*?)^```$"     # an imported static block
    r"|^```python\n(.*?)^```$",                   # a plain fence
    re.S | re.M)

# A slide header: "## Title {#id .center .scrollable}"
HEADER = re.compile(r"^## +(.*?)(?: *\{([^}]*)\})? *$", re.M)

# Headers that are structure rather than content, and never belong in an outline.
SKIP_TITLES = re.compile(
    r"^(outline|references?|course objectives|your python so far|"
    r"what this session is for|thank you|questions?|end)\b", re.I)


def decks():
    """Every deck in the repository, as (session, kind, path)."""
    for d in sorted(ROOT.glob("[01][0-9]-*")):
        if not d.is_dir():
            continue
        for kind in KINDS:
            for q in sorted((d / kind).glob("*.qmd")) if (d / kind).is_dir() else []:
                # Session decks are named MATH60033A-Snn-<Kind>.qmd. Anything
                # else in these folders is a standing supplement — the GitHub
                # and teamwork walkthrough, for one — which has no session goals.
                if not q.name.startswith("MATH60033A-"):
                    continue
                yield d.name[:2], kind, q


def strip_block(text):
    """Remove a previously generated block, so this script is idempotent."""
    return re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", "",
                  text, flags=re.S)


def clean_title(raw):
    """Turn a slide header into something readable in an outline.

    The imported decks carry pandoc's rendering of inline maths — a title can
    arrive as `Adjusted [\\(R\\^2\\)]{.math .inline} and RSE`. Outlines want the
    words, so the maths is reduced to a placeholder rather than reproduced.
    """
    # Pandoc wrote inline maths as `[\\(R\\^2\\)]{.math .inline}` when these decks
    # were imported. Recover the TeX and put it back in dollars.
    t = re.sub(r"\[\\\\\((.*?)\\\\\)\]\{[^}]*\}",
               lambda m: "$" + m.group(1).replace("\\^", "^") + "$", raw)
    t = re.sub(r"\{[^}]*\}", "", t)                 # the attribute block
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t)          # bold inside a title
    t = re.sub(r"^\d+(?:\\?\.\d+)*\\?\.?\s+", "", t)    # "2\. " and "2.2 "
    t = t.replace(chr(92) + chr(39), chr(39))        # pandoc escapes apostrophes
    t = re.sub(r"\s*-{2,}\s*", " \u2014 ", t)          # "Model --- Maximise"
    t = re.sub(r"\s+", " ", t).strip(" -\u2014\u00b7:")
    return t


def outline_of(text):
    """The deck's sections, taken from its own `.center` divider slides.

    These decks use a `.center` slide to open each part — that is exactly an
    outline, already written and already in the right order. Where a deck has no
    dividers, every slide title is used instead, which is only sensible on the
    short decks that lack dividers in the first place.
    """
    heads = [(clean_title(m.group(1)), (m.group(2) or "")) for m in HEADER.finditer(text)]
    heads = [(t, c) for t, c in heads if t and not SKIP_TITLES.match(t)]
    dividers = [t for t, c in heads if "center" in c]
    chosen = dividers if len(dividers) >= 3 else [t for t, _ in heads]

    seen, out = set(), []
    for t in chosen:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def api_names(code):
    """Every call and attribute in one code block, as written."""
    out = set()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return out
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            out |= {a.name for a in n.names}
            out |= {f"{n.module}.{a.name}" for a in n.names if n.module}
        elif isinstance(n, ast.Attribute):
            out.add("." + n.attr)
            if isinstance(n.value, ast.Name):
                out.add(f"{n.value.id}.{n.attr}")
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            out.add(n.func.id)
    return out


def surface():
    """The real API surface, per session, from every code block in the repo."""
    per = {}
    for sess, _kind, q in decks():
        got = per.setdefault(sess, set())
        for m in FENCE.finditer(q.read_text()):
            body = next(g for g in m.groups() if g is not None)
            got |= api_names("\n".join(
                l for l in body.splitlines() if not l.lstrip().startswith("#|")))
    return per


# ---------------------------------------------------------------------------
# Writing the block

def render_outline(items, kind):
    what = {"00-pre-session": "Before class", "01-lecture": "The hour ahead",
            "02-practice": "The workshop"}[kind]
    body = "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))
    return f"## Outline · {what} {{.center .scrollable}}\n\n{body}\n"


def render_goals(goals, sess):
    cols = [("The mathematics", goals.get("maths", [])),
            ("The Python", goals.get("python", [])),
            ("The international business", goals.get("ib", []))]
    parts = [f"## What session {int(sess)} is for {{.scrollable}}\n",
             '::::: columns\n']
    for title, items in cols:
        bullets = "\n".join(f"- {b}" for b in items)
        parts.append(f'\n:::: {{.column width="33%"}}\n\n### {title}\n\n{bullets}\n\n::::\n')
    parts.append("\n:::::\n")
    return "".join(parts)


def render_toolkit(sess):
    """The Python taught before this session, grouped by what it is for."""
    earlier = {k: v for k, v in TOOLKIT.items() if v[0] < sess}
    if not earlier:
        return None

    newest = max(v[0] for v in earlier.values())
    by_group = OrderedDict((g, []) for g in GROUPS)
    for name, (when, group, gloss) in sorted(earlier.items(), key=lambda kv: (kv[1][0], kv[0])):
        by_group[group].append((name, when, gloss))
    by_group = OrderedDict((g, v) for g, v in by_group.items() if v)

    oldest = min(v[0] for v in earlier.values())
    # Marking the newest session's entries only helps when there is something to
    # contrast them with. On the first toolkit slide everything is new, and
    # saying so about every line says nothing.
    mark_new = oldest != newest

    rows = []
    for group, entries in by_group.items():
        rows.append(f"\n### {group}\n")
        for name, when, gloss in entries:
            mark = f" · *new in session {int(newest)}*" if mark_new and when == newest else ""
            rows.append(f"- `{name}` — {gloss}{mark}")

    n = len(earlier)
    where = (f"session {int(oldest)}" if oldest == newest
             else f"sessions {int(oldest)}–{int(newest)}")
    lead = (f"The {n} names below came out of {where}. Today's slides assume them, "
            "and add to them.")
    if mark_new:
        lead += f" The ones marked are the newest, from session {int(newest)}."
    return f"## Your Python so far {{.scrollable}}\n\n{lead}\n" + "\n".join(rows) + "\n"


def block_for(sess, kind, text, plan):
    parts = []
    # An `outline:` in the plan file overrides the derivation. A bare list means
    # the lecture deck, which is the one that usually needs the help; a mapping
    # keyed by deck kind overrides a specific deck.
    override = plan.get("outline")
    if isinstance(override, dict):
        items = override.get(kind)
    elif isinstance(override, list) and kind == "01-lecture":
        items = override
    else:
        items = None
    items = items or outline_of(strip_block(text))
    if items:
        parts.append(render_outline(items, kind))
    if any(plan.get(k) for k in ("maths", "python", "ib")):
        parts.append(render_goals(plan, sess))
    if KINDS[kind]["toolkit"]:
        tk = render_toolkit(sess)
        if tk:
            parts.append(tk)
    if not parts:
        return None
    return BEGIN + "\n\n" + "\n".join(parts) + "\n" + END + "\n\n"


def insert(text, block):
    """Put the block after the YAML header and any setup cell, before slide one.

    A deck opens with its YAML, sometimes a comment explaining the import, and
    sometimes an `#| label: setup` cell that must run before anything else. The
    block goes after all of that and before the first real slide, so the setup
    cell keeps its place at the top.
    """
    text = strip_block(text)

    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    at = m.end() if m else 0

    # Skip a leading comment and a setup cell, if they are there.
    rest = text[at:]
    for pat in (r"^\s*<!--.*?-->\n", r"^\s*```\{python\}\n.*?^```\n"):
        m2 = re.match(pat, rest, re.S | re.M)
        if m2:
            at += m2.end()
            rest = text[at:]

    return text[:at] + "\n" + block + text[at:].lstrip("\n")


def drop_superseded(text):
    """Remove the slides the generated block replaces, and say which.

    Two kinds go: the deck's own `Outline`, and its `Learning objectives` or
    `Goals` slide. Both are now written by this script, and the imported ones
    were also the last place in these decks still promising to estimate things
    "in R using the lavaan package" — the course is Python.

    A slide is only removed when its body is prose and bullets. If it carries a
    figure or a code cell it is content rather than a heading, and it is left
    alone so that nothing is lost silently.
    """
    removed = []
    # Case-insensitive: the imported decks spell it "Outline" in one place and
    # "outline" in another.
    pattern = re.compile(
        r"^## +(Outline|Learning objectives|Goals)\b[^\n]*\n(.*?)(?=^#{1,6} |\Z)",
        re.S | re.M | re.I)

    while True:
        m = pattern.search(text)
        if not m:
            return text, removed
        body = m.group(2)
        if "![" in body or "```" in body:
            # Keep it, and stop looking: scanning past it would need an offset
            # and there is at most one of each in these decks.
            return text, removed
        removed.append(m.group(1))
        text = text[:m.start()] + text[m.end():]


def main():
    args = sys.argv[1:]
    check = "--check" in args
    only = next((a for a in args if a.isdigit()), None)

    plans = yaml.safe_load(PLAN.read_text())
    plans = {f"{int(k):02d}": v for k, v in plans.items()}

    if check:
        real = surface()
        cumulative, unknown = set(), {}
        for sess in sorted(real):
            cumulative |= real[sess]
        print("── registry entries the code no longer contains")
        for name, (when, _g, _d) in sorted(TOOLKIT.items()):
            probes = [p.strip() for p in name.replace("/", " ").split()]
            probes = [p if p.startswith((".", "np.", "pd.", "plt.", "sm.", "smf.", "stats.", "semopy.", "qmib."))
                      else p for p in probes]
            # `stats.chi2.sf` is parsed as `.sf` on an attribute chain, so a
            # three-level name is matched on its last segment too.
            def seen(name):
                n = name.rstrip("()")
                return (n in cumulative or n + "()" in cumulative
                        or ("." + n.rsplit(".", 1)[-1]) in cumulative)
            hit = any(seen(p) for p in probes)
            if not hit:
                print(f"     S{when}  {name}")
        print("\n── frequent names the registry has never heard of")
        known = " ".join(TOOLKIT)
        for sess in sorted(real):
            new = {n for n in real[sess]
                   if n.startswith((".", "np.", "pd.", "plt.", "sm.", "smf."))
                   and n not in known and len(n) > 4}
            if new:
                unknown[sess] = sorted(new)[:14]
        for sess, names in unknown.items():
            print(f"     S{sess}  {', '.join(names)}")
        return

    touched = 0
    for sess, kind, q in decks():
        if only and sess != only:
            continue
        plan = plans.get(sess)
        if not plan:
            continue
        text = q.read_text()
        # Drop the deck's own Outline slide first: the generated block contains
        # one too, and removing afterwards would take the new one with it.
        base, dropped = drop_superseded(strip_block(text))
        block = block_for(sess, kind, base, plan)
        if not block:
            continue
        out = insert(base, block)
        if out != text:
            q.write_text(out)
            touched += 1
            note = f"  (removed: {', '.join(dropped)})" if dropped else ""
            print(f"  {q.relative_to(ROOT)}{note}")

    print(f"\n{touched} decks updated")


if __name__ == "__main__":
    main()
