"""scipy — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#0054a6"

META = dict(
    title="scipy",
    color=ACCENT,
    tagline="scipy.stats: describe a distribution, read a test, turn a statistic into a p-value",
    sessions="2, 4, 5, 6, 9 and 10",
)
META["import"] = "from scipy import stats"
META["version_note"] = "every distribution has .pdf, .cdf, .ppf, .sf"


def skew_fig():
    import qmib
    from scipy import stats
    g = qmib.load("core")["gdp_pc_eur"].dropna()
    fig, ax = small(3.0, 1.4)
    ax.hist(g, bins=30, color="#7fa7d4")
    ax.axvline(g.mean(), color="#e3120b", lw=1.5, label="mean")
    ax.axvline(g.median(), color="#2e8b57", lw=1.5, ls="--", label="median")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.set_title(f"GDP per capita · skew g1 = {stats.skew(g):.2f} > 2√(6/n) = {2*(6/len(g))**.5:.2f}",
                 fontsize=7)
    ax.legend(fontsize=6, frameon=False)
    return fig


def normal_fig():
    import numpy as np
    from scipy import stats
    x = np.linspace(-4, 4, 400)
    fig, ax = small(3.0, 1.35)
    ax.plot(x, stats.norm.pdf(x), color=ACCENT, lw=1.8)
    for side in (x <= -1.96, x >= 1.96):
        ax.fill_between(x[side], stats.norm.pdf(x[side]), color="#e3120b", alpha=.5)
    ax.annotate("2.5%", (-2.6, 0.03), fontsize=6.5, ha="center")
    ax.annotate("2.5%", (2.6, 0.03), fontsize=6.5, ha="center")
    ax.annotate("95%", (0, 0.15), fontsize=7, ha="center", color=ACCENT)
    ax.set_xticks([-1.96, 0, 1.96])
    ax.set_xlabel("stats.norm.ppf(0.975) = 1.96", fontsize=7)
    return fig


def chi2_fig():
    import numpy as np
    from scipy import stats
    x = np.linspace(0, 20, 400)
    lr, df = 12.6, 3
    fig, ax = small(3.0, 1.35)
    ax.plot(x, stats.chi2.pdf(x, df), color=ACCENT, lw=1.8)
    tail = x >= lr
    ax.fill_between(x[tail], stats.chi2.pdf(x[tail], df), color="#e3120b", alpha=.6)
    ax.axvline(stats.chi2.ppf(0.95, df), color="#888", ls=":", lw=1)
    ax.annotate(f"LR = {lr}\np = {stats.chi2.sf(lr, df):.4f}", (lr, 0.01), xytext=(14, 0.12),
                fontsize=6.5, arrowprops=dict(arrowstyle="-", color="#999", lw=0.6))
    ax.annotate("5% critical\nvalue 7.81", (7.81, 0.2), fontsize=6, ha="left", color="#666")
    ax.set_xlabel("chi-square with 3 df", fontsize=7)
    return fig


def t_fig():
    import numpy as np
    from scipy import stats
    x = np.linspace(-4, 4, 400)
    fig, ax = small(3.0, 1.2)
    ax.plot(x, stats.norm.pdf(x), color="#888", lw=1.2, label="normal")
    for df, c in ((3, "#e3120b"), (10, ACCENT)):
        ax.plot(x, stats.t.pdf(x, df), color=c, lw=1.6, label=f"t, {df} df")
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlabel("fatter tails with few observations", fontsize=7)
    return fig


PAGES = [[
    dict(title="1 · Describe a distribution (session 2)",
         figure_top=skew_fig,
         items=[
             dict(code="stats.trim_mean(x, 0.05)", text="the mean after cutting 5% off each tail: between the mean and the median.",
                  ex='stats.trim_mean(core["gdp_pc_eur"].dropna(), 0.05)'),
             dict(code="stats.skew(x)", text="g1: 0 = symmetric, > 0 = a long right tail. Substantially skewed if |g1| > 2√(6/n)."),
             dict(code="stats.kurtosis(x)", text="g2, **excess** kurtosis: 0 for a normal; > 0 = more extreme values. Substantial if |g2| > 4√(6/n)."),
             dict(code="stats.shapiro(resid)", text="a test of normality; p < 0.05 says the residuals are not normal."),
         ],
         tip="Always report a skewness or a kurtosis **with** its threshold — the number alone says little."),
    dict(title="2 · Four methods, every distribution",
         items=[
             dict(code=".pdf(x)", text="density: the height of the curve."),
             dict(code=".cdf(x)", text="P(X ≤ x): the area to the left."),
             dict(code=".sf(x)", text="P(X > x) = 1 − cdf: the area to the right — a one-sided p-value."),
             dict(code=".ppf(q)", text="the inverse of the cdf: the critical value for a level q."),
         ],
         tip="`sf` is more precise than `1 - cdf` for tiny p-values."),
    dict(title="3 · The normal distribution",
         intro="`stats.norm` is the bell curve. The same four methods work for every distribution.",
         figure_top=normal_fig,
         items=[
             dict(code="stats.norm.pdf(x)", text="the height of the curve at x — for drawing it."),
             dict(code="stats.norm.cdf(1.96)", text="the area to the left of x: 0.975."),
             dict(code="stats.norm.ppf(0.975)", text="the inverse: the x that leaves 97.5% to its left — 1.96, the 95% critical value."),
             dict(code="stats.norm.sf(z) * 2", text="the area to the right, doubled: a two-sided p-value for a z-statistic."),
         ]),
    dict(title="4 · The t distribution",
         figure_top=t_fig,
         items=[
             dict(code="stats.t.ppf(0.975, df=n - k - 1)", text="the critical value with few observations: above 1.96, closer to it as n grows."),
             dict(code="stats.t.sf(abs(t), df) * 2", text="the two-sided p-value of a t-statistic — what a regression table prints."),
         ]),
    dict(title="5 · Chi-square: the LR test (session 4)",
         intro="Several coefficients at once: compare the log-likelihoods of two nested models.",
         figure_top=chi2_fig,
         items=[
             dict(code="lr = 2 * (full.llf - restricted.llf)", text="the LR statistic: how much the dropped coefficients improved the fit."),
             dict(code="stats.chi2.sf(lr, df=q)", text="its p-value, with q = the number of coefficients dropped.",
                  ex="stats.chi2.sf(12.6, 3)    # 0.0056: keep the three dummies"),
             dict(code="stats.chi2.ppf(0.95, df=3)", text="the 5% critical value: 7.81. Reject when LR is above it."),
         ]),
    dict(title="6 · Correlation",
         items=[
             dict(code="r, p = stats.pearsonr(x, y)", text="the correlation and the p-value of \"no correlation\"."),
             dict(code="rho, p = stats.spearmanr(x, y)", text="the same on ranks: robust to outliers and to curves that only go up."),
         ],
         warn="A p-value after you picked the variable with the strongest correlation is not valid: the same data chose and tested it."),
    dict(title="7 · A regression line, by hand",
         intro="What the summary table computes for each coefficient.",
         items=[
             dict(code="t = coef / se", text="how many standard errors the estimate is from zero."),
             dict(code="p = 2 * stats.t.sf(abs(t), df)", text="the two-sided p-value, df = n − k − 1."),
             dict(code="coef ± stats.t.ppf(0.975, df) * se", text="the 95% confidence interval."),
         ]),
]]
