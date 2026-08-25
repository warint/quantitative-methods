# Session 09 — Data

**A corpus of central bank communications (ECB / Bank of Canada / Fed statements) + a regional economic panel**

- **Source:** ECB press releases; Eurostat regional accounts
- **URL:** <https://www.ecb.europa.eu/press/pr/date/html/index.en.html>

---

The instructor will supply `data/cb_statements.parquet` (date, institution, text) so
that the practice has no scraping dependency. If you extend the corpus yourself, respect each site's
terms of use and record your collection date - provenance is part of the deliverable.

The regional panel (Eurostat `nama_10r_2gdp`, `lfst_r_lfu3rt`) supports the clustering half.

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
