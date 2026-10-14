"""statsmodels — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#4f2d7f"
BLUE, RED, GREEN, SAND, LILAC = "#cfe0f5", "#f8d3cd", "#d4ecd9", "#f2efe8", "#e6dcf2"

META = dict(
    title="statsmodels",
    color=ACCENT,
    tagline="Regression you can read: fit, read, check, predict",
    sessions="2 to 7, 10, 11 and 13",
)
META["import"] = "import statsmodels.formula.api as smf"
META["version_note"] = "+ import statsmodels.api as sm (no formula)"


# ---------------------------------------------------------------- diagrams
def formula_pic():
    b = text(130, 15, 'smf.ols("gdp ~ prod + invest", data=d)', 9.5, "middle", ACCENT, "bold")
    b += text(62, 33, "outcome", 9) + text(62, 44, "left of ~", 8, "middle", "#666")
    b += text(130, 33, "~", 10, "middle", ACCENT, "bold") + text(130, 44, "explained by", 8, "middle", "#666")
    b += text(200, 33, "predictors", 9) + text(200, 44, "joined by +", 8, "middle", "#666")
    b += text(130, 60, "intercept added for you · .fit() estimates", 8, "middle", "#444")
    return svg(260, 66, b)


def summary_pic():
    rows = [("", "coef", "std err", "P>|t|"), ("Intercept", "-86118", "4375", "0.000"),
            ("productivity", "1111.3", "41.5", "0.000")]
    b = f'<rect x="2" y="2" width="256" height="112" fill="{SAND}" stroke="#bbb"/>'
    b += text(8, 15, "OLS Regression Results", 8.5, "start", "#222", "bold")
    b += text(8, 28, "No. Observations: 428", 8, "start", "#222")
    b += text(150, 15, "R-squared: 0.627", 8, "start", "#222")
    b += text(150, 28, "Adj. R-sq.: 0.626", 8, "start", "#222")
    b += f'<rect x="146" y="5" width="96" height="27" fill="none" stroke="#e3120b" stroke-width="1.5"/>'
    b += text(194, 42, "share of variance explained", 7.5, "middle", "#e3120b")
    xs = [8, 98, 150, 204]
    for r, row in enumerate(rows):
        for x, cell in zip(xs, row):
            b += text(x, 58 + 13 * r, cell, 8, "start", "#222", "bold" if r == 0 else "normal")
    b += f'<rect x="95" y="62" width="44" height="30" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>'
    b += f'<rect x="201" y="62" width="36" height="30" fill="none" stroke="#2e8b57" stroke-width="1.5"/>'
    b += text(117, 104, "slope: y units per x unit", 7.5, "middle", ACCENT, "bold")
    b += text(219, 104, "p < 0.05", 7.5, "middle", "#2e8b57", "bold")
    return svg(260, 116, b)


def cutpoints_pic():
    b = f'<rect x="10" y="22" width="90" height="24" fill="{RED}"/>'
    b += f'<rect x="100" y="22" width="70" height="24" fill="{SAND}"/>'
    b += f'<rect x="170" y="22" width="70" height="24" fill="{GREEN}"/>'
    b += f'<line x1="10" y1="46" x2="250" y2="46" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>'
    b += text(254, 50, "y*", 9, "start")
    for x, c in ((100, "c₁"), (170, "c₂")):
        b += f'<line x1="{x}" y1="14" x2="{x}" y2="50" stroke="{ACCENT}" stroke-width="2.2"/>'
        b += text(x, 11, c, 9, "middle", ACCENT, "bold")
    b += text(55, 38, "unlikely", 8.5) + text(135, 38, "somewhat", 8.5) + text(205, 38, "very likely", 8.5)
    b += arrow(105, 62, 160, 62, ACCENT)
    b += text(130, 76, "a positive β shifts y* right: higher categories", 8, "middle", "#333")
    return svg(260, 80, b)


def chain_pic():
    boxes = [("β", "log-odds"), ("e^β", "odds ratio"), ("predict()", "probability")]
    b = ""
    for i, (top, bot) in enumerate(boxes):
        x = 4 + i * 86
        b += f'<rect x="{x}" y="4" width="70" height="36" rx="5" fill="{LILAC}" stroke="{ACCENT}"/>'
        b += text(x + 35, 19, top, 9.5, "middle", ACCENT, "bold") + text(x + 35, 33, bot, 8.5)
        if i < 2:
            b += arrow(x + 71, 22, x + 85, 22)
    return svg(260, 44, b)


# ---------------------------------------------------------------- plots
def _ols():
    import qmib
    import statsmodels.formula.api as smf
    d = qmib.load("core").dropna(subset=["gdp_pc_eur", "productivity_idx"])
    return d, smf.ols("gdp_pc_eur ~ productivity_idx", data=d).fit()


def resid_plot():
    d, fit = _ols()
    fig, ax = small(3.0, 1.3)
    ax.scatter(fit.fittedvalues / 1000, fit.resid / 1000, s=4, alpha=0.5, color="#7a62a8")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("fitted (k€)", fontsize=6.5); ax.set_ylabel("residual (k€)", fontsize=6.5)
    ax.set_title("residuals vs fitted: look for curves, funnels", fontsize=7)
    return fig


def cooks_plot():
    d, fit = _ols()
    cd = fit.get_influence().cooks_distance[0]
    fig, ax = small(3.0, 1.15)
    ax.vlines(range(len(cd)), 0, cd, color="#7a62a8", lw=0.7)
    ax.axhline(4 / len(cd), color="#e3120b", ls="--", lw=1)
    ax.set_xlabel("observation", fontsize=6.5); ax.set_ylabel("Cook's D", fontsize=6.5)
    ax.set_title("one spike per row; dashed: 4/n", fontsize=7)
    return fig


def scurve():
    import numpy as np
    import pandas as pd
    import qmib
    import statsmodels.formula.api as smf
    loans = qmib.load("loans")
    m = smf.logit("default ~ fico", data=loans).fit(disp=0)
    g = pd.DataFrame({"fico": np.arange(612, 828)})
    fig, ax = small(3.0, 1.25)
    ax.plot(g.fico, m.predict(g), color=ACCENT, lw=2)
    for f in (650, 700, 800):
        p = float(m.predict(pd.DataFrame({"fico": [f]}))[0])
        ax.scatter(f, p, color="#e3120b", s=10, zorder=3)
        ax.annotate(f"{p:.2f}", (f, p), xytext=(4, 4), textcoords="offset points", fontsize=6)
    ax.set_xlabel("FICO score", fontsize=6.5); ax.set_ylabel("P(default)", fontsize=6.5)
    ax.set_ylim(0, 0.4)
    return fig


def stacked():
    import pandas as pd
    import qmib
    import statsmodels.api as sm
    import numpy as np
    ml = qmib.load("hsbdemo")
    levels = ["academic", "general", "vocation"]
    y = pd.Categorical(ml["prog"], categories=levels).codes
    X = sm.add_constant(ml[["write"]].astype(float))
    mn = sm.MNLogit(y, X).fit(disp=0)
    w = np.arange(31, 68)
    P = mn.predict(sm.add_constant(pd.DataFrame({"write": w.astype(float)})))
    fig, ax = small(3.0, 1.3)
    ax.stackplot(w, P[0], P[1], P[2], labels=levels, colors=["#7a62a8", "#c9b8e3", "#f2c9a0"])
    ax.set_xlim(31, 67); ax.set_ylim(0, 1)
    ax.set_xlabel("writing score", fontsize=6.5); ax.set_ylabel("probability", fontsize=6.5)
    ax.legend(fontsize=5.8, frameon=False, loc="upper left", ncol=3)
    return fig


PAGES = [[
    dict(title="1 · Write the model as a formula",
         figure_top=formula_pic,
         items=[
             dict(code='smf.ols("y ~ x", data=d).fit()', text="ordinary least squares: the line that makes the squared misses smallest."),
             dict(code='"y ~ x + z"', text="two predictors: each slope now **holds the other fixed**."),
             dict(code='"y ~ C(region)"', text="a categorical predictor: one dummy per level, minus a reference."),
             dict(code='"y ~ x + I(x**2)"', text="a squared term: `I()` means *compute this*. The effect of x depends on x."),
             dict(code='"y ~ a * b"', text="an interaction: expands to `a + b + a:b`, a slope per group."),
             dict(code='"np.log(y) ~ x"', text="functions work inside the formula."),
         ],
         tip="Read `~` as *explained by*. Write the formula you would say aloud."),
    dict(title="2 · Read the fit",
         figure_top=summary_pic,
         items=[
             dict(code="fit.summary()", text="the whole table: coefficients, p-values, R², n."),
             dict(code="fit.summary().tables[1]", text="only the coefficient table — what fits on a slide."),
             dict(code="fit.params", text="the estimates, as a Series you can compute with.",
                  ex='fit.params["productivity_idx"]   # 1111.3 €/point'),
             dict(code="fit.pvalues  ·  fit.conf_int()", text="p-values · 95% intervals, one row per coefficient."),
             dict(code="fit.rsquared  ·  fit.rsquared_adj", text="share of variance explained · the same, penalised for extra predictors."),
             dict(code="fit.aic  ·  fit.bic  ·  fit.nobs", text="information criteria (lower is better) · rows used."),
         ],
         warn="A slope is a sentence with units: *one more point of x goes with b more units of y, holding the others fixed*."),
    dict(title="3 · Predict",
         items=[
             dict(code="fit.predict(new)", text="fitted values for new rows: a DataFrame with the predictor columns.",
                  ex='fit.predict(pd.DataFrame({"productivity_idx": [100, 120]}))'),
             dict(code="fit.get_prediction(new).summary_frame()", text="the prediction **with** its interval."),
         ],
         tip="Predict only inside the range of the data you fitted."),
    dict(title="4 · Check the fit — diagnostics",
         intro="Session 3: is the line adequate, valid, robust?",
         figure_top=resid_plot,
         items=[
             dict(code="fit.fittedvalues  ·  fit.resid", text="what the line predicts · what it missed, row by row."),
             dict(code="infl = fit.get_influence()", text="the whole diagnostic bundle, computed once."),
             dict(code="infl.hat_matrix_diag", text="leverage: how unusual each row's x is. They sum to the number of parameters."),
             dict(code="infl.cooks_distance[0]", text="influence: how far the fit moves without that row."),
         ],
         figure=cooks_plot,
         warn="A tall spike is a row to **look at**, not to delete: report the fit with and without it."),
], [
    dict(title="5 · Binary logit — a 0/1 outcome",
         figure_top=chain_pic,
         items=[
             dict(code='m = smf.logit("default ~ fico", data=loans).fit(disp=0)', text="maximum likelihood; `disp=0` silences the iteration log."),
             dict(code="m.params", text="**log-odds**: read the sign, not the size."),
             dict(code='np.exp(m.params["fico"])', text="the **odds ratio**: 0.988 = odds of default 1.2% lower per point."),
             dict(code='m.predict(pd.DataFrame({"fico": [650, 700, 800]}))', text="the **probability**: the whole linear predictor through the S-curve."),
         ],
         figure=scurve,
         warn="An odds ratio of 1.5 is *odds* 50% higher — not a probability 50% higher."),
    dict(title="6 · Which model for which outcome?",
         items=[
             dict(code="a number  →  smf.ols", text="GDP, productivity, a return: the slope is in units of y."),
             dict(code="yes / no  →  smf.logit", text="default, exports, an up day: odds ratios and probabilities."),
             dict(code="ordered categories  →  OrderedModel", text="unlikely < somewhat < very likely; low < middle < high."),
             dict(code="unordered categories  →  sm.MNLogit", text="programme, entry mode, owner type: everything against a baseline."),
         ]),
    dict(title="7 · Ordinal logit — ordered categories",
         figure_top=cutpoints_pic,
         items=[
             dict(code="from statsmodels.miscmodels.ordinal_model import OrderedModel", text=""),
             dict(code='d["y_c"] = pd.Categorical(d["y"], categories=order, ordered=True)', text="give the categories their order first."),
             dict(code='om = OrderedModel(d["y_c"], d[["x1", "x2"]], distr="logit")', text="one slope per predictor, shared by every cut: *proportional odds*.",
                  ex='om = om.fit(method="bfgs", disp=0)'),
             dict(code="np.exp(om.params[[\"x1\", \"x2\"]])", text="odds of a **higher** category, at any cut."),
             dict(code="om.predict(new)", text="one probability per category; each row sums to 1."),
         ]),
    dict(title="8 · When statsmodels complains",
         items=[
             dict(code="PatsyError: ... not defined", text="a name in the formula is not a column of `data=`: check the spelling."),
             dict(code="Optimization terminated / Iterations", text="the logit's log: add `disp=0` to `.fit()`."),
             dict(code="Singular matrix / perfect separation", text="two predictors are copies, or one predicts the outcome perfectly."),
             dict(code="ConvergenceWarning", text="try another optimiser: `.fit(method=\"bfgs\")`."),
             dict(code="AIC comparison looks too good", text="the models dropped different rows: `dropna` on the union first."),
         ]),
    dict(title="9 · Multinomial logit — unordered categories",
         figure_top=stacked,
         items=[
             dict(code='y = pd.Categorical(ml["prog"], categories=levels).codes', text="code 0 — the first level — is the **baseline**."),
             dict(code="X = sm.add_constant(X)", text="no formula here: add the intercept yourself."),
             dict(code="mn = sm.MNLogit(y, X).fit(disp=0)", text="one equation per category, each **against the baseline**."),
             dict(code="np.exp(mn.params)", text="relative risk ratios: multiply P(category) / P(baseline)."),
             dict(code="mn.predict(grid)", text="probabilities for every category — what to report."),
         ],
         tip="Say *relative to the baseline* every time: a negative coefficient does not mean that category's probability falls."),
    dict(title="10 · Compare models",
         items=[
             dict(code="LR = 2 * (full.llf - small.llf)", text="likelihood-ratio statistic for nested models; `.llf` is the log-likelihood."),
             dict(code="stats.chi2.sf(LR, df=q)", text="its p-value, with q = coefficients dropped (from scipy)."),
             dict(code="full.compare_f_test(small)", text="the F-test for nested OLS models."),
             dict(code="a.aic, b.aic", text="any two models — but only **on the same rows**."),
             dict(code="1 - m.llf / null.llf", text="McFadden's pseudo-R² for a logit; 0.2–0.4 is already good."),
         ]),
]]
