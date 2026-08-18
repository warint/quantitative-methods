"""
MATH60033A — generate the teaching fixtures for the data spine.

    python scripts/build_spine/make_fixtures.py

Writes ten parquet files (one per group) plus the shared core to data/spine/.

WHY FIXTURES EXIST
------------------
The real spine is built by `build.py` from Eurostat, Comtrade and the ECB, and must be
run somewhere with network access to those hosts. These fixtures are the same schema,
the same country and year coverage, the same flags and the same missingness patterns —
generated from a known latent structure so that the pipeline, the labs and the
solutions can be tested before, or instead of, the real download.

They are NOT real data and every file says so in its own provenance row.

WHAT IS DELIBERATELY BUILT IN
-----------------------------
The fixtures are engineered so that each session's lesson actually lands:

  S02  composition effects are real — outcomes genuinely depend on structure, so
       partialling out with FWL changes the answer
  S03  heteroskedasticity (variance scales with country size), within-country
       correlation, and an omittable confounder with a signable bias
  S04  temporal dependence, so random K-fold is genuinely wrong
  S05  many correlated predictors over few true signals, so the lasso is unstable
       across bootstrap replicates and the elastic net behaves differently
  S06  a rare 'falling behind' event (~7%) with real but imperfect signal
  S08  a genuine 3-factor low-rank structure underlying the observed series
  S09  four country types that actually exist in the generating process
  S10  a treatment assigned on covariates, with a known true effect to recover
  S11  a distribution shift after 2021

The latent factors, cluster labels and true treatment effect are NOT written to the
files. They are recorded in scripts/build_spine/.truth/ for the instructor only.
"""

import json
import os

import numpy as np
import pandas as pd

import spec

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "data", "spine"))
TRUTH = os.path.join(HERE, ".truth")
SEED = 60033

GEO, YEARS = spec.GEO, spec.YEARS
NG, NT = len(GEO), len(YEARS)
rng = np.random.default_rng(SEED)

# ── ground truth, written only to .truth/ ────────────────────────────────────
TRUE = {"seed": SEED, "n_geo": NG, "n_years": NT}


# ═════════════════════════════════════════════════════════════════ latent layer
def latent():
    """Four country types, three latent factors, common shocks, country trends."""
    # 4 types with distinct factor means: advanced-north, continental, southern, eastern
    types = rng.choice([0, 1, 2, 3], size=NG, p=[0.25, 0.30, 0.20, 0.25])
    type_mu = np.array([[1.6, 1.2, 1.4],      # advanced-north
                        [0.7, -0.4, 0.5],     # continental
                        [-0.6, -0.9, -0.4],   # southern
                        [-1.3, 0.2, -1.1]])   # eastern

    # F1 development · F2 energy position · F3 institutional capacity
    F0 = type_mu[types] + rng.normal(0, 0.28, (NG, 3))

    # slow country-specific drift, plus persistence over time
    drift = rng.normal(0.02, 0.03, (NG, 3))
    F = np.zeros((NG, NT, 3))
    F[:, 0, :] = F0
    for t in range(1, NT):
        F[:, t, :] = 0.92 * F[:, t - 1, :] + drift + rng.normal(0, 0.12, (NG, 3))

    # common shocks
    covid = np.array([1.0 if y in (2020, 2021) else 0.0 for y in YEARS])
    energy = np.array([1.0 if y >= 2022 else 0.0 for y in YEARS])
    post21 = np.array([1.0 if y >= 2021 else 0.0 for y in YEARS])   # the S11 shift

    TRUE["country_type"] = {g: int(t) for g, t in zip(GEO, types)}
    TRUE["type_labels"] = ["advanced-north", "continental", "southern", "eastern"]
    return F, types, covid, energy, post21


F, TYPES, COVID, ENERGY, POST21 = latent()
SIZE = np.exp(rng.normal(0, 0.9, NG))          # country size, drives heteroskedasticity
SIZE = SIZE / SIZE.mean()


def grid(**cols):
    """Long geo × time frame with any extra key columns."""
    base = pd.MultiIndex.from_product([GEO, YEARS], names=["geo", "time"]).to_frame(index=False)
    for k, v in cols.items():
        base = base.merge(pd.DataFrame({k: v}), how="cross")
    return base


def gi(df):
    return df["geo"].map({g: i for i, g in enumerate(GEO)}).to_numpy()


