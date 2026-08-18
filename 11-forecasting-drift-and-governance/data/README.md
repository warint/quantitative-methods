# Session 11 — Data

**Your group's own final-project data**

- **Source:** Chosen by Session 10 and approved by the instructor


---

Final projects use a dataset of the group's choosing, subject to two constraints: it
must be publicly reproducible, and it must be relevant to a question posed or implied by
*Europe 2031*.

If your project is time-dependent, you will also want a **real-time vintage** source
(ALFRED, or the Philadelphia Fed's real-time dataset) — see section 11.1 on why.

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
