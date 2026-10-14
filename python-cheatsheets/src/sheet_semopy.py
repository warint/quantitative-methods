"""semopy — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import arrow, svg, text, small  # noqa: E402

ACCENT = "#6a3d9a"
LIGHT = "#ece3f5"

META = dict(
    title="semopy",
    color=ACCENT,
    tagline="Structural equation models: latent variables, measured by indicators, linked by paths",
    sessions="9",
)
META["import"] = "import semopy"
META["version_note"] = "pip install semopy · the Python counterpart of R's lavaan"


def oval(cx, cy, label, rx=30, ry=13):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{LIGHT}" stroke="{ACCENT}" '
            f'stroke-width="1.3"/>' + text(cx, cy + 3, label, 8, "middle", ACCENT, "bold"))


def square(x, y, label, w=24, h=15):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#555" stroke-width="1"/>'
            + text(x + w / 2, y + 11, label, 7.5))


def path_diagram():
    """Two latent variables, three indicators each, and one regression path."""
    b = ""
    for i, lab in enumerate(["x1", "x2", "x3"]):
        x = 8 + i * 30
        b += square(x, 8, lab)
        b += arrow(50, 52, x + 12, 25)
    b += oval(50, 65, "visual")
    for i, lab in enumerate(["x4", "x5", "x6"]):
        x = 148 + i * 30
        b += square(x, 8, lab)
        b += arrow(190, 52, x + 12, 25)
    b += oval(190, 65, "textual")
    b += arrow(81, 65, 158, 65, color=ACCENT)
    b += text(120, 60, "textual ~ visual", 7.2, "middle", ACCENT, "bold")
    b += text(50, 92, "visual =~ x1 + x2 + x3", 7.2, "middle", "#333")
    b += text(190, 92, "textual =~ x4 + x5 + x6", 7.2, "middle", "#333")
    b += text(120, 108, "oval = latent (not observed) · box = measured · arrow = effect", 7, "middle", "#555")
    return svg(240, 114, b)


def operators():
    rows = [("=~", "is measured by", "visual =~ x1 + x2 + x3"),
            ("~", "is regressed on", "textual ~ visual"),
            ("~~", "covaries with", "x1 ~~ x4")]
    b = ""
    for i, (op, meaning, ex) in enumerate(rows):
        y = 16 + i * 22
        b += f'<rect x="6" y="{y - 12}" width="30" height="17" rx="3" fill="{ACCENT}"/>'
        b += text(21, y, op, 9.5, "middle", "#fff", "bold")
        b += text(44, y, meaning, 8, "start", "#222", "bold")
        b += text(140, y, ex, 7.5, "start", "#333")
    return svg(240, 72, b)


def loadings_bar():
    """Standardised loadings of the Holzinger–Swineford three-factor model."""
    import semopy
    from semopy.examples import holzinger39
    data = holzinger39.get_data()
    m = semopy.Model("visual =~ x1 + x2 + x3\ntextual =~ x4 + x5 + x6\nspeed =~ x7 + x8 + x9")
    m.fit(data)
    ins = m.inspect(std_est=True)
    ld = ins[(ins.op == "~") & ins.rval.isin(["visual", "textual", "speed"])]
    fig, ax = small(3.0, 1.55)
    colors = {"visual": "#6a3d9a", "textual": "#2b5d8a", "speed": "#2e8b57"}
    ax.bar(ld.lval, ld["Est. Std"], color=[colors[r] for r in ld.rval])
    ax.axhline(0.5, color="#e3120b", lw=0.8, ls="--")
    ax.set_ylim(0, 1); ax.set_ylabel("std. loading", fontsize=7)
    for f, c in colors.items():
        ax.bar(0, 0, color=c, label=f)
    ax.legend(fontsize=6, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    return fig


def fit_gauges():
    """Where the common cut-offs sit."""
    rows = [("CFI", "≥ 0.95 good · ≥ 0.90 acceptable", 0.931),
            ("TLI", "≥ 0.95 good · ≥ 0.90 acceptable", 0.896),
            ("RMSEA", "≤ 0.06 good · ≤ 0.08 acceptable", 0.092)]
    b = ""
    for i, (name, rule, val) in enumerate(rows):
        y = 14 + i * 20
        b += text(6, y, name, 8, "start", ACCENT, "bold")
        b += text(48, y, f"{val:.3f}", 8, "start", "#222", "bold")
        b += text(90, y, rule, 7.2, "start", "#333")
    b += text(6, 74, "the three-factor model: acceptable at best", 7, "start", "#555")
    return svg(240, 80, b)


PAGES = [[
    dict(title="1 · Write the model as text",
         intro="A model is a string: one line per relation, using three operators.",
         figure_top=operators,
         items=[
             dict(code='desc = """ … """',
                  text="the **measurement** part: each latent variable on the left, its indicators on the right.",
                  ex='desc = """\nvisual  =~ x1 + x2 + x3\ntextual =~ x4 + x5 + x6\nspeed   =~ x7 + x8 + x9\n"""'),
             dict(code="textual ~ visual", text="the **structural** part: a regression between latent variables."),
             dict(code="x1 ~~ x4", text="a covariance between two residuals, when the questions share something the factors do not."),
         ]),
    dict(title="2 · Read it as a picture",
         figure_top=path_diagram,
         tip="Draw the diagram **before** writing the string: every arrow is one term in the model."),
    dict(title="3 · Fit",
         items=[
             dict(code="from semopy.examples import holzinger39",
                  text="the classic data set: 301 children, nine ability tests — ships with semopy.",
                  ex="data = holzinger39.get_data()"),
             dict(code="fit = semopy.Model(desc)", text="build the model from the string."),
             dict(code="fit.fit(data)", text="estimate it, by maximum likelihood; the column names must match the string."),
         ],
         warn="Each latent variable needs a scale: semopy fixes the **first** loading of each factor to 1. That row has no standard error."),
    dict(title="4 · Read the estimates",
         figure_top=loadings_bar,
         items=[
             dict(code="print(fit.inspect(std_est=True))",
                  text="every parameter: estimate, **standardised** estimate (`Est. Std`), standard error, z, p."),
             dict(code="lval  op  rval", text="how to read a row: `x2 ~ visual` is the loading of x2 on visual (semopy prints `=~` lines as `~`)."),
             dict(code='ins[ins["op"] == "~~"]', text="the variances and covariances, including those of the latent variables."),
         ],
         tip="Standardised loadings above about 0.5 say the indicator measures its factor well; x2 here is weak (0.42)."),
    dict(title="5 · Judge the fit",
         figure_top=fit_gauges,
         items=[
             dict(code="print(semopy.calc_stats(fit).T)",
                  text="χ² and its p-value, CFI, TLI, RMSEA, AIC, BIC, … in one table."),
             dict(code="chi2 p-value", text="almost always significant with real data and a decent sample: read it, but do not decide on it alone."),
         ],
         warn="Report **all** the indices, not the one that passes. A good fit does not make the model true — other models fit too."),
    dict(title="6 · A full model: measurement and paths",
         intro="Session 9's second example: 75 countries.",
         items=[
             dict(code="from semopy.examples import political_democracy", text="the data: x1–x3 measure industrialisation in 1960, y1–y8 democracy in 1960 and 1965."),
             dict(code="ind60 =~ x1 + x2 + x3", text="measurement, as before — three latent variables.",
                  ex='model = """\n  ind60 =~ x1 + x2 + x3\n  dem60 =~ y1 + y2 + y3 + y4\n  dem65 =~ y5 + y6 + y7 + y8\n  dem60 ~ ind60\n  dem65 ~ ind60 + dem60\n"""'),
             dict(code="dem65 ~ ind60 + dem60", text="the structural paths: a regression whose variables are all latent."),
         ]),
    dict(title="7 · Pitfalls",
         items=[
             dict(code="KeyError / variable not found", text="a name in the string is not a column of the data: check spelling and case."),
             dict(code="three indicators per factor", text="fewer than three and the factor is hard to identify; one indicator cannot carry a latent variable."),
         ]),
]]
