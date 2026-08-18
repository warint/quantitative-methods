# Session 07 — Data

**Ames Housing (regression) + Bank Marketing (classification)**

- **Source:** OpenML / UCI
- **URL:** <https://archive.ics.uci.edu/dataset/222/bank+marketing>

---

Reusing Ames lets you compare directly against your Session 2-5 linear results on identical
folds - which is the point of the lab. Keep the same random seed and the same CV splits.

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
