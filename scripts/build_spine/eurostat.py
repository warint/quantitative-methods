"""
Minimal Eurostat dissemination API client.

The API returns JSON-stat 2.0: a flat `value` dict keyed by a linear index into the
cartesian product of the dimensions. This module turns that into a tidy long DataFrame,
preserving the observation status flags — which matter, because dropping `u` (low
reliability) and `c` (confidential) cells silently biases coverage toward large economies.

    from eurostat import fetch
    df = fetch("isoc_eb_ai", {"unit": "PC_ENT", "indic_is": "E_AI_TANY"},
               geo=["DE", "FR"], time=[2021, 2022, 2023])
"""

import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
UA = {"User-Agent": "qmib-course-build/1.0"}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".raw")


def _get(url, timeout=90, retries=3):
    """GET with an on-disk cache, so a failed build does not re-hammer the API."""
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode())
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
            return payload
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Eurostat request failed after {retries} attempts: {url}\n  {last}")


def _jsonstat_to_long(payload):
    """JSON-stat 2.0 -> list of dicts, one per observation, with flags preserved."""
    ids = payload["id"]
    sizes = payload["size"]
    dims = payload["dimension"]

    # index position -> category code, per dimension
    cats = []
    for d in ids:
        idx = dims[d]["category"]["index"]
        if isinstance(idx, dict):
            inv = {v: k for k, v in idx.items()}
            cats.append([inv[i] for i in range(len(inv))])
        else:                                   # already a list
            cats.append(list(idx))

    # strides for the row-major linear index
    strides, acc = [0] * len(sizes), 1
    for i in range(len(sizes) - 1, -1, -1):
        strides[i] = acc
        acc *= sizes[i]

    status = payload.get("status", {}) or {}
    rows = []
    for linear, value in payload.get("value", {}).items():
        n = int(linear)
        rec = {}
        for i, d in enumerate(ids):
            rec[d] = cats[i][(n // strides[i]) % sizes[i]]
        rec["value"] = value
        rec["flag"] = status.get(linear, "")
        rows.append(rec)
    return rows


def fetch(code, filters=None, geo=None, time_=None, lang="EN"):
    """Fetch one Eurostat dataset slice as a pandas DataFrame in long form."""
    import pandas as pd

    params = [("format", "JSON"), ("lang", lang)]
    for k, v in (filters or {}).items():
        params.append((k, v))
    for g in (geo or []):
        params.append(("geo", g))
    for t in (time_ or []):
        params.append(("time", str(t)))

    url = f"{BASE}/{code}?" + urllib.parse.urlencode(params)
    payload = _get(url)
    if payload.get("class") != "dataset":
        raise RuntimeError(f"{code}: unexpected payload — has the code been renamed?")

    df = pd.DataFrame(_jsonstat_to_long(payload))
    if df.empty:
        return df
    if "time" in df:
        df["time"] = df["time"].astype(int)
    df.attrs["code"] = code
    df.attrs["label"] = payload.get("label", "")
    df.attrs["updated"] = payload.get("updated", "")
    df.attrs["url"] = url
    return df


def coverage(df, geo_expected, time_expected):
    """How complete is this slice? Returned verbatim into PROVENANCE.md."""
    if df.empty:
        return {"rows": 0, "geo": 0, "time": 0, "flagged": 0, "coverage_pct": 0.0}
    got_geo = df["geo"].nunique() if "geo" in df else 0
    got_time = df["time"].nunique() if "time" in df else 0
    flagged = int((df["flag"].astype(str).str.strip() != "").sum())
    expected = max(1, len(geo_expected) * len(time_expected))
    return {"rows": len(df), "geo": got_geo, "time": got_time, "flagged": flagged,
            "coverage_pct": round(100 * len(df) / expected, 1)}
