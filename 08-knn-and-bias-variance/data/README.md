# Session 08 — Data

**The Jordà–Schularick–Taylor Macrohistory Database — 18 economies, 1870–2020, 88 financial crises, with the paper's predictors already derived**

```python
import qmib
data = qmib.load("jst")
```

One call. It resolves a local cache first, then the committed spine, then the published URL —
downloading once and caching as parquet. After the first run the practice works offline.

- Everything available: `qmib.catalog()`
- Your group's columns, units and traps: [data dictionaries](../../data/spine/dictionaries/)
- Provenance and flags: [`data/spine/PROVENANCE.md`](../../data/spine/PROVENANCE.md)

---

## Rules for this folder

- Raw data files are **git-ignored**. Never commit them; `qmib` fetches and caches instead.
- The synthetic spine is the exception: small, licence-free, committed deliberately so the
  practice runs with no network.
- If you bring in a dataset of your own, record its source, date and licence in `PROVENANCE.md`.
