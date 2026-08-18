# Building the data spine

Run once per term, by the instructor.

```bash
python scripts/verify_sources.py       # 1. confirm every endpoint still resolves
python scripts/build_spine/build.py    # 2. fetch, clean, join, write parquet + PROVENANCE.md
git add data/spine && git commit -m "Rebuild data spine (<term>)"
```

## Design rules

- **One fetch per series, cached raw** in `scripts/build_spine/.raw/` (git-ignored) so a failed
  build does not re-hammer the APIs.
- **Every transformation logged** to `data/spine/PROVENANCE.md`: source, dataset code, download
  timestamp, sha256, row count, and every filter or reshape applied.
- **Do not impute here.** Missingness is pedagogically useful — students must decide how to handle
  it inside their CV pipeline. Deliver the holes, documented.
- **Do not standardise here**, for the same reason.
- **Keep the keys clean:** `geo` (Eurostat country code), `time` (integer year), plus `nace_r2`,
  `isco08`, `size_emp`, `partner`, `doc_id` as the angle requires.

## Files expected

| Script | Writes |
|---|---|
| `fetch_eurostat.py` | thin wrapper over the dissemination API, returns tidy long format |
| `build_core.py` | `core.parquet` |
| `build_angle_a.py` … `build_angle_e.py` | one parquet per angle |
| `build.py` | orchestrates all of the above, then writes `PROVENANCE.md` |
