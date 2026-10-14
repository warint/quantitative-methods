"""matplotlib — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import svg, text, small  # noqa: E402

ACCENT = "#11557c"
BLUE, RED = "#4c7fb0", "#c0392b"

META = dict(
    title="matplotlib",
    color=ACCENT,
    tagline="Pictures of your data: look before you model, check after you fit",
    sessions="3 to 13",
)
META["import"] = "import matplotlib.pyplot as plt"
META["version_note"] = "one figure, one or more axes; draw on the axes"


# ---------------------------------------------------------------- data, once
_cache = {}


def _core():
    if "core" not in _cache:
        import qmib
        _cache["core"] = qmib.load("core").dropna(subset=["gdp_pc_eur", "productivity_idx"])
    return _cache["core"]


def _fit():
    if "fit" not in _cache:
        import statsmodels.formula.api as smf
        _cache["fit"] = smf.ols("gdp_pc_eur ~ productivity_idx", data=_core()).fit()
    return _cache["fit"]


# ---------------------------------------------------------------- diagrams
def anatomy():
    b = f'<rect x="4" y="4" width="292" height="150" rx="4" fill="#f2efe8" stroke="#888"/>'
    b += text(14, 16, "Figure  (fig)", 7.5, "start", ACCENT, "bold")
    b += f'<rect x="48" y="26" width="200" height="98" fill="#fff" stroke="#555"/>'
    b += text(58, 38, "Axes  (ax)", 7.5, "start", ACCENT, "bold")
    b += text(148, 22, "ax.set_title(\"…\")", 7, "middle", RED)
    # points and a line
    pts = [(70, 110), (95, 98), (120, 92), (140, 80), (165, 70), (190, 60), (215, 48), (235, 40)]
    b += "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{BLUE}"/>' for x, y in pts)
    b += f'<line x1="62" y1="114" x2="242" y2="38" stroke="{RED}" stroke-width="1.3"/>'
    # ticks
    b += "".join(f'<line x1="{x}" y1="124" x2="{x}" y2="128" stroke="#555"/>' for x in (80, 130, 180, 230))
    b += "".join(f'<line x1="44" y1="{y}" x2="48" y2="{y}" stroke="#555"/>' for y in (40, 70, 100))
    b += text(148, 138, "ax.set_xlabel(\"…\")  — x axis, ticks", 7, "middle", RED)
    b += text(14, 75, "y label", 7, "start", RED)
    b += f'<rect x="196" y="98" width="46" height="20" fill="#fff" stroke="#999"/>'
    b += text(219, 111, "legend", 7, "middle", "#333")
    b += text(270, 50, "spines", 6.5, "middle", "#555")
    b += f'<line x1="258" y1="54" x2="249" y2="62" stroke="#555"/>'
    b += text(150, 151, 'fig, ax = plt.subplots(figsize=(7, 3))', 7, "middle", ACCENT, "bold")
    return svg(300, 158, b)


def panels():
    b = ""
    for i, x in enumerate((10, 105, 200)):
        b += f'<rect x="{x}" y="14" width="88" height="46" fill="#fff" stroke="#555"/>'
        b += text(x + 44, 40, f"axes[{i}]", 8, "middle", ACCENT, "bold")
    b += text(150, 9, "fig, axes = plt.subplots(1, 3, figsize=(9, 3))", 7, "middle", "#333")
    b += text(150, 72, "sharey=True: one y scale for all three", 7, "middle", "#555")
    return svg(300, 78, b)


# ---------------------------------------------------------------- gallery
def g_scatter():
    d = _core()
    fig, ax = small(2.9, 1.45)
    ax.scatter(d["productivity_idx"], d["gdp_pc_eur"], s=8, alpha=0.5, color=BLUE)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.set_xlabel("productivity index (EU = 100)", fontsize=7)
    ax.set_ylabel("GDP per capita (€)", fontsize=7)
    return fig


def g_hist():
    g = _core()["gdp_pc_eur"]
    fig, ax = small(2.9, 1.35)
    ax.hist(g, bins=30, color=BLUE)
    ax.axvline(g.median(), color=RED, lw=1.5, ls="--")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.set_xlabel("GDP per capita (€) · dashed: median", fontsize=7)
    return fig


def g_resid():
    fit = _fit()
    fig, ax = small(2.9, 1.35)
    ax.scatter(fit.fittedvalues, fit.resid, s=8, alpha=0.5, color=BLUE)
    ax.axhline(0, color="black", lw=1)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.set_xlabel("fitted values", fontsize=7); ax.set_ylabel("residuals", fontsize=7)
    return fig


def g_stem():
    fit, d = _fit(), _core()
    cooks = fit.get_influence().cooks_distance[0]
    fig, ax = small(2.9, 1.3)
    ax.stem(cooks, markerfmt=" ", basefmt=" ")
    ax.axhline(4 / len(d), color=RED, ls="--", lw=1)
    ax.set_xlabel("observation · dashed: 4/n", fontsize=7); ax.set_ylabel("Cook's D", fontsize=7)
    return fig


def g_path():
    import numpy as np
    import qmib
    from sklearn.linear_model import lasso_path
    from sklearn.preprocessing import StandardScaler
    raw = qmib.load("angle_c_country")
    y = "rd_pct_gdp"
    xs = [c for c in raw.columns if c not in ("geo", "time", "flag", y)]
    d = raw.dropna(subset=[y] + xs)
    Z = StandardScaler().fit_transform(d[xs].to_numpy(float))
    alphas, coefs, _ = lasso_path(Z, d[y].to_numpy(float), alphas=np.logspace(-3, 0, 60))
    fig, ax = small(2.9, 1.35)
    for k in range(coefs.shape[0]):
        ax.plot(alphas, coefs[k], lw=0.9)
    ax.set_xscale("log"); ax.axhline(0, color="black", lw=0.7)
    ax.set_xlabel("penalty λ (log scale)", fontsize=7); ax.set_ylabel("coefficient", fontsize=7)
    return fig


def g_bar():
    import qmib
    s = qmib.load("hsbdemo")["prog"].value_counts()
    fig, ax = small(2.9, 1.15)
    ax.barh(s.index, s.values, color=BLUE)
    ax.invert_yaxis()
    ax.set_xlabel("students per programme", fontsize=7)
    return fig


def g_box():
    import qmib
    w = qmib.load("redwines")
    fig, ax = small(2.9, 1.35)
    w.boxplot(column="alcohol", by="good", ax=ax, grid=False)
    ax.set_title(""); fig.suptitle("")
    ax.set_xlabel("good wine (0/1)", fontsize=7); ax.set_ylabel("alcohol (%)", fontsize=7)
    return fig


def g_annot():
    import numpy as np
    lam = np.logspace(-3, 3, 60)
    err = 1 + 0.6 * (np.log10(lam) - 0.3) ** 2 / 9 + 0.05 * np.exp(-lam)
    best = lam[err.argmin()]
    fig, ax = small(2.9, 1.3)
    ax.plot(lam, err, color=BLUE, lw=1.6)
    ax.set_xscale("log")
    ax.axvline(best, color="#2e8b57", ls=":", lw=1.3)
    ax.annotate("lowest error", xy=(best, err.min()), xytext=(best * 15, err.min() + 0.25),
                fontsize=7, arrowprops=dict(arrowstyle="->", color="#2e8b57"))
    ax.set_xlabel("penalty λ  (a sketch)", fontsize=7); ax.set_ylabel("CV error", fontsize=7)
    return fig


# ---------------------------------------------------------------- pages
PAGES = [[
    dict(title="1 · The anatomy of a figure",
         intro="A **figure** is the page; an **axes** is one plot on it. You draw on the axes.",
         figure_top=anatomy,
         items=[
             dict(code="fig, ax = plt.subplots(figsize=(7, 3))",
                  text="one figure with one axes, 7 × 3 inches — wide and short fits a slide."),
             dict(code="ax.scatter(...) · ax.plot(...) · ax.hist(...)",
                  text="every drawing call is a method of `ax`."),
             dict(code="plt.show()", text="display the figure (in a script, it opens a window)."),
         ],
         tip="`plt.scatter(...)` also works: it draws on the *current* axes. With several panels, use `ax.` — it says which one."),
    dict(title="2 · Several panels",
         figure_top=panels,
         items=[
             dict(code="fig, axes = plt.subplots(1, 3, figsize=(9, 3))",
                  text="a row of three axes; `axes[0]`, `axes[1]`, `axes[2]`."),
             dict(code="plt.subplots(2, 2)  →  axes[0, 1]", text="a grid: row, then column."),
             dict(code="plt.tight_layout()", text="stop labels from overlapping between panels."),
         ]),
    dict(title="3 · Points and lines",
         items=[
             dict(code='ax.scatter(x, y, s=12, alpha=0.6)',
                  text="one dot per row. `s` is the marker size, `alpha` the transparency: with hundreds of points, see-through dots show density.",
                  ex='ax.scatter(d["productivity_idx"], d["gdp_pc_eur"], s=12, alpha=0.6)'),
             dict(code='ax.plot(x, y, color="…", lw=2, ls="--")',
                  text="a line through the points, in order of x. `lw` width, `ls` style: `\"-\"`, `\"--\"`, `\":\"`."),
             dict(code='ax.plot(x, y, label="ridge"); ax.legend()',
                  text="name each line, then draw the legend."),
         ],
         figure=g_scatter),
    dict(title="4 · Distributions",
         items=[
             dict(code="ax.hist(x, bins=30)", text="how a variable is spread: count of rows per bin. Try several `bins`."),
             dict(code='d.boxplot(column="alcohol", by="good", ax=ax)',
                  text="pandas draws a box per group on a matplotlib axes: median, quartiles, outliers."),
         ],
         figure=g_hist),
    dict(title="Before any model: look",
         intro="The habits of session 3, on every plot you make.",
         items=[
             dict(code="1 · draw the data first", text="a straight line through a curved cloud is still a straight line — the software will not warn you."),
             dict(code="2 · say the units", text="on both axes, every time: € per head, % of GDP, index points."),
             dict(code="3 · one question per plot", text="a residual plot asks *what did the line miss?*; a histogram asks *how is it spread?*"),
             dict(code="4 · a line is a prompt", text="a threshold or a zero line says where to look, not what to delete."),
         ]),
    dict(title="Gallery · a box per group (session 4)",
         figure_top=g_box,
         items=[dict(code='w.boxplot(column="alcohol", by="good", ax=ax)',
                     text="if the two boxes overlap completely, no coefficient will rescue the predictor.")]),
    dict(title="Gallery · a bar chart",
         figure_top=g_bar,
         items=[dict(code='ax.barh(s.index, s.values); ax.invert_yaxis()',
                     text="counts or scores per category; horizontal bars keep long names readable.")]),
], [
    dict(title="5 · Reference lines and words",
         items=[
             dict(code="ax.axhline(0, color=\"black\", lw=1)", text="a horizontal line across the plot — zero, a threshold, a mean."),
             dict(code="ax.axvline(x, ls=\":\")", text="a vertical line — the chosen λ, the median."),
             dict(code='ax.text(x, y, "sweet spot", fontsize=9)', text="words placed at data coordinates."),
             dict(code='ax.annotate("lowest", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="->"))',
                  text="words with an arrow pointing at a point."),
         ],
         figure=g_annot,
         tip="A threshold line is a prompt to **look** at the rows above it — not a rule to delete them."),
    dict(title="6 · Labels, scales, limits",
         items=[
             dict(code='ax.set_xlabel("GDP per capita (€)")  ·  ax.set_ylabel(…)', text="**say the units, every time**."),
             dict(code='ax.set_title("…")  ·  fig.suptitle("…")', text="a title per panel · one for the figure."),
             dict(code='ax.set_xscale("log")', text="a log axis: λ grids, incomes, FDI — anything spanning orders of magnitude."),
             dict(code="ax.set_xlim(0, 10)  ·  ax.set_ylim(…)", text="fix the range shown."),
             dict(code="ax.set_xticks(pos); ax.set_xticklabels(names, rotation=60)",
                  text="name the ticks, tilted when the names are long."),
             dict(code="ax.invert_yaxis()", text="largest bar at the top in a horizontal bar chart."),
         ]),
    dict(title="7 · Save",
         items=[
             dict(code='plt.savefig("out.png", dpi=110, bbox_inches="tight")',
                  text="a file for a paper or a slide. Call it **before** `plt.show()`, which empties the figure."),
         ]),
    dict(title="Gallery · residuals vs fitted (session 3)",
         figure_top=g_resid,
         items=[dict(code="ax.scatter(fit.fittedvalues, fit.resid, s=12, alpha=0.6); ax.axhline(0)",
                     text="random scatter around zero: fine. A curve or a funnel: the model missed something.")]),
    dict(title="Gallery · Cook's distance (session 3)",
         figure_top=g_stem,
         items=[dict(code="ax.stem(cooks_d); ax.axhline(4 / len(d), ls=\"--\")",
                     text="one spike per row: a tower above the rest is a row carrying the result.")]),
    dict(title="Gallery · a coefficient path (session 5)",
         figure_top=g_path,
         items=[dict(code='for k in range(P): ax.plot(alphas, coefs[k]); ax.set_xscale("log")',
                     text="one line per predictor as λ grows: the lasso switches them off one by one.")]),
    dict(title="8 · Colours, markers, styles",
         items=[
             dict(code='color="tab:blue"  ·  color="#11557c"', text="a named colour or a hex code; keep one colour per meaning across panels."),
             dict(code='marker="o"  ·  ls="--"  ·  lw=2', text="dots, dashed lines, line width — for lines that must print in black and white."),
             dict(code="alpha=0.3", text="transparency: overlapping points show where the data are dense."),
             dict(code='ax.grid(axis="y", visible=False)', text="remove grid lines that compete with the data."),
             dict(code='cmap="Blues"  in ax.imshow(corr)', text="a colour scale, e.g. a correlation matrix as a heat map."),
         ]),
    dict(title="9 · When a plot looks wrong",
         items=[
             dict(code="nothing appears", text="in a script, call `plt.show()` at the end."),
             dict(code="the saved file is blank", text="`plt.savefig` must come **before** `plt.show()`."),
             dict(code="labels overlap", text="`plt.tight_layout()`, a wider `figsize`, or `rotation=60` on the ticks."),
             dict(code="a solid blob of points", text="smaller `s=`, lower `alpha=`, or a histogram instead."),
             dict(code="a line zig-zags", text="`ax.plot` joins points in row order: sort by x first."),
             dict(code="one panel's scale hides another's", text="`plt.subplots(..., sharey=False)`, or a log axis."),
         ],
         warn="A plot without units on its axes is not finished."),
]]
