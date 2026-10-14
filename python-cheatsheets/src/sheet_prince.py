"""prince — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import svg, text, small  # noqa: E402

ACCENT = "#c0392b"

META = dict(
    title="prince",
    color=ACCENT,
    tagline="Many variables, a few dimensions: PCA for numbers, FAMD for numbers and categories",
    sessions="13",
)
META["import"] = "import prince"
META["version_note"] = "fits like scikit-learn: .fit(df), then read attributes"

MOVIES = ["budget", "popularity", "revenue", "runtime", "vote_average", "vote_count"]


def _movies():
    import qmib
    return qmib.load("movies")[MOVIES].dropna()


def _pca():
    import prince
    return prince.PCA(n_components=4, rescale_with_mean=True, rescale_with_std=True,
                      random_state=0).fit(_movies())


def _wine():
    import numpy as np
    import qmib
    wine = qmib.load("redwines")
    wine["quality_label"] = np.where(wine["good"] == 1, "good", "ordinary")
    return wine.drop(columns=["good"])


def scree():
    import numpy as np
    p = _pca()
    ev = np.asarray(p.eigenvalues_)
    fig, ax = small(3.0, 1.45)
    ax.bar(range(1, len(ev) + 1), ev, color="#e6a59c")
    ax.plot(range(1, len(ev) + 1), ev, color=ACCENT, marker="o", ms=3)
    ax.axhline(1, color="#555", lw=0.8, ls="--")
    for i, v in enumerate(p.percentage_of_variance_):
        ax.text(i + 1, ev[i] + 0.08, f"{v:.0f}%", fontsize=6, ha="center")
    ax.set_xticks(range(1, len(ev) + 1)); ax.set_xlabel("component", fontsize=7)
    ax.set_ylabel("eigenvalue", fontsize=7); ax.set_ylim(0, ev.max() * 1.25)
    return fig


def circle():
    import numpy as np
    p = _pca()
    cc = p.column_correlations
    fig, ax = small(2.2, 2.2)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), color="#999", lw=0.8)
    ax.axhline(0, color="#ccc", lw=0.6); ax.axvline(0, color="#ccc", lw=0.6)
    for name, (x, y) in cc[[0, 1]].iterrows():
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1))
    spots = {"budget": (0.55, -0.32), "revenue": (1.02, -0.34), "vote_count": (1.08, 0.05),
             "popularity": (0.62, 0.2), "runtime": (0.12, 0.76), "vote_average": (0.28, 0.9)}
    for name, (x, y) in spots.items():
        ax.text(x, y, name, fontsize=6, ha="right" if name == "runtime" else "center", va="center")
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.set_aspect("equal")
    ax.set_xlabel(f"PC1 ({p.percentage_of_variance_[0]:.0f}%)", fontsize=7)
    ax.set_ylabel(f"PC2 ({p.percentage_of_variance_[1]:.0f}%)", fontsize=7)
    ax.set_xticks([]); ax.set_yticks([])
    return fig


def famd_map():
    import prince
    wine = _wine()
    f = prince.FAMD(n_components=5, random_state=0).fit(wine)
    rc = f.row_coordinates(wine)
    good = wine["quality_label"] == "good"
    fig, ax = small(3.0, 1.55)
    ax.scatter(rc.loc[~good, 0], rc.loc[~good, 1], s=3, alpha=.3, color="#7a8fbf", label="ordinary")
    ax.scatter(rc.loc[good, 0], rc.loc[good, 1], s=3, alpha=.5, color=ACCENT, label="good")
    ax.set_xlabel("Dim 1", fontsize=7); ax.set_ylabel("Dim 2", fontsize=7)
    ax.legend(fontsize=6, frameon=False, markerscale=3)
    return fig


def which_tool():
    rows = [("only numbers", "prince.PCA", "or sklearn PCA"),
            ("numbers + categories", "prince.FAMD", "session 13's wines"),
            ("only categories", "prince.MCA", "survey answers"),
            ("latent factors, rotated", "statsmodels", "Factor + varimax")]
    b = text(6, 12, "your columns are…", 7.5, "start", "#555", "bold") + text(112, 12, "use", 7.5, "start", "#555", "bold")
    for i, (kind, tool, note) in enumerate(rows):
        y = 28 + i * 15
        b += text(6, y, kind, 7.6, "start", "#222")
        b += text(112, y, tool, 7.6, "start", ACCENT, "bold")
        b += text(234, y, note, 6.6, "end", "#555")
    return svg(240, 90, b)


PAGES = [[
    dict(title="1 · Which method?",
         intro="All four turn many correlated columns into a few dimensions.",
         figure_top=which_tool,
         tip="Session 13 runs PCA with **scikit-learn** and factor analysis with **statsmodels**: both have their own cheatsheet. prince does the same PCA, and FAMD for mixed data."),
    dict(title="2 · PCA — fit",
         items=[
             dict(code='df = movies[["budget", "popularity", ...]].dropna()',
                  text="numeric columns only, no gaps."),
             dict(code="pca = prince.PCA(n_components=4,\n    rescale_with_mean=True, rescale_with_std=True)",
                  text="**standardise** (the two `rescale_` options): otherwise budget in dollars outweighs a rating out of 10.",
                  ex="pca = pca.fit(df)"),
         ],
         warn="PCA on unstandardised columns ranks variables by their units, not their information."),
    dict(title="3 · The observations on the map",
         items=[
             dict(code="pca.row_coordinates(df)",
                  text="every film's position on the components — a method: pass the data."),
             dict(code="pca.row_contributions_", text="which observations pull a component most."),
         ]),
    dict(title="4 · How many components?",
         figure_top=scree,
         items=[
             dict(code="pca.eigenvalues_summary",
                  text="eigenvalue, % of variance and cumulative % per component — the table behind the scree plot."),
             dict(code="pca.percentage_of_variance_", text="the same percentages, as numbers."),
         ],
         tip="Keep components with eigenvalue above 1 (the dashed line), or up to the elbow of the scree plot; here two (68% of the variance)."),
    dict(title="5 · What the components mean",
         figure_top=circle, fig_width="68%",
         items=[
             dict(code="pca.column_correlations",
                  text="each variable's correlation with each component: the arrows of the circle."),
             dict(code="pca.column_contributions_", text="how much each variable builds each component (shares)."),
         ],
         tip="PC1 here is **size** (budget, revenue, votes); PC2 is **quality and length** (rating, runtime)."),
    dict(title="6 · FAMD — numbers and categories together",
         intro="Session 13: the wines' chemistry (numbers) and their verdict (a category).",
         items=[
             dict(code='wine["quality_label"] = np.where(wine["good"] == 1, "good", "ordinary")',
                  text="the category as **text**: FAMD treats object columns as categorical."),
             dict(code="famd = prince.FAMD(n_components=5, random_state=0).fit(wine)",
                  text="no rescaling options: FAMD standardises the numbers and weights the categories itself."),
             dict(code="famd.eigenvalues_summary", text="as for PCA."),
             dict(code="famd.column_coordinates_",
                  text="how much each variable — number or category — carries each dimension. An **attribute**: no brackets."),
             dict(code="famd.row_coordinates(wine)", text="each wine on the dimensions, as plotted below."),
         ],
         figure=famd_map, fig_width="88%",
         warn="Drop the 0/1 column once you have made it a label, or the same information enters twice."),
    dict(title="7 · Pitfalls",
         items=[
             dict(code="column_coordinates_  vs  row_coordinates(df)", text="the first is an attribute, the second a method that takes the data."),
             dict(code="components are 0, 1, 2 …", text="prince counts from 0: column `0` is the first component."),
             dict(code="a component is not a cause", text="it summarises correlation; naming it is your interpretation, to defend."),
         ]),
]]
