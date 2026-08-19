"""
declarative catalogue of every series in the data spine.

One place to look when a dataset code changes. `build.py` reads this and nothing else.
Verify the whole catalogue with:  python scripts/verify_sources.py
"""

# Geography: EU-27 + UK, Norway, Switzerland. Eurostat codes.
GEO = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU",
    "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK",
    "UK", "NO", "CH",
]
YEARS = list(range(2010, 2025))

# NACE sections used wherever a sector dimension exists
NACE = ["C", "F", "G", "H", "J", "K", "M"]
NACE_LABEL = {
    "C": "Manufacturing", "F": "Construction", "G": "Wholesale and retail trade",
    "H": "Transportation and storage", "J": "Information and communication",
    "K": "Financial and insurance activities", "M": "Professional, scientific and technical",
}

SIZE_CLASS = ["10-49", "50-249", "GE250"]
ISCO = ["OC1", "OC2", "OC3", "OC4", "OC5", "OC7", "OC8", "OC9"]
ISCO_LABEL = {
    "OC1": "Managers", "OC2": "Professionals", "OC3": "Technicians and associate professionals",
    "OC4": "Clerical support workers", "OC5": "Service and sales workers",
    "OC7": "Craft and related trades", "OC8": "Plant and machine operators",
    "OC9": "Elementary occupations",
}
PARTNERS = ["US", "CN", "JP", "KR", "TW", "EU_INTRA", "ROW"]
HS_LINES = {
    "8541": "Semiconductor devices, diodes, transistors",
    "8542": "Electronic integrated circuits",
    "8486": "Semiconductor manufacturing equipment",
    "8471": "Automatic data-processing machines",
    "847950": "Industrial robots",
    "8517": "Telecommunications equipment",
}

# ─────────────────────────────────────────────────────────────────────────────
# SERIES = (key, eurostat_code, filters, value_column_name, notes)
# filters are passed straight to the dissemination API as query parameters.
# ─────────────────────────────────────────────────────────────────────────────

CORE = [
    ("gdp_pc", "nama_10_pc",
     {"unit": "CP_EUR_HAB", "na_item": "B1GQ"}, "gdp_pc_eur",
     "GDP per capita, current prices. Revised; chain-linked alternatives exist."),
    ("population", "demo_pjan",
     {"sex": "T", "age": "TOTAL"}, "population",
     "Population on 1 January."),
    ("employment", "nama_10_a10_e",
     {"unit": "THS_PER", "na_item": "EMP_DC", "nace_r2": "TOTAL"}, "employment_ths",
     "Total employment, domestic concept, thousands of persons."),
    ("productivity", "nama_10_lp_ulc",
     {"unit": "I15", "na_item": "RLPR_PER"}, "productivity_idx",
     "Real labour productivity per person, index 2015 = 100."),
    ("gfcf", "nama_10_gdp",
     {"unit": "CP_MEUR", "na_item": "P51G"}, "gfcf_meur",
     "Gross fixed capital formation, current prices, million EUR."),
]

ANGLE_A = [
    ("elec_price_ind", "nrg_pc_205",
     {"unit": "KWH", "product": "6000", "consom": "4161903", "tax": "X_TAX",
      "currency": "EUR"}, "elec_price_eur_kwh",
     "Non-household electricity price, band IC (500-2000 MWh), excluding taxes. "
     "SEMI-ANNUAL and BAND-DEPENDENT: a price without its band is meaningless."),
    ("elec_price_tax", "nrg_pc_205",
     {"unit": "KWH", "product": "6000", "consom": "4161903", "tax": "I_TAX",
      "currency": "EUR"}, "elec_price_incl_tax",
     "Same band, including taxes and levies. The difference is the policy wedge."),
    ("energy_intensity", "nrg_ind_ei",
     {"unit": "KGOE_TEUR"}, "energy_intensity",
     "Energy intensity of the economy, kg oil equivalent per thousand EUR of GDP."),
    ("elec_final_ind", "nrg_bal_c",
     {"nrg_bal": "FC_IND_E", "siec": "E7000", "unit": "GWH"}, "elec_industry_gwh",
     "Final electricity consumption, industry sector, GWh."),
    ("elec_final_serv", "nrg_bal_c",
     {"nrg_bal": "FC_OTH_CP_E", "siec": "E7000", "unit": "GWH"}, "elec_services_gwh",
     "Final electricity consumption, commercial and public services. The best available "
     "proxy for data-centre load, and a poor one — say so."),
]

