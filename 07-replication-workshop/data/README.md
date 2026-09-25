# Session 07 — Data

**No new data.** The workshop reuses the five papers' data from sessions 2 to 6, each where its own
session put it:

| # | Paper | Where the data lives | How it gets there |
|---|---|---|---|
| 1 | Fraiberger et al. (2021) | `02-exploratory-data-analysis/data/replication/public/` | Dataverse [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF) |
| 2 | Amsili et al. (2024) | `03-regression-adequacy-and-validity/data/replication/` | Dataverse [10.7910/DVN/U5DAEP](https://doi.org/10.7910/DVN/U5DAEP) |
| 3 | Saganowski et al. (2019) | `04-logistic-ordinal-multinomial/data/replication/` | Dataverse [10.7910/DVN/ONOFS7](https://doi.org/10.7910/DVN/ONOFS7) |
| 4 | Blonigen & Piger (2014) | committed with the repository | `qmib.load("fdi")` — no download |
| 5 | Topalova & Khandelwal (2011) | `06-advanced-regression/data/replication/` | Dataverse [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) |

The one-line download for each package, for macOS, Linux and Windows, is on the
[pre-session page](../00-pre-session/README.md), section 2.
[`check_setup.py`](../02-practice/starter/check_setup.py) says which you already have.

---

## Rules for this folder

- The authors' packages are **git-ignored** wherever they sit. Never commit them.
- Cite each article and each Dataverse package separately: they are distinct contributions with
  distinct DOIs.
- The figures the scripts save go to `02-practice/output/`, which is git-ignored too.
