"""
Session 11 · the difference-in-differences figures, computed rather than drawn.

Every number on a picture here comes from the same simulation or the same data,
with the same seed, that the matching slide computes live, so what the slide
says about a picture is true of the picture.

    .venv/bin/python 11-causal-inference-did/01-lecture/economist-assets/build_did_figures.py

Writes, next to this file:
    housing-2x2.png        Example 1: four means, the counterfactual, and the two differences
    housing-estimators.png Example 1: after-only, before-after and DiD against the truth
    housing-trends.png     Example 2: six years of prices, versions A and B
    housing-event-study.png Example 2: the event study, versions A and B
    ai-estimates.png       Example 3: TWFE, Callaway-Sant'Anna and the cohorts, against the truth
    ai-honest.png          Example 3: how large a violation of parallel trends the result survives
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

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


if __name__ == "__main__":
    houses = simulate_two_periods()
    m, cf = housing_2x2(houses)
    print(m.round(1), "counterfactual", round(cf, 1))
    print(housing_estimators(m))
    out = housing_trends_and_events()
    for v, (did, es) in out.items():
        print(v, round(did, 1), es.round(1).to_dict())
    print(ai_figures())
