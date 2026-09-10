"""Write a one-page Python cheatsheet, as a PDF, for every session.

    python scripts/build_cheatsheets.py             # every session
    python scripts/build_cheatsheets.py 03          # one session
    python scripts/build_cheatsheets.py --no-render # write the .qmd, skip LaTeX

Why this exists
---------------
Every lecture deck used to open with "Your Python so far": a cumulative list of
every function taught before that session, on a slide nobody can read from the
back of a room and nobody can copy from. It is reference material, and reference
material belongs on a page beside the keyboard rather than on a slide behind the
speaker.

So each session gets `PYTHON-CHEATSHEET.pdf`, and the deck carries a link to it
instead of the list.

What goes on it
---------------
1. **Starting Python in VS Codium** — the environment, a new file, running it.
   Three platforms, always: `python3` does not exist on Windows and
   `source .venv/bin/activate` is `.venv\\Scripts\\activate` there.
2. **The four things you always do** — build a DataFrame, look at what is in
   it, read a file in, write a CSV out. The same on every sheet, because they
   are the four things a student actually forgets.
3. **Installing a package you do not have** — because the sheet says `read_excel`
   needs openpyxl, and saying that without saying how to get it is half an
   instruction. Recurrent, since the question recurs.
4. **What you have learned so far** — every name taught up to *and including*
   this session, one session at a time, each with a runnable line. Session 03's
   sheet covers sessions 1, 2 and 3: a student holding it is holding everything
   the course has asked them to type, not only last week's half.

Part 4 is driven by TOOLKIT in `build_deck_frontmatter.py`, which is the
registry the deck slide used, so the two can never disagree about *what* was
taught. SNIPPETS below adds the missing half: what it looks like when you type
it. A registry entry with no snippet is a build error rather than a silent gap.
"""

import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_deck_frontmatter import GROUPS, TOOLKIT  # noqa: E402
from course_spec import COHORT, SESSIONS, ordered  # noqa: E402

FILENAME = "PYTHON-CHEATSHEET"


# ---------------------------------------------------------------------------
# One runnable line per registry name.
#
# These are written the way they appear in the session that introduced them, so
# a student who copies a line out of the sheet is copying something that ran on
# the course data rather than a signature from the documentation.

