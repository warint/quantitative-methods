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
    houses = simulate_two_periods()
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
