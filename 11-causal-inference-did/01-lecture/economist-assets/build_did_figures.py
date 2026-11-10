"""
Session 11 · the difference-in-differences figures, computed rather than drawn.

Every number on a picture here comes from the same simulation or the same data,
with the same seed, that the matching slide computes live, so what the slide
says about a picture is true of the picture.

    .venv/bin/python 11-causal-inference-did/01-lecture/economist-assets/build_did_figures.py

Writes, next to this file:
    did-idea.png           Part 1: the two differences, drawn
    parallel-idea.png      Part 1: parallel trends allow any gap in level, not a change in the gap
    housing-map.png        Example 1: the city, the sites, the near and the far houses
    housing-2x2.png        Example 1: four means, the counterfactual, and the two differences
    housing-betas.png      Example 1: the four regression coefficients, on the same picture
    housing-b-counterfactual.png Example 2: the counterfactual DiD assumes, against the true one
    ai-adoption.png        Example 3: who adopted when, and which country-years carry an outcome
    ai-trends.png          Example 3: average AI use by adoption cohort, 2021-2024
    twfe-comparisons.png   Example 3: the clean comparisons, and the one TWFE also makes
    iv-management.png      Example 4: exporters are better managed: the confounder you cannot see
    housing-estimators.png Example 1: after-only, before-after and DiD against the truth
    housing-trends.png     Example 2: six years of prices, versions A and B
    housing-event-study.png Example 2: the event study, versions A and B
    ai-estimates.png       Example 3: TWFE, Callaway-Sant'Anna and the cohorts, against the truth
    ai-honest.png          Example 3: how large a violation of parallel trends the result survives
    iv-diagram.png         Example 4: the instrument, and the path that breaks it in version B
    iv-two-stages.png      Example 4: the first stage and the reduced form, by distance to port
    iv-estimates.png       Example 4: naive and IV estimates, versions A and B, against the truth
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from statsmodels.sandbox.regression.gmm import IV2SLS

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent

# The course's figure palette (scripts/build_economist_assets.R)
BG, INK, MUTED, RED = "#F7F4ED", "#222222", "#6B6B67", "#E3120B"
BLUE, TEAL, GOLD, GRID = "#356B8C", "#2A8C82", "#D49A00", "#D8D3C8"
PALE_BLUE, PALE_RED, PALE_TEAL = "#C9DCE8", "#F7C9C6", "#C6E2DE"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "font.family": "sans-serif", "font.size": 12, "text.color": INK,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("wrote", name)


# --- the simulations the slides run (same seeds, same lines) -------------------
def simulate_two_periods():
    """Example 1: 1,000 houses, half near a new affordable-housing site; truth -10."""
    rng = np.random.default_rng(11)
    n = 1000
    near = (np.arange(n) < 500).astype(int)
    base = 250 - 15 * near + rng.normal(0, 20, n)          # near houses were cheaper already
    before = base + rng.normal(0, 10, n)
    after = base + 30 - 10 * near + rng.normal(0, 10, n)   # +30 for everyone; -10 near the site
    return pd.DataFrame({"house": np.r_[np.arange(n), np.arange(n)],
                         "near": np.r_[near, near],
                         "post": np.r_[np.zeros(n), np.ones(n)].astype(int),
                         "price": np.r_[before, after]})


def simulate_six_years(drift):
    """Example 2: the same city, 2003-2008, site opens in 2006; drift = extra trend near the site."""
    rng = np.random.default_rng(12)
    n = 1000
    near = (np.arange(n) < 500).astype(int)
    house_effect = rng.normal(0, 20, n)
    rows = []
    for year in range(2003, 2009):
        price = (250 - 15 * near + house_effect + 8 * (year - 2003)
                 + drift * near * (year - 2003)
                 - 10 * near * (year >= 2006) + rng.normal(0, 10, n))
        rows.append(pd.DataFrame({"house": np.arange(n), "near": near,
                                  "year": year, "price": price}))
    return pd.concat(rows, ignore_index=True)


# --- Part 1: the ideas, drawn --------------------------------------------------
def did_idea():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    co = (40, 60); tr = (60, 70); cf = tr[0] + (co[1] - co[0])
    ax.plot([0, 1], co, marker="o", ms=10, lw=2.6, color=BLUE, label="control group")
    ax.plot([0, 1], tr, marker="o", ms=10, lw=2.6, color=RED, label="treated group")
    ax.plot([0, 1], [tr[0], cf], ls="--", lw=2, color=RED, alpha=0.5,
            label="treated, had the policy not happened")
    for lvl, col in ((co[0], BLUE), (tr[0], RED)):
        ax.plot([0, 1.0], [lvl, lvl], ls=":", color=col, lw=1.2)
    def arrow_(x, a_, b_, col, txt, dx=0.03):
        ax.annotate("", xy=(x, b_), xytext=(x, a_), arrowprops=dict(arrowstyle="->", color=col, lw=2))
        ax.text(x + dx, (a_ + b_) / 2, txt, color=col, fontsize=10.5, va="center", fontweight="bold")
    arrow_(1.04, co[0], co[1], BLUE, "change among the\ncontrols: +20")
    ax.annotate("", xy=(0.86, tr[1]), xytext=(0.86, tr[0]), arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.text(0.83, tr[0] - 2.2, "change among the treated: +10", color=RED, fontsize=10.5,
            ha="right", va="top", fontweight="bold")
    ax.annotate("", xy=(1.04, tr[1]), xytext=(1.04, cf), arrowprops=dict(arrowstyle="<->", color=INK, lw=2))
    ax.text(1.07, (tr[1] + cf) / 2, "DiD = +10 − (+20) = −10", fontsize=11, fontweight="bold",
            va="center")
    ax.set_xticks([0, 1], ["before", "after"])
    ax.set_xlim(-0.3, 1.75)
    ax.set_ylabel("average outcome")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title("Two changes, and the difference between them", loc="left", fontsize=12.5,
                 fontweight="bold")
    fig.tight_layout()
    save(fig, "did-idea.png")


def parallel_idea():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
    t = np.arange(5)
    for ax, (co, tr, title, col) in zip(axes, (
            (20 + 4 * t, 45 + 4 * t, "Parallel: far apart in level, the gap never moves", TEAL),
            (20 + 4 * t, 45 + 1 * t, "Not parallel: the gap shrinks by itself", RED))):
        ax.plot(t, co, marker="o", color=BLUE, lw=2.2, label="control")
        ax.plot(t, tr, marker="o", color=RED, lw=2.2, label="treated")
        for x in (0, 4):
            ax.annotate("", xy=(x, tr[x]), xytext=(x, co[x]),
                        arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2))
            ax.text(x + 0.12, (tr[x] + co[x]) / 2, f"gap {tr[x] - co[x]:.0f}", fontsize=10,
                    color=MUTED, va="center")
        ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold", color=col)
        ax.set_xticks(t, [f"year {i + 1}" for i in t])
    axes[0].legend(frameon=False, loc="lower right")
    axes[0].set_ylabel("outcome, before any policy")
    fig.tight_layout()
    save(fig, "parallel-idea.png")


def housing_map():
    rng = np.random.default_rng(5)
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.set_xlim(0, 20); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    for x in range(0, 21, 2):
        ax.plot([x, x], [0, 10], color=GRID, lw=0.6, zorder=0)
    for y in range(0, 11, 2):
        ax.plot([0, 20], [y, y], color=GRID, lw=0.6, zorder=0)
    sites = [(4, 6.5), (11, 3), (16.5, 7)]
    for sx, sy in sites:
        ax.add_patch(plt.Circle((sx, sy), 2.2, color=PALE_RED, alpha=0.5, zorder=1))
    pts = rng.uniform([0.3, 0.3], [19.7, 9.7], size=(140, 2))
    for x, y in pts:
        near = min(np.hypot(x - sx, y - sy) for sx, sy in sites) < 2.2
        ax.scatter(x, y, marker="s", s=26, color=RED if near else BLUE, zorder=2)
    for sx, sy in sites:
        ax.scatter(sx, sy, marker="^", s=220, color=INK, zorder=3)
    ax.scatter([], [], marker="^", s=90, color=INK, label="new affordable-housing site")
    ax.scatter([], [], marker="s", s=30, color=RED, label="house near a site: treated")
    ax.scatter([], [], marker="s", s=30, color=BLUE, label="house far from any site: control")
    ax.legend(frameon=True, facecolor=BG, edgecolor=GRID, loc="lower center",
              bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=9.5)
    save(fig, "housing-map.png")


# --- Example 1 -----------------------------------------------------------------
def housing_2x2(h):
    m = h.groupby(["near", "post"])["price"].mean().unstack()
    cf = m.loc[1, 0] + (m.loc[0, 1] - m.loc[0, 0])
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    x = [0, 1]
    ax.plot(x, m.loc[0], marker="o", ms=9, lw=2.4, color=BLUE, label="far from a site (control)")
    ax.plot(x, m.loc[1], marker="o", ms=9, lw=2.4, color=RED, label="near a site (treated)")
    ax.plot(x, [m.loc[1, 0], cf], ls="--", lw=2, color=RED, alpha=0.55,
            label="near, had the site not opened")
    ax.annotate("", xy=(1.03, m.loc[1, 1]), xytext=(1.03, cf),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text(1.06, (cf + m.loc[1, 1]) / 2, f"DiD\n{m.loc[1, 1] - cf:+.1f}", va="center",
            fontsize=12, fontweight="bold")
    for g, col in ((0, BLUE), (1, RED)):
        ax.text(-0.06, m.loc[g, 0], f"{m.loc[g, 0]:.1f}", ha="right", va="center",
                color=col, fontsize=11)
    ax.text(1.0, m.loc[0, 1] + 3, f"{m.loc[0, 1]:.1f}", ha="center", color=BLUE, fontsize=11)
    ax.text(1.0, m.loc[1, 1] - 5, f"{m.loc[1, 1]:.1f}", ha="center", color=RED, fontsize=11)
    ax.text(0.95, cf, f"{cf:.1f}", ha="right", va="center", color=RED, alpha=0.7, fontsize=11)
    ax.set_xticks(x, ["before the site opened", "after"])
    ax.set_xlim(-0.35, 1.3)
    ax.set_ylabel("average price, $ thousands")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    fig.tight_layout()
    save(fig, "housing-2x2.png")
    return m, cf


def housing_betas(h):
    r = smf.ols("price ~ near * post", data=h).fit().params
    b0, b1, b2, b3 = r["Intercept"], r["near"], r["post"], r["near:post"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot([0, 1], [b0, b0 + b2], marker="o", ms=9, lw=2.4, color=BLUE, label="far (control)")
    ax.plot([0, 1], [b0 + b1, b0 + b1 + b2 + b3], marker="o", ms=9, lw=2.4, color=RED,
            label="near (treated)")
    ax.plot([0, 1], [b0 + b1, b0 + b1 + b2], ls="--", lw=2, color=RED, alpha=0.5,
            label="near, without the site")
    def tag(x, y, txt, col, ha="left"):
        ax.text(x, y, txt, color=col, fontsize=11, fontweight="bold", ha=ha, va="center",
                bbox=dict(fc=BG, ec="none", pad=1))
    tag(-0.05, b0, f"β₀ = {b0:.1f}", BLUE, "right")
    ax.annotate("", xy=(-0.02, b0 + b1), xytext=(-0.02, b0), arrowprops=dict(arrowstyle="<->", color=GOLD))
    tag(-0.05, b0 + b1 / 2, f"β₁ = {b1:.1f}", GOLD, "right")
    ax.annotate("", xy=(1.02, b0 + b2), xytext=(1.02, b0), arrowprops=dict(arrowstyle="<->", color=TEAL))
    tag(1.05, b0 + b2 / 2 + 6, f"β₂ = {b2:.1f}", TEAL)
    ax.annotate("", xy=(1.02, b0 + b1 + b2 + b3), xytext=(1.02, b0 + b1 + b2),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.8))
    tag(1.05, b0 + b1 + b2 + b3 / 2, f"β₃ = {b3:.1f}: the DiD", INK)
    ax.set_xticks([0, 1], ["before", "after"])
    ax.set_xlim(-0.45, 1.5)
    ax.set_ylabel("average price, $ thousands")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title("price ~ near * post: each coefficient is a piece of the picture", loc="left",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "housing-betas.png")
    return b0, b1, b2, b3


def housing_estimators(m):
    vals = {"after only: near vs far, after": m.loc[1, 1] - m.loc[0, 1],
            "before-after: near houses only": m.loc[1, 1] - m.loc[1, 0],
            "difference-in-differences": (m.loc[1, 1] - m.loc[1, 0]) - (m.loc[0, 1] - m.loc[0, 0])}
    fig, ax = plt.subplots(figsize=(8.4, 2.9))
    ax.axvline(-10, color=TEAL, lw=2, ls="--")
    ax.axvline(0, color=MUTED, lw=1)
    ys = np.arange(len(vals))[::-1]
    cols = [RED, GOLD, BLUE]
    ax.scatter(list(vals.values()), ys, s=120, color=cols, zorder=3)
    for v, y in zip(vals.values(), ys):
        ax.text(v, y + 0.3, f"{v:+.1f}", ha="center", fontweight="bold")
    ax.text(-9.4, -0.55, "truth: -10", color=TEAL, fontweight="bold")
    ax.set_yticks(ys, list(vals.keys()))
    ax.set_ylim(-0.8, len(vals) - 0.3)
    ax.set_xlabel("estimated effect of the site on nearby prices, $ thousands")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "housing-estimators.png")
    return vals


# --- Example 2 -----------------------------------------------------------------
def event_study(p):
    g = p.groupby(["year", "near"])["price"].mean().unstack()
    gap = g[1] - g[0]
    return g, gap - gap[2005]


def housing_trends_and_events():
    out = {}
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
    fig2, axes2 = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
    for k, (version, drift, title) in enumerate(
            (("A", 0.0, "A · the trends were parallel"),
             ("B", -3.0, "B · near houses were already slipping"))):
        p = simulate_six_years(drift)
        g, es = event_study(p)
        two = p[p["year"].isin([2005, 2008])].assign(post=lambda d: (d["year"] == 2008).astype(int))
        did = smf.ols("price ~ near * post", data=two).fit().params["near:post"]
        out[version] = (did, es)
        ax = axes[k]
        ax.axvspan(2005.5, 2008.4, color=PALE_TEAL, alpha=0.5, zorder=0)
        ax.plot(g.index, g[0], marker="o", color=BLUE, lw=2, label="far")
        ax.plot(g.index, g[1], marker="o", color=RED, lw=2, label="near")
        ax.set_title(title, loc="left", fontsize=12.5, fontweight="bold")
        ax.set_xticks(g.index)
        if k == 0:
            ax.set_ylabel("average price, $ thousands")
            ax.legend(frameon=False, loc="upper left")
        ax.text(2006.95, ax.get_ylim()[0] + 4 if k else g.values.min(), "site open",
                ha="center", color=TEAL, fontsize=10)
        ax2 = axes2[k]
        ax2.axvspan(2005.5, 2008.4, color=PALE_TEAL, alpha=0.5, zorder=0)
        ax2.axhline(0, color=MUTED, lw=1)
        ax2.axhline(-10, color=TEAL, lw=1.6, ls="--")
        ax2.plot(es.index, es.values, marker="o", ms=8, lw=2,
                 color=BLUE if version == "A" else RED)
        for x, y in es.items():
            ax2.text(x + 0.12, y + 1.2, f"{y:+.1f}", ha="left", fontsize=10)
        ax2.set_ylim(-24, 9)
        ax2.set_title(title, loc="left", fontsize=12.5, fontweight="bold")
        ax2.set_xticks(es.index)
        if k == 0:
            ax2.set_ylabel("near minus far, relative to 2005")
        ax2.text(2003, -11.5, "truth: -10", color=TEAL, fontsize=10, va="top")
    fig.tight_layout()
    save(fig, "housing-trends.png")
    fig2.tight_layout()
    save(fig2, "housing-event-study.png")
    return out


def housing_b_counterfactual():
    p = simulate_six_years(-3.0)
    g = p.groupby(["year", "near"])["price"].mean().unstack()
    years = g.index.values
    true_cf = g[1] + 10 * (years >= 2006)                 # the same houses, without the -10
    did_cf = g.loc[2005, 1] + (g[0] - g.loc[2005, 0])     # what DiD assumes: the far trend
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.axvspan(2005.5, 2008.4, color=PALE_TEAL, alpha=0.5, zorder=0)
    ax.plot(years, g[0], marker="o", color=BLUE, lw=2, label="far: observed")
    ax.plot(years, g[1], marker="o", color=RED, lw=2.4, label="near: observed")
    post = years >= 2005
    ax.plot(years[post], did_cf[post], ls="--", color=GOLD, lw=2.2,
            label="near without the site, as DiD assumes (far's trend)")
    ax.plot(years[post], true_cf[post], ls=":", color=INK, lw=2.2,
            label="near without the site, in truth (still slipping)")
    y8 = 2008.08
    ax.annotate("", xy=(y8, g.loc[2008, 1]), xytext=(y8, true_cf[2008]),
                arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text(y8 + 0.06, (g.loc[2008, 1] + true_cf[2008]) / 2, "true\neffect −10", fontsize=9.5)
    ax.annotate("", xy=(y8 + 0.35, g.loc[2008, 1]), xytext=(y8 + 0.35, did_cf[2008]),
                arrowprops=dict(arrowstyle="<->", color=GOLD))
    ax.text(y8 + 0.41, (g.loc[2008, 1] + did_cf[2008]) / 2 + 3, f"DiD\n{g.loc[2008, 1] - did_cf[2008]:.0f}",
            fontsize=9.5, color=GOLD, fontweight="bold")
    ax.set_xlim(2002.7, 2009.1)
    ax.set_xticks(years)
    ax.set_ylabel("average price, $ thousands")
    ax.legend(frameon=False, loc="upper left", fontsize=9.5)
    ax.set_title("Version B: DiD borrows the far houses' trend, but the near ones were already falling",
                 loc="left", fontsize=11.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "housing-b-counterfactual.png")


# --- Example 3: the course data, as in book chapter 11 -------------------------------
def ai_figures():
    import sys
    import diff_diff as dd
    sys.path.insert(0, str(OUT.parents[2]))                # the repository root holds qmib.py
    import qmib

    Y, D, TRUE_EFFECT = "ai_use_any", "has_ai_strategy", 2.4
    wide = qmib.load("angle_c_country")
    adopted = wide[wide[D] == 1].groupby("geo")["time"].min()
    panel = wide[(wide["time"] >= 2021) & wide[Y].notna()].copy()
    panel["cohort"] = panel["geo"].map(adopted).fillna(9999).astype(int)

    design = pd.concat([
        panel[[Y, D]].reset_index(drop=True),
        pd.get_dummies(panel["geo"], drop_first=True, dtype=float).reset_index(drop=True),
        pd.get_dummies(panel["time"], prefix="yr", drop_first=True, dtype=float).reset_index(drop=True),
    ], axis=1)
    twfe = sm.OLS(design[Y], sm.add_constant(design.drop(columns=[Y]))).fit(
        cov_type="cluster", cov_kwds={"groups": panel["geo"].reset_index(drop=True)})

    panel["g"] = panel["cohort"].replace(9999, 0)
    cs = dd.CallawaySantAnna(cluster="geo").fit(panel, outcome=Y, unit="geo", time="time",
                                                first_treat="g")
    groups = cs.aggregate("group").to_dataframe()

    # who adopted when: the grid
    years = [2021, 2022, 2023, 2024]
    counts = panel.groupby("cohort")["geo"].nunique()
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    ax.set_xlim(-2.6, 4.2); ax.set_ylim(-0.6, 4.2); ax.axis("off")
    rows_ = [(2021, "adopted 2021"), (2022, "adopted 2022"), (2023, "adopted 2023"), (9999, "never")]
    for j, yr in enumerate(years):
        ax.text(j + 0.5, 3.95, str(yr), ha="center", fontsize=11, fontweight="bold")
    for i, (c, lab) in enumerate(rows_):
        y = 3 - i
        ax.text(-0.15, y + 0.4, f"{lab}  ·  {counts.get(c, 0)} countr{'y' if counts.get(c, 0) == 1 else 'ies'}",
                ha="right", va="center", fontsize=10.5, color=RED if c != 9999 else BLUE,
                fontweight="bold")
        for j, yr in enumerate(years):
            treated = c != 9999 and yr >= c
            ax.add_patch(plt.Rectangle((j + 0.05, y + 0.08), 0.9, 0.7,
                                       fc=RED if treated else PALE_BLUE, ec=BG, lw=2))
            ax.text(j + 0.5, y + 0.43, "treated" if treated else "before",
                    ha="center", va="center", fontsize=9, color="white" if treated else INK)
    ax.text(2.0, -0.4, "the outcome is only measured from 2021: the 2021 cohort has no 'before' cell",
            ha="center", fontsize=10, color=RED)
    save(fig, "ai-adoption.png")

    # average AI use by cohort
    means = panel.groupby(["time", "cohort"])[Y].mean().unstack()
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    cols = {2021: GOLD, 2022: RED, 2023: TEAL, 9999: BLUE}
    for c in means.columns:
        n = counts.get(c, 0)
        lab = "never adopted" if c == 9999 else f"adopted {c}"
        ax.plot(means.index, means[c], marker="o", lw=2.2, color=cols[c],
                label=f"{lab} ({n})")
        if c != 9999:
            ax.scatter([c], [means.loc[c, c]], s=160, facecolors="none", edgecolors=cols[c], lw=2)
    ax.set_xticks(means.index)
    ax.set_ylabel("share of firms using AI, %")
    ax.legend(frameon=False, fontsize=9.5, loc="lower right", bbox_to_anchor=(1.0, 0.13))
    ax.set_title("Average AI use by cohort; the circle marks each cohort's adoption year",
                 loc="left", fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "ai-trends.png")

    rows = [("two-way fixed effects, all cohorts", twfe.params[D], twfe.bse[D], GOLD),
            ("Callaway–Sant'Anna, overall", cs.overall_att, cs.overall_se, BLUE)]
    for _, r in groups.iterrows():
        n = panel.loc[panel["cohort"] == int(r.label), "geo"].nunique()
        rows.append((f"  cohort {r.label} ({n} countr{'y' if n == 1 else 'ies'})",
                     r.att, r.se, BLUE if n > 1 else MUTED))
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    ax.axvline(TRUE_EFFECT, color=TEAL, lw=2, ls="--")
    ax.axvline(0, color=MUTED, lw=1)
    ys = np.arange(len(rows))[::-1]
    for (lab, v, se, col), y in zip(rows, ys):
        ax.plot([v - 1.96 * se, v + 1.96 * se], [y, y], color=col, lw=2.5, alpha=0.6)
        ax.scatter(v, y, s=110, color=col, zorder=3)
        ax.text(v, y + 0.28, f"{v:.2f}", ha="center", fontweight="bold", fontsize=11)
    ax.text(TRUE_EFFECT + 0.08, -0.6, "truth: 2.4", color=TEAL, fontweight="bold")
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_ylim(-0.9, len(rows) - 0.3)
    ax.set_xlabel("effect of a national AI strategy on firms' AI use, percentage points (95% interval)")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "ai-estimates.png")

    es = cs.aggregate("event_study")
    Ms = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    lo, hi = [], []
    for M in Ms:
        h = dd.HonestDiD(method="relative_magnitude", M=M).fit(es)
        lo.append(h.ci_lb)
        hi.append(h.ci_ub)
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.axhline(0, color=RED, lw=1.4)
    ax.axhline(TRUE_EFFECT, color=TEAL, lw=1.4, ls="--")
    for M, a, b in zip(Ms, lo, hi):
        col = BLUE if a > 0 else MUTED
        ax.plot([M, M], [a, b], color=col, lw=5, alpha=0.8, solid_capstyle="round")
    ax.set_xticks(Ms)
    ax.set_xlabel("M: allowed post-treatment departure from parallel trends,\n"
                  "as a multiple of the one pre-treatment departure observed")
    ax.set_ylabel("95% robust interval")
    ax.set_title("The result survives M = 0.25 and not M = 0.5", loc="left",
                 fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "ai-honest.png")
    return twfe.params[D], cs.overall_att, cs.overall_se, groups, list(zip(Ms, lo, hi))


def twfe_comparisons():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.3), sharey=True)
    t = np.array([0, 1, 2, 3])
    early = np.array([10, 13, 15, 17]); late = np.array([8, 9, 10, 13]); never = np.array([9, 10, 11, 12])
    specs = [("1 · early adopter vs never: clean", (early, RED, 1), (never, BLUE, None), TEAL),
             ("2 · late adopter vs never: clean", (late, GOLD, 3), (never, BLUE, None), TEAL),
             ("3 · late vs early, already treated:\nTWFE uses it, and should not", (late, GOLD, 3), (early, RED, 1), RED)]
    for ax, (title, a, b, col) in zip(axes, specs):
        for series, c, start in (a, b):
            ax.plot(t, series, marker="o", color=c, lw=2)
            if start is not None:
                ax.axvline(start - 0.5, color=c, ls=":", lw=1.2)
        ax.set_title(title, loc="left", fontsize=10.5, fontweight="bold", color=col)
        ax.set_xticks(t, ["2021", "2022", "2023", "2024"], fontsize=9)
    axes[0].set_ylabel("outcome")
    axes[2].text(2.0, 8.0, "the 'control' here is still\nchanging because of its\nown treatment",
                 fontsize=9, color=RED, ha="center", va="bottom")
    fig.tight_layout()
    save(fig, "twfe-comparisons.png")


def iv_management(firms):
    fig, ax = plt.subplots(figsize=(8.4, 3.5))
    bins = np.linspace(-3.5, 3.5, 30)
    for e, col, lab in ((0, MUTED, "non-exporters"), (1, BLUE, "exporters")):
        v = firms.loc[firms["exports"] == e, "management"]
        ax.hist(v, bins=bins, alpha=0.6, color=col, label=f"{lab}: mean {v.mean():+.2f}")
        ax.axvline(v.mean(), color=col, lw=2)
    ax.set_xlabel("management quality (in the simulation only: real data never record it)")
    ax.set_ylabel("firms")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title("Exporters are better managed, and management raises productivity on its own",
                 loc="left", fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "iv-management.png")


# --- Example 4: an instrument (same seed, same lines as the slide) ------------------
def simulate_exporters(direct):
    """2,000 firms; exporting raises productivity by 5; management is never observed;
    distance to the nearest port moves exporting. direct != 0 lets distance also
    lower productivity on its own, which breaks the exclusion restriction."""
    rng = np.random.default_rng(13)
    n = 2000
    management = rng.normal(0, 1, n)                     # never in the data
    distance = rng.uniform(0, 300, n)                    # km to the nearest port
    exports = (0.8 * management - 0.01 * distance + rng.normal(0, 1, n) > -1.5).astype(int)
    productivity = (100 + 5 * exports + 6 * management + direct * distance
                    + rng.normal(0, 5, n))
    return pd.DataFrame({"exports": exports, "distance": distance,
                         "productivity": productivity, "management": management})


def iv_fit(firms):
    naive = (firms.loc[firms["exports"] == 1, "productivity"].mean()
             - firms.loc[firms["exports"] == 0, "productivity"].mean())
    first = smf.ols("exports ~ distance", data=firms).fit()
    reduced = smf.ols("productivity ~ distance", data=firms).fit()
    iv = IV2SLS(firms["productivity"], sm.add_constant(firms[["exports"]]),
                sm.add_constant(firms[["distance"]])).fit()
    return {"naive": naive, "first": first.params["distance"],
            "F": first.tvalues["distance"] ** 2, "reduced": reduced.params["distance"],
            "iv": iv.params["exports"], "se": iv.bse["exports"]}


def _node(ax, x, y, text, fc="white", ec=INK, dashed=False, w=2.6, h=0.9):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                       fc=fc, ec=ec, lw=1.6, ls="--" if dashed else "-", zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=11.5, fontweight="bold", zorder=4)
    return p


def _arrow(ax, a, b, color=INK, rad=0.0, lw=2, ls="-"):
    ax.add_patch(FancyArrowPatch(_c(a), _c(b), patchA=a, patchB=b,
                                 arrowstyle="-|>", mutation_scale=16, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=2))


def _c(p):
    return (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / 2)


def iv_diagram():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.6))
    for ax, title, broken in ((axes[0], "A · a valid instrument", False),
                              (axes[1], "B · the exclusion fails", True)):
        ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
        z = _node(ax, 1.6, 1.4, "distance\nto port", fc=PALE_TEAL, ec=TEAL)
        d = _node(ax, 6.0, 1.4, "exports", fc=PALE_BLUE, ec=BLUE)
        y = _node(ax, 10.4, 1.4, "productivity", fc="white")
        u = _node(ax, 8.2, 4.0, "management\n(not in the data)", fc=BG, ec=MUTED, dashed=True,
                  w=3.6, h=1.1)
        _arrow(ax, z, d, color=TEAL)
        _arrow(ax, d, y, color=BLUE, lw=2.6)
        _arrow(ax, u, d, color=MUTED, ls="--")
        _arrow(ax, u, y, color=MUTED, ls="--")
        if broken:
            _arrow(ax, z, y, color=RED, rad=0.32, lw=2.4)
            ax.text(6.0, -0.15, "remote firms also pay more for inputs", color=RED,
                    ha="center", fontsize=10.5, fontweight="bold")
        ax.set_title(title, loc="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "iv-diagram.png")


def iv_two_stages(firms, r):
    bins = pd.cut(firms["distance"], np.arange(0, 301, 30))
    g = firms.groupby(bins, observed=True).agg(d=("distance", "mean"), exp=("exports", "mean"),
                                               prod=("productivity", "mean"))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    for ax, col, raw, ylab, color, title in (
            (axes[0], "exp", "exports", "share of firms exporting", TEAL,
             f"First stage: {r['first'] * 100 * 100:+.0f} points of exporting per 100 km"),
            (axes[1], "prod", "productivity", "average productivity", BLUE,
             f"Reduced form: {r['reduced'] * 100:+.2f} productivity per 100 km")):
        ax.scatter(g["d"], g[col], s=60, color=color, zorder=3)
        xs = np.array([0, 300])
        fit = np.polyfit(firms["distance"], firms[raw], 1)
        ax.plot(xs, np.polyval(fit, xs), color=color, lw=2, alpha=0.7)
        ax.set_xlabel("distance to the nearest port, km")
        ax.set_ylabel(ylab)
        ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "iv-two-stages.png")


def iv_estimates(rA, rB):
    rows = [("A · naive: exporters vs not", rA["naive"], None, RED),
            ("A · instrumental variable", rA["iv"], rA["se"], BLUE),
            ("B · naive: exporters vs not", rB["naive"], None, RED),
            ("B · instrumental variable", rB["iv"], rB["se"], GOLD)]
    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    ax.axvline(5, color=TEAL, lw=2, ls="--")
    ys = np.arange(len(rows))[::-1]
    for (lab, v, se, col), y in zip(rows, ys):
        if se is not None:
            ax.plot([v - 1.96 * se, v + 1.96 * se], [y, y], color=col, lw=2.5, alpha=0.6)
        ax.scatter(v, y, s=110, color=col, zorder=3)
        ax.text(v, y + 0.28, f"{v:.1f}", ha="center", fontweight="bold")
    ax.text(5.2, -0.65, "truth: +5", color=TEAL, fontweight="bold")
    ax.set_yticks(ys, [r[0] for r in rows])
    ax.set_ylim(-0.9, len(rows) - 0.3)
    ax.set_xlim(0, 15)
    ax.set_xlabel("effect of exporting on productivity (95% interval for IV)")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "iv-estimates.png")


if __name__ == "__main__":
    did_idea()
    parallel_idea()
    housing_map()
    twfe_comparisons()
    houses = simulate_two_periods()
    print("betas", housing_betas(houses))
    housing_b_counterfactual()
    m, cf = housing_2x2(houses)
    print(m.round(1), "counterfactual", round(cf, 1))
    print(housing_estimators(m))
    out = housing_trends_and_events()
    for v, (did, es) in out.items():
        print(v, round(did, 1), es.round(1).to_dict())
    print(ai_figures())
    fA, fB = simulate_exporters(0.0), simulate_exporters(-0.02)
    rA, rB = iv_fit(fA), iv_fit(fB)
    print("IV A", {k: round(v, 4) for k, v in rA.items()})
    print("IV B", {k: round(v, 4) for k, v in rB.items()})
    print("management by exports", fA.groupby("exports")["management"].mean().round(2).to_dict())
    iv_diagram()
    iv_two_stages(fA, rA)
    iv_estimates(rA, rB)
    iv_management(fA)
