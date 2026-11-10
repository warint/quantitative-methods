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
    firms-two-outcomes.png  Example 1: both potential outcomes for 40 firms, +2 apart
    firms-who-joins.png   Example 1: the probability of joining rises with productivity
    coin-vs-choice.png    Example 1: productivity of the two groups, under a coin and under choice
    coin-histogram.png    1,000 coin flips: randomisation is right on average
    firms-balance.png     productivity of the firms that joined and did not, before the programme
    nsw-design.png        LaLonde's test: an experiment, then its controls swapped for a survey
    nsw-profiles.png      Example 2: trainees against survey people, four characteristics
    nsw-pairs.png         Example 2: what a match looks like, five trainees and their matches
    nsw-overlap.png       the propensity score in each group: is there anyone to compare with?
    nsw-regression.png    Example 2: regression extrapolates along a line; matching compares like with like
    nsw-loveplot.png      standardised differences before and after matching (the love plot)
    matching-idea.png     each treated person paired with the nearest control on the score
    nsw-estimates.png     every estimate on one axis, against the experimental benchmark
    hr-dag.png            Example 3: who enrols, in versions A and B
    hr-estimates.png      Example 3: naive and matched estimates, selection on records vs on motivation
    hr-hidden.png         Example 3: perfect balance on the records, none on motivation
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


# Example 3: the employee-training simulation the slides run (same seed, same lines)
def simulate_staff():
    rng = np.random.default_rng(10)
    n = 800
    age = rng.normal(40, 10, n).round()
    education = rng.normal(14, 2, n).round()
    experience = np.clip(age - 6 - education + rng.normal(0, 3, n), 0, None).round()
    motivation = rng.normal(0, 1, n)                      # never in the HR file
    perf_without = (50 + 0.3 * experience + 1.5 * (education - 14) + 4 * motivation
                    + rng.normal(0, 5, n))
    perf_with = perf_without + 5                          # the true effect: +5
    records = -1 + 0.05 * (age - 40) + 0.4 * (education - 14) + 0.03 * (experience - 20)
    out = {}
    for version, index in [("A", records), ("B", records + 1.2 * motivation)]:
        draw = np.random.default_rng(11)
        treat = (draw.uniform(size=n) < 1 / (1 + np.exp(-index))).astype(int)
        out[version] = pd.DataFrame({
            "age": age, "education": education, "experience": experience,
            "motivation": motivation, "treat": treat,
            "performance": np.where(treat == 1, perf_with, perf_without)})
    return out


def match_staff(staff):
    staff = staff.copy()
    staff["pscore"] = smf.logit("treat ~ age + education + experience",
                                data=staff).fit(disp=0).predict(staff)
    t, c = staff[staff["treat"] == 1], staff[staff["treat"] == 0]
    _, idx = NearestNeighbors(n_neighbors=1).fit(c[["pscore"]]).kneighbors(t[["pscore"]])
    return t, c, c.iloc[idx.ravel()]


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


