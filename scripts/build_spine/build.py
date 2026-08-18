"""
MATH60033A — build the REAL data spine from the public sources.

    python scripts/verify_sources.py            # 1. confirm the codes still resolve
    python scripts/build_spine/build.py         # 2. fetch, clean, join, write
    python scripts/build_spine/make_dictionaries.py   # 3. regenerate the dictionaries
    git add data/spine && git commit -m "Rebuild data spine (<term>)"

Requires outbound network access to ec.europa.eu, comtradeapi.un.org and
ecb.europa.eu. Run it on your own machine, once per term.

DESIGN RULES — do not violate these when extending
--------------------------------------------------
* One fetch per series, cached raw in .raw/ so a failed build does not re-hammer the API.
* Every transformation is logged to data/spine/PROVENANCE.md.
* NO imputation. Missingness is pedagogically useful; students must decide how to
  handle it inside their CV pipeline. Deliver the holes, documented.
* NO standardisation, for the same reason.
* NO outlier removal. Session 03 asks students to find high-leverage points themselves.
* Observation status flags are PRESERVED, never dropped.
"""

import argparse
import datetime as dt
import hashlib
import os
import sys
import traceback

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import spec                       # noqa: E402
from eurostat import fetch, coverage   # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "data", "spine"))
LOG = []          # provenance rows
STEPS = []        # transformation log


def note(file, step, detail):
    STEPS.append({"file": file, "step": step, "detail": detail})


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def pull(key, code, filters, valcol, notes, angle, extra_dims=()):
    """Fetch one series, return it in wide-by-key form, and record provenance."""
    df = fetch(code, filters, geo=spec.GEO, time_=spec.YEARS)
    cov = coverage(df, spec.GEO, spec.YEARS)
    LOG.append({"angle": angle, "key": key, "code": code, "label": df.attrs.get("label", ""),
                "updated": df.attrs.get("updated", ""),
                "downloaded": dt.datetime.now().isoformat(timespec="seconds"),
                "filters": "; ".join(f"{k}={v}" for k, v in (filters or {}).items()),
                **cov, "notes": notes})
    if df.empty:
        print(f"    !! {key:<18s} {code:<18s} EMPTY — check the filters")
        return None
    keep = ["geo", "time", *extra_dims, "value", "flag"]
    keep = [c for c in keep if c in df.columns]
    out = df[keep].rename(columns={"value": valcol, "flag": f"flag_{key}"})
    print(f"    {key:<18s} {code:<18s} {cov['rows']:>6,d} rows  "
          f"{cov['coverage_pct']:>5.1f}% coverage  {cov['flagged']:>4d} flagged")
    return out


def merge_all(parts, keys):
    out = None
    for p in parts:
        if p is None:
            continue
        out = p if out is None else out.merge(p, on=keys, how="outer")
    return out


def build_core():
    print("  core")
    parts = [pull(k, c, f, v, n, "core") for k, c, f, v, n in spec.CORE]
    d = merge_all(parts, ["geo", "time"])
    d = d.sort_values(["geo", "time"])
    note("core.parquet", "derive", "prod_growth = yoy % change in productivity_idx, by geo")
    d["prod_growth"] = d.groupby("geo")["productivity_idx"].pct_change() * 100
    note("core.parquet", "derive",
         "falling_behind = prod_growth below the within-year 10th percentile; "
         "falling_behind_next = that variable led one year (the Session 06 label)")
    thr = d.groupby("time")["prod_growth"].transform(lambda s: s.quantile(0.10))
    d["falling_behind"] = (d["prod_growth"] < thr).astype("Int64")
    d["falling_behind_next"] = d.groupby("geo")["falling_behind"].shift(-1)
    return {"core.parquet": d}


def build_angle_a():
    print("  angle A")
    country = merge_all([pull(k, c, f, v, n, "a") for k, c, f, v, n in spec.ANGLE_A],
                        ["geo", "time"])
    note("angle_a_country.parquet", "reshape",
         "one row per geo × time; each series joined on the full key, outer join so that "
         "coverage gaps remain visible rather than being dropped")
    sector = pull("elec_by_sector", "nrg_bal_c",
                  {"nrg_bal": "FC_IND_E", "siec": "E7000", "unit": "GWH"},
                  "elec_use_gwh", "Electricity use by NACE section", "a",
                  extra_dims=("nace_r2",))
    return {"angle_a_country.parquet": country, "angle_a_sector.parquet": sector}


