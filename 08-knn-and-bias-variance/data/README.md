# Session 08 — Data

**FRED-MD (revisited, from Session 5) + a target series for nowcasting**

- **Source:** Federal Reserve Bank of St. Louis
- **URL:** <https://www.stlouisfed.org/research/economists/mccracken/fred-databases>

---

You already have the transformed panel from Session 5. Reuse it - and this time, exploit
its correlation structure instead of penalising it.

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