# --- 2b. Example 1: a thousand coins, and the balance a choice destroys --------
def coin_histogram():
    rng = np.random.default_rng(10)
    n = 1000
    productivity = rng.normal(0, 1, n)
    sales_without = 10 + 3 * productivity + rng.normal(0, 2, n)
    sales_with = sales_without + 2
    est = []
    for _ in range(1000):
        coin = rng.integers(0, 2, n)
        obs = np.where(coin == 1, sales_with, sales_without)
        est.append(obs[coin == 1].mean() - obs[coin == 0].mean())
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.hist(est, bins=30, color=BLUE, alpha=0.85)
    ax.axvline(2, color=RED, lw=2)
    ax.text(1.98, ax.get_ylim()[1] * 0.92, "true effect: +2", color=RED, fontweight="bold",
            ha="right", bbox=dict(fc=BG, ec="none", pad=1.5))
    ax.set_xlabel("difference in means, one coin flip per firm, 1,000 experiments")
    ax.set_ylabel("experiments")
    ax.set_title(f"Centred on the truth (mean {np.mean(est):.2f}); any one experiment misses by "
                 f"about {np.std(est):.2f}", loc="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "coin-histogram.png")


def firms_balance(firms):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    groups = [firms.loc[firms["applies"] == g, "productivity"] for g in (0, 1)]
    bp = ax.boxplot(groups, widths=0.5, patch_artist=True, medianprops=dict(color=INK))
    for patch, col in zip(bp["boxes"], (PALE_BLUE, PALE_RED)):
        patch.set_facecolor(col)
    ax.set_xticks([1, 2], [f"did not join\nmean {groups[0].mean():.2f}",
                           f"joined\nmean {groups[1].mean():.2f}"])
    ax.set_ylabel("productivity, before the programme")
    ax.set_title("The firms that chose to join were already different", loc="left",
                 fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "firms-balance.png")


# --- 5b. Example 2: overlap and the love plot -----------------------------------
def nsw_overlap_and_balance():
    nsw = pd.read_stata(URL + "nsw_dw.dta")
    cps = pd.read_stata(URL + "cps_controls.dta")
    df = pd.concat([nsw[nsw["treat"] == 1], cps], ignore_index=True)
    t0, c0 = df[df["treat"] == 1], df[df["treat"] == 0]
    sd = np.sqrt((t0[X].var() + c0[X].var()) / 2)
    before = (t0[X].mean() - c0[X].mean()) / sd
    after = {}
    for key, f in [("first score", PS1), ("score fixed for balance", PS2)]:
        df["pscore"] = smf.logit(f, data=df).fit(disp=0).predict(df)
        t, c = df[df["treat"] == 1], df[df["treat"] == 0]
        _, idx = NearestNeighbors(n_neighbors=1).fit(c[["pscore"]]).kneighbors(t[["pscore"]])
        after[key] = (t[X].mean() - c.iloc[idx.ravel()][X].mean()) / sd
        if key == "first score":
            fig, ax = plt.subplots(figsize=(8, 3.8))
            bins = np.linspace(0, 0.5, 26)
            ax.hist(c["pscore"], bins=bins, alpha=0.75, color=BLUE, label="survey (control)")
            ax.hist(t["pscore"], bins=bins, alpha=0.75, color=RED, label="trained")
            ax.set_yscale("log")
            ax.set_xlabel("propensity score: the probability of being trained")
            ax.set_ylabel("people (log scale)")
            ax.legend(frameon=False)
            ax.set_title("Almost every survey person sits near 0, but every bar with trainees "
                         "also has controls", loc="left", fontsize=12, fontweight="bold")
            fig.tight_layout()
            save(fig, "nsw-overlap.png")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axvspan(-0.1, 0.1, color=PALE_TEAL, zorder=0)
    ax.axvline(0, color=MUTED, lw=1)
    y = np.arange(len(X))
    ax.scatter(before.astype(float), y, s=60, color=RED, label="before matching", zorder=3)
    ax.scatter(after["first score"].astype(float), y, s=60, color=GOLD,
               label="after, first score", zorder=3)
    ax.scatter(after["score fixed for balance"].astype(float), y, s=60, color=BLUE,
               label="after, score fixed for balance", zorder=3)
    ax.set_yticks(y, X)
    ax.invert_yaxis()
    ax.set_xlabel("standardised difference, trained minus controls (shaded: within ±0.1)")
    ax.legend(frameon=False, loc="lower right", fontsize=10)
    ax.set_title("The love plot: matching closes every gap; age needs a better score",
                 loc="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "nsw-loveplot.png")


# --- 2c. Example 1, made visible ----------------------------------------------------
def firms_two_outcomes(firms):
    """Both columns for 40 firms: the vertical gap is the effect, the slope is productivity."""
    f = firms.head(40)
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    for _, r in f.iterrows():
        ax.plot([r.productivity, r.productivity], [r.sales_without, r.sales_with],
                color=GRID, lw=2, zorder=1)
    ax.scatter(f["productivity"], f["sales_without"], s=40, color=MUTED,
               label="Y(0): growth WITHOUT the programme", zorder=2)
    ax.scatter(f["productivity"], f["sales_with"], s=40, color=BLUE,
               label="Y(1): growth WITH the programme", zorder=3)
    xs = np.linspace(-2.5, 2.5, 2)
    ax.plot(xs, 10 + 3 * xs, color=MUTED, lw=1.2, ls="--")
    ax.plot(xs, 12 + 3 * xs, color=BLUE, lw=1.2, ls="--")
    i = f["productivity"].idxmax()
    ax.annotate("each firm's effect:\nexactly +2", xy=(f.loc[i, "productivity"], f.loc[i, "sales_with"] - 1),
                xytext=(1.0, 2.5), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK))
    ax.set_xlabel("productivity (nobody in the ministry sees it)")
    ax.set_ylabel("export sales growth, points")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.set_title("In a simulation both columns exist; in real data you see one dot per firm",
                 loc="left", fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "firms-two-outcomes.png")


def firms_who_joins(firms):
    """P(join | productivity): applies = productivity + noise > 0.5, so P = Phi(productivity - 0.5)."""
    from scipy.stats import norm
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    xs = np.linspace(-3, 3, 200)
    ax.plot(xs, norm.cdf(xs - 0.5), color=RED, lw=2.4, label="probability of joining")
    jit = np.random.default_rng(0).uniform(-0.04, 0.04, len(firms))
    ax.scatter(firms["productivity"], firms["applies"] + jit, s=6, alpha=0.25,
               color=np.where(firms["applies"] == 1, RED, MUTED))
    ax.set_yticks([0, 0.5, 1], ["did not join", "50%", "joined"])
    ax.set_xlabel("productivity")
    ax.set_title("The more productive the firm, the more likely it joins: that is self-selection",
                 loc="left", fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "firms-who-joins.png")


def coin_vs_choice(firms):
    rng = np.random.default_rng(10)                     # the coin cell's own draws
    n = 1000
    productivity = rng.normal(0, 1, n)
    rng.normal(0, 2, n)
    coin = rng.integers(0, 2, n)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    bins = np.linspace(-3.5, 3.5, 29)
    for ax, groups, title in (
            (axes[0], (productivity[coin == 0], productivity[coin == 1]),
             "A coin decides: the groups overlap"),
            (axes[1], (firms.loc[firms["applies"] == 0, "productivity"],
                       firms.loc[firms["applies"] == 1, "productivity"]),
             "The firms decide: the joiners sit to the right")):
        ax.hist(groups[0], bins=bins, alpha=0.6, color=MUTED, label="did not join")
        ax.hist(groups[1], bins=bins, alpha=0.6, color=RED, label="joined")
        for g, col in ((groups[0], MUTED), (groups[1], RED)):
            ax.axvline(np.mean(g), color=col, lw=2)
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
        ax.set_xlabel("productivity, before the programme")
        ax.text(0.98, 0.95, f"means: {np.mean(groups[0]):+.2f} vs {np.mean(groups[1]):+.2f}",
                transform=ax.transAxes, ha="right", va="top", fontsize=10.5)
    axes[0].set_ylabel("firms")
    axes[0].legend(frameon=False, loc="upper left", fontsize=10)
    fig.tight_layout()
    save(fig, "coin-vs-choice.png")


# --- 5c. Example 2, made visible ----------------------------------------------------
def _nsw_data():
    nsw = pd.read_stata(URL + "nsw_dw.dta")
    cps = pd.read_stata(URL + "cps_controls.dta")
    return nsw, pd.concat([nsw[nsw["treat"] == 1], cps], ignore_index=True)


def nsw_profiles():
    _, df = _nsw_data()
    t, c = df[df["treat"] == 1], df[df["treat"] == 0]
    items = [("age", "age, years", "{:.0f}"), ("married", "share married", "{:.0%}"),
             ("nodegree", "share without a diploma", "{:.0%}"),
             ("re75", "earnings in 1975, $", "{:,.0f}")]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.0))
    for ax, (col, lab, fmt) in zip(axes, items):
        vals = [t[col].mean(), c[col].mean()]
        ax.bar([0, 1], vals, color=[RED, MUTED], width=0.6)
        for x, v in zip([0, 1], vals):
            ax.text(x, v, fmt.format(v), ha="center", va="bottom", fontsize=11, fontweight="bold")
        ax.set_xticks([0, 1], ["trainees", "survey"])
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_title(lab, fontsize=11.5, fontweight="bold")
        ax.set_ylim(0, max(vals) * 1.25)
    fig.suptitle("The survey's average worker is nobody's idea of a trainee", x=0.01, ha="left",
                 fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "nsw-profiles.png")


