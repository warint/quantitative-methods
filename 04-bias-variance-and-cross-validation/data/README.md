# Session 04 — Data

**Ames Housing (continued) + a synthetic polynomial DGP**

- **Source:** Cached from Session 2 + generated locally
- **URL:** <https://www.openml.org/d/42165>

---

The synthetic part lets you *see* bias and variance separately, because you know the truth.
The Ames part shows you what it looks like when you do not.

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
