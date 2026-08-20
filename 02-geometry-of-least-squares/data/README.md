# Session 02 — Data

**Ames Housing (2,930 residential sales, 79 features)**

- **Source:** OpenML / scikit-learn `fetch_openml`
- **URL:** <https://www.openml.org/d/42165>

---

Download once and cache locally:

```python
from sklearn.datasets import fetch_openml
ames = fetch_openml(name="house_prices", as_frame=True, parser="auto")
ames.frame.to_parquet("data/ames.parquet")
```

Everything after the first run reads the local parquet file. **No network access is needed during
the practice.**

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
