#!/usr/bin/env python3
"""
Build the Session 05 dataset: 56 candidate determinants of bilateral FDI.

    python scripts/build_fdi_determinants.py

Why this exists
---------------
Session 05 reads Blonigen & Piger (2014), "Determinants of foreign direct
investment", Canadian Journal of Economics 47(3), 775-812. The paper collects
56 candidate covariates for bilateral FDI, runs Bayesian model averaging over
them, and reports that only about sixteen carry any weight: the gravity
variables, cultural distance, parent income, a few trade-agreement dummies and
host skill. Host business costs, communications infrastructure, financial depth
and host institutions -- the variables a great many published FDI papers lean
on -- do not survive.

That is the session's question in one sentence: of many indicators, which few
actually carry the signal? The practice puts the lasso, ridge and the elastic
net on the same question and asks whether penalisation keeps the paper's short
list.

The authors published no replication package -- the paper says only that "a
full list of data sources is available from the authors upon request" -- so
this script rebuilds their design from the three sources they name (page 792:
"the Penn World Tables, the World Development Indicators database and the
Gravity database at CEPII"), plus the OECD for the dependent variable. Every
number below is real. Nothing here is simulated.

What it produces
----------------
data/spine/fdi_determinants.parquet -- one row per parent-host country pair,
2019, with the FDI position and 56 candidate covariates. Small enough to
commit, so the practice runs with the wifi off.

Sources, all free and public
----------------------------
OECD    Bilateral FDI positions, BMD4, outward directional principle, all
        resident units, immediate counterpart, USD.
        sdmx.oecd.org -- dataflow DSD_FDI@DF_FDI_POS_CTRY.
CEPII   Gravity database V202211 (Conte, Cotterlaz & Mayer). Distance,
        contiguity, language, colonial history, trade agreements, GDP.
        cepii.fr -- 207 MB zip, sliced to one year here.
WDI     World Development Indicators, World Bank API, 2019.
FH      Freedom House, Freedom in the World, 2020 edition (2019 coverage).
        Supplies the paper's political rights and civil liberties variables
        at their original 1-7 definition.

Where this departs from the paper, and why
------------------------------------------
The paper uses year 2000. This script uses 2019. The 2000 bilateral FDI stocks
came from SourceOECD, which was retired; the current OECD API serves the
counterpart-area series only from the mid-2000s. Using 2019 makes the exercise
a genuine question rather than an arithmetic check: do the determinants that
held for 2000 still hold two decades on?

Four of the paper's covariates (41-44: time to enforce a contract, register
property, start a business, resolve insolvency) came from Doing Business, which
the World Bank discontinued in 2021 and withdrew from the WDI API. They are
replaced by four host-country cost-and-capacity measures that are still
published -- new business density, logistics performance, unemployment and
secondary enrolment. The substitution is named in the data dictionary.

Two more (47-48: bilateral investment treaty, double taxation treaty) have no
free machine-readable source. They are replaced by shared WTO membership and
shared EU membership, which are bilateral policy dummies of the same kind.

Capital per worker (24-26) is built from gross fixed capital formation and the
labour force rather than from the Penn World Table capital stock, so it is a
flow per worker, not a stock per worker. It is named accordingly.

The count is held at 56 so the comparison with the paper's table 3 stays
one-to-one. Six substitutions are flagged in the dictionary and in the
pre-session deck; students are expected to say what the substitution costs
them, which is part of the point.
"""

from __future__ import annotations

import io
import pathlib
import sys
import time
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPINE = ROOT / "data" / "spine"
CACHE = ROOT / "data" / "build-cache"

GRAVITY_URL = "https://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip"
FH_URL = "https://freedomhouse.org/sites/default/files/2024-02/All_data_FIW_2013-2024.xlsx"
OECD_URL = (
    "https://sdmx.oecd.org/public/rest/data/OECD.DAF.INV,DSD_FDI@DF_FDI_POS_CTRY,/all"
    "?startPeriod=2019&endPeriod=2019&format=csvfilewithlabels"
)
YEAR = 2019