def nsw_pairs():
    _, df = _nsw_data()
    df["pscore"] = smf.logit(PS2, data=df).fit(disp=0).predict(df)
    t, c = df[df["treat"] == 1], df[df["treat"] == 0]
    _, idx = NearestNeighbors(n_neighbors=1).fit(c[["pscore"]]).kneighbors(t[["pscore"]])
    m = c.iloc[idx.ravel()]
    rows = list(range(0, 185, 37))[:5]
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.axis("off")
    ax.set_xlim(0, 11); ax.set_ylim(-0.3, 6.4)
    head = ["", "score", "age", "school", "earned 1975", "earned 1978"]
    xs = [0.9, 2.6, 3.9, 5.1, 6.9, 9.4]
    for x, h in zip(xs, head):
        ax.text(x, 6.0, h, ha="center", fontsize=11, fontweight="bold")
    ax.plot([0.1, 10.9], [5.65, 5.65], color=INK, lw=1)
    for k, i in enumerate(rows):
        y = 5.1 - k * 1.05
        for dy, r, who, col in ((0.22, t.iloc[i], "trainee", RED), (-0.22, m.iloc[i], "match", BLUE)):
            ax.text(xs[0], y + dy, who, ha="center", va="center", fontsize=10, color=col,
                    fontweight="bold")
            vals = [f"{r.pscore:.3f}", f"{r.age:.0f}", f"{r.education:.0f}",
                    f"${r.re75:,.0f}", f"${r.re78:,.0f}"]
            for x, v in zip(xs[1:], vals):
                ax.text(x, y + dy, v, ha="center", va="center", fontsize=10.5,
                        color=INK if x < 9 else col, fontweight="bold" if x > 9 else "normal")
        ax.plot([0.1, 10.9], [y - 0.5, y - 0.5], color=GRID, lw=0.8)
    ax.text(8.15, -0.15, "← fixed before training: matched on these   ·   after: compared →",
            ha="center", fontsize=9.5, color=MUTED)
    save(fig, "nsw-pairs.png")