SNIPPETS = {
    # ---- Session 02 -------------------------------------------------------
    "qmib.load": 'core = qmib.load("core")            # a course dataset, by name',
    "pd.read_parquet": 'core = pd.read_parquet("data/spine/core.parquet")',
    ".dropna": 'd = core.dropna(subset=["gdp_pc_eur", "productivity_idx"])\n'
               '# subset= matters: without it a row missing ANY column goes',
    ".merge": 'both = left.merge(right, on=["geo", "time"], how="inner")',
    ".shape": "n_rows, n_cols = core.shape",
    ".mean / .median": "gdp.mean(), gdp.median()      # the gap between them is the finding",
    ".std / .var": "gdp.std(ddof=1), gdp.var(ddof=1)  # ddof=1 divides by n-1",
    ".quantile": "gdp.quantile([0.25, 0.5, 0.75])    # IQR is the third minus the first",
    "stats.trim_mean": "from scipy import stats\n"
                       "stats.trim_mean(gdp, 0.05)        # mean after cutting 5% off each tail",

    # ---- Session 03 -------------------------------------------------------
    "smf.ols": "import statsmodels.formula.api as smf\n"
               'fit = smf.ols("gdp_pc_eur ~ productivity_idx", data=d).fit()\n'
               '# read the ~ as "explained by"; the intercept is added for you',
    ".fit()": "fit = model.fit()                 # .fit() does the arithmetic",
    ".params": "fit.params                        # the coefficients, in units of y",
    ".rsquared": "fit.rsquared                      # share of variance explained",
    ".rsquared_adj": "fit.rsquared_adj                  # penalised for each extra predictor",
    ".mse_resid": "np.sqrt(fit.mse_resid)            # the RSE, in the units of y",
    ".resid / .fittedvalues": "fit.resid, fit.fittedvalues       # what is left, and what was predicted",
    "qmib.regtable": ('print(qmib.regtable([m1, m2], names=["simple", "+ investment"],\n'
                      '                    order=["productivity_idx", "gfcf_meur", "Intercept"]))\n'
                      '# one column per model, stars, SEs beneath, fit stats at the foot.\n'
                      '# .as_latex() for a paper, .as_html() for a slide.'),
    ".get_influence()": "influence = fit.get_influence()    # the whole diagnostic bundle",
    ".hat_matrix_diag": "leverage = influence.hat_matrix_diag        # sums to p, always",
    ".cooks_distance": "cooks_d = influence.cooks_distance[0]       # screen at 4/n",
    ".resid_studentized_internal": "influence.resid_studentized_internal        # on a common scale",
    ".aic / .bic": "fit.aic, fit.bic                  # lower is better, and only relatively",
    "plt.scatter": "import matplotlib.pyplot as plt\n"
                   'plt.scatter(d["productivity_idx"], d["gdp_pc_eur"], s=12, alpha=0.6)',
    "plt.xlabel / plt.ylabel": 'plt.xlabel("Productivity index"); plt.ylabel("GDP per capita (EUR)")\n'
                               "# say the units, every time",
    "plt.axhline / plt.axvline": 'plt.axhline(0, color="black", lw=1)\n'
                                 'plt.axvline(2 * 2 / len(d), color="red", ls="--")   # the 2p/n screen',
    "plt.stem": "plt.stem(cooks_d)                 # one spike per observation",

    # ---- Session 04 -------------------------------------------------------
    "smf.logit": 'fit = smf.logit("default ~ fico + dti", data=d).fit()',
    "OrderedModel": "from statsmodels.miscmodels.ordinal_model import OrderedModel\n"
                    'fit = OrderedModel(y, X, distr="logit").fit(method="bfgs")',
    "sm.MNLogit": "import statsmodels.api as sm\n"
                  "fit = sm.MNLogit(y, sm.add_constant(X)).fit()",
    "sm.add_constant": "X = sm.add_constant(X)            # the intercept, with no formula",
    ".predict": "p = fit.predict(newdata)          # probabilities, not classes",
    ".get_prediction": "fit.get_prediction(newdata).summary_frame()  # with an interval",
    "np.exp": "np.exp(fit.params)                # a log-odds becomes an odds ratio",
    ".llf": "lr = 2 * (full.llf - reduced.llf)  # the likelihood-ratio statistic",
    "stats.chi2.sf": "stats.chi2.sf(lr, df=2)           # its p-value",
    "pd.get_dummies": 'X = pd.get_dummies(d[["grade"]], drop_first=True)',
    "pd.crosstab": 'pd.crosstab(d["grade"], d["default"])',
    ".value_counts": 'd["default"].value_counts(normalize=True)    # how unbalanced is it',
    "plt.subplots": "fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9))",

    # ---- Session 05 -------------------------------------------------------
    "StandardScaler": "from sklearn.preprocessing import StandardScaler\n"
                      "Z = StandardScaler().fit(Xtr).transform(Xtr)   # fit on TRAIN only",
    "make_pipeline": "pipe = make_pipeline(StandardScaler(), Ridge(alpha=1.0))\n"
                     "# so the scaler never sees the held-out fold",
    "Ridge / Lasso / ElasticNet": "Ridge(alpha=1.0).fit(Ztr, ytr)     # Lasso, ElasticNet take the same shape",
    "RidgeCV / LassoCV / ElasticNetCV": "LassoCV(cv=5).fit(Ztr, ytr).alpha_     # lambda by cross-validation",
    "lasso_path": "alphas, coefs, _ = lasso_path(Z, y)    # the whole coefficient path",
    "train_test_split": "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7)",
    "KFold": "KFold(n_splits=5, shuffle=True, random_state=7)",
    "mean_squared_error": "mean_squared_error(yte, model.predict(Zte)) ** 0.5    # RMSE",
    ".coef_ / .alpha_": "model.coef_, model.alpha_         # scikit-learn's spelling of .params",
    "np.logspace": "alphas = np.logspace(-3, 2, 100)   # a grid even in log-lambda",

    # ---- Session 06 -------------------------------------------------------
    "PanelOLS": "from linearmodels.panel import PanelOLS\n"
                'fit = PanelOLS.from_formula("y ~ x + EntityEffects", data=panel).fit()',
    "RandomEffects": 'RandomEffects.from_formula("y ~ 1 + x", data=panel).fit()',
    "I(x**2)": 'smf.ols("price ~ living_area + I(living_area**2)", data=d).fit()',
    "a * b": 'smf.ols("wage ~ age * female", data=d).fit()\n'
             "# a * b expands to a + b + a:b",
    ".compare_f_test": "big.compare_f_test(small)         # nested models only",
    "np.linalg.pinv": "np.linalg.pinv(v_fe - v_re)       # for the Hausman statistic",

    # ---- Session 07 -------------------------------------------------------
    "PCA": "from sklearn.decomposition import PCA\n"
           "p = PCA().fit(Z)                  # on standardised columns",
    ".explained_variance_ratio_": "p.explained_variance_ratio_       # what the scree plot is drawn from",
    ".components_": "p.components_                     # loadings: variables on components",
    "prince.FAMD": "import prince\n"
                   "famd = prince.FAMD(n_components=3).fit(mixed)   # numeric AND categorical",
    "Factor": "from statsmodels.multivariate.factor import Factor\n"
              'f = Factor(df.to_numpy(), n_factor=2, method="ml").fit()',
    ".rotate('varimax')": 'f.rotate("varimax")               # same fit, readable loadings',
    "np.linalg.eigvalsh": "np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False))",

    # ---- Session 08 -------------------------------------------------------
    "KNeighborsClassifier": "KNeighborsClassifier(n_neighbors=15).fit(Xtr, ytr)",
    "KNeighborsRegressor": "KNeighborsRegressor(n_neighbors=15).fit(Xtr, ytr)",
    "GridSearchCV": 'gs = GridSearchCV(knn, {"n_neighbors": range(1, 40)}, cv=5).fit(Xtr, ytr)',
    ".best_params_ / .best_score_": "gs.best_params_, gs.best_score_   # what it chose, and how it scored",
    "cross_val_score": 'cross_val_score(model, X, y, cv=5, scoring="accuracy").mean()',
    "permutation_importance": "permutation_importance(model, Xte, yte, n_repeats=10).importances_mean",
    "confusion_matrix": "confusion_matrix(yte, model.predict(Xte))   # the four cells accuracy hides",
    "classification_report": "print(classification_report(yte, model.predict(Xte)))",
    "RandomForestClassifier": "RandomForestClassifier(n_estimators=500, random_state=7).fit(Xtr, ytr)",

    # ---- Session 09 -------------------------------------------------------
    "semopy.Model": "import semopy\n"
                    "m = semopy.Model(desc); m.fit(df)   # desc is the model description string",
    ".inspect()": "m.inspect()                       # loadings and paths, estimated",
    "semopy.calc_stats": "semopy.calc_stats(m)              # CFI, TLI, RMSEA — report all three",
    "np.cov": "np.cov(df.to_numpy(), rowvar=False)   # the matrix the model reproduces",

    # ---- Session 10 -------------------------------------------------------
    "expit": "from scipy.special import expit\n"
             "p = expit(X @ beta)               # the inverse logit",
    "NearestNeighbors": "nn = NearestNeighbors(n_neighbors=1).fit(ps_control.reshape(-1, 1))",
    ".kneighbors": "dist, idx = nn.kneighbors(ps_treated.reshape(-1, 1))   # who matched to whom",
    "pd.concat": "matched = pd.concat([treated, control.iloc[idx.ravel()]])",
    ".boxplot": 'matched.boxplot(column="ps", by="treated")   # balance, before and after',
}