def ti(df):
    return df["time"].map({y: i for i, y in enumerate(YEARS)}).to_numpy()


def add_missing(df, cols, rate=0.04, small_bias=True, flag_rate=0.06):
    """MAR missingness, heavier in small countries — dropping it biases coverage."""
    g = gi(df)
    p = rate * (2.2 - np.clip(SIZE[g], 0, 2.0)) if small_bias else np.full(len(df), rate)
    for c in cols:
        m = rng.random(len(df)) < p
        df.loc[m, c] = np.nan
    fl = rng.random(len(df)) < flag_rate
    df["flag"] = np.where(fl, rng.choice(["u", "c", "b", "p"], len(df), p=[.55, .15, .1, .2]), "")
    df.loc[df["flag"] == "c", cols] = np.nan          # confidential really is missing
    return df


def rnd(df, cols, nd=3):
    for c in cols:
        df[c] = df[c].astype(float).round(nd)
    return df


# ═════════════════════════════════════════════════════════════════════════ core
def build_core():
    d = grid()
    g, t = gi(d), ti(d)
    f1, _f2, f3 = F[g, t, 0], F[g, t, 1], F[g, t, 2]

    d["gdp_pc_eur"] = np.exp(10.05 + 0.52 * f1 + 0.07 * f3
                             - 0.11 * COVID[t] + rng.normal(0, 0.07, len(d)))
    d["population"] = (SIZE[g] * 9.4e6 * np.exp(rng.normal(0, 0.06, len(d)))).round()
    d["employment_ths"] = (d["population"] / 1000 * (0.44 + 0.03 * f1
                           - 0.02 * COVID[t]) * np.exp(rng.normal(0, 0.03, len(d))))
    d["productivity_idx"] = (100 + 9.5 * f1 + 2.1 * f3 - 4.2 * COVID[t]
                             + 1.15 * (d["time"] - 2015) + rng.normal(0, 2.4, len(d)))
    d["gfcf_meur"] = d["gdp_pc_eur"] * d["population"] / 1e6 * (0.205 + 0.012 * f1) / 1e3

    # the S06 label: bottom-decile productivity growth, one period ahead
    d = d.sort_values(["geo", "time"])
    d["prod_growth"] = d.groupby("geo")["productivity_idx"].pct_change() * 100
    thr = d.groupby("time")["prod_growth"].transform(lambda s: s.quantile(0.10))
    d["falling_behind"] = (d["prod_growth"] < thr).astype("Int64")
    d["falling_behind_next"] = d.groupby("geo")["falling_behind"].shift(-1)

    cols = ["gdp_pc_eur", "population", "employment_ths", "productivity_idx",
            "gfcf_meur", "prod_growth"]
    d = rnd(add_missing(d, cols, rate=0.02, flag_rate=0.04), cols)
    TRUE["falling_behind_rate"] = float(d["falling_behind"].mean())
    return d


