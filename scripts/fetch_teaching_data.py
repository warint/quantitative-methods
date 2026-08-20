#!/usr/bin/env python3
"""
Download the teaching datasets used in the lecture examples, once, into data/.

    python scripts/fetch_teaching_data.py

Every practice session must run with the wifi off, so nothing in a lab or a
report may download anything. Run this once after cloning; everything
afterwards reads the cached parquet files.

The files are small — a few hundred kilobytes in total — and are deliberately
*not* committed: they belong to their original publishers, and a repository
should carry the script that fetches data rather than the data itself.

`requests` is used rather than `urllib` on purpose: it ships its own
certificate bundle, so it keeps working behind the TLS-inspecting proxies
common on university and corporate networks, where `urllib` fails with
CERTIFICATE_VERIFY_FAILED.

Sources
-------
loans      Lending Club, 9,578 three-year loans funded May 2007 - Feb 2010.
           Session 06's classification example. The `fico` column is the
           lender's own risk score, which is the FICO discussion.
redwines   1,599 Portuguese red vinho verde wines, chemically assayed and
           rated by blind tasters (Cortez et al.; also at UCI as
           `winequality-red.csv`). Session 06.
hsbdemo    200 students, "high school and beyond". Multinomial outcome
           (`prog`), for the multinomial logit aside.
ologit     400 applicants, ordered outcome (`apply`), for the ordinal logit
           aside.
"""

import io
import pathlib
import sys

BASE = "https://www.warin.ca/datalake/courses_data/qmibr"

DATASETS = {
    "loans": f"{BASE}/session7/loans.csv",
    "redwines": f"{BASE}/session8/redwines.csv",
    "hsbdemo": f"{BASE}/session8/hsbdemo.csv",
    "ologit": f"{BASE}/session8/ologit.csv",
}

# Where a public mirror exists, record it: if the first host moves, the course
# should not stop working.
MIRRORS = {
    "redwines": "https://archive.ics.uci.edu/ml/machine-learning-databases/"
                "wine-quality/winequality-red.csv",
}

OUT = pathlib.Path(__file__).resolve().parents[1] / "data"


def tidy(df, name):
    """Fix column names R can produce but a Python formula cannot use."""
    df.columns = [c.replace(".", "_") for c in df.columns]
    if name == "loans":
        df = df.rename(columns={"not_fully_paid": "default"})
    # `good` arrives as the strings Yes/No; astype(int) on that raises
    if name == "redwines" and "good" in df.columns and df["good"].dtype != "int64":
        df["good"] = (df["good"].astype(str).str.strip() == "Yes").astype(int)
    return df


def fetch(name, url):
    import pandas as pd
    import requests

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    df = tidy(pd.read_csv(io.BytesIO(r.content)), name)
    dest = OUT / f"{name}.parquet"
    df.to_parquet(dest)
    return df.shape, dest


def main():
    try:
        import pandas  # noqa: F401
        import requests  # noqa: F401
    except ImportError:
        print("Missing dependencies. Activate .venv, then:")
        print("    pip install -r requirements.txt")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    failed = []

    for name, url in DATASETS.items():
        sources = [url] + ([MIRRORS[name]] if name in MIRRORS else [])
        last = None
        for i, src in enumerate(sources):
            try:
                shape, dest = fetch(name, src)
                tag = "  (from mirror)" if i else ""
                print(f"  {name:10s} {shape[0]:6d} x {shape[1]:<3d} "
                      f"-> {dest.relative_to(OUT.parent)}{tag}")
                last = None
                break
            except Exception as exc:
                last = exc
        if last is not None:
            print(f"  {name:10s} FAILED: {type(last).__name__}: {last}")
            failed.append(name)

    print()
    if failed:
        print(f"{len(failed)} dataset(s) unavailable: {', '.join(failed)}")
        print("The lecture examples using them will not run. Tell the instructor —")
        print("a moved URL is a course bug, not something for you to work around.")
        return 1
    print("All teaching datasets cached. Nothing else in the course needs the internet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
