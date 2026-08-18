"""
Generate one data dictionary per group, read from the actual parquet files.

    python scripts/build_spine/make_dictionaries.py

Accurate by construction: column lists, dtypes, ranges and missingness are measured,
not asserted. Re-run after every rebuild of the spine.
"""

import os
import pandas as pd
import spec

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.abspath(os.path.join(HERE, "..", "..", "data", "spine"))
OUT = os.path.join(SPINE, "dictionaries")

GROUPS = {
    "G01": ("angle_a_country.parquet", "A", "Compute, energy and the physical constraint",
            "country × time",
            "Prices, generation mix and intensity for 30 European countries, 2010–2024."),
    "G02": ("angle_a_sector.parquet", "A", "Compute, energy and the physical constraint",
            "country × sector × time",
            "Industrial and services energy use by NACE section."),
    "G03": ("angle_b_occupation.parquet", "B", "Work, skills and the social contract",
            "occupation × country × time",
            "Employment, wages and task-exposure by ISCO-08 major group."),
    "G04": ("angle_b_sector.parquet", "B", "Work, skills and the social contract",
            "sector × country × time",
            "Employment, earnings, vacancies and education by NACE section."),
    "G05": ("angle_c_country.parquet", "C", "AI adoption and the productivity question",
            "country × time",
            "Adoption indicators and barriers. Digital series from 2014; AI module from 2021."),
    "G06": ("angle_c_sector_size.parquet", "C", "AI adoption and the productivity question",
            "country × sector × size class × time",
            "Where the adoption gradient is steepest."),
    "G07": ("angle_d_partner.parquet", "D", "Trade, inputs and dependence",
            "reporter × partner × time",
            "Bilateral flows in AI-relevant goods, aggregated over products."),
    "G08": ("angle_d_product.parquet", "D", "Trade, inputs and dependence",
            "reporter × product × time",
            "Product-level flows by HS line."),
    "G09": ("angle_e_centralbank.parquet", "E", "Institutional language and policy attention",
            "document",
            "Central bank communications, monthly, ECB / BoE / BoC, 2010–2024."),
    "G10": ("angle_e_national.parquet", "E", "Institutional language and policy attention",
            "document",
            "National policy and strategy documents, cross-country."),
}