def nsw_regression():
    """re75 against re78: the treated sit near zero; a line through everyone carries the comparison."""
    _, df = _nsw_data()
    df["pscore"] = smf.logit(PS2, data=df).fit(disp=0).predict(df)
    t, c = df[df["treat"] == 1], df[df["treat"] == 0]
    _, idx = NearestNeighbors(n_neighbors=1).fit(c[["pscore"]]).kneighbors(t[["pscore"]])
    m = c.iloc[idx.ravel()]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    sample = c.sample(3000, random_state=1)
    ax.scatter(sample["re75"] / 1000, sample["re78"] / 1000, s=5, alpha=0.18, color=MUTED,
               label="survey people (3,000 of 15,992)")
    ax.scatter(m["re75"] / 1000, m["re78"] / 1000, s=22, color=BLUE, alpha=0.8,
               label="the controls matching uses")
    ax.scatter(t["re75"] / 1000, t["re78"] / 1000, s=22, color=RED, alpha=0.8, label="trainees")
    fit = np.polyfit(c["re75"], c["re78"], 1)
    xs = np.array([0, 26000])
    ax.plot(xs / 1000, np.polyval(fit, xs) / 1000, color=GOLD, lw=2.4,
            label="a straight line through every survey person")
    ax.set_xlim(-1, 27); ax.set_ylim(-1, 40)
    ax.set_xlabel("earnings in 1975, $ thousands (before training)")
    ax.set_ylabel("earnings in 1978, $ thousands")
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.set_title("The line is learnt where the survey people are; the trainees sit at the far left",
                 loc="left", fontsize=11.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "nsw-regression.png")


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