# ---------------------------------------------------------------------------
# The parts that are the same on every sheet

PREAMBLE = r"""\usepackage{titling}
\usepackage{xcolor}
\definecolor{accent}{HTML}{E3120B}
\definecolor{ink}{HTML}{222222}
\definecolor{muted}{HTML}{6B6B67}

% A modest title block: the sheet is a reference, not a paper. The author line
% is deliberately small.
\pretitle{\begin{flushleft}\large\bfseries\color{ink}}
\posttitle{\end{flushleft}\vspace{-0.6em}%
  {\color{accent}\rule{3.2em}{2pt}}\vspace{0.4em}}
\preauthor{\begin{flushleft}\footnotesize\color{muted}}
\postauthor{\end{flushleft}}
\predate{\begin{flushleft}\footnotesize\color{muted}}
\postdate{\end{flushleft}}
\setlength{\droptitle}{-3.2em}

\usepackage{titlesec}
\titlespacing*{\section}{0pt}{1.1em}{0.35em}
\titlespacing*{\subsection}{0pt}{0.8em}{0.25em}
\titleformat{\section}{\normalsize\bfseries\color{ink}}{}{0pt}{}
\titleformat{\subsection}{\small\bfseries\color{accent}}{}{0pt}{}
"""

GETTING_STARTED = """## Starting Python in VS Codium

Open the course folder once — **File > Open Folder**, then pick the repository. Everything below
assumes you are inside it.

Open a terminal with **View > Terminal** (`Ctrl` + `` ` `` on Windows and Linux, `Cmd` + `` ` `` on
macOS). Create the environment the first time only:

```bash
python3 -m venv .venv      # macOS
python3 -m venv .venv      # Linux
py -m venv .venv           # Windows (PowerShell)
```

Then activate it — **every time you open a new terminal**:

```bash
source .venv/bin/activate  # macOS
source .venv/bin/activate  # Linux
.venv\\Scripts\\activate     # Windows (PowerShell)
```

You will see `(.venv)` at the start of the prompt. If you do not, nothing below will find pandas.
Install the packages once, with the environment active:

```bash
pip install -r requirements.txt
```

Finally tell the editor which Python to use: `Ctrl`/`Cmd` + `Shift` + `P`, type
**Python: Select Interpreter**, and choose the one inside `.venv`.

## A new file, and running it

**File > New File**, then save it with a `.py` ending — `sessionSESSIONNUM.py`, say. Write your code,
save it, and in the terminal:

```bash
python sessionSESSIONNUM.py     # macOS, Linux and Windows alike, inside .venv
```

Inside the environment the command is `python` on all three platforms. Outside it, macOS and Linux
need `python3` and Windows needs `py`, which is one more reason to activate first.

For trying one line at a time, type `python` on its own to get the `>>>` prompt, and `exit()` to
leave. The editor's **Run** triangle does the same thing as the command above.

## The four things you always do

```python
import pandas as pd

# 1 - build a DataFrame
df = pd.DataFrame({"country": ["FR", "DE", "IT"],
                   "gdp_pc_eur": [37_000, 46_000, 32_000]})

# 2 - look at what is in it
df.head()          # the first five rows
df.shape           # (rows, columns)
df.dtypes          # what type each column holds
df.info()          # types, and how many values are missing
df.describe()      # count, mean, sd and quartiles, per numeric column

# 3 - read a file in
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")                    # needs openpyxl - see below
df = pd.read_parquet("data/spine/core.parquet")

import qmib
df = qmib.load("core")                             # a course dataset, by name

# 4 - write a CSV out
df.to_csv("out.csv", index=False)   # index=False, or you get a stray column
```

## Installing a package you do not have

Everything this course needs is already in `requirements.txt`. When you meet a
`ModuleNotFoundError` anyway, or a line above says a reader needs something extra, install it
**into the environment** — never outside it:

```bash
pip install openpyxl                # one package, by name
pip install -r requirements.txt     # or the whole course list again
```

Two rules, and both are about where it lands:

- Your prompt must show `(.venv)` **first**. `pip -V` prints the path it is about to install into;
  that path has to contain `.venv`.
- Type `pip`, not `pip3`, and never `sudo`. Inside an activated environment `pip` is already the
  environment's own.

Then check it arrived:

```bash
pip show openpyxl                   # name, version and location - or nothing at all
python -c "import openpyxl; print(openpyxl.__version__)"
```
"""