def build_angle_b():
    print("  angle B")
    occ = pull("emp_occ", "lfsa_egais", {"sex": "T", "age": "Y15-64", "unit": "THS_PER"},
               "employment_ths", "Employment by ISCO-08", "b", extra_dims=("isco08",))
    sector = merge_all([
        pull("vacancy", "jvs_a_rate_r2", {"sizeclas": "TOTAL", "s_adj": "NSA"},
             "vacancy_rate", "Job vacancy rate", "b", extra_dims=("nace_r2",)),
        pull("earnings", "earn_ses_annual", {"sex": "T", "unit": "EUR",
                                             "indic_se": "MEAN_E_EUR"},
             "annual_earnings_eur", "Mean annual earnings (QUADRENNIAL)", "b",
             extra_dims=("nace_r2",)),
    ], ["geo", "time", "nace_r2"])
    note("angle_b_occupation.parquet", "warn",
         "O*NET task-exposure scores must be merged separately: they describe the US "
         "labour market and the SOC->ISCO crosswalk is lossy. Document your crosswalk.")
    return {"angle_b_occupation.parquet": occ, "angle_b_sector.parquet": sector}


def build_angle_c():
    print("  angle C")
    country = merge_all([pull(k, c, f, v, n, "c") for k, c, f, v, n in spec.ANGLE_C],
                        ["geo", "time"])
    note("angle_c_country.parquet", "warn",
         "AI module (isoc_eb_ai) begins 2021; cloud, ICT specialists and R&D run longer. "
         "The resulting ragged panel is REAL and must not be trimmed away.")
    size = pull("ai_by_size", "isoc_eb_ai",
                {"unit": "PC_ENT", "indic_is": "E_AI_TANY"},
                "ai_use_any", "AI use by size class and sector", "c",
                extra_dims=("nace_r2", "size_emp"))
    return {"angle_c_country.parquet": country, "angle_c_sector_size.parquet": size}


def build_angle_d():
    print("  angle D")
    print("    Comtrade is not implemented here: its API requires a key and its rate limits")
    print("    make an unattended build unreliable. Download the extract manually from")
    print("    https://comtradeplus.un.org/ (or CEPII BACI) for HS "
          f"{', '.join(spec.HS_LINES)},")
    print("    reporters = the 30 spine countries, partners = "
          f"{', '.join(spec.PARTNERS)},")
    print("    and place it at data/spine/.raw/comtrade_extract.csv. Then re-run.")
    raw = os.path.join(HERE, ".raw", "comtrade_extract.csv")
    if not os.path.exists(raw):
        LOG.append({"angle": "d", "key": "trade", "code": "COMTRADE", "rows": 0,
                    "notes": "NOT BUILT — manual extract missing"})
        return {}
    t = pd.read_csv(raw)
    note("angle_d_partner.parquet", "aggregate", "summed over HS lines within reporter × partner")
    note("angle_d_product.parquet", "aggregate", "summed over partners within reporter × HS line")
    by_partner = t.groupby(["geo", "time", "partner"], as_index=False)[
        ["import_value_eur", "export_value_eur"]].sum()
    by_partner["is_reexport_hub"] = by_partner["geo"].isin(["NL", "BE", "IE"]).astype(int)
    by_product = t.groupby(["geo", "time", "hs"], as_index=False)[
        ["import_value_eur", "export_value_eur"]].sum()
    by_product["hs_revision_break"] = by_product["time"].isin([2012, 2017, 2022]).astype(int)
    return {"angle_d_partner.parquet": by_partner, "angle_d_product.parquet": by_product}


def build_angle_e():
    print("  angle E")
    print("    The ECB corpus is scraped separately — see scripts/build_spine/README.md.")
    print("    Place the collected corpus at data/spine/.raw/cb_corpus.csv with columns")
    print("    doc_id, date, institution, country, doc_type, text. Then re-run.")
    raw = os.path.join(HERE, ".raw", "cb_corpus.csv")
    if not os.path.exists(raw):
        LOG.append({"angle": "e", "key": "corpus", "code": "ECB", "rows": 0,
                    "notes": "NOT BUILT — corpus missing"})
        return {}
    c = pd.read_csv(raw)
    note("angle_e_centralbank.parquet", "derive", "n_words = whitespace token count")
    c["n_words"] = c["text"].astype(str).str.split().str.len()
    cb = c[c["institution"].isin(["ECB", "BoE", "BoC"])]
    nat = c[~c["institution"].isin(["ECB", "BoE", "BoC"])]
    return {"angle_e_centralbank.parquet": cb, "angle_e_national.parquet": nat}