ANGLE_B = [
    ("emp_occ", "lfsa_egais",
     {"sex": "T", "age": "Y15-64", "unit": "THS_PER"}, "employment_ths",
     "Employment by ISCO-08 occupation. SURVEY ESTIMATE: small cells carry real "
     "sampling error and Eurostat flags them."),
    ("unemp_educ", "lfsa_urgaed",
     {"sex": "T", "age": "Y15-74", "unit": "PC"}, "unemployment_rate",
     "Unemployment rate by educational attainment."),
    ("vacancy_rate", "jvs_a_rate_r2",
     {"sizeclas": "TOTAL", "s_adj": "NSA"}, "vacancy_rate",
     "Job vacancy rate by NACE section."),
    ("earnings", "earn_ses_annual",
     {"sex": "T", "unit": "EUR", "indic_se": "MEAN_E_EUR"}, "annual_earnings_eur",
     "Mean annual earnings. QUADRENNIAL (2010, 2014, 2018, 2022) — not annual."),
]

ANGLE_C = [
    ("ai_any", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_TANY", "nace_r2": "C10-S951_X_K"}, "ai_use_any",
     "Enterprises using at least one AI technology. STARTS 2021 — the panel is short, "
     "and question wording changed between waves."),
    ("ai_ml", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_TML", "nace_r2": "C10-S951_X_K"}, "ai_use_ml",
     "Enterprises using machine learning for data analysis."),
    ("ai_ge3", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_TGE3", "nace_r2": "C10-S951_X_K"}, "ai_use_ge3",
     "Enterprises using three or more AI technologies — an intensity measure."),
    ("ai_bar_cost", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_BCST", "nace_r2": "C10-S951_X_K"}, "barrier_cost",
     "Did not adopt: costs too high."),
    ("ai_bar_skills", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_BLE", "nace_r2": "C10-S951_X_K"}, "barrier_skills",
     "Did not adopt: lack of relevant expertise."),
    ("ai_bar_data", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_BDDT", "nace_r2": "C10-S951_X_K"}, "barrier_data",
     "Did not adopt: data availability or quality."),
    ("ai_bar_legal", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_BLEG", "nace_r2": "C10-S951_X_K"}, "barrier_legal",
     "Did not adopt: lack of clarity about legal consequences."),
    ("ai_bias_check", "isoc_eb_ai",
     {"unit": "PC_ENT", "indic_is": "E_AI_BIAS", "nace_r2": "C10-S951_X_K"}, "bias_checks",
     "Has measures to check AI results for bias towards individuals."),
    ("cloud", "isoc_cicce_use",
     {"unit": "PC_ENT", "indic_is": "E_CC", "nace_r2": "C10-S951_X_K"}, "cloud_use",
     "Enterprises buying cloud computing services."),
    ("ict_specialists", "isoc_ske_itspen",
     {"unit": "PC_ENT", "indic_is": "E_ITSPS", "nace_r2": "C10-S951_X_K"}, "ict_specialists",
     "Enterprises employing ICT specialists."),
    ("rd_exp", "rd_e_gerdtot",
     {"unit": "PC_GDP", "sectperf": "TOTAL"}, "rd_pct_gdp",
     "Gross domestic expenditure on R&D, % of GDP."),
]

# Angle D is not Eurostat — Comtrade. Declared here for documentation and fixtures.
ANGLE_D = [
    ("trade_imports", "COMTRADE",
     {"flow": "M", "hs": list(HS_LINES), "partners": PARTNERS}, "import_value_eur",
     "Imports by HS line and partner. MIRROR STATISTICS DISAGREE; re-exports through "
     "NL/BE/IE distort apparent bilateral flows. HS revised 2012/2017/2022."),
    ("trade_exports", "COMTRADE",
     {"flow": "X", "hs": list(HS_LINES), "partners": PARTNERS}, "export_value_eur",
     "Exports by HS line and partner."),
]

# Angle E is a document corpus, not a table.
ANGLE_E = [
    ("cb_statements", "ECB",
     {"kinds": ["press_release", "speech", "monetary_decision"]}, "text",
     "Central bank communications. CORPUS COMPOSITION DRIVES RAW COUNTS: if more "
     "documents are published, term frequency rises without any change in attention. "
     "Normalise, and say how."),
]

ANGLES = {
    "core": CORE, "a": ANGLE_A, "b": ANGLE_B,
    "c": ANGLE_C, "d": ANGLE_D, "e": ANGLE_E,
}

ANGLE_TITLE = {
    "core": "Shared core (every group joins to this)",
    "a": "A — Compute, energy and the physical constraint",
    "b": "B — Work, skills and the social contract",
    "c": "C — AI adoption and the productivity question",
    "d": "D — Trade, inputs and dependence",
    "e": "E — Institutional language and policy attention",
}

# Structural breaks every group must know about, whatever their angle.
BREAKS = [
    (2020, 2021, "COVID-19", "employment, energy demand, mobility — every angle"),
    (2021, None, "Eurostat AI module begins", "angle C has no observations before 2021"),
    (2022, None, "European energy price shock", "angle A; dominates any model that ignores it"),
    (2020, None, "UK leaves EU reporting frameworks", "coverage discontinuity, all angles"),
    (2012, 2022, "HS classification revisions", "angle D; concordances are imperfect"),
]
