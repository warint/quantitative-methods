"""One call to load any dataset used in this course.

    import qmib

    core  = qmib.load("core")        # the shared European panel
    loans = qmib.load("loans")       # Lending Club, 9,578 loans
    qmib.catalog()                   # what else is there

Why this exists
---------------
The course data lives in three different places: the synthetic spine is
committed to this repository, the four teaching datasets are published on
warin.ca and are deliberately *not* committed, and both need caching so a
practice session runs with the wifi off. Remembering which is which is not
part of learning statistics, so this module hides it.

`load()` resolves a name in this order:

1. a parquet cache in `data/`,
2. the file committed under `data/spine/`,
3. the published URL — downloaded once, then cached as parquet.

After the first call everything is local, so the notebook you run in class
does not depend on the room's network.

Note on "an API"
----------------
GitHub serves files; it cannot run a server, so there is no endpoint to call.
This module is the API in the sense that matters: a stable function you call,
which is free to change where the bytes come from without your code changing.
For use outside a clone — Colab, a student's own notebook — set

    qmib.REMOTE = "https://warint.github.io/quantitative-methods/data"

and the same `load()` fetches over HTTPS instead.
"""

from __future__ import annotations

import io
import pathlib

import pandas as pd

__all__ = ["load", "view", "catalog", "path", "ROOT", "REMOTE"]

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
SPINE = DATA / "spine"

# Set this to serve the spine over HTTPS when the repository is not on disk.
REMOTE: str | None = None

_BASE = "https://www.warin.ca/datalake/courses_data/qmibr"

# Published datasets: not committed (they belong to their publishers), fetched
# once and cached. A mirror is recorded where one exists, so the course does not
# stop working if the first host moves.
PUBLISHED = {
    "loans":    (f"{_BASE}/session7/loans.csv", None),
    "redwines": (f"{_BASE}/session8/redwines.csv",
                 "https://archive.ics.uci.edu/ml/machine-learning-databases/"
                 "wine-quality/winequality-red.csv"),
    "hsbdemo":  (f"{_BASE}/session8/hsbdemo.csv", None),
    "ologit":   (f"{_BASE}/session8/ologit.csv", None),
    "panel":      (f"{_BASE}/session5/panel_data_1.csv", None),
    "realestate": (f"{_BASE}/session5/Real_Estate_Sample.csv", None),
    "glassdoor":  (f"{_BASE}/session5/glassdoordata.csv", None),
    "movies":     (f"{_BASE}/session9/movies_metadata.csv", None),
    "efa":        (f"{_BASE}/session9/EFA.csv", None),
}

# The spine: committed, synthetic, safe to ship. `core` is shared by every
# group; the angles are one per project.
SPINE_FILES = {
    "core": "core.parquet",
    "angle_a_country": "angle_a_country.parquet",
    "angle_a_sector": "angle_a_sector.parquet",
    "angle_b_occupation": "angle_b_occupation.parquet",
    "angle_b_sector": "angle_b_sector.parquet",
    "angle_c_country": "angle_c_country.parquet",
    "angle_c_sector_size": "angle_c_sector_size.parquet",
    "angle_d_partner": "angle_d_partner.parquet",
    "angle_d_product": "angle_d_product.parquet",
    "angle_e_centralbank": "angle_e_centralbank.parquet",
    "angle_e_national": "angle_e_national.parquet",
}

DESCRIPTIONS = {
    "core": "European panel: GDP, population, employment, productivity, investment",
    "loans": "Lending Club — 9,578 three-year loans, FICO and default",
    "redwines": "Portuguese red wines — 1,599 bottles, physico-chemical measures",
    "hsbdemo": "High school programme choice — 200 students (multinomial)",
    "ologit": "Graduate school application — 400 juniors (ordinal)",
    "panel": "Country panel: government debt and economic-freedom indices",
    "realestate": "Residential sales — price, living area, bedrooms, bathrooms",
    "glassdoor": "Glassdoor pay data — salary, bonus, gender, education, age",
    "movies": "Movie metadata — budget, popularity, revenue, runtime, votes",
    "efa": "Questionnaire on car purchase decisions — 14 items (factor analysis)",
}


def path(name: str) -> pathlib.Path:
    """Where `name` is cached locally, whether or not it exists yet."""
    if name in SPINE_FILES:
        return SPINE / SPINE_FILES[name]
    return DATA / f"{name}.parquet"


def catalog() -> pd.DataFrame:
    """Every dataset this module can load, and whether it is on disk."""
    rows = []
    for name in list(SPINE_FILES) + list(PUBLISHED):
        p = path(name)
        rows.append({
            "name": name,
            "source": "spine (committed)" if name in SPINE_FILES else "published",
            "cached": p.exists(),
            "description": DESCRIPTIONS.get(name, ""),
        })
    return pd.DataFrame(rows)


