# Session 10 — Data

**401(k) eligibility and financial wealth (the DML canonical example), or the NSW/LaLonde job-training data**

- **Source:** Available via the `doubleml` Python package; LaLonde via `causaldata`
- **URL:** <https://docs.doubleml.org/stable/examples/py_double_ml_pension.html>

---

```python
from doubleml.datasets import fetch_401K
df = fetch_401K(return_type="DataFrame")
df.to_parquet("data/pension401k.parquet")
```

The 401(k) example is ideal: eligibility is plausibly exogenous conditional on income and
demographics, the sample is large, and the literature gives a benchmark estimate to compare against.
The LaLonde data is the harder, more humbling case - the experimental benchmark is known, and most
observational methods miss it.

---

## Rules for this folder

- Data files are **git-ignored**. Never commit raw data.
- Download **once**, cache as parquet, and read from the cache. The practice must run offline.
- Record your download date and, where available, a checksum in `PROVENANCE.md`.
- If you extend the dataset yourself, document the source and respect its licence.

```bash
# record provenance after downloading
echo "$(date -Iseconds)  $(shasum -a 256 <file>)" >> PROVENANCE.md
```
