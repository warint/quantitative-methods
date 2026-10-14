"""linearmodels — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#2b5d8a"
BLUE, RED, GREEN, SAND = "#cfe0f5", "#f8d3cd", "#d4ecd9", "#f2efe8"

META = dict(
    title="linearmodels",
    color=ACCENT,
    tagline="Panel data: the same countries or firms, followed over time",
    sessions="6",
)
META["import"] = "from linearmodels.panel import PanelOLS, RandomEffects"
META["version_note"] = "a panel needs a two-level index: entity, then time"


def panel_pic():
    """Long format: one row per entity-year, indexed by (entity, time)."""
    cols = {"Austria": BLUE, "Belgium": RED, "Canada": GREEN}
    b = text(10, 11, "long format: one row = one entity in one year", 8, "start", ACCENT, "bold")
    y = 18
    for name, c in cols.items():
        for yr in (2010, 2011, 2012):
            b += f'<rect x="10" y="{y}" width="48" height="12" fill="{c}" stroke="#555" stroke-width="0.6"/>'
            b += f'<rect x="58" y="{y}" width="30" height="12" fill="{SAND}" stroke="#555" stroke-width="0.6"/>'
            b += grid(88, y, 1, 2, 12)
            b += text(34, y + 9, name, 7) + text(73, y + 9, str(yr), 7)
            y += 12
    b += text(34, y + 10, "entity", 7.5, "middle", ACCENT, "bold") + text(73, y + 10, "time", 7.5, "middle", ACCENT, "bold")
    b += text(100, y + 10, "y, x", 7.5)
    b += text(178, 42, 'set_index(["country", "year"])', 8, "middle", ACCENT, "bold")
    b += text(178, 56, "tells linearmodels which", 7.5) + text(178, 66, "rows are the same entity", 7.5)
    b += text(178, 86, "missing years? fine:", 7.5) + text(178, 96, "the panel is unbalanced", 7.5)
    return svg(240, y + 15, b)


def within_between():
    """Illustration: within each entity the slope is negative, across entities positive."""
    import numpy as np
    fig, ax = small(3.0, 1.7)
    rng = np.random.default_rng(1)
    colors = ["#2b5d8a", "#e3120b", "#2e8b57"]
    centres = [(2, 3), (4, 5), (6, 7)]
    for (cx, cy), col in zip(centres, colors):
        x = cx + rng.uniform(-0.9, 0.9, 12)
        y = cy - 0.8 * (x - cx) + rng.normal(0, 0.15, 12)
        ax.scatter(x, y, s=8, color=col, alpha=.7)
        xs = np.array([cx - 0.9, cx + 0.9])
        ax.plot(xs, cy - 0.8 * (xs - cx), color=col, lw=1.6)
    mx = np.array([c[0] for c in centres]); my = np.array([c[1] for c in centres])
    ax.scatter(mx, my, s=36, marker="D", color="black", zorder=5)
    ax.plot([1.2, 6.8], [2.2, 7.8], color="black", lw=1, ls="--")
    ax.text(1.1, 7.2, "between: averages rise", fontsize=6.5)
    ax.text(4.6, 2.6, "within: each entity falls", fontsize=6.5, color="#e3120b")
    ax.set_xlabel("x", fontsize=7); ax.set_ylabel("y", fontsize=7)
    ax.set_xticks([]); ax.set_yticks([])
    return fig


def fe_vs_re():
    b = text(60, 13, "fixed effects", 9, "middle", ACCENT, "bold")
    b += text(60, 27, "one intercept per entity,", 7.5) + text(60, 38, "absorbed: only change", 7.5)
    b += text(60, 49, "within an entity is used", 7.5)
    b += text(180, 13, "random effects", 9, "middle", ACCENT, "bold")
    b += text(180, 27, "intercepts drawn at random,", 7.5) + text(180, 38, "assumed unrelated to x:", 7.5)
    b += text(180, 49, "more precise, riskier", 7.5)
    b += text(120, 70, "Hausman: do they disagree beyond noise?", 7.8, "middle", "#333", "bold")
    b += text(120, 82, "yes (small p) → keep fixed effects", 7.5)
    b += '<line x1="120" y1="6" x2="120" y2="54" stroke="#bbb" stroke-dasharray="3,2"/>'
    return svg(240, 88, b)


PAGES = [[
    dict(title="1 · Shape the panel",
         intro="Same structure as any DataFrame, plus an index that says who and when.",
         figure_top=panel_pic,
         items=[
             dict(code='panel = d.dropna(subset=cols).set_index(["country", "year"])',
                  text="drop the gaps in what you use, then index by **entity, then time** — in that order."),
             dict(code='y = panel["grossdebt"]', text="the outcome, a Series with the two-level index."),
             dict(code='X = panel[["busfreedom", "finfreedom", "invfreedom"]]', text="the regressors, a DataFrame with the same index."),
             dict(code="panel.index.get_level_values(0).nunique()", text="how many entities (here 16 countries; 23 years; 314 rows)."),
             dict(code="panel.groupby(level=0).size()", text="rows per entity: is the panel balanced?"),
         ],
         warn="Index in the wrong order — time first — and every \"country effect\" becomes a year effect."),
    dict(title="2 · Fixed effects — PanelOLS",
         items=[
             dict(code="fixed = PanelOLS(y, X, entity_effects=True).fit()",
                  text="one intercept per country, absorbed rather than printed. Each slope now compares a country **with itself** over time."),
             dict(code="PanelOLS(y, X, entity_effects=True, time_effects=True)",
                  text="**two-way**: also one intercept per year, which removes shocks every country shared."),
             dict(code='PanelOLS.from_formula("y ~ x1 + x2 + EntityEffects", data=panel)',
                  text="the same model, written as a formula."),
             dict(code="print(fixed)", text="the table: coefficients, standard errors, R² within / between / overall."),
             dict(code="fixed.params  ·  fixed.std_errors  ·  fixed.pvalues", text="the numbers, as Series."),
         ],
         tip="A fixed-effects slope answers a **within** question: when *this* country's x rises, what happens to *its* y?"),
    dict(title="3 · Within against between",
         intro="An illustration: three entities, each followed over time (coloured lines); the diamonds are their averages.",
         figure_top=within_between,
         items=[
             dict(code="fixed.rsquared_within  ·  fixed.rsquared_between",
                  text="how much of the variation **inside** countries, and **across** country averages, the model accounts for."),
         ],
         warn="Anything constant within a country — geography, legal origin — is absorbed: fixed effects cannot estimate its effect."),
    dict(title="4 · Random effects, and choosing",
         figure_top=fe_vs_re,
         items=[
             dict(code="random_ = RandomEffects(y, X).fit()",
                  text="treats the country intercepts as random draws: uses within **and** between variation."),
             dict(code="diff = fixed.params - random_.params",
                  text="the Hausman test, as in session 6: compare the two sets of slopes…"),
             dict(code="vdiff = fixed.cov - random_.cov",
                  text="…against the difference of their covariance matrices…"),
             dict(code="H = diff @ np.linalg.pinv(vdiff) @ diff",
                  text="…a χ² with one degree of freedom per slope.",
                  ex="p = stats.chi2.sf(H, len(diff))"),
         ],
         tip="Choose on the assumption, never on which model gives the significant answer."),
    dict(title="5 · Standard errors that respect the panel",
         items=[
             dict(code='.fit(cov_type="clustered", cluster_entity=True)',
                  text="years of the same country are not independent: cluster by entity. The estimates do not move; the standard errors do — here they roughly double."),
             dict(code='.fit(cov_type="robust")', text="heteroskedasticity-robust only, without clustering."),
         ]),
    dict(title="6 · When linearmodels complains",
         items=[
             dict(code="ValueError: ... MultiIndex", text="the data has no (entity, time) index: `set_index` first."),
             dict(code="AbsorbingEffectError", text="a regressor never changes within an entity: fixed effects have absorbed it. Drop it, or pass `drop_absorbed=True` to `PanelOLS`."),
             dict(code="matrix not positive definite (Hausman)", text="use `np.linalg.pinv`, as the deck does, not `inv`."),
         ]),
]]
