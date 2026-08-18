# Session 03 — Data

**CPS / IPUMS-style wage microdata (use the Wooldridge `wage2` or CPS 1985 extract)**

- **Source:** `statsmodels` datasets, or the Wooldridge R package data mirrored as CSV
- **URL:** <https://cran.r-project.org/package=wooldridge>

---

A clean, dependency-free option:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/JeffSackmann/.../cps85.csv"  # replace with your mirror
```

**Recommended:** the instructor will place `data/wages.csv` in the shared repo before class so the
lab has no network dependency. Verify with `md5sum` against the value in `data/CHECKSUMS.txt`.

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
