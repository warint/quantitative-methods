"""
Session 10 · the causal-inference figures, computed rather than drawn.

Every number on a picture here comes from the same simulation or the same
data, with the same seed, that the matching slide computes live, so what the
slide says about a picture is true of the picture.

    .venv/bin/python 10-causal-inference-foundations/01-lecture/economist-assets/build_causal_figures.py

Writes, next to this file:
    po-table.png          the table you never get to see: both potential outcomes
    po-decomposition.png  naive difference = effect + selection bias, in bars
    dag-selection.png     why self-selection biases the comparison (and a coin flip does not)
    nsw-design.png        LaLonde's test: an experiment, then its controls swapped for a survey
    matching-idea.png     each treated person paired with the nearest control on the score
    nsw-estimates.png     every estimate on one axis, against the experimental benchmark
    dag-bad-control.png   a confounder to control for, a mediator not to
    ci-workflow.png       the seven steps of a matching study
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch
from sklearn.neighbors import NearestNeighbors

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


# --- drawing primitives -----------------------------------------------------
def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, text, w=1.3, h=0.62, fs=12, fc="white", ec=INK, bold=False):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                       fc=fc, ec=ec, lw=1.3, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
            fontweight="bold" if bold else "normal")
    return p


def oval(ax, x, y, text, w=2.6, h=1.0, fs=12, fc=PALE_BLUE, ec=BLUE):
    p = Ellipse((x, y), w, h, fc=fc, ec=ec, lw=1.8, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, fontweight="bold", zorder=4)
    return p


def link(ax, a, b, label=None, color=MUTED, lw=1.6, rad=0.0, dashed=False, fs=11,
         lcolor=None):
    ca, cb = _centre(a), _centre(b)
    arr = FancyArrowPatch(ca, cb, patchA=a, patchB=b, arrowstyle="-|>",
                          mutation_scale=15, lw=lw, color=color, zorder=2,
                          connectionstyle=f"arc3,rad={rad}",
                          linestyle=(0, (4, 3)) if dashed else "-")
    ax.add_patch(arr)
    if label is not None:
        mx, my = (ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2
        mx += rad * (cb[1] - ca[1]) * 0.5
        my -= rad * (cb[0] - ca[0]) * 0.5
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=lcolor or color, zorder=5, bbox=dict(fc=BG, ec="none", pad=1.5))
    return arr


def _centre(p):
    if isinstance(p, Ellipse):
        return p.center
    return (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / 2)


def note(ax, x, y, text, color=MUTED, fs=11, ha="left", va="center", **kw):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, **kw)


def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("wrote", name)


# --- the simulation the slides run (same seed, same lines) ------------------
def simulate():
    rng = np.random.default_rng(10)
    n = 1000
    productivity = rng.normal(0, 1, n)
    sales_without = 10 + 3 * productivity + rng.normal(0, 2, n)
    sales_with = sales_without + 2
    firms = pd.DataFrame({"productivity": productivity,
                          "sales_without": sales_without, "sales_with": sales_with})
    firms["applies"] = (productivity + rng.normal(0, 1, n) > 0.5).astype(int)
    return firms


# --- the LaLonde / Dehejia-Wahba analysis the slides run ---------------------
URL = "https://users.nber.org/~rdehejia/data/"
X = ["age", "education", "black", "hispanic", "married", "nodegree", "re74", "re75"]
PS1 = "treat ~ age + education + black + hispanic + married + nodegree + re74 + re75"
PS2 = PS1 + " + I(age**2) + I(re74 == 0) + I(re75 == 0)"


def nsw_numbers():
    nsw = pd.read_stata(URL + "nsw_dw.dta")
    cps = pd.read_stata(URL + "cps_controls.dta")
    ols = smf.ols("re78 ~ treat", data=nsw).fit()
    exp, exp_se = ols.params["treat"], ols.bse["treat"]
    df = pd.concat([nsw[nsw["treat"] == 1], cps], ignore_index=True)
    naive = df.loc[df["treat"] == 1, "re78"].mean() - df.loc[df["treat"] == 0, "re78"].mean()
    reg = smf.ols("re78 ~ treat + " + " + ".join(X), data=df).fit().params["treat"]
    out = {"experiment": (exp, exp_se), "naive": naive, "regression": reg}
    for key, f in [("match1", PS1), ("match2", PS2)]:
        df["pscore"] = smf.logit(f, data=df).fit(disp=0).predict(df)
        t, c = df[df["treat"] == 1], df[df["treat"] == 0]
        nn = NearestNeighbors(n_neighbors=1).fit(c[["pscore"]])
        _, idx = nn.kneighbors(t[["pscore"]])
        out[key] = t["re78"].mean() - c.iloc[idx.ravel()]["re78"].mean()
    return out


# --- 1. the table you never see ---------------------------------------------
def po_table(firms):
    # three firms that applied and three that did not, in their original order
    rows = pd.concat([firms[firms["applies"] == 1].head(3),
                      firms[firms["applies"] == 0].head(3)]).sort_index()
    fig, ax = plt.subplots(figsize=(10.5, 3.9))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.4, 7.4)
    ax.axis("off")
    cols = [(0.9, "firm"), (2.9, "sales WITH\nthe programme"), (5.1, "sales WITHOUT\nthe programme"),
            (7.2, "effect\nfor this firm"), (9.3, "what you\nobserve")]
    for x, t in cols:
        ax.text(x, 6.8, t, ha="center", va="center", fontsize=11.5, fontweight="bold")
    ax.plot([0.2, 10.3], [6.15, 6.15], color=INK, lw=1)
    for i, (_, r) in enumerate(rows.iterrows()):
        y = 5.55 - i * 0.95
        treated = bool(r.applies)
        ax.text(0.9, y, f"{r.name + 1}", ha="center", va="center", fontsize=12)
        for x, v, seen in [(2.9, r.sales_with, treated), (5.1, r.sales_without, not treated)]:
            ax.add_patch(FancyBboxPatch((x - 0.75, y - 0.33), 1.5, 0.66,
                                        boxstyle="round,pad=0,rounding_size=0.06",
                                        fc=PALE_BLUE if seen else "#ECE8DF",
                                        ec=BLUE if seen else GRID, lw=1.2))
            ax.text(x, y, f"{v:.1f}" if seen else "?", ha="center", va="center",
                    fontsize=12.5, color=INK if seen else MUTED,
                    fontweight="bold" if seen else "normal")
        ax.text(7.2, y, "?", ha="center", va="center", fontsize=13, color=RED,
                fontweight="bold")
        ax.text(9.3, y, "took it" if treated else "did not", ha="center", va="center",
                fontsize=11, color=BLUE if treated else MUTED)
    save(fig, "po-table.png")


# --- 2. naive = effect + selection bias -------------------------------------
def po_decomposition(firms):
    a = firms["applies"] == 1
    observed = np.where(a, firms["sales_with"], firms["sales_without"])
    naive = observed[a].mean() - observed[~a].mean()
    effect = (firms.loc[a, "sales_with"] - firms.loc[a, "sales_without"]).mean()
    bias = firms.loc[a, "sales_without"].mean() - firms.loc[~a, "sales_without"].mean()
    fig, ax = plt.subplots(figsize=(9, 3.3))
    ax.barh(2, naive, color=INK, height=0.55)
    ax.barh(1, effect, color=TEAL, height=0.55)
    ax.barh(1, bias, left=effect, color=RED, height=0.55)
    ax.barh(0, effect, color=TEAL, height=0.55)
    ax.text(naive + 0.1, 2, f"{naive:.2f}", va="center", fontsize=12, fontweight="bold")
    ax.text(effect / 2, 1, f"effect\n{effect:.2f}", va="center", ha="center",
            fontsize=10.5, color="white", fontweight="bold")
    ax.text(effect + bias / 2, 1, f"selection bias  {bias:.2f}", va="center", ha="center",
            fontsize=11, color="white", fontweight="bold")
    ax.text(effect + 0.1, 0, f"{effect:.2f}", va="center", fontsize=12, fontweight="bold",
            color=TEAL)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(["what you compute:\nmean(applied) − mean(did not)",
                        "is really", "what you wanted:\nthe effect on those who applied"],
                       fontsize=11)
    ax.set_xlim(0, 6.6)
    ax.set_xlabel("sales growth, percentage points")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "po-decomposition.png")
    return naive, effect, bias


# --- 3. the selection diagram -------------------------------------------------
def dag_selection():
    fig, ax = canvas(12, 3.6, (-0.4, 23.6), (-3.6, 3.4))
    for x0, title, coin in [(0, "Firms choose", False), (12.2, "A coin decides", True)]:
        note(ax, x0 + 5.5, 3.0, title, ha="center", color=RED if not coin else TEAL,
             fontweight="bold", fs=14)
        p = oval(ax, x0 + 5.5, 1.3, "productivity", w=3.6, h=1.0, fc="#ECE8DF", ec=MUTED)
        t = box(ax, x0 + 1.9, -1.9, "programme", w=3.4, h=0.9, fc=PALE_BLUE, ec=BLUE, bold=True)
        y = box(ax, x0 + 9.1, -1.9, "sales growth", w=3.4, h=0.9, fc=PALE_BLUE, ec=BLUE, bold=True)
        link(ax, t, y, label="effect: +2", color=TEAL, lw=2.2, lcolor=TEAL)
        link(ax, p, y, color=MUTED, lw=1.6)
        if coin:
            c = box(ax, x0 + 1.9, 1.3, "coin", w=1.6, h=0.8, fc="white", ec=TEAL)
            link(ax, c, t, color=TEAL, lw=1.6)
            note(ax, x0 + 5.5, -3.25, "productivity no longer reaches the programme:\n"
                 "the groups differ only by chance", ha="center", fs=10.5, color=TEAL)
        else:
            link(ax, p, t, color=RED, lw=2.0)
            note(ax, x0 + 5.5, -3.25, "a back door: productivity drives both,\n"
                 "so the comparison mixes the two paths", ha="center", fs=10.5, color=RED)
    ax.plot([11.7, 11.7], [-3.5, 3.3], color=GRID, lw=1.2)
    save(fig, "dag-selection.png")


# --- 4. LaLonde's design ------------------------------------------------------
def nsw_design():
    fig, ax = canvas(12.5, 3.4, (-0.3, 25.3), (-3.3, 3.3))
    note(ax, 5.6, 2.9, "1 · The experiment (1976–77)", ha="center", fontweight="bold",
         fs=13, color=TEAL)
    a = box(ax, 2.8, 1.0, "185 trained\n(by lottery)", w=4.4, h=1.3, fc=PALE_BLUE, ec=BLUE)
    b = box(ax, 8.4, 1.0, "260 not trained\n(by lottery)", w=4.4, h=1.3, fc=PALE_TEAL, ec=TEAL)
    note(ax, 5.6, -1.3, "difference in 1978 earnings\n= the true effect, about +$1,800",
         ha="center", fs=11.5, color=TEAL, fontweight="bold")
    note(ax, 19.4, 2.9, "2 · The test LaLonde set (1986)", ha="center", fontweight="bold",
         fs=13, color=RED)
    c = box(ax, 16.6, 1.0, "the same\n185 trained", w=4.4, h=1.3, fc=PALE_BLUE, ec=BLUE)
    d = box(ax, 22.2, 1.0, "15,992 people from\na survey (CPS)", w=4.8, h=1.3, fc=PALE_RED, ec=RED)
    note(ax, 19.4, -1.3, "can a method applied to these\nrecover +$1,800?",
         ha="center", fs=11.5, color=RED, fontweight="bold")
    arr = FancyArrowPatch((10.9, 1.0), (14.1, 1.0), arrowstyle="-|>", mutation_scale=18,
                          lw=2, color=INK)
    ax.add_patch(arr)
    note(ax, 12.5, 1.6, "throw away\nthe controls", ha="center", va="bottom", fs=10)
    note(ax, 12.5, -2.85, "The experiment gives the answer. The survey version is the "
         "situation you are usually in.", ha="center", fs=11, color=INK)
    _ = (a, b, c, d)
    save(fig, "nsw-design.png")


# --- 5. the matching idea ----------------------------------------------------
def matching_idea():
    rng = np.random.default_rng(4)
    treated = np.sort(rng.uniform(0.25, 0.85, 7))
    control = np.sort(np.concatenate([rng.uniform(0.02, 0.35, 12), rng.uniform(0.3, 0.8, 6)]))
    fig, ax = plt.subplots(figsize=(11, 2.9))
    ax.set_xlim(-0.13, 1.02)
    ax.set_ylim(-1.6, 1.9)
    ax.axis("off")
    ax.plot([0, 1], [-0.62, -0.62], color=GRID, lw=1)
    for x in np.linspace(0, 1, 6):
        ax.plot([x, x], [-0.66, -0.58], color=MUTED, lw=1)
        ax.text(x, -0.78, f"{x:.1f}", ha="center", va="top", fontsize=9.5, color=MUTED)
    used = set()
    for t in treated:
        j = int(np.argmin(np.abs(control - t)))
        used.add(j)
        ax.plot([t, control[j]], [1.15, -0.15], color=INK, lw=1, alpha=0.6)
    ax.scatter(treated, np.full_like(treated, 1.2), s=120, color=BLUE, zorder=3)
    ax.scatter(control, np.full_like(control, -0.2), s=120, zorder=3,
               color=[TEAL if j in used else "#CFC9BD" for j in range(len(control))])
    ax.text(-0.01, 1.2, "treated", ha="right", va="center", fontsize=12, color=BLUE,
            fontweight="bold")
    ax.text(-0.01, -0.2, "controls", ha="right", va="center", fontsize=12, color=TEAL,
            fontweight="bold")
    ax.text(0.5, 1.75, "propensity score: the probability of being treated, given X",
            ha="center", fontsize=12)
    ax.text(0.5, -1.2, "grey controls are nobody's nearest match: they never enter the comparison",
            ha="center", va="top", fontsize=11, color=MUTED)
    save(fig, "matching-idea.png")


# --- 6. every estimate on one axis --------------------------------------------
def nsw_estimates(r):
    exp, se = r["experiment"]
    labels = ["naive: trained vs survey", "regression with the 8 controls",
              "matching, first score", "matching, score fixed for balance",
              "the experiment (benchmark)"]
    vals = [r["naive"], r["regression"], r["match1"], r["match2"], exp]
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axvspan(exp - 1.96 * se, exp + 1.96 * se, color=PALE_TEAL, zorder=0)
    ax.axvline(exp, color=TEAL, lw=1.5, ls="--", zorder=1)
    ax.axvline(0, color=MUTED, lw=1)
    yy = np.arange(len(vals))[::-1]
    cols = [RED, GOLD, BLUE, BLUE, TEAL]
    ax.scatter(vals, yy, s=110, color=cols, zorder=3)
    for v, y in zip(vals, yy):
        ax.text(v, y + 0.32, f"{v:+,.0f}", ha="center", fontsize=11, fontweight="bold")
    ax.set_yticks(yy)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_ylim(-0.6, len(vals) - 0.2)
    ax.set_xlabel("estimated effect of training on 1978 earnings, US dollars")
    ax.text(exp + 1.96 * se + 150, 0.0, "95% interval of\nthe experiment", fontsize=9.5,
            color=TEAL, va="center")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "nsw-estimates.png")


# --- 7. good and bad controls ---------------------------------------------------
def dag_bad_control():
    fig, ax = canvas(12, 3.4, (-0.4, 23.6), (-3.2, 3.2))
    for x0, title, col, kind in [(0, "Control for it: a confounder", TEAL, "conf"),
                                 (12.2, "Do not: a mediator", RED, "med")]:
        note(ax, x0 + 5.5, 2.85, title, ha="center", color=col, fontweight="bold", fs=13.5)
        t = box(ax, x0 + 1.9, -1.2, "programme", w=3.4, h=0.9, fc=PALE_BLUE, ec=BLUE, bold=True)
        y = box(ax, x0 + 9.1, -1.2, "sales growth", w=3.4, h=0.9, fc=PALE_BLUE, ec=BLUE, bold=True)
        if kind == "conf":
            z = oval(ax, x0 + 5.5, 1.3, "firm size\nbefore", w=3.4, h=1.2, fc=PALE_TEAL, ec=TEAL)
            link(ax, z, t, color=TEAL)
            link(ax, z, y, color=TEAL)
            link(ax, t, y, color=INK, lw=2)
            note(ax, x0 + 5.5, -2.65, "measured BEFORE: it opens a back door; close it",
                 ha="center", fs=10.5, color=TEAL)
        else:
            z = oval(ax, x0 + 5.5, 1.3, "new export\ncontracts", w=3.4, h=1.2, fc=PALE_RED, ec=RED)
            link(ax, t, z, color=RED)
            link(ax, z, y, color=RED)
            link(ax, t, y, color=INK, lw=2)
            note(ax, x0 + 5.5, -2.65, "measured AFTER: part of the effect; controlling removes it",
                 ha="center", fs=10.5, color=RED)
    ax.plot([11.7, 11.7], [-3.1, 3.1], color=GRID, lw=1.2)
    save(fig, "dag-bad-control.png")


# --- 8. the workflow ------------------------------------------------------------
def workflow():
    steps = ["1 · Question\nATE or ATT?", "2 · Draw\nwhat drives T", "3 · Naive\ndifference",
             "4 · Score\nsmf.logit", "5 · Match\nnearest\nneighbours", "6 · Check\nbalance",
             "7 · Estimate\nthe ATT"]
    fig, ax = canvas(13, 3.4, (-0.3, 27.6), (-3.4, 2.2))
    prev = None
    for i, s in enumerate(steps):
        b = box(ax, 1.8 + 3.95 * i, 0, s, w=3.7, h=1.7, fs=9.8,
                fc=PALE_BLUE if i < 2 else "white")
        if prev is not None:
            link(ax, prev, b, color=INK, lw=1.4)
        prev = b
    back = FancyArrowPatch((21.6, -0.9), (13.6, -0.9), connectionstyle="arc3,rad=-0.35",
                           arrowstyle="-|>", mutation_scale=14, lw=1.6, color=RED,
                           linestyle=(0, (4, 3)), zorder=1)
    ax.add_patch(back)
    note(ax, 17.6, -2.95, "not balanced? change the SCORE, never look at the outcome first",
         ha="center", color=RED, fontweight="bold", fs=12)
    note(ax, 3.8, 1.4, "on paper, before Python", ha="center", color=BLUE,
         fontweight="bold", fs=11, va="bottom")
    save(fig, "ci-workflow.png")


if __name__ == "__main__":
    firms = simulate()
    po_table(firms)
    print("decomposition (naive, effect, bias):", po_decomposition(firms))
    dag_selection()
    nsw_design()
    matching_idea()
    r = nsw_numbers()
    print(r)
    nsw_estimates(r)
    dag_bad_control()
    workflow()