# ══════════════════════════════════════════════════════════════════ angle A (2)
def build_angle_a():
    # A1 — country × time
    d = grid()
    g, t = gi(d), ti(d)
    f1, f2 = F[g, t, 0], F[g, t, 1]

    # generation mix: a composition variable that genuinely drives price (S02)
    raw = np.column_stack([1.1 + 0.85 * f2, 1.0 - 0.55 * f2, 0.55 + 0.30 * f1]) \
        + rng.normal(0, 0.22, (len(d), 3))
    mix = np.exp(raw); mix = mix / mix.sum(1, keepdims=True)
    d["share_renew"], d["share_fossil"], d["share_nuclear"] = mix[:, 0], mix[:, 1], mix[:, 2]

    d["elec_price_eur_kwh"] = (0.083 + 0.052 * d["share_fossil"] - 0.021 * d["share_nuclear"]
                               - 0.014 * f1 + 0.061 * ENERGY[t] * (0.5 + d["share_fossil"])
                               + rng.normal(0, 0.006, len(d)))
    d["elec_price_incl_tax"] = d["elec_price_eur_kwh"] * (1.34 + 0.16 * f3_of(g, t)) \
        + rng.normal(0, 0.004, len(d))
    d["energy_intensity"] = 128 - 27 * f1 + 11 * ENERGY[t] + rng.normal(0, 9, len(d))
    d["elec_industry_gwh"] = SIZE[g] * (31500 + 4200 * f1) * (1 - 0.05 * ENERGY[t]) \
        * np.exp(rng.normal(0, 0.09, len(d)))
    d["elec_services_gwh"] = SIZE[g] * (17800 + 6100 * f1) \
        * np.exp(0.035 * (d["time"] - 2010) + rng.normal(0, 0.10, len(d)))

    cols = ["share_renew", "share_fossil", "share_nuclear", "elec_price_eur_kwh",
            "elec_price_incl_tax", "energy_intensity", "elec_industry_gwh", "elec_services_gwh"]
    a1 = rnd(add_missing(d, cols), cols, 4)

    # A2 — country × sector × time
    s = grid(nace_r2=spec.NACE)
    g2, t2 = gi(s), ti(s)
    sec = s["nace_r2"].map({n: i for i, n in enumerate(spec.NACE)}).to_numpy()
    intensity = np.array([2.6, 0.7, 0.5, 1.4, 0.9, 0.2, 0.3])[sec]     # sector energy intensity
    s["elec_use_gwh"] = SIZE[g2] * 4300 * intensity \
        * (1 + 0.14 * F[g2, t2, 0]) * np.exp(rng.normal(0, 0.14, len(s)))
    s["energy_cost_share"] = (0.021 * intensity * (1 + 0.55 * ENERGY[t2])
                              - 0.004 * F[g2, t2, 1] + rng.normal(0, 0.004, len(s))).clip(0.001)
    s["gva_meur"] = SIZE[g2] * 8600 * np.exp(0.28 * F[g2, t2, 0] + rng.normal(0, 0.15, len(s)))
    cols = ["elec_use_gwh", "energy_cost_share", "gva_meur"]
    a2 = rnd(add_missing(s, cols), cols, 4)
    return a1, a2


def f3_of(g, t):
    return F[g, t, 2]


# ══════════════════════════════════════════════════════════════════ angle B (2)
def build_angle_b():
    # B1 — occupation × country × time, with a task-exposure index
    d = grid(isco08=spec.ISCO)
    g, t = gi(d), ti(d)
    occ = d["isco08"].map({o: i for i, o in enumerate(spec.ISCO)}).to_numpy()

    # exposure is a property of the occupation, with small country variation
    base_exp = np.array([0.31, 0.44, 0.52, 0.71, 0.38, 0.46, 0.58, 0.29])[occ]
    d["exposure_index"] = (base_exp + 0.03 * F[g, t, 2] + rng.normal(0, 0.035, len(d))).clip(0, 1)
    d["routine_share"] = (base_exp * 0.85 + rng.normal(0, 0.05, len(d))).clip(0, 1)
    d["ict_task_share"] = (0.62 - 0.55 * base_exp + 0.05 * F[g, t, 0]
                           + rng.normal(0, 0.05, len(d))).clip(0, 1)

    share0 = np.array([0.07, 0.19, 0.16, 0.11, 0.17, 0.12, 0.08, 0.10])[occ]
    trend = -0.010 * (base_exp - 0.45) * (d["time"] - 2010)
    d["employment_ths"] = (SIZE[g] * 19500 * share0 * (1 + trend)
                           * (1 - 0.04 * COVID[t]) * np.exp(rng.normal(0, 0.08, len(d))))
    d["mean_wage_eur"] = (21000 + 26000 * (1 - base_exp) + 7400 * F[g, t, 0]
                          + rng.normal(0, 2100, len(d)))
    cols = ["exposure_index", "routine_share", "ict_task_share",
            "employment_ths", "mean_wage_eur"]
    b1 = rnd(add_missing(d, cols, rate=0.05, flag_rate=0.11), cols)   # survey: more flags

    # B2 — sector × country × time
    s = grid(nace_r2=spec.NACE)
    g2, t2 = gi(s), ti(s)
    sec = s["nace_r2"].map({n: i for i, n in enumerate(spec.NACE)}).to_numpy()
    skill = np.array([0.42, 0.31, 0.35, 0.33, 0.78, 0.71, 0.74])[sec]
    s["employment_ths"] = SIZE[g2] * 1350 * np.exp(0.18 * F[g2, t2, 0]
                                                   + rng.normal(0, 0.13, len(s)))
    s["annual_earnings_eur"] = (23500 + 27500 * skill + 8200 * F[g2, t2, 0]
                                + 480 * (s["time"] - 2010) + rng.normal(0, 2400, len(s)))
    s["vacancy_rate"] = (1.5 + 2.1 * skill + 0.34 * F[g2, t2, 0] - 0.9 * COVID[t2]
                         + rng.normal(0, 0.36, len(s))).clip(0.05)
    s["tertiary_share"] = (0.20 + 0.52 * skill + 0.06 * F[g2, t2, 0]
                           + rng.normal(0, 0.05, len(s))).clip(0, 1)
    cols = ["employment_ths", "annual_earnings_eur", "vacancy_rate", "tertiary_share"]
    b2 = rnd(add_missing(s, cols, rate=0.05, flag_rate=0.09), cols)
    return b1, b2


