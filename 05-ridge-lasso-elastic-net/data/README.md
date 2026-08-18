# Session 05 — Data

**FRED-MD: a monthly US macroeconomic panel (~127 series)**

- **Source:** Federal Reserve Bank of St. Louis (McCracken & Ng)
- **URL:** <https://www.stlouisfed.org/research/economists/mccracken/fred-databases>

---

Download `current.csv` from the FRED-MD page. The first row contains the
transformation codes (1 = level, 2 = first difference, 5 = log difference, ...). Apply them before
modelling - the series are not stationary in levels.

```python
import pandas as pd
raw = pd.read_csv("data/fred_md_current.csv")
tcode = raw.iloc[0, 1:].astype(int)
df = raw.iloc[1:].set_index("sasdate")
```

This is a genuinely wide problem: many correlated series, a short sample. Exactly where
regularisation earns its keep.

---

## Rules for this folder

- Data files are **git-ignored**. Never commit raw data.
- Download **once**, cache as parquet, and read from the cache. The lab must run offline.
- Record your download date and, where available, a checksum in `PROVENANCE.md`.
- If you extend the dataset yourself, document the source and respect its licence.

```bash
# record provenance after downloading
echo "$(date -Iseconds)  $(shasum -a 256 <file>)" >> PROVENANCE.md
```