def snippet_for(name, sess):
    code = SNIPPETS.get(name)
    if code is None:
        raise SystemExit(f"No snippet for registry entry {name!r} (session {sess}). "
                         f"Add one to SNIPPETS in {Path(__file__).name}.")
    return code


def session_block(sess):
    """One fenced block for a session, subdivided by what the names are for.

    Registry order, not alphabetical: the registry is written in teaching order,
    so `smf.ols` comes before `.fit()` and `.get_influence()` before the four
    things you pull off it. Sorting by name reverses both.
    """
    names = [k for k, v in TOOLKIT.items() if v[0] == sess]
    if not names:
        return None
    by_group = OrderedDict((g, []) for g in GROUPS)
    for name in names:
        by_group[TOOLKIT[name][1]].append(name)

    lines = []
    for group, group_names in by_group.items():
        if not group_names:
            continue
        rule = "-" * max(3, 62 - len(group))
        lines.append(f"# -- {group} {rule}")
        lines.extend(snippet_for(n, sess) for n in group_names)
        lines.append("")
    return "```python\n" + "\n".join(lines).rstrip() + "\n```\n"


def recap(num):
    """Everything taught up to and including this session, session by session.

    Cumulative rather than last-week-only: a student sitting in session 08 has
    to remember `dropna` from session 02 as much as `GridSearchCV` from today,
    and a sheet that carried only session 07 would send them hunting through
    six other PDFs.
    """
    n = int(num)
    if n == 1:
        return ("## What you have learned so far\n\nThis is the first session — the three "
                "sections above are all of it.\n")

    out = [f"## What you have learned so far\n",
           f"Sessions 1 to {n}, in the order you met them. Every line below has run on the course "
           f"data.\n"]
    for sess, meta in ordered():
        if int(sess) > n:
            break
        head = f"### Session {int(sess)} · {meta['short']}\n"
        block = session_block(sess)
        if block:
            out.append(head + "\n" + block)
        elif int(sess) == 1:
            out.append(head + "\nThe workstation itself — the editor, the environment, and loading "
                              "a course dataset with one line. That is section 1 above.\n")
        else:
            out.append(head + f"\nNo new Python: session {int(sess)} reuses what you already "
                              f"have.\n")
    return "\n".join(out)