# World Development Indicators. The year is carried per indicator because the
# logistics index is published only in survey years.
WDI = {
    "urban": ("SP.URB.TOTL.IN.ZS", 2019),
    "tert": ("SE.TER.ENRR", 2019),
    "advedu": ("SL.TLF.ADVN.ZS", 2019),
    "sec": ("SE.SEC.ENRR", 2019),
    "popdens": ("EN.POP.DNST", 2019),
    "land": ("AG.LND.TOTL.K2", 2019),
    "open": ("NE.TRD.GNFS.ZS", 2019),
    "rents": ("NY.GDP.TOTL.RT.ZS", 2019),
    "fuelx": ("TX.VAL.FUEL.ZS.UN", 2019),
    "mobile": ("IT.CEL.SETS.P2", 2019),
    "fixed": ("IT.MLT.MAIN.P2", 2019),
    "internet": ("IT.NET.USER.ZS", 2019),
    "credit": ("FS.AST.PRVT.GD.ZS", 2019),
    "mktcap": ("CM.MKT.LCAP.GD.ZS", 2019),
    "tax": ("GC.TAX.TOTL.GD.ZS", 2019),
    "newbiz": ("IC.BUS.NDNS.ZS", 2019),
    "lpi": ("LP.LPI.OVRL.XQ", 2018),
    "unemp": ("SL.UEM.TOTL.ZS", 2019),
    "hitech": ("TX.VAL.TECH.MF.ZS", 2019),
    "gcf": ("NE.GDI.FTOT.ZS", 2019),
    "labor": ("SL.TLF.TOTL.IN", 2019),
    "gdp": ("NY.GDP.MKTP.KD", 2019),
}

# OECD's own list of jurisdictions historically identified as tax havens, as
# used in the paper's variable 46.
TAX_HAVENS = {
    "AND", "AIA", "ATG", "ABW", "BHS", "BHR", "BRB", "BLZ", "BMU", "VGB",
    "CYM", "COK", "CYP", "DMA", "GIB", "GRD", "GGY", "IMN", "JEY", "LBR",
    "LIE", "MAC", "MDV", "MHL", "MCO", "MSR", "NRU", "ANT", "NIU", "PAN",
    "KNA", "LCA", "VCT", "WSM", "SMR", "SYC", "TCA", "VUT", "MLT", "MUS",
}


def _say(msg: str) -> None:
    print(msg, flush=True)


def _requests():
    try:
        import requests
    except ImportError:
        sys.exit("requests is missing. pip install -r requirements.txt")
    return requests


def fetch_gravity(pd):
    """CEPII gravity, sliced to YEAR. The zip is 207 MB; the slice is a few MB."""
    slim = CACHE / f"gravity_{YEAR}.parquet"
    if slim.exists():
        return pd.read_parquet(slim)

    raw = CACHE / "Gravity_csv_V202211.zip"
    if not raw.exists():
        _say(f"  downloading CEPII gravity ({GRAVITY_URL}) -- 207 MB, once")
        requests = _requests()
        with requests.get(GRAVITY_URL, stream=True, timeout=1800) as r:
            r.raise_for_status()
            with open(raw, "wb") as fh:
                for chunk in r.iter_content(1 << 20):
                    fh.write(chunk)

    keep = [
        "year", "iso3_o", "iso3_d", "dist", "contig", "comlang_off", "comlang_ethno",
        "col_dep_ever", "col45", "gdp_o", "gdp_d", "gdpcap_o", "gdpcap_d",
        "pop_o", "pop_d", "gmt_offset_2020_o", "gmt_offset_2020_d",
        "fta_wto", "rta_coverage", "rta_type", "wto_o", "wto_d", "eu_o", "eu_d",
    ]
    _say("  slicing gravity to one year")
    with zipfile.ZipFile(raw) as z:
        name = next(n for n in z.namelist() if n.endswith("Gravity_V202211.csv"))
        chunks = []
        with z.open(name) as fh:
            for part in pd.read_csv(fh, usecols=keep, chunksize=500_000, low_memory=False):
                chunks.append(part[part.year == YEAR])
    g = pd.concat(chunks, ignore_index=True)
    slim.parent.mkdir(parents=True, exist_ok=True)
    g.to_parquet(slim)
    return g