# ══════════════════════════════════════════════════════════════════ angle C (2)
def build_angle_c():
    """The wide, correlated, short-panel angle. Carries the S05 and S10 lessons."""
    # The digital indicators run from 2014; the AI module only from 2021. Both live in
    # the same file, so the ragged panel is visible rather than being the whole file —
    # which is exactly what the real Eurostat data looks like.
    years_c = [y for y in YEARS if y >= 2014]
    AI_FIRST = 2021
    d = pd.MultiIndex.from_product([GEO, years_c], names=["geo", "time"]).to_frame(index=False)
    g, t = gi(d), ti(d)
    f1, f3 = F[g, t, 0], F[g, t, 2]

    # S10 treatment: national AI strategy, assigned on covariates (confounded)
    ps = 1 / (1 + np.exp(-(0.9 * F[:, 0, 0] + 0.7 * F[:, 0, 2] - 0.2)))
    treated = rng.random(NG) < ps
    strat_year = np.where(treated, rng.choice([2021, 2022, 2023], NG), 9999)
    TRUE["ai_strategy_treated"] = {GEO[i]: bool(treated[i]) for i in range(NG)}
    TRUE["ai_strategy_true_effect_pp"] = 2.4
    d["has_ai_strategy"] = (d["time"].to_numpy() >= strat_year[g]).astype(int)

    # Two latents, and the distinction matters for Session 10.
    #   lat_pre  — digital infrastructure. Depends on country characteristics ONLY.
    #              These are legitimate PRE-TREATMENT controls.
    #   lat_ai   — AI adoption. Depends on the same characteristics PLUS the treatment.
    # Keeping the treatment out of the infrastructure columns is what makes them valid
    # controls; if it leaked in, conditioning on them would block the causal path and
    # DML would under-recover the effect (the classic bad-control problem).
    lat_pre = 0.95 * f1 + 0.45 * f3
    lat_ai = lat_pre + 2.4 / 4.1 * d["has_ai_strategy"].to_numpy()

    pre_cols = {"cloud_use": (34.0, 0.71), "ict_specialists": (19.0, 0.66),
                "digital_intensity": (41.0, 0.83)}
    ai_cols = {"ai_use_any": (7.9, 1.00), "ai_use_ml": (5.1, 0.92), "ai_use_ge3": (3.2, 0.88),
               "ai_text_mining": (3.4, 0.79), "ai_image_reco": (2.9, 0.74)}
    for col, (base, w) in pre_cols.items():
        d[col] = (base + base * 0.52 * w * lat_pre + rng.normal(0, base * 0.13, len(d))).clip(0.1)
    for col, (base, w) in ai_cols.items():
        d[col] = (base + base * 0.52 * w * lat_ai + rng.normal(0, base * 0.13, len(d))).clip(0.1)

    # barriers: negatively related, plus their own factor
    barf = -0.55 * lat_ai + rng.normal(0, 0.45, len(d))
    for col, base in [("barrier_cost", 32.0), ("barrier_skills", 38.0),
                      ("barrier_data", 21.0), ("barrier_legal", 18.0)]:
        d[col] = (base + base * 0.28 * barf + rng.normal(0, base * 0.15, len(d))).clip(0.5)

    d["bias_checks"] = (11.0 + 5.5 * lat_ai + rng.normal(0, 2.6, len(d))).clip(0.1)
    d["rd_pct_gdp"] = (0.95 + 0.62 * f1 + 0.11 * f3 + rng.normal(0, 0.16, len(d))).clip(0.05)
    # 15 pure-noise columns, so variable selection has something to get wrong
    for k in range(15):
        d[f"aux_{k:02d}"] = rng.normal(0, 1, len(d)) + 0.25 * lat_pre * (k % 3 == 0)

    # The AI module did not exist before 2021 — those cells are structurally absent,
    # not missing at random. Students must notice the difference.
    pre = (d["time"] < AI_FIRST).to_numpy()
    for col in ["ai_use_any", "ai_use_ml", "ai_use_ge3", "ai_text_mining", "ai_image_reco",
                "bias_checks", "barrier_cost", "barrier_skills", "barrier_data",
                "barrier_legal"]:
        d.loc[pre, col] = np.nan

    cols = [c for c in d.columns if c not in ("geo", "time", "has_ai_strategy")]
    c1 = rnd(add_missing(d, cols, rate=0.04, flag_rate=0.14), cols)

    # C2 — country × sector × size class
    s = pd.MultiIndex.from_product([GEO, [y for y in years_c if y >= AI_FIRST], spec.NACE, spec.SIZE_CLASS],
                                   names=["geo", "time", "nace_r2", "size_emp"]).to_frame(index=False)
    g2, t2 = gi(s), ti(s)
    sec = s["nace_r2"].map({n: i for i, n in enumerate(spec.NACE)}).to_numpy()
    sz = s["size_emp"].map({"10-49": 0, "50-249": 1, "GE250": 2}).to_numpy()
    sec_eff = np.array([0.1, -0.5, -0.2, -0.1, 1.5, 0.9, 0.7])[sec]     # J and K adopt most
    sz_eff = np.array([-0.6, 0.15, 1.05])[sz]
    lat2 = 0.85 * F[g2, t2, 0] + 0.4 * F[g2, t2, 2] + sec_eff + sz_eff
    s["ai_use_any"] = (7.5 + 4.6 * lat2 + rng.normal(0, 2.3, len(s))).clip(0.1)
    s["ai_use_ml"] = (4.6 + 3.0 * lat2 + rng.normal(0, 1.7, len(s))).clip(0.1)
    s["cloud_use"] = (32.0 + 11.5 * lat2 + rng.normal(0, 6.4, len(s))).clip(0.5)
    s["barrier_skills"] = (39.0 - 6.2 * lat2 + rng.normal(0, 6.0, len(s))).clip(0.5)
    s["n_enterprises"] = (SIZE[g2] * np.array([9200, 2100, 380])[sz]
                          * np.exp(rng.normal(0, 0.25, len(s)))).round()
    cols = ["ai_use_any", "ai_use_ml", "cloud_use", "barrier_skills"]
    c2 = rnd(add_missing(s, cols, rate=0.09, flag_rate=0.20), cols)
    return c1, c2