def sheet(num, s):
    n = int(num)
    lead = (f"Everything you need to type, in one place. The first four sections are the same "
            f"every week; the last one is every name from sessions 1 to {n}."
            if n > 1 else "Everything you need to type, in one place.")
    return f"""---
title: "Python Cheatsheet"
subtitle: "MATH60033A · Session {num} · {s['short']}"
author: "Thierry Warin, PhD · HEC Montréal · {COHORT}"
format:
  pdf:
    documentclass: article
    geometry: [top=2cm, bottom=2cm, left=2.2cm, right=2.2cm]
    fontsize: 9pt
    linestretch: 1.05
    colorlinks: true
    linkcolor: accent
    urlcolor: accent
    highlight-style: github
    include-in-header:
      text: |
{chr(10).join("        " + line for line in PREAMBLE.splitlines())}
---

<!-- Generated by scripts/build_cheatsheets.py — edit that, not this. -->

{lead}

{GETTING_STARTED.replace('SESSIONNUM', num)}
{recap(num)}"""


def render(qmd):
    r = subprocess.run(["quarto", "render", qmd.name, "--to", "pdf"],
                       cwd=qmd.parent, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout[-3000:] + r.stderr[-3000:])
    return r.returncode == 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_render = "--no-render" not in sys.argv
    wanted = set(args) or None

    if not (ROOT / ".venv").exists():
        print("note: no .venv found; quarto will use whatever python is on PATH")

    written = failed = 0
    for num, s in ordered():
        if wanted and num not in wanted:
            continue
        d = ROOT / s["dir"]
        qmd = d / f"{FILENAME}.qmd"
        qmd.write_text(sheet(num, s), encoding="utf-8")
        written += 1
        if not do_render:
            print(f"  session {num}: {qmd.relative_to(ROOT)}")
            continue
        ok = render(qmd)
        pdf = d / f"{FILENAME}.pdf"
        size = f"{pdf.stat().st_size / 1024:.0f} KB" if pdf.exists() else "—"
        print(f"  session {num}: {'ok  ' if ok else 'FAIL'} {size}  {pdf.relative_to(ROOT)}")
        failed += not ok

    print(f"\n{written} cheatsheet(s) written" + (f", {failed} failed to render" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