def fetch_fdi(pd):
    """OECD bilateral FDI positions: parent's outward position in each host."""
    slim = CACHE / f"fdi_{YEAR}.parquet"
    if slim.exists():
        return pd.read_parquet(slim)

    _say("  downloading OECD FDI positions -- large, once")
    requests = _requests()
    r = requests.get(OECD_URL, timeout=900)
    r.raise_for_status()
    cols = [
        "REF_AREA", "MEASURE", "UNIT_MEASURE", "MEASURE_PRINCIPLE", "ACCOUNTING_ENTRY",
        "TYPE_ENTITY", "COUNTERPART_AREA", "LEVEL_COUNTERPART", "OBS_VALUE", "UNIT_MULT",
    ]
    df = pd.read_csv(io.BytesIO(r.content), usecols=cols, low_memory=False)

    # Total FDI position, in USD, outward (so REF_AREA is the parent), net,
    # all resident units, immediate counterpart. Anything else double-counts
    # or measures something different.
    q = df.query(
        "MEASURE == 'LE_FA_F' and UNIT_MEASURE == 'USD_EXC' "
        "and MEASURE_PRINCIPLE == 'DO' and ACCOUNTING_ENTRY == 'NET_FDI' "
        "and TYPE_ENTITY == 'ALL' and LEVEL_COUNTERPART == 'IMC'"
    ).copy()
    q["fdi_stock_musd"] = q.OBS_VALUE * (10 ** q.UNIT_MULT) / 1e6
    q = (
        q.loc[q.REF_AREA != q.COUNTERPART_AREA, ["REF_AREA", "COUNTERPART_AREA", "fdi_stock_musd"]]
        .rename(columns={"REF_AREA": "parent", "COUNTERPART_AREA": "host"})
        .dropna(subset=["fdi_stock_musd"])
        .groupby(["parent", "host"], as_index=False)
        .fdi_stock_musd.mean()
    )
    slim.parent.mkdir(parents=True, exist_ok=True)
    q.to_parquet(slim)
    return q


def fetch_wdi(pd):
    """World Development Indicators, one call per series."""
    slim = CACHE / f"wdi_{YEAR}.parquet"
    if slim.exists():
        return pd.read_parquet(slim)

    requests = _requests()
    out = {}
    for key, (code, year) in WDI.items():
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}"
        js = requests.get(
            url, params={"date": str(year), "format": "json", "per_page": 400}, timeout=90
        ).json()
        rows = js[1] if len(js) > 1 and js[1] else []
        out[key] = {
            x["countryiso3code"]: x["value"]
            for x in rows
            if x.get("countryiso3code") and x["value"] is not None
        }
        _say(f"    {key:9s} {code:22s} n={len(out[key])}")
        time.sleep(0.15)
    wdi = pd.DataFrame(out)
    wdi.index.name = "iso3"
    wdi = wdi[wdi.index.str.len() == 3]
    slim.parent.mkdir(parents=True, exist_ok=True)
    wdi.to_parquet(slim)
    return wdi


def fetch_freedom_house(pd, countries):
    """Freedom House political rights and civil liberties, 1 (most free) to 7."""
    slim = CACHE / f"fh_{YEAR}.parquet"
    if slim.exists():
        return pd.read_parquet(slim)

    requests = _requests()
    r = requests.get(FH_URL, timeout=180)
    r.raise_for_status()
    fh = pd.read_excel(io.BytesIO(r.content), sheet_name="FIW13-24", skiprows=1)
    fh = fh[(fh["Edition"] == YEAR + 1) & (fh["C/T"] == "c")]
    fh = fh[["Country/Territory", "PR rating", "CL rating"]].rename(
        columns={"Country/Territory": "name", "PR rating": "polrights", "CL rating": "civlib"}
    )

    # Freedom House names to ISO3, via the CEPII country table plus the
    # handful of names the two sources spell differently.
    lookup = {n.lower(): i for n, i in zip(countries["country"], countries["iso3"])}
    manual = {
        "south korea": "KOR", "north korea": "PRK", "russia": "RUS", "syria": "SYR",
        "iran": "IRN", "vietnam": "VNM", "laos": "LAO", "tanzania": "TZA",
        "moldova": "MDA", "bolivia": "BOL", "venezuela": "VEN", "brunei": "BRN",
        "cape verde": "CPV", "the gambia": "GMB", "czech republic": "CZE",
        "republic of the congo": "COG", "democratic republic of the congo": "COD",
        "ivory coast": "CIV", "east timor": "TLS", "eswatini": "SWZ",
        "myanmar": "MMR", "taiwan": "TWN", "macedonia": "MKD",
        "north macedonia": "MKD", "slovakia": "SVK", "united states": "USA",
        "united kingdom": "GBR", "st. kitts and nevis": "KNA",
        "st. lucia": "LCA", "st. vincent and the grenadines": "VCT",
        "sao tome and principe": "STP", "micronesia": "FSM",
    }
    lookup.update(manual)
    fh["iso3"] = fh.name.str.strip().str.lower().map(lookup)
    fh = fh.dropna(subset=["iso3"]).set_index("iso3")[["polrights", "civlib"]]
    fh = fh[~fh.index.duplicated()]
    slim.parent.mkdir(parents=True, exist_ok=True)
    fh.to_parquet(slim)
    return fh