# What each column is, its unit, and the trap in it.
NOTES = {
    # ── keys
    "geo": ("Country code (Eurostat)", "code", ""),
    "time": ("Year", "year", ""),
    "nace_r2": ("Economic activity, NACE Rev. 2 section", "code", ""),
    "isco08": ("Occupation, ISCO-08 major group", "code", ""),
    "size_emp": ("Enterprise size class, persons employed", "code", ""),
    "partner": ("Trade partner or bloc", "code", "EU_INTRA aggregates intra-EU flows."),
    "hs": ("Harmonised System product line", "code",
           "HS was revised in 2012, 2017 and 2022; concordances are imperfect."),
    "doc_id": ("Document identifier", "id", ""),
    "date": ("Document date", "date", ""),
    "flag": ("Eurostat observation status", "code",
             "u = low reliability · c = confidential (value is NaN) · b = break in series · "
             "p = provisional. Dropping 'u' silently biases coverage toward large economies."),
    # ── core
    "gdp_pc_eur": ("GDP per capita, current prices", "EUR", "Revised. Not volume-adjusted."),
    "population": ("Population on 1 January", "persons", ""),
    "employment_ths": ("Employment", "thousand persons", ""),
    "productivity_idx": ("Real labour productivity per person", "index, 2015 = 100", ""),
    "gfcf_meur": ("Gross fixed capital formation", "million EUR", ""),
    "prod_growth": ("Year-on-year productivity growth", "%", "First year per country is NaN."),
    "falling_behind": ("Bottom-decile productivity growth this year", "0/1",
                       "Threshold is computed within year, so the rate is ~10% by construction."),
    "falling_behind_next": ("Bottom-decile growth NEXT year", "0/1",
                            "THE SESSION 06 LABEL. Last year per country is NaN — that is "
                            "correct, not a defect."),
    # ── angle A
    "share_renew": ("Renewable share of electricity generation", "share 0–1", ""),
    "share_fossil": ("Fossil share of electricity generation", "share 0–1",
                     "The three shares sum to 1: including all three plus an intercept is "
                     "exact collinearity. Drop one."),
    "share_nuclear": ("Nuclear share of electricity generation", "share 0–1", ""),
    "elec_price_eur_kwh": ("Non-household electricity price, excl. taxes", "EUR/kWh",
                           "Band IC (500–2000 MWh). A price without its band is meaningless. "
                           "Structural break in 2022."),
    "elec_price_incl_tax": ("Same price including taxes and levies", "EUR/kWh",
                            "The difference from the excl.-tax series is the policy wedge."),
    "energy_intensity": ("Energy intensity of the economy", "kgoe per thousand EUR", ""),
    "elec_industry_gwh": ("Final electricity consumption, industry", "GWh", ""),
    "elec_services_gwh": ("Final electricity consumption, commercial and public services", "GWh",
                          "The best available proxy for data-centre load, and a poor one."),
    "elec_use_gwh": ("Electricity use by sector", "GWh", ""),
    "energy_cost_share": ("Energy cost as a share of sector gross output", "share 0–1", ""),
    "gva_meur": ("Gross value added", "million EUR", ""),
    # ── angle B
    "exposure_index": ("Task-based automation exposure", "index 0–1",
                       "A CONSTRUCT, not a measurement. Session 09's validity framework "
                       "applies to it in full."),
    "routine_share": ("Share of routine task content", "share 0–1", ""),
    "ict_task_share": ("Share of ICT-intensive task content", "share 0–1",
                       "Strongly negatively correlated with exposure_index by construction."),
    "mean_wage_eur": ("Mean annual wage in the occupation", "EUR", ""),
    "annual_earnings_eur": ("Mean annual earnings", "EUR",
                            "Real source is quadrennial; treat annual variation with care."),
    "vacancy_rate": ("Job vacancy rate", "%", ""),
    "tertiary_share": ("Share of employment with tertiary education", "share 0–1", ""),
    # ── angle C
    "ai_use_any": ("Enterprises using at least one AI technology", "% of enterprises",
                   "NOT AVAILABLE BEFORE 2021 — structurally absent, not missing at random."),
    "ai_use_ml": ("Enterprises using machine learning", "% of enterprises", ""),
    "ai_use_ge3": ("Enterprises using three or more AI technologies", "% of enterprises",
                   "An intensity measure. Highly correlated with ai_use_any."),
    "ai_text_mining": ("Enterprises using text mining", "% of enterprises", ""),
    "ai_image_reco": ("Enterprises using image recognition", "% of enterprises", ""),
    "cloud_use": ("Enterprises buying cloud computing services", "% of enterprises",
                  "Available from 2014 — a longer panel than the AI columns."),
    "ict_specialists": ("Enterprises employing ICT specialists", "% of enterprises", ""),
    "digital_intensity": ("Digital intensity index", "% of enterprises, high or very high", ""),
    "barrier_cost": ("Did not adopt: costs too high", "% of enterprises", ""),
    "barrier_skills": ("Did not adopt: lack of expertise", "% of enterprises", ""),
    "barrier_data": ("Did not adopt: data availability or quality", "% of enterprises", ""),
    "barrier_legal": ("Did not adopt: legal uncertainty", "% of enterprises", ""),
    "bias_checks": ("Has measures to check AI output for bias", "% of enterprises", ""),
    "rd_pct_gdp": ("Gross domestic expenditure on R&D", "% of GDP", ""),
    "has_ai_strategy": ("National AI strategy in force", "0/1",
                        "THE SESSION 10 TREATMENT. Adoption is NOT random — it depends on "
                        "country characteristics. That is the whole problem."),
    "n_enterprises": ("Number of enterprises in the cell", "count",
                      "Use as a weight. Unweighted means across size classes are misleading."),
    # ── angle D
    "import_value_eur": ("Import value", "EUR", "Mirror statistics disagree with the partner's "
                         "reported exports, sometimes substantially."),
    "export_value_eur": ("Export value", "EUR", ""),
    "is_reexport_hub": ("Reporter is NL, BE or IE", "0/1",
                        "Rotterdam is not a producer. Ignoring re-exports will make these "
                        "countries look like manufacturing powers."),
    "top_partner_share": ("Share of the largest single partner", "share 0–1", ""),
    "hs_revision_break": ("Year of an HS classification revision", "0/1", ""),
    # ── angle E
    "institution": ("Issuing institution", "code", ""),
    "country": ("Country or area", "code", ""),
    "doc_type": ("Document type", "code", ""),
    "n_words": ("Document length", "words",
                "NORMALISE BY THIS. Raw term counts rise when documents get longer or more "
                "numerous, with no change in attention."),
    "text": ("Document text", "string", ""),
}