# ══════════════════════════════════════════════════════════════════ angle D (2)
def build_angle_d():
    hs = list(spec.HS_LINES)
    # D1 — reporter × partner × time, aggregated over products
    d = grid(partner=spec.PARTNERS)
    g, t = gi(d), ti(d)
    p = d["partner"].map({q: i for i, q in enumerate(spec.PARTNERS)}).to_numpy()
    base = np.array([0.16, 0.30, 0.09, 0.07, 0.05, 0.26, 0.07])[p]
    # China share trends up, US down; hub countries (NL/BE/IE) inflate everything
    hub = np.isin(d["geo"], ["NL", "BE", "IE"]).astype(float)
    trend = np.where(p == 1, 0.011, np.where(p == 0, -0.006, 0.0)) * (d["time"] - 2010)
    share = (base + trend + 0.02 * rng.normal(0, 1, len(d))).clip(0.005)
    d["import_value_eur"] = (SIZE[g] * (1 + 2.4 * hub) * 2.1e9 * share
                             * np.exp(0.35 * F[g, t, 0] + rng.normal(0, 0.22, len(d))))
    d["export_value_eur"] = (SIZE[g] * (1 + 2.1 * hub) * 1.6e9 * share
                             * np.exp(0.42 * F[g, t, 0] + rng.normal(0, 0.26, len(d))))
    d["is_reexport_hub"] = hub.astype(int)
    cols = ["import_value_eur", "export_value_eur"]
    d1 = rnd(add_missing(d, cols, rate=0.03, flag_rate=0.05), cols, 0)

    # D2 — reporter × product × time
    s = grid(hs=hs)
    g2, t2 = gi(s), ti(s)
    hi = s["hs"].map({h: i for i, h in enumerate(hs)}).to_numpy()
    scale = np.array([0.9, 3.4, 0.6, 2.2, 0.4, 1.8])[hi]
    # NL carries the 8486 (lithography) export line — the ASML fact
    asml = ((s["geo"] == "NL") & (s["hs"] == "8486")).to_numpy().astype(float)
    s["import_value_eur"] = (SIZE[g2] * scale * 4.6e8
                             * np.exp(0.30 * F[g2, t2, 0] + rng.normal(0, 0.28, len(s))))
    s["export_value_eur"] = (SIZE[g2] * scale * 3.9e8 * (1 + 14.0 * asml)
                             * np.exp(0.36 * F[g2, t2, 0] + rng.normal(0, 0.31, len(s))))
    s["top_partner_share"] = (0.34 + 0.16 * rng.normal(0, 1, len(s))).clip(0.05, 0.95)
    s["hs_revision_break"] = np.isin(s["time"], [2012, 2017, 2022]).astype(int)
    cols = ["import_value_eur", "export_value_eur", "top_partner_share"]
    d2 = rnd(add_missing(s, cols, rate=0.05, flag_rate=0.07), cols, 4)
    return d1, d2