def build():
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        sys.exit("pandas and numpy are missing. pip install -r requirements.txt")

    CACHE.mkdir(parents=True, exist_ok=True)

    _say("CEPII gravity")
    g = fetch_gravity(pd)
    _say("OECD FDI positions")
    fdi = fetch_fdi(pd)
    _say("World Development Indicators")
    wdi = fetch_wdi(pd)

    requests = _requests()
    with zipfile.ZipFile(CACHE / "Gravity_csv_V202211.zip") as z:
        name = next(n for n in z.namelist() if n.endswith("Countries_V202211.csv"))
        with z.open(name) as fh_:
            countries = pd.read_csv(fh_)
    _say("Freedom House")
    fh = fetch_freedom_house(pd, countries)

    iso = set(countries.iso3.dropna())
    fdi = fdi[fdi.parent.isin(iso) & fdi.host.isin(iso)]

    df = fdi.merge(g, left_on=["parent", "host"], right_on=["iso3_o", "iso3_d"], how="inner")
    for side, code in (("h", "host"), ("p", "parent")):
        df = df.merge(wdi.add_prefix(f"{side}_"), left_on=code, right_index=True, how="left")
        df = df.merge(fh.add_prefix(f"{side}_"), left_on=code, right_index=True, how="left")

    # ---- the 56 candidates, in the paper's own order and grouping ----------
    out = pd.DataFrame({"parent": df.parent, "host": df.host, "year": YEAR})
    out["fdi_stock_musd"] = df.fdi_stock_musd

    def sqdiff(a, b):
        return (a - b) ** 2

    # Gravity measures (1-3)
    out["parent_gdp"] = df.gdp_o
    out["host_gdp"] = df.gdp_d
    out["distance"] = df.dist

    # Other GDP-related terms (4-11)
    out["parent_gdp_pc"] = df.gdpcap_o
    out["host_gdp_pc"] = df.gdpcap_d
    out["gdp_sum"] = df.gdp_o + df.gdp_d
    out["gdp_similarity"] = (df.gdp_d / (df.gdp_o + df.gdp_d)) * (df.gdp_o / (df.gdp_o + df.gdp_d))
    out["gdp_diff_sq"] = sqdiff(df.gdp_d, df.gdp_o)
    out["gdp_pc_diff_sq"] = sqdiff(df.gdpcap_d, df.gdpcap_o)
    out["host_urban"] = df.h_urban
    out["parent_urban"] = df.p_urban

    # Geography other than distance (12-15)
    out["contiguity"] = df.contig
    # Remoteness: distance to all others, weighted by their share of world GDP.
    gdp_by_iso = wdi.gdp.dropna()
    world = gdp_by_iso.sum()
    dist_all = g[["iso3_o", "iso3_d", "dist"]].dropna()
    dist_all = dist_all[dist_all.iso3_d.isin(gdp_by_iso.index)]
    dist_all["w"] = dist_all.iso3_d.map(gdp_by_iso) / world
    remote = dist_all.groupby("iso3_o").apply(
        lambda t: (t.dist * t.w).sum() / t.w.sum(), include_groups=False
    )
    out["host_remoteness"] = df.host.map(remote)
    out["parent_remoteness"] = df.parent.map(remote)
    out["timezone_diff"] = (df.gmt_offset_2020_d - df.gmt_offset_2020_o).abs()

    # Relative labour endowments (16-23)
    out["host_education"] = df.h_tert
    out["host_skill"] = df.h_advedu
    out["parent_education"] = df.p_tert
    out["parent_skill"] = df.p_advedu
    out["education_diff_sq"] = sqdiff(df.p_tert, df.h_tert)
    out["skill_diff_sq"] = sqdiff(df.p_advedu, df.h_advedu)
    gdp_diff = df.gdp_d - df.gdp_o
    out["gdpdiff_x_edudiff"] = gdp_diff * (df.p_tert - df.h_tert)
    out["gdpdiff_x_skilldiff"] = gdp_diff * (df.p_advedu - df.h_advedu)

    # Other relative endowments (24-30)
    host_kpw = (df.h_gcf / 100) * df.h_gdp / df.h_labor
    parent_kpw = (df.p_gcf / 100) * df.p_gdp / df.p_labor
    out["host_capital_per_worker"] = host_kpw
    out["parent_capital_per_worker"] = parent_kpw
    out["capital_per_worker_diff_sq"] = sqdiff(host_kpw, parent_kpw)
    out["host_land"] = df.h_land
    out["parent_land"] = df.p_land
    out["host_pop_density"] = df.h_popdens
    out["host_is_oil"] = (df.h_fuelx > 30).astype("float")

    # Cultural distance (31-33)
    out["common_language_official"] = df.comlang_off
    out["common_language_overlap"] = df.comlang_ethno
    out["colonial_link"] = df.col_dep_ever

    # Multilateral trade openness (34-37)
    out["host_openness"] = df.h_open
    out["parent_openness"] = df.p_open
    out["edudiff_x_hostopen"] = (df.p_tert - df.h_tert) * df.h_open
    out["skilldiff_x_hostopen"] = (df.p_advedu - df.h_advedu) * df.h_open

    # Bilateral trade openness (38-40)
    out["regional_trade_agreement"] = df.fta_wto
    out["customs_union"] = df.rta_coverage.isin([2, 3]).astype("float")
    out["services_agreement"] = df.rta_type.isin([3, 4]).astype("float")

    # Host business costs (41-44) -- substituted, see the module docstring
    out["host_new_business_density"] = df.h_newbiz
    out["host_logistics"] = df.h_lpi
    out["host_unemployment"] = df.h_unemp
    out["host_secondary_enrolment"] = df.h_sec

    # Host tax policy (45-46)
    out["host_tax_revenue"] = df.h_tax
    out["host_is_tax_haven"] = df.host.isin(TAX_HAVENS).astype("float")

    # Bilateral agreements (47-48) -- substituted
    out["both_wto"] = ((df.wto_o > 0) & (df.wto_d > 0)).astype("float")
    out["both_eu"] = ((df.eu_o > 0) & (df.eu_d > 0)).astype("float")

    # Host communications infrastructure (49-51)
    out["host_mobile"] = df.h_mobile
    out["host_internet"] = df.h_internet
    out["host_fixed_line"] = df.h_fixed

    # Host financial infrastructure (52-53)
    out["host_domestic_credit"] = df.h_credit
    out["host_market_cap"] = df.h_mktcap

    # Political environment and institutions (54-56)
    out["host_hitech_exports"] = df.h_hitech
    out["host_political_rights"] = df.h_polrights
    out["host_civil_liberties"] = df.h_civlib

    covariates = [c for c in out.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
    assert len(covariates) == 56, f"expected 56 covariates, built {len(covariates)}"

    out = out.replace([np.inf, -np.inf], np.nan)
    out = out.sort_values(["parent", "host"]).reset_index(drop=True)

    SPINE.mkdir(parents=True, exist_ok=True)
    target = SPINE / "fdi_determinants.parquet"
    out.to_parquet(target, index=False)

    positive = out[out.fdi_stock_musd > 0]
    complete = positive.dropna(subset=covariates)
    _say("")
    _say(f"wrote {target.relative_to(ROOT)}")
    _say(f"  {len(out):,} country pairs, {len(covariates)} candidate covariates")
    _say(f"  {len(positive):,} with a positive FDI position (the log-levels sample)")
    _say(f"  {len(complete):,} complete cases across all 56")
    _say(f"  parents: {out.parent.nunique()}   hosts: {out.host.nunique()}")
    thin = positive[covariates].notna().mean().sort_values().head(5)
    _say("  thinnest coverage: " + ", ".join(f"{k} {v:.0%}" for k, v in thin.items()))


if __name__ == "__main__":
    build()
