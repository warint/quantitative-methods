# Session 02 — Data

**The course data spine** — thirty European countries, 2010–2024. Already in the repository; no
download and no network access required.

```python
import pandas as pd

core = pd.read_parquet("data/spine/core.parquet")          # shared by every group
mine = pd.read_parquet("data/spine/angle_c_country.parquet")  # your angle
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

- **Specification:** [`RESEARCH-MANDATES.md`, section 7](../../RESEARCH-MANDATES.md#7-the-data-spine)
- **Provenance and flags:** [`data/spine/PROVENANCE.md`](../../data/spine/PROVENANCE.md)
- **Your columns, units, ranges and traps:** [`data/spine/dictionaries/`](../../data/spine/dictionaries/)

> **Read your data dictionary before you profile anything.** Several columns carry observation
> flags, breaks in series, or structural missingness — `ai_use_any` does not exist before 2021, for
> instance. A profile computed over a window you did not intend is clean, precise, and about the
> wrong thing.

---

## What you need for this session

Three numeric variables from your angle: the outcome your research question is about, and the two
you most expect to explain it. That is all.

---

## Rules for this folder

- Data files are **git-ignored**. Never commit raw data.
- The spine is the exception: it is small, synthetic, and committed deliberately so the practice
  runs offline.
- If you bring in a dataset of your own, download **once**, cache as parquet, and read from the
  cache. Record the download date and a checksum in `PROVENANCE.md`.

```bash
# record provenance after downloading anything of your own
echo "$(date -Iseconds)  $(shasum -a 256 <file>)" >> PROVENANCE.md
```