# ══════════════════════════════════════════════════════════════════ angle E (2)
UNC = ["uncertain", "uncertainty", "unclear", "risk", "risks", "volatile", "unpredictable",
       "downside", "fragile", "concern", "concerns", "tension"]
CALM = ["stable", "resilient", "orderly", "anchored", "steady", "robust", "confidence",
        "sustained", "balanced", "moderate"]
TOPIC = {"inflation": ["inflation", "prices", "wages", "energy costs", "core inflation"],
         "growth": ["growth", "output", "demand", "investment", "employment"],
         "digital": ["digital", "artificial intelligence", "automation", "technology",
                     "data", "productivity"],
         "finance": ["credit", "banks", "liquidity", "spreads", "funding"]}
FRAME = ["The Governing Council notes that {a} remain {b}.",
         "Developments in {a} are expected to stay {b} over the projection horizon.",
         "Members observed that {a} conditions appear {b} at present.",
         "Assessment of {a} indicates a {b} outlook for the coming quarters.",
         "The outlook for {a} continues to be {b}, warranting close monitoring."]


def _doc(rs, unc_level, topics, n_sent):
    out = []
    for _ in range(n_sent):
        tp = rs.choice(topics)
        a = rs.choice(TOPIC[tp])
        b = rs.choice(UNC) if rs.random() < unc_level else rs.choice(CALM)
        out.append(rs.choice(FRAME).format(a=a, b=b))
    return " ".join(out)


def build_angle_e():
    rs = np.random.default_rng(SEED + 7)
    # a latent monthly uncertainty index the students must recover
    months = pd.date_range("2010-01-01", "2024-12-01", freq="MS")
    x = np.arange(len(months))
    lat = (0.30 + 0.16 * np.sin(x / 11.0)
           + 0.26 * ((months.year >= 2020) & (months.year <= 2021))
           + 0.22 * (months.year >= 2022)
           + rs.normal(0, 0.05, len(months))).clip(0.05, 0.92)
    TRUE["text_latent_uncertainty"] = {str(m.date()): float(v) for m, v in zip(months, lat)}

    # E1 — central bank corpus
    rows = []
    for m, u in zip(months, lat):
        for inst, n_docs in [("ECB", 4), ("BoE", 3), ("BoC", 2)]:
            # corpus composition grows over time — the trap in the mandate brief
            k = n_docs + int(m.year >= 2018) + int(m.year >= 2022)
            for j in range(k):
                txt = _doc(rs, float(u), ["inflation", "growth", "finance", "digital"],
                           rs.integers(14, 30))
                rows.append({"doc_id": f"{inst}-{m.date()}-{j}", "date": m.date(),
                             "institution": inst, "country": {"ECB": "EA", "BoE": "UK",
                                                              "BoC": "CA"}[inst],
                             "doc_type": rs.choice(["press_release", "speech",
                                                    "monetary_decision"]),
                             "n_words": 0, "text": txt})
    e1 = pd.DataFrame(rows)
    e1["n_words"] = e1["text"].str.split().str.len()

    # E2 — national policy / strategy corpus, cross-country
    rows = []
    for g in GEO:
        gidx = GEO.index(g)
        for y in YEARS:
            k = 2 + int(y >= 2019) + int(F[gidx, YEARS.index(y), 2] > 0.5)
            for j in range(k):
                u = float(np.clip(0.30 + 0.20 * (y >= 2020) - 0.10 * F[gidx, YEARS.index(y), 2]
                                  + rs.normal(0, 0.07), 0.05, 0.92))
                txt = _doc(rs, u, ["digital", "growth", "inflation"], rs.integers(18, 36))
                rows.append({"doc_id": f"{g}-{y}-{j}", "date": f"{y}-06-01", "institution": "GOV",
                             "country": g, "doc_type": rs.choice(["strategy", "consultation",
                                                                  "regulation"]),
                             "n_words": 0, "text": txt})
    e2 = pd.DataFrame(rows)
    e2["n_words"] = e2["text"].str.split().str.len()
    return e1, e2