def hr_dag():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.4))
    for ax, title, hidden in ((axes[0], "A · enrolment follows the HR file", False),
                              (axes[1], "B · motivation drives it too", True)):
        ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
        rec = box(ax, 1.8, 2.5, "age, education,\nexperience", w=3.0, h=1.2, fs=11,
                  fc=PALE_BLUE, ec=BLUE)
        tr = box(ax, 6.0, 2.5, "takes the\ncourse", w=2.2, h=1.2, fs=11, bold=True)
        y = box(ax, 10.2, 2.5, "performance", w=2.6, h=1.2, fs=11, bold=True)
        link(ax, rec, tr, color=BLUE, lw=2)
        link(ax, tr, y, color=TEAL, lw=2.6, label="+5", lcolor=TEAL)
        link(ax, rec, y, color=BLUE, lw=1.6, rad=0.35)
        mot = box(ax, 8.1, 4.5, "motivation (not in the file)", w=4.6, h=0.8, fs=10.5,
                  fc=BG, ec=RED if hidden else GRID)
        if hidden:
            link(ax, mot, tr, color=RED, lw=2, dashed=True)
        link(ax, mot, y, color=RED if hidden else GRID, lw=2 if hidden else 1.4, dashed=True)
        ax.set_title(title, loc="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "hr-dag.png")


# --- 6b. Example 3: what matching cannot see ------------------------------------
def hr_figures(staff):
    res = {}
    for v, d in staff.items():
        t, c, m = match_staff(d)
        res[v] = {"naive": t["performance"].mean() - c["performance"].mean(),
                  "matched": t["performance"].mean() - m["performance"].mean(),
                  "t": t, "c": c, "m": m}
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    rows = [("A · sign-up driven by the records", "A"),
            ("B · motivation drives it too", "B")]
    for i, (lab, v) in enumerate(rows):
        ax.plot([res[v]["naive"], res[v]["matched"]], [i, i], color=GRID, lw=3, zorder=1)
        ax.scatter(res[v]["naive"], i, s=110, color=RED, zorder=3)
        ax.scatter(res[v]["matched"], i, s=110, color=BLUE, zorder=3)
        ax.text(res[v]["naive"], i - 0.28, f"naive {res[v]['naive']:.1f}", ha="center",
                fontsize=10.5, color=RED, fontweight="bold")
        ax.text(res[v]["matched"], i - 0.28, f"matched {res[v]['matched']:.1f}", ha="center",
                fontsize=10.5, color=BLUE, fontweight="bold")
    ax.axvline(5, color=TEAL, lw=2, ls="--")
    ax.text(5.1, 1.45, "truth: +5", color=TEAL, fontweight="bold")
    ax.set_yticks([0, 1], [r[0] for r in rows])
    ax.set_ylim(1.7, -0.6)
    ax.set_xlim(3, 13)
    ax.set_xlabel("estimated effect of the training on performance, points")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "hr-estimates.png")

    t, c, m = res["B"]["t"], res["B"]["c"], res["B"]["m"]
    cols = ["age", "education", "experience", "motivation"]
    sd = np.sqrt((t[cols].var() + c[cols].var()) / 2)
    after = (t[cols].mean() - m[cols].mean()) / sd
    fig, ax = plt.subplots(figsize=(8, 3.0))
    ax.axvspan(-0.1, 0.1, color=PALE_TEAL, zorder=0)
    ax.axvline(0, color=MUTED, lw=1)
    colors = [BLUE, BLUE, BLUE, RED]
    ax.scatter(after.values, range(4), s=90, color=colors, zorder=3)
    for k, v in enumerate(after.values):
        ax.text(v + 0.04, k, f"{v:+.2f}", va="center", fontsize=10.5,
                color=colors[k], fontweight="bold")
    ax.set_yticks(range(4), ["age", "education", "experience",
                             "motivation (not in the file)"])
    ax.invert_yaxis()
    ax.set_xlim(-0.3, 1.4)
    ax.set_xlabel("standardised difference after matching, version B")
    ax.set_title("The love plot you can draw is perfect; the one you cannot is not",
                 loc="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "hr-hidden.png")
    return {v: (round(r["naive"], 2), round(r["matched"], 2)) for v, r in res.items()}, after


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
    coin_histogram()
    firms_balance(firms)
    firms_two_outcomes(firms)
    firms_who_joins(firms)
    coin_vs_choice(firms)
    print("decomposition (naive, effect, bias):", po_decomposition(firms))
    dag_selection()
    nsw_design()
    matching_idea()
    r = nsw_numbers()
    print(r)
    nsw_estimates(r)
    nsw_overlap_and_balance()
    nsw_profiles()
    nsw_pairs()
    nsw_regression()
    hr_dag()
    print(hr_figures(simulate_staff()))
    dag_bad_control()
    workflow()
