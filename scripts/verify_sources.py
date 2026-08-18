"""
MATH60033A — verify that every public data source in RESEARCH-MANDATES.md is still reachable.

Run at the start of each term, and before rebuilding the data spine:

    python scripts/verify_sources.py

Statistical agencies retire and rename dataset codes without notice. This script tells you
which ones broke before a room full of students finds out for you.

Exit code 0 if every REQUIRED source passes, 1 otherwise.
"""

import json
import sys
import urllib.error
import urllib.request

TIMEOUT = 20
UA = {"User-Agent": "MATH60033A-course-check/1.0 (teaching material verification)"}

EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}"

# (angle, code, human label, required?)
EUROSTAT_CODES = [
    ("core", "nama_10_gdp",       "GDP and main aggregates",                True),
    ("core", "nama_10_lp_ulc",    "Labour productivity and unit labour cost", True),
    ("core", "lfsa_egan22d",      "Employment by sector (NACE)",            True),

    ("A",    "nrg_pc_205",        "Electricity prices, non-household",      True),
    ("A",    "nrg_pc_205_c",      "Electricity price components",           False),
    ("A",    "nrg_bal_c",         "Energy balances",                        True),
    ("A",    "nrg_ind_ei",        "Energy intensity of the economy",        False),

    ("B",    "lfsa_egais",        "Employment by occupation (ISCO-08)",     True),
    ("B",    "lfsa_urgaed",       "Unemployment by education",              False),
    ("B",    "jvs_a_rate_r2",     "Job vacancy rate",                       False),

    ("C",    "isoc_eb_ai",        "AI use by enterprises",                  True),
    ("C",    "isoc_cicce_use",    "Cloud computing services",               True),
    ("C",    "isoc_ske_itspen",   "ICT specialists employed",               False),
    ("C",    "isoc_e_dii",        "Digital intensity index",                False),
    ("C",    "rd_e_gerdtot",      "R&D expenditure",                        True),
]

OTHER_SOURCES = [
    ("D", "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=276&period=2022"
          "&partnerCode=0&cmdCode=8542&flowCode=M",
     "UN Comtrade public preview API", False),
    ("D", "https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37",
     "CEPII BACI landing page", False),
    ("E", "https://www.ecb.europa.eu/press/pr/date/2026/html/index.en.html",
     "ECB press releases index", True),
    ("E", "https://eur-lex.europa.eu/homepage.html",
     "EUR-Lex", True),
    ("E", "https://oecd.ai/en/dashboards/policy-initiatives",
     "OECD.AI policy initiatives", False),
    ("B", "https://www.onetcenter.org/database.html",
     "O*NET database downloads", True),
    ("B", "https://esco.ec.europa.eu/en/use-esco/download",
     "ESCO downloads", False),
    ("A", "https://ember-energy.org/data/",
     "Ember electricity data", False),
]

results = []


def record(angle, label, ok, required, detail=""):
    results.append((angle, label, ok, required, detail))
    mark = "[ok]  " if ok else ("[FAIL]" if required else "[warn]")
    req = "" if required else "  (optional)"
    print(f"{mark} {angle:5s} {label}{req}")
    if detail and not ok:
        print(f"         {detail}")


def check_eurostat(angle, code, label, required):
    """Request a single tiny slice and confirm the dataset responds with a JSON-stat structure."""
    url = EUROSTAT.format(code=code) + "?format=JSON&lang=EN&geo=DE"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode())
        if payload.get("class") == "dataset":
            ann = {a.get("type"): a for a in payload.get("extension", {}).get("annotation", [])}
            oldest = ann.get("OBS_PERIOD_OVERALL_OLDEST", {}).get("title", "?")
            latest = ann.get("OBS_PERIOD_OVERALL_LATEST", {}).get("title", "?")
            record(angle, f"{code:18s} {label}  [{oldest}–{latest}]", True, required)
        else:
            record(angle, f"{code:18s} {label}", False, required, "unexpected payload shape")
    except urllib.error.HTTPError as e:
        record(angle, f"{code:18s} {label}", False, required,
               f"HTTP {e.code} — code may have been renamed or retired")
    except Exception as e:
        record(angle, f"{code:18s} {label}", False, required, f"{type(e).__name__}: {e}")


def check_url(angle, url, label, required):
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            code = resp.getcode()
            n = len(resp.read(2048))
        ok = code == 200 and n > 0
        record(angle, f"{label}", ok, required, "" if ok else f"HTTP {code}, {n} bytes")
    except urllib.error.HTTPError as e:
        record(angle, label, False, required, f"HTTP {e.code}")
    except Exception as e:
        record(angle, label, False, required, f"{type(e).__name__}: {e}")


def main():
    print("=" * 74)
    print("  MATH60033A — public data source verification")
    print("=" * 74)
    print()
    print("-- Eurostat dissemination API " + "-" * 43)
    for angle, code, label, required in EUROSTAT_CODES:
        check_eurostat(angle, code, label, required)

    print()
    print("-- Other public sources " + "-" * 49)
    for angle, url, label, required in OTHER_SOURCES:
        check_url(angle, url, label, required)

    print()
    print("=" * 74)
    failed = [(a, l) for a, l, ok, req, _ in results if not ok and req]
    warned = [(a, l) for a, l, ok, req, _ in results if not ok and not req]
    passed = sum(1 for *_, ok, req, _ in [(r[0], r[1], r[2], r[3], r[4]) for r in results] if ok)

    print(f"  {passed}/{len(results)} sources reachable")
    if warned:
        print(f"  {len(warned)} optional source(s) unreachable — the course still runs")
    if failed:
        print(f"  {len(failed)} REQUIRED source(s) unreachable:")
        for a, l in failed:
            print(f"      angle {a}: {l}")
        print()
        print("  Fix before rebuilding the spine. Check whether the dataset code was renamed:")
        print("  https://ec.europa.eu/eurostat/web/main/data/database")
        print("=" * 74)
        sys.exit(1)
    print("  All required sources reachable.")
    print("=" * 74)


if __name__ == "__main__":
    main()