# ═══════════════════════════════════════════════════════════════════════ output
FILES = {
    "core.parquet": ("core", "Shared core — every group joins to this on (geo, time)"),
    "angle_a_country.parquet": ("G01", "A1 · country × time · prices, mix, intensity"),
    "angle_a_sector.parquet": ("G02", "A2 · country × sector × time · industrial energy use"),
    "angle_b_occupation.parquet": ("G03", "B1 · occupation × country × time · task exposure"),
    "angle_b_sector.parquet": ("G04", "B2 · sector × country × time · employment and earnings"),
    "angle_c_country.parquet": ("G05", "C1 · country × time · adoption, barriers (2021–)"),
    "angle_c_sector_size.parquet": ("G06", "C2 · country × sector × size class (2021–)"),
    "angle_d_partner.parquet": ("G07", "D1 · reporter × partner × time · bilateral flows"),
    "angle_d_product.parquet": ("G08", "D2 · reporter × product × time · HS lines"),
    "angle_e_centralbank.parquet": ("G09", "E1 · central bank corpus, monthly 2010–2024"),
    "angle_e_national.parquet": ("G10", "E2 · national policy corpus, cross-country"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TRUTH, exist_ok=True)

    core = build_core()
    a1, a2 = build_angle_a()
    b1, b2 = build_angle_b()
    c1, c2 = build_angle_c()
    d1, d2 = build_angle_d()
    e1, e2 = build_angle_e()

    frames = dict(zip(FILES, [core, a1, a2, b1, b2, c1, c2, d1, d2, e1, e2]))

    print("=" * 74)
    print("  MATH60033A — teaching fixtures")
    print("=" * 74)
    rows = []
    for name, df in frames.items():
        grp, desc = FILES[name]
        df.attrs["fixture"] = True
        df.to_parquet(os.path.join(OUT, name), index=False)
        miss = float(df.isna().mean().mean()) * 100
        print(f"  {grp:<5s} {name:<32s} {len(df):>7,d} rows × {df.shape[1]:>2d} cols "
              f"· {miss:4.1f}% missing")
        rows.append({"file": name, "group": grp, "description": desc,
                     "rows": len(df), "cols": df.shape[1],
                     "missing_pct": round(miss, 2),
                     "keys": ", ".join([c for c in ("geo", "time", "nace_r2", "isco08",
                                                    "size_emp", "partner", "hs", "doc_id")
                                        if c in df.columns])})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "MANIFEST.csv"), index=False)

    with open(os.path.join(TRUTH, "ground_truth.json"), "w", encoding="utf-8") as f:
        json.dump(TRUE, f, indent=2, default=str)

    print()
    print(f"  wrote {len(frames)} files + MANIFEST.csv to data/spine/")
    print("  ground truth (INSTRUCTOR ONLY) -> scripts/build_spine/.truth/ground_truth.json")
    print(f"  falling-behind base rate: {TRUE['falling_behind_rate']:.1%}")
    print(f"  true AI-strategy effect:  +{TRUE['ai_strategy_true_effect_pp']} pp "
          f"({sum(TRUE['ai_strategy_treated'].values())}/{NG} treated, confounded)")
    print("=" * 74)


if __name__ == "__main__":
    main()
