"""
Session 09 · the SEM figures, computed rather than drawn.

Every number on a path diagram here is an estimate from the model the slide
fits, with the same data and the same description, so what the slide says
about a picture is true of the picture. The diagrams are drawn with matplotlib
because semopy's own plotting (semopy.semplot) needs Graphviz, which is one
installation more than a student should need to follow the lecture.

    .venv/bin/python 09-structural-equation-modelling/01-lecture/economist-assets/build_sem_figures.py

Writes, next to this file:
    sem-anatomy.png       one latent variable and its three indicators, labelled
    sem-symbols.png       the five symbols of a path diagram
    sem-two-halves.png    the measurement model and the structural model, shaded
    hs-model.png          Holzinger-Swineford: the three-factor model, before fitting
    hs-model-fitted.png   the same diagram with the standardised estimates on it
    hs-reproduce.png      observed correlations, the model's, and the difference
    hs-one-vs-three.png   one general factor against three, with their fit
    pd-model.png          Political Democracy: measurement + structural, before fitting
    pd-model-fitted.png   the same diagram with the standardised estimates on it
    pd-effects.png        direct, indirect and total effect of industrialisation
    sem-equivalent.png    two opposite arrows, one fit
    sem-workflow.png      the seven steps of building an SEM
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import semopy
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch
from semopy.examples import holzinger39, political_democracy

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent

# The course's figure palette (scripts/build_economist_assets.R)
BG, INK, MUTED, RED = "#F7F4ED", "#222222", "#6B6B67", "#E3120B"
BLUE, TEAL, GOLD, GRID = "#356B8C", "#2A8C82", "#D49A00", "#D8D3C8"
PALE_BLUE, PALE_RED, PALE_TEAL = "#C9DCE8", "#F7C9C6", "#C6E2DE"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "font.family": "sans-serif", "font.size": 12, "text.color": INK,
})


# --- drawing primitives -----------------------------------------------------
def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, text, w=1.3, h=0.62, fs=12, fc="white"):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="square,pad=0",
                       fc=fc, ec=INK, lw=1.3, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4)
    return p


def oval(ax, x, y, text, w=2.1, h=1.05, fs=13, color=BLUE):
    p = Ellipse((x, y), w, h, fc=PALE_BLUE if color == BLUE else PALE_RED,
                ec=color, lw=1.8, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold", color=INK, zorder=4)
    return p


def err(ax, x, y, text="e", r=0.28, fs=10):
    p = Circle((x, y), r, fc="white", ec=MUTED, lw=1.1, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=MUTED, zorder=4)
    return p


def link(ax, a, b, label=None, color=MUTED, lw=1.4, rad=0.0, both=False,
         dashed=False, at=0.5, fs=11, lcolor=None, bold=False):
    """An arrow from patch a to patch b, clipped to both outlines."""
    ca, cb = _centre(a), _centre(b)
    arr = FancyArrowPatch(ca, cb, patchA=a, patchB=b,
                          arrowstyle="<|-|>" if both else "-|>",
                          mutation_scale=14, lw=lw, color=color, zorder=2,
                          connectionstyle=f"arc3,rad={rad}",
                          linestyle=(0, (4, 3)) if dashed else "-")
    ax.add_patch(arr)
    if label is not None:
        # The label sits on the straight line, pushed sideways for a curve.
        mx, my = ca[0] + at * (cb[0] - ca[0]), ca[1] + at * (cb[1] - ca[1])
        dx, dy = cb[0] - ca[0], cb[1] - ca[1]
        mx += rad * dy * 0.5
        my -= rad * dx * 0.5
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=lcolor or INK, fontweight="bold" if bold else "normal",
                zorder=5, bbox=dict(fc=BG, ec="none", pad=1.2))
    return arr


def _centre(p):
    if isinstance(p, (Ellipse, Circle)):
        return p.center
    return (p.get_x() + p.get_width() / 2, p.get_y() + p.get_height() / 2)


def note(ax, x, y, text, color=MUTED, fs=11, ha="left", va="center", **kw):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, **kw)


def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("wrote", name)


def fit(desc, data):
    m = semopy.Model(desc)
    m.fit(data)
    return m, m.inspect(std_est=True), semopy.calc_stats(m)


def std(est, lval, op, rval):
    row = est[(est["lval"] == lval) & (est["op"] == op) & (est["rval"] == rval)]
    return float(row["Est. Std"].iloc[0])


def stat(stats, k):
    return float(stats[k].iloc[0])


# --- the models the slides fit ----------------------------------------------
HS = holzinger39.get_data()
HS_DESC = """
visual  =~ x1 + x2 + x3
textual =~ x4 + x5 + x6
speed   =~ x7 + x8 + x9
"""
HS_ONE = "ability =~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9"
TESTS = {"x1": "visual perception", "x2": "cubes", "x3": "lozenges",
         "x4": "paragraph comp.", "x5": "sentence compl.", "x6": "word meaning",
         "x7": "speeded addition", "x8": "speeded dot counting", "x9": "straight vs curved capitals"}

PD = political_democracy.get_data()
PD_DESC = """
ind60 =~ x1 + x2 + x3
dem60 =~ y1 + y2 + y3 + y4
dem65 =~ y5 + y6 + y7 + y8
dem60 ~ ind60
dem65 ~ ind60 + dem60
y1 ~~ y5
y2 ~~ y6
y3 ~~ y7
y4 ~~ y8
"""


# --- 1. anatomy: one construct, three indicators ----------------------------
def anatomy():
    fig, ax = canvas(11, 4.6, (-4.2, 11.6), (-3.0, 3.2))
    lat = oval(ax, 0, 0, "verbal\nability", w=2.6, h=1.5)
    items = ["paragraph\ncomprehension", "sentence\ncompletion", "word\nmeaning"]
    for i, t in enumerate(items):
        y = 2.0 - 2.0 * i
        b = box(ax, 5.0, y, t, w=2.6, h=1.0, fs=11)
        e = err(ax, 7.9, y, "e")
        link(ax, lat, b, color=BLUE, lw=1.8)
        link(ax, e, b)
    note(ax, 0, -1.25, "LATENT: never measured,\ndrawn as an ellipse", ha="center",
         va="top", color=BLUE, fontweight="bold")
    note(ax, 5.0, -2.75, "OBSERVED: a column in your data, drawn as a rectangle",
         ha="center", color=INK, fontweight="bold")
    note(ax, 2.45, 2.45, "loading", color=BLUE, ha="center", fs=12, fontweight="bold")
    note(ax, 8.4, 2.0, "error: everything in the\nscore that is not\nverbal ability",
         va="center", fs=10.5)
    note(ax, 8.4, -0.6, "The arrows point FROM the\nability TO the scores: the\n"
         "ability is what the three\nscores have in common.", fs=10.5, color=INK)
    save(fig, "sem-anatomy.png")


# --- 2. the five symbols ----------------------------------------------------
def symbols():
    fig, ax = canvas(12, 2.6, (-0.5, 21.5), (-2.4, 1.3))
    box(ax, 1.2, 0, "x1", w=1.6, h=0.9)
    note(ax, 1.2, -1.3, "observed variable\n(a column)", ha="center", color=INK)
    oval(ax, 5.5, 0, "F", w=2.0, h=1.1)
    note(ax, 5.5, -1.3, "latent variable\n(a construct)", ha="center", color=INK)
    a, b = Circle((8.7, 0), 0.01), Circle((11.3, 0), 0.01)
    ax.add_patch(a); ax.add_patch(b)
    link(ax, a, b, color=BLUE, lw=2)
    note(ax, 10, -1.3, "one-headed arrow\n(effect, loading)", ha="center", color=INK)
    a, b = Circle((13.2, -0.1), 0.01), Circle((15.8, -0.1), 0.01)
    ax.add_patch(a); ax.add_patch(b)
    link(ax, a, b, color=RED, lw=1.8, both=True, rad=-0.5, dashed=True)
    note(ax, 14.5, -1.3, "two-headed arrow\n(covariance)", ha="center", color=INK)
    err(ax, 19.3, 0, "e", r=0.45, fs=13)
    note(ax, 19.3, -1.3, "error / disturbance\n(what is left)", ha="center", color=INK)
    save(fig, "sem-symbols.png")


# --- 3. the two halves --------------------------------------------------------
def two_halves():
    fig, ax = canvas(12, 4.8, (-1.2, 21.2), (-4.6, 4.4))
    ax.add_patch(FancyBboxPatch((-0.9, -4.3), 7.6, 8.4, boxstyle="round,pad=0.1",
                                fc=PALE_BLUE, ec="none", alpha=0.45, zorder=0))
    ax.add_patch(FancyBboxPatch((13.0, -4.3), 7.9, 8.4, boxstyle="round,pad=0.1",
                                fc=PALE_BLUE, ec="none", alpha=0.45, zorder=0))
    ax.add_patch(FancyBboxPatch((6.9, -1.4), 6.0, 2.8, boxstyle="round,pad=0.1",
                                fc=PALE_RED, ec="none", alpha=0.6, zorder=0))
    xi = oval(ax, 5.3, 0, "cause", w=2.4, h=1.2)
    eta = oval(ax, 14.6, 0, "effect", w=2.4, h=1.2)
    for i in range(3):
        y = 2.3 - 2.3 * i
        bx = box(ax, 0.8, y, f"x{i + 1}")
        link(ax, xi, bx, color=BLUE)
        by = box(ax, 19.2, y, f"y{i + 1}")
        link(ax, eta, by, color=BLUE)
    link(ax, xi, eta, color=RED, lw=2.6, label="path", lcolor=RED, bold=True)
    z = err(ax, 14.6, 2.6, "ζ", r=0.38, fs=13)
    link(ax, z, eta)
    note(ax, 2.9, 3.75, "MEASUREMENT", ha="center", color=BLUE, fontweight="bold", fs=13)
    note(ax, 16.9, 3.75, "MEASUREMENT", ha="center", color=BLUE, fontweight="bold", fs=13)
    note(ax, 9.95, 2.0, "STRUCTURAL", ha="center", color=RED, fontweight="bold", fs=13)
    note(ax, 2.9, -3.75, "do the x's measure one thing?", ha="center", color=INK)
    note(ax, 16.9, -3.75, "do the y's measure one thing?", ha="center", color=INK)
    note(ax, 9.95, -2.0, "does the cause move\nthe effect?", ha="center", color=INK,
         va="top")
    save(fig, "sem-two-halves.png")


# --- 4. Holzinger-Swineford, before and after fitting -----------------------
def hs_diagram(est=None, name="hs-model.png"):
    fig, ax = canvas(12, 6.4, (-5.6, 11.6), (-5.6, 5.9))
    lats = {"visual": 3.5, "textual": 0.0, "speed": -3.5}
    groups = {"visual": ["x1", "x2", "x3"], "textual": ["x4", "x5", "x6"],
              "speed": ["x7", "x8", "x9"]}
    L = {k: oval(ax, 0, y, k, w=2.5, h=1.2) for k, y in lats.items()}
    for k, items in groups.items():
        for j, it in enumerate(items):
            y = lats[k] + 1.15 * (1 - j)
            b = box(ax, 5.6, y, it, w=1.1, h=0.72)
            note(ax, 7.75, y, TESTS[it], fs=10.5, color=MUTED)
            e = err(ax, 7.05, y, "e" if est is None else
                    f"{std(est, it, '~~', it):.2f}", r=0.42, fs=9.5)
            link(ax, e, b, color=GRID)
            if est is None:
                link(ax, L[k], b, color=BLUE, lw=1.6)
            else:
                v = std(est, it, "~", k)
                link(ax, L[k], b, color=RED if v < 0.6 else BLUE,
                     lw=1.0 + 2.5 * v, label=f"{v:.2f}", at=0.62, fs=10.5,
                     lcolor=RED if v < 0.6 else INK, bold=v < 0.6)
    pairs = [("visual", "textual", 0.55), ("textual", "speed", 0.55),
             ("visual", "speed", 0.62)]
    for a, b, rad in pairs:
        lab = None
        if est is not None:
            r = est[(est["op"] == "~~") & (((est["lval"] == a) & (est["rval"] == b)) |
                                           ((est["lval"] == b) & (est["rval"] == a)))]
            lab = f"{float(r['Est. Std'].iloc[0]):.2f}"
        link(ax, L[a], L[b], both=True, dashed=True, color=RED, rad=rad, label=lab,
             fs=10.5, lcolor=RED)
    if est is None:
        note(ax, 7.05, 4.95, "error", ha="center", fs=10.5, va="bottom")
        note(ax, -5.4, -5.3, "3 latent abilities · 9 observed tests · "
             "the abilities may correlate (dashed)", fs=11)
    else:
        note(ax, 7.05, 4.95, "share left\nunexplained", ha="center", fs=10, va="bottom")
        note(ax, -5.4, -5.3, "standardised estimates · a loading in red is below 0.6: "
             "the weakest test of its ability", fs=11)
    save(fig, name)


def hs_reproduce(model):
    cols = model.vars["observed"]
    S = HS[cols].corr().to_numpy()
    sigma = model.calc_sigma()[0]
    d = np.sqrt(np.diag(sigma))
    R = sigma / np.outer(d, d)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    panels = [(S, "what the data say", "Blues", (0, 1)),
              (R, "what the model says", "Blues", (0, 1)),
              (S - R, "the difference", "RdBu_r", (-0.3, 0.3))]
    for ax, (M, title, cmap, (lo, hi)) in zip(axes, panels):
        ax.imshow(M, cmap=cmap, vmin=lo, vmax=hi)
        for i in range(9):
            for j in range(9):
                v = 0.0 if abs(M[i, j]) < 0.005 else M[i, j]
                ax.text(j, i, f"{v:.2f}".replace("0.", ".").replace("-.", "−."),
                        ha="center", va="center", fontsize=7.5,
                        color="white" if (cmap == "Blues" and v > 0.6) else INK)
        ax.set_xticks(range(9), cols, fontsize=9)
        ax.set_yticks(range(9), cols, fontsize=9)
        ax.set_title(title, fontsize=13, loc="left", fontweight="bold")
        for s in ax.spines.values():
            s.set_visible(False)
        for k in (2.5, 5.5):
            ax.axhline(k, color=INK, lw=0.8)
            ax.axvline(k, color=INK, lw=0.8)
    fig.tight_layout()
    save(fig, "hs-reproduce.png")


def hs_one_vs_three(s1, s3):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4))
    for ax in (a1, a2):
        ax.set_xlim(-3.4, 6.0)
        ax.set_ylim(-6.4, 5.6)
        ax.set_aspect("equal")
        ax.axis("off")
    items = list(TESTS)
    g = oval(a1, -0.3, 0, "general\nability", w=3.2, h=1.6, color=RED)
    for i, it in enumerate(items):
        b = box(a1, 4.6, 4.4 - 1.1 * i, it, w=1.1, h=0.7)
        link(a1, g, b, color=RED, lw=1.2)
    lats = {"visual": 3.3, "textual": 0.0, "speed": -3.3}
    L = {k: oval(a2, 0, y, k, w=2.4, h=1.15) for k, y in lats.items()}
    for i, it in enumerate(items):
        b = box(a2, 4.6, 4.4 - 1.1 * i, it, w=1.1, h=0.7)
        link(a2, L[list(lats)[i // 3]], b, color=BLUE, lw=1.2)
    for ax, s, title in ((a1, s1, "one factor"), (a2, s3, "three factors")):
        ax.set_title(title, fontsize=15, fontweight="bold", loc="left")
        txt = (f"χ² = {stat(s, 'chi2'):.0f} on {stat(s, 'DoF'):.0f} df\n"
               f"CFI = {stat(s, 'CFI'):.3f}   TLI = {stat(s, 'TLI'):.3f}   "
               f"RMSEA = {stat(s, 'RMSEA'):.3f}")
        ax.text(-3.2, -5.2, txt, fontsize=12, va="center", color=INK)
    save(fig, "hs-one-vs-three.png")


# --- 5. Political Democracy, before and after fitting -----------------------
def pd_diagram(est=None, name="pd-model.png"):
    fig, ax = canvas(13, 6.4, (-1.6, 20.4), (-6.4, 6.4))
    I = oval(ax, 1.2, -1.6, "ind60", w=2.5, h=1.2)
    D60 = oval(ax, 6.0, 1.6, "dem60", w=2.5, h=1.2)
    D65 = oval(ax, 13.0, 1.6, "dem65", w=2.5, h=1.2)
    labels = {"x1": "GNP", "x2": "energy", "x3": "industry\nlabour"}
    xs = {}
    for i, it in enumerate(["x1", "x2", "x3"]):
        b = box(ax, -0.6 + 1.8 * i, -4.7, it, w=1.2, h=0.7)
        note(ax, -0.6 + 1.8 * i, -5.45, labels[it], ha="center", va="top", fs=9.5)
        xs[it] = b
    ys = {}
    for i, it in enumerate(["y1", "y2", "y3", "y4"]):
        ys[it] = box(ax, 3.9 + 1.4 * i, 4.6, it, w=1.0, h=0.7)
    for i, it in enumerate(["y5", "y6", "y7", "y8"]):
        ys[it] = box(ax, 10.9 + 1.4 * i, 4.6, it, w=1.0, h=0.7)
    note(ax, 15.6, 3.2, "y1, y5  press freedom\ny2, y6  freedom of opposition\n"
         "y3, y7  fair elections\ny4, y8  effective legislature", fs=10, va="top")

    def lab(l, op, r):
        return None if est is None else f"{std(est, l, op, r):.2f}"

    for it, b in xs.items():
        link(ax, I, b, color=BLUE, label=lab(it, "~", "ind60"), fs=9.5, at=0.6)
    for it in ["y1", "y2", "y3", "y4"]:
        link(ax, D60, ys[it], color=BLUE, label=lab(it, "~", "dem60"), fs=9.5, at=0.62)
    for it in ["y5", "y6", "y7", "y8"]:
        link(ax, D65, ys[it], color=BLUE, label=lab(it, "~", "dem65"), fs=9.5, at=0.62)
    for a, b in [("y1", "y5"), ("y2", "y6"), ("y3", "y7"), ("y4", "y8")]:
        link(ax, ys[a], ys[b], both=True, dashed=True, color=GOLD, rad=-0.22, lw=1.1)
    note(ax, 9.4, 6.0, "same question, five years apart (dashed)", ha="center",
         color=GOLD, fs=10, fontweight="bold")
    link(ax, I, D60, color=RED, lw=2.6, label=lab("dem60", "~", "ind60"),
         lcolor=RED, bold=True)
    link(ax, D60, D65, color=RED, lw=2.6, label=lab("dem65", "~", "dem60"),
         lcolor=RED, bold=True)
    link(ax, I, D65, color=RED, lw=2.6, rad=0.25, label=lab("dem65", "~", "ind60"),
         lcolor=RED, bold=True)
    for D, n, x in ((D60, "dem60", 6.0), (D65, "dem65", 13.0)):
        z = err(ax, x + 2.2, 0.0, "ζ" if est is None else
                f"{std(est, n, '~~', n):.2f}", r=0.45, fs=9.5)
        link(ax, z, D)
    if est is None:
        note(ax, 9.0, -4.9, "blue: measurement · red: structural\n"
             "ζ: what the arrows in leave unexplained", fs=11, color=INK)
    else:
        r60 = 1 - std(est, "dem60", "~~", "dem60")
        r65 = 1 - std(est, "dem65", "~~", "dem65")
        note(ax, 8.6, -4.9, f"standardised estimates\nR² dem60 = {r60:.2f}  ·  "
             f"R² dem65 = {r65:.2f}\n(R² = 1 − the number in the ζ circle)",
             fs=11, color=INK)
    save(fig, name)


def pd_effects(est):
    a = std(est, "dem60", "~", "ind60")
    b = std(est, "dem65", "~", "dem60")
    c = std(est, "dem65", "~", "ind60")
    fig, ax = canvas(12, 4.4, (-1.5, 21.0), (-3.6, 4.2))
    I = oval(ax, 1.2, -1.6, "ind60", w=2.6, h=1.2)
    D60 = oval(ax, 7.5, 2.4, "dem60", w=2.6, h=1.2)
    D65 = oval(ax, 13.8, -1.6, "dem65", w=2.6, h=1.2)
    link(ax, I, D60, color=GOLD, lw=3, label=f"a = {a:.2f}", lcolor=INK, bold=True)
    link(ax, D60, D65, color=GOLD, lw=3, label=f"b = {b:.2f}", lcolor=INK, bold=True)
    link(ax, I, D65, color=RED, lw=3, label=f"c = {c:.2f}", lcolor=INK, bold=True)
    x0 = 16.0
    note(ax, x0, 2.6, "direct", color=RED, fontweight="bold", fs=13)
    note(ax, x0, 1.9, f"c = {c:.2f}", color=INK, fs=13)
    note(ax, x0, 0.9, "indirect", color=GOLD, fontweight="bold", fs=13)
    note(ax, x0, 0.2, f"a × b = {a:.2f} × {b:.2f} = {a * b:.2f}", color=INK, fs=13)
    note(ax, x0, -0.8, "total", color=INK, fontweight="bold", fs=13)
    note(ax, x0, -1.5, f"c + a × b = {c + a * b:.2f}", color=INK, fs=13)
    note(ax, -1.2, -3.2, "Two roads from 1960 industrialisation to 1965 democracy: "
         "straight there, or through 1960 democracy.", fs=11.5, color=INK)
    save(fig, "pd-effects.png")


# --- 6. equivalent models -----------------------------------------------------
def equivalent():
    A = "ind60 =~ x1 + x2 + x3\ndem60 =~ y1 + y2 + y3 + y4\ndem60 ~ ind60"
    B = "ind60 =~ x1 + x2 + x3\ndem60 =~ y1 + y2 + y3 + y4\nind60 ~ dem60"
    _, _, sa = fit(A, PD)
    _, _, sb = fit(B, PD)
    fig, ax = canvas(12, 3.0, (-0.5, 23.0), (-2.5, 2.7))
    for x0, s, rev, title in ((0, sa, False, "industry → democracy"),
                              (12.2, sb, True, "democracy → industry")):
        I = oval(ax, x0 + 1.6, 0.6, "ind60", w=2.6, h=1.2)
        D = oval(ax, x0 + 8.0, 0.6, "dem60", w=2.6, h=1.2)
        link(ax, D if rev else I, I if rev else D, color=RED, lw=3)
        note(ax, x0 + 4.8, 2.2, title, ha="center", color=INK, fontweight="bold", fs=13)
        note(ax, x0 + 4.8, -1.5,
             f"χ² = {stat(s, 'chi2'):.2f} on {stat(s, 'DoF'):.0f} df\n"
             f"CFI = {stat(s, 'CFI'):.3f}  ·  RMSEA = {stat(s, 'RMSEA'):.3f}",
             ha="center", fs=12, color=INK)
    save(fig, "sem-equivalent.png")


# --- 7. the workflow ----------------------------------------------------------
def workflow():
    steps = ["1 · Theory\nthe argument", "2 · Draw\nthe diagram",
             "3 · Write\nthe description", "4 · Look\nat the data",
             "5 · Fit\nModel().fit()", "6 · Read\nloadings, paths",
             "7 · Judge\nthe fit"]
    fig, ax = canvas(13, 3.4, (-0.3, 27.6), (-3.4, 2.2))
    prev = None
    for i, s in enumerate(steps):
        b = box(ax, 1.8 + 3.95 * i, 0, s, w=3.6, h=1.7, fs=10.5,
                fc=PALE_BLUE if i < 3 else "white")
        if prev is not None:
            link(ax, prev, b, color=INK, lw=1.4)
        prev = b
        if i == 0:
            first = b
    back = FancyArrowPatch((25.5, -0.9), (1.8, -0.9), connectionstyle="arc3,rad=-0.12",
                           arrowstyle="-|>", mutation_scale=14, lw=1.6, color=RED,
                           linestyle=(0, (4, 3)), zorder=1)
    ax.add_patch(back)
    note(ax, 13.6, -2.95, "if it does not fit: go back to THEORY, not to the fit indices",
         ha="center", color=RED, fontweight="bold", fs=12)
    note(ax, 1.8 + 3.95, 1.4, "on paper, before Python", ha="center",
         color=BLUE, fontweight="bold", fs=11, va="bottom")
    save(fig, "sem-workflow.png")


if __name__ == "__main__":
    anatomy()
    symbols()
    two_halves()
    hs_diagram()
    m3, e3, s3 = fit(HS_DESC, HS)
    hs_diagram(e3, "hs-model-fitted.png")
    hs_reproduce(m3)
    _, _, s1 = fit(HS_ONE, HS)
    hs_one_vs_three(s1, s3)
    pd_diagram()
    _, ep, _ = fit(PD_DESC, PD)
    pd_diagram(ep, "pd-model-fitted.png")
    pd_effects(ep)
    equivalent()
    workflow()
