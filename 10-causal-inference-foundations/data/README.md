# Session 10 — Data

**The spine's documented treatment, with a known effect to recover**

```python
import qmib
data = qmib.load("core")
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