def _download(url: str) -> pd.DataFrame:
    # requests, not urllib: urllib fails with CERTIFICATE_VERIFY_FAILED behind
    # the TLS-inspecting proxies common on university networks.
    import requests

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    sep = ";" if "winequality" in url else ","
    return pd.read_csv(io.StringIO(r.text), sep=sep)


def load(name: str) -> pd.DataFrame:
    """Load a course dataset by name. Downloads once, then reads the cache.

    >>> core = qmib.load("core")
    >>> core.shape
    (450, 11)
    """
    p = path(name)
    if p.exists():
        return _label(pd.read_parquet(p), name)

    if name in SPINE_FILES:
        if REMOTE:
            return _label(pd.read_parquet(f"{REMOTE}/{SPINE_FILES[name]}"), name)
        raise FileNotFoundError(
            f"{p} is missing. The spine is committed to the repository — run this "
            f"from the course folder, or set qmib.REMOTE to fetch it over HTTPS."
        )

    if name not in PUBLISHED:
        known = ", ".join(sorted(set(SPINE_FILES) | set(PUBLISHED)))
        raise KeyError(f"unknown dataset {name!r}. Available: {known}")

    url, mirror = PUBLISHED[name]
    try:
        df = _download(url)
    except Exception as first:                       # noqa: BLE001 — mirror is the fallback
        if not mirror:
            raise
        print(f"  {url} failed ({first}); trying the mirror")
        df = _download(mirror)

    df = _tidy(df, name)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p)
    print(f"  cached {name} -> {p.relative_to(ROOT)}  ({len(df):,} rows)")
    return _label(df, name)




def _label(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Remember which dataset this is, so view() can say so without being told."""
    df.attrs["qmib_name"] = name
    return df

def view(df: pd.DataFrame, n: int = 12, name: str | None = None):
    """Look at a dataframe — the equivalent of R's `View()`.

    >>> core = qmib.load("core")
    >>> qmib.view(core)

    R users reach for `View(df)` and get a scrollable window. Python has no
    single answer: a notebook renders the last expression, a script prints
    nothing at all, and `print(df)` truncates to whatever fits the terminal.
    This gives the same information in every context — the shape, what each
    column is, how much of it is missing, and the first rows.

    In a notebook or a rendered Quarto chapter it returns a styled, scrollable
    table. In a plain terminal it prints a summary and returns the frame, so
    `qmib.view(df)` is safe to leave in a script.
    """
    label = name or getattr(df, "attrs", {}).get("qmib_name", "dataframe")
    missing = df.isna().mean()

    header = (f"{label}: {len(df):,} rows x {df.shape[1]} columns"
              f"  ({missing.mean():.1%} missing overall)")

    summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": (missing * 100).round(1).astype(str) + "%",
        "distinct": df.nunique(dropna=True),
    })

    try:                                     # notebook / Quarto
        from IPython.display import display, HTML
        get_ipython                          # noqa: F821 - defined only in IPython
    except (ImportError, NameError):
        print(header)
        print(summary.to_string())
        print()
        print(df.head(n).to_string())
        return df

    styled = (df.head(n).style
              .set_caption(header)
              .set_table_attributes('style="font-size:0.82rem"')
              .format(precision=3, na_rep="&mdash;"))
    display(HTML(f'<div style="max-height:22rem;overflow:auto">'
                 f'{styled.to_html()}</div>'))
    display(HTML('<details style="font-size:0.85rem;margin-top:.3rem">'
                 '<summary>columns, types and missingness</summary>'
                 f'{summary.to_html()}</details>'))
    return None

def _tidy(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Normalise the published files so the column names are predictable."""
    df = df.rename(columns=lambda c: str(c).strip().lower().replace(".", "_").replace(" ", "_"))
    if name == "loans":
        df = df.rename(columns={"not_fully_paid": "default", "fico_range_low": "fico"})
    if name == "redwines":
        df = df.rename(columns={"quality": "good"})
        if df["good"].dtype == object:
            df["good"] = (df["good"].astype(str).str.strip().str.lower() == "yes").astype(int)
    if name == "movies":
        # The raw file mixes numbers and strings in several columns, which
        # parquet will not store. Coerce the numeric ones and drop the rest.
        numeric = ["budget", "popularity", "revenue", "runtime",
                   "vote_average", "vote_count"]
        keep = [c for c in numeric if c in df.columns]
        for c in keep:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        title = [c for c in ("title", "original_title") if c in df.columns][:1]
        df = df[title + keep].dropna(subset=keep, how="all")
    return df


if __name__ == "__main__":
    print(catalog().to_string(index=False))