def write_provenance(written):
    p = os.path.join(OUT, "PROVENANCE.md")
    L = ["# Data spine — provenance", "",
         f"Built: **{dt.datetime.now().isoformat(timespec='seconds')}** · "
         f"source: **live public APIs** (not fixtures)", "",
         "> Students: read this before you model. Knowing that a series is survey-based, "
         "or revised, or breaks in 2021, is part of your answer — not a footnote.", "",
         "---", "", "## Files written", "",
         "| File | Rows | Columns | sha256 (16) |", "|---|---|---|---|"]
    for name, path in written.items():
        d = pd.read_parquet(path)
        L.append(f"| `{name}` | {len(d):,} | {d.shape[1]} | `{sha(path)}` |")

    L += ["", "---", "", "## Series inventory", "",
          "| Angle | Key | Code | Label | Rows | Coverage | Flagged | Updated | Notes |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in LOG:
        L.append(f"| {r.get('angle','')} | `{r.get('key','')}` | `{r.get('code','')}` | "
                 f"{r.get('label','')[:48]} | {r.get('rows',0):,} | "
                 f"{r.get('coverage_pct','—')}% | {r.get('flagged','—')} | "
                 f"{r.get('updated','')[:10]} | {r.get('notes','')} |")

    L += ["", "---", "", "## Transformations applied", "",
          "| File | Step | Detail |", "|---|---|---|"]
    for s in STEPS:
        L.append(f"| `{s['file']}` | {s['step']} | {s['detail']} |")

    L += ["", "**What the build deliberately does NOT do:** no imputation, no standardisation, "
          "no outlier removal. Those belong inside your cross-validation pipeline, and "
          "deciding on them is part of the exercise.", "",
          "---", "", "## Flags you will encounter", "",
          "| Flag | Meaning | What to do |", "|---|---|---|",
          "| `u` | low reliability | Do not drop silently — it biases coverage toward large economies |",
          "| `c` | confidential | Genuinely unavailable; treat as missing and report how many |",
          "| `b` | break in series | A break is a modelling problem, not a data error |",
          "| `p` / `e` | provisional / estimated | Relevant to any real-time or vintage claim |",
          "", "---", "", "## Structural breaks", "",
          "| From | To | What | Affects |", "|---|---|---|---|"]
    for a, b, what, aff in spec.BREAKS:
        L.append(f"| {a} | {b or '—'} | {what} | {aff} |")
    L += ["", "---", "",
          "## Adding your own series", "",
          "Append a row to the inventory with source, code, download date, licence and known "
          "issues. This is an ongoing obligation and part of what the Session 12 governance "
          "file is assessed on."]
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"\n  provenance -> {os.path.relpath(p, os.path.join(HERE, '..', '..'))}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", choices=["core", "a", "b", "c", "d", "e"],
                    help="build only these angles")
    args = ap.parse_args()
    want = set(args.only or ["core", "a", "b", "c", "d", "e"])

    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("  MATH60033A — building the data spine from live sources")
    print("=" * 74)

    builders = {"core": build_core, "a": build_angle_a, "b": build_angle_b,
                "c": build_angle_c, "d": build_angle_d, "e": build_angle_e}
    written, failed = {}, []
    for key, fn in builders.items():
        if key not in want:
            continue
        try:
            for name, df in (fn() or {}).items():
                if df is None or len(df) == 0:
                    failed.append(name)
                    continue
                path = os.path.join(OUT, name)
                df.to_parquet(path, index=False)
                written[name] = path
        except Exception:
            print(f"  !! angle {key} failed:")
            traceback.print_exc(limit=2)
            failed.append(key)

    write_provenance(written)
    print()
    print("=" * 74)
    print(f"  {len(written)} file(s) written to data/spine/")
    if failed:
        print(f"  {len(failed)} not built: {', '.join(failed)}")
        print("  Fixtures remain in place for those. Re-run when the inputs are available.")
    print("  Next: python scripts/build_spine/make_dictionaries.py")
    print("=" * 74)


if __name__ == "__main__":
    main()