# What each group should notice in its own data before modelling anything.
FIRST_LOOK = {
    "G01": ["Plot `elec_price_eur_kwh` against time for six countries. Find 2022.",
            "Confirm the three generation shares sum to 1. What does that forbid?",
            "Which countries have the most missing rows, and how large are they?"],
    "G02": ["Rank sectors by `energy_cost_share`. Does the ordering match your priors?",
            "Compute electricity per unit of GVA by sector. Which sector is the outlier?",
            "Check whether the 2022 shock hits all sectors equally."],
    "G03": ["Plot `exposure_index` against `mean_wage_eur`. What is the sign, and is it causal?",
            "Which occupations are shrinking? Compare to `exposure_index`.",
            "Count the `u` flags. Which occupations are worst affected, and why would that be?"],
    "G04": ["Plot earnings against `tertiary_share` by sector.",
            "Find 2020 in the vacancy rate.",
            "Is the earnings series smooth year to year? Should it be?"],
    "G05": ["Count non-missing `ai_use_any` by year. When does the series start, and why?",
            "Compute the correlation matrix of the adoption columns. Report the maximum.",
            "Tabulate `has_ai_strategy` against `gdp_pc_eur`. Is treatment random?"],
    "G06": ["Plot adoption by size class. How steep is the gradient?",
            "Which NACE section adopts most? Does that survive controlling for size?",
            "Weight by `n_enterprises` and redo. Does the ranking change?"],
    "G07": ["Plot each partner's share over time. Which trends up?",
            "Compare NL and DE import values per capita. Explain the gap.",
            "Compute an HHI of partner concentration by country and year."],
    "G08": ["Find the NL row for HS 8486. Why does it dominate?",
            "Plot `top_partner_share` by product. Which line is most concentrated?",
            "Check what happens to the series in 2012, 2017 and 2022."],
    "G09": ["Count documents per month. Is the corpus growing?",
            "Compute raw uncertainty-term counts, then the same normalised by `n_words`. "
            "Do the two series tell the same story?",
            "Compare ECB and BoC. Do they differ in level, in trend, or in both?"],
    "G10": ["Count documents per country. Which countries publish most, and is that attention "
            "or administrative habit?",
            "Build a term-frequency index by country-year and map it.",
            "Compare your index to G09's. Should they agree?"],
}


def describe(df, col):
    s = df[col]
    if pd.api.types.is_numeric_dtype(s) and s.notna().any():
        if col == "time":
            return f"{int(s.min())}–{int(s.max())}", f"{s.isna().mean() * 100:.1f}%"
        if set(s.dropna().unique()) <= {0, 1}:
            return f"0/1 (mean {s.mean():.3f})", f"{s.isna().mean() * 100:.1f}%"
        return f"{s.min():,.4g} … {s.max():,.4g}", f"{s.isna().mean() * 100:.1f}%"
    if s.dtype == object and col == "text":
        return f"{s.str.len().min()}–{s.str.len().max()} chars", "0.0%"
    n = s.nunique(dropna=True)
    ex = ", ".join(map(str, sorted(s.dropna().unique())[:6]))
    return f"{n} values: {ex}{' …' if n > 6 else ''}", f"{s.isna().mean() * 100:.1f}%"


