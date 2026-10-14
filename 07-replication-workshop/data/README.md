# Session 07 — Data

**No new data**, and nothing to download by hand. The workshop reuses the data of four papers from
sessions 2 to 6. Each script reads its paper's file from the course site, so it runs in any folder
with the internet — no clone of the repository needed.

| # | Paper | File the script reads | Source |
|---|---|---|---|
| 1 | Fraiberger et al. (2021) | [`paper1_fraiberger_2021.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper1_fraiberger_2021.csv) — the five columns used | Dataverse [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF) · CC0 |
| 2 | Saganowski et al. (2019) | [`paper2_saganowski_2019.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper2_saganowski_2019.csv) — the authors' file, unchanged | Dataverse [10.7910/DVN/ONOFS7](https://doi.org/10.7910/DVN/ONOFS7) · CC0 |
| 3 | Blonigen & Piger (2014) | [`paper3_blonigen_piger_2014.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper3_blonigen_piger_2014.csv) — the course's rebuild | public sources, rebuilt by `scripts/build_fdi_determinants.py` |
| 4 | Topalova & Khandelwal (2011) | [`paper4_topalova_khandelwal_2011.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper4_topalova_khandelwal_2011.csv) — the columns used | Dataverse [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) · CC0 |

The CSVs in this folder are those files. They are written by `scripts/build_session07_data.py` from
the replication packages of sessions 02, 04 and 06, and published to the site by
`scripts/build_docs.py`. The rows are left alone: every filter the analysis applies is in the
student's script, where they can see it.

---

## Rules for this folder

- Cite each article and each Dataverse package separately: they are distinct contributions with
  distinct DOIs.
- The three Dataverse packages are CC0, which is why their extracts can be republished here.
