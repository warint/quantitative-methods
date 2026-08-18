# Session 01 — Data

**No external dataset (environment smoke test only)**

- **Source:** Generated locally by `00-pre-session/verify_environment.py`


---

Session 1 uses a synthetic dataset created on your own machine. This confirms your
environment works before we depend on real downloads in Session 2.

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