def one(gid):
    fname, angle, atitle, unit, blurb = GROUPS[gid]
    df = pd.read_parquet(os.path.join(SPINE, fname))
    keys = [c for c in ("geo", "time", "nace_r2", "isco08", "size_emp", "partner", "hs",
                        "doc_id", "date", "institution", "country") if c in df.columns]

    L = []
    L.append(f"# {gid} — data dictionary\n")
    L.append(f"**Angle {angle} — {atitle}**  \n**Unit of analysis:** {unit}\n")
    L.append(f"{blurb}\n")
    L.append(f"```python\nimport pandas as pd\n"
             f"core = pd.read_parquet(\"data/spine/core.parquet\")\n"
             f"mine = pd.read_parquet(\"data/spine/{fname}\")\n")
    if "geo" in df.columns and "time" in df.columns:
        L.append("df   = mine.merge(core, on=[\"geo\", \"time\"], how=\"left\")\n```\n")
    else:
        L.append("```\n")
    L.append(f"| | |\n|---|---|\n| **File** | `data/spine/{fname}` |\n"
             f"| **Rows** | {len(df):,} |\n| **Columns** | {df.shape[1]} |\n"
             f"| **Keys** | {', '.join('`' + k + '`' for k in keys)} |\n"
             f"| **Overall missing** | {df.isna().mean().mean() * 100:.1f}% |\n")

    L.append("\n---\n\n## Columns\n")
    L.append("| Column | Meaning | Unit | Range / values | Missing |")
    L.append("|---|---|---|---|---|")
    for c in df.columns:
        meaning, cunit, _ = NOTES.get(c, ("*(undocumented — tell the instructor)*", "", ""))
        rng_, miss = describe(df, c)
        L.append(f"| `{c}` | {meaning} | {cunit} | {rng_} | {miss} |")

    traps = [(c, NOTES[c][2]) for c in df.columns if c in NOTES and NOTES[c][2]]
    if traps:
        L.append("\n---\n\n## Traps in this file\n")
        L.append("> Read these before you model. Each one has cost somebody a week.\n")
        for c, t in traps:
            L.append(f"- **`{c}`** — {t}")

    L.append("\n---\n\n## Structural breaks\n")
    L.append("| From | To | What | Affects |")
    L.append("|---|---|---|---|")
    for a, b, what, aff in spec.BREAKS:
        L.append(f"| {a} | {b or '—'} | {what} | {aff} |")

    L.append("\n---\n\n## First look — do these before Session 02\n")
    for i, t in enumerate(FIRST_LOOK[gid], 1):
        L.append(f"{i}. {t}")

    L.append("\n---\n\n## Missing data\n")
    miss = (df.isna().mean() * 100).sort_values(ascending=False)
    miss = miss[miss > 0]
    if len(miss):
        L.append("| Column | % missing |\n|---|---|")
        for c, v in miss.items():
            L.append(f"| `{c}` | {v:.1f} |")
        L.append("\n**Missingness is not random.** It is heavier in small countries, so listwise "
                 "deletion shifts your sample toward large economies. Whatever you do about it, "
                 "do it *inside* the cross-validation loop and report which countries you lost.")
    else:
        L.append("No missing values in this file.")

    L.append("\n---\n\n"
             "> ⚠️ **These are teaching fixtures, not observed data.** They carry the schema, "
             "coverage, flags and pathologies of the real sources so that every method behaves as "
             "it would on the real thing. Do not cite any number from them as a fact about "
             "Europe. See [`../PROVENANCE.md`](../PROVENANCE.md).\n")
    L.append("*Related: [research mandates](../../../RESEARCH-MANDATES.md) · "
             "[spine overview](../README.md)*")
    return "\n".join(L)


def main():
    os.makedirs(OUT, exist_ok=True)
    for gid in GROUPS:
        path = os.path.join(OUT, f"{gid}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(one(gid) + "\n")
        print(f"  wrote data/spine/dictionaries/{gid}.md")
    print(f"\n{len(GROUPS)} data dictionaries written.")


if __name__ == "__main__":
    main()
