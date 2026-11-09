"""diff-diff — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import svg, text, small  # noqa: E402

ACCENT = "#1f6f5c"
LIGHT = "#d6ece5"
GREY = "#e9e6df"

META = dict(
    title="diff-diff",
    color=ACCENT,
    tagline="Difference-in-differences when units are treated in different years",
    sessions="11",
)
META["import"] = "import diff_diff as dd"
META["version_note"] = "pip install diff-diff · the Python counterpart of R's did and HonestDiD"


def cohorts_pic():
    """Adoption cohorts on a timeline: which cells are treated, which are clean controls."""
    years = [2021, 2022, 2023, 2024]
    rows = [("cohort 2021", 2021), ("cohort 2022", 2022), ("cohort 2023", 2023), ("never", None)]
    b = ""
    for j, yr in enumerate(years):
        b += text(92 + j * 36, 12, str(yr), 7.5, "middle", "#333", "bold")
    for i, (lab, g) in enumerate(rows):
        y = 18 + i * 17
        b += text(66, y + 10, lab, 7.5, "end", ACCENT if g else "#555", "bold")
        for j, yr in enumerate(years):
            treated = g is not None and yr >= g
            fill = ACCENT if treated else (LIGHT if g is None or yr < g else GREY)
            b += (f'<rect x="{75 + j * 36}" y="{y}" width="34" height="14" rx="2" fill="{fill}" '
                  f'stroke="#fff" stroke-width="1"/>')
    b += text(120, 98, "dark = treated · light = untreated, usable as a control", 7, "middle", "#555")
    b += text(120, 109, "cohort 2021 has no untreated year: it cannot be used", 7, "middle", "#b03a2e", "bold")
    return svg(240, 114, b)


def honest_pic():
    """Robust intervals widening with M, the allowed violation of parallel trends."""
    fig, ax = small(3.0, 1.55)
    Ms = [0, 0.25, 0.5, 1.0, 2.0]
    lo = [0.61, 0.05, -0.51, -1.64, -3.89]
    hi = [3.81, 4.37, 4.94, 6.06, 8.32]
    for k, (m, a, c) in enumerate(zip(Ms, lo, hi)):
        ax.plot([k, k], [a, c], lw=4, color=ACCENT if a > 0 else "#9a978f", solid_capstyle="round")
    ax.axhline(0, color="#b03a2e", lw=1)
    ax.set_xticks(range(len(Ms)), [str(m) for m in Ms], fontsize=6.5)
    ax.set_xlabel("M (allowed violation)", fontsize=6.5)
    ax.set_ylabel("95% robust CI", fontsize=6.5)
    ax.tick_params(axis="y", labelsize=6)
    ax.text(0.2, 7.4, "survives M = 0.25, not 0.5", fontsize=6.5, color=ACCENT)
    return fig


PAGES = [[
    dict(title="1 · Shape the panel",
         intro="Long format: one row per unit and year, plus one column saying when each unit was first treated.",
         figure_top=cohorts_pic,
         items=[
             dict(code='adopted = d[d["treated"] == 1].groupby("geo")["time"].min()',
                  text="the adoption year, from the **full** treatment series — not from the rows that happen to have an outcome."),
             dict(code='d["g"] = d["geo"].map(adopted).fillna(0).astype(int)',
                  text="`first_treat`: the adoption year, and **0** for units never treated."),
         ],
         warn="Count the cohorts and their pre-periods **before** fitting: a cohort with no untreated year is no evidence, and a cohort of one is one unit's story."),
    dict(title="2 · Fit Callaway–Sant'Anna",
         items=[
             dict(code='cs = dd.CallawaySantAnna(cluster="geo")',
                  text="each cohort against **clean** controls (never or not-yet treated), standard errors clustered by unit."),
             dict(code='cs = cs.fit(d, outcome="y", unit="geo", time="time", first_treat="g")',
                  text="the column names, said out loud."),
             dict(code="cs.overall_att, cs.overall_se, cs.n_clusters",
                  text="the average effect on the treated, its standard error, the number of clusters."),
         ],
         tip="Report it **beside** two-way fixed effects (`smf.ols(\"y ~ D + C(geo) + C(time)\")`). If they agree, show it; if not, that is the finding."),
    dict(title="3 · Read the group-time effects",
         items=[
             dict(code="gt = cs.to_dataframe()",
                  text="one row per (cohort, year): `group`, `time`, `effect`, `se`."),
             dict(code='gt["skip_reason"]',
                  text="why a cell was **dropped**: `missing_period` (no pre-period), `zero_treated_control` (nobody to compare)."),
             dict(code='gt[gt["time"] < gt["group"]]',
                  text="the rows **before** treatment: pre-trend evidence, not effects."),
         ],
         warn="A one-unit cohort can show a *smaller* standard error than a large one. That is not precision: there is no variation left to measure."),
    dict(title="4 · Aggregate",
         items=[
             dict(code='cs.aggregate("group").to_dataframe()', text="one effect per cohort."),
             dict(code='es = cs.aggregate("event_study")', text="effects by years since adoption: the event study."),
             dict(code='es.to_dataframe().query("event_time < 0")', text="the pre-treatment points; the reference year is zero by construction."),
         ]),
    dict(title="5 · How much violation does it survive?",
         intro="Rambachan and Roth (2023): do not test parallel trends; ask how much of it the result needs.",
         figure_top=honest_pic,
         items=[
             dict(code='h = dd.HonestDiD(method="relative_magnitude", M=0.5).fit(es)',
                  text="allow post-treatment departures up to M times the largest pre-treatment one."),
             dict(code="h.ci_lb, h.ci_ub, h.is_significant",
                  text="the robust 95% interval, and whether it still excludes zero."),
         ],
         tip="Report the **breakdown** value: the M at which the interval first reaches zero."),
    dict(title="6 · When diff-diff complains",
         items=[
             dict(code="KeyError on a column name", text="`outcome`, `unit`, `time`, `first_treat` must name columns of the data."),
             dict(code="a cohort is missing from the output", text="it had no pre-period or no control: read `skip_reason`, and say so in the report."),
             dict(code="the never-treated coded as 9999", text="use **0**: any other number is read as an adoption year."),
         ]),
]]
