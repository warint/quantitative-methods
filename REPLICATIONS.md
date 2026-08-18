# Session replications — the article behind each lab

Every session's 90-minute practice block is built on a **published article**. You
read it before class; the lab reproduces a piece of it.

There are two kinds of lab, and the table says which you are getting:

| Kind | What it means |
|---|---|
| **Real data** | The authors deposited their replication package. You work with the numbers the paper was written from. |
| **Synthetic replication** | No usable public package exists. You reproduce the paper's *design* on the course data spine, which was generated to carry the same pathology. |

A synthetic replication is not a lesser exercise. It is the same reasoning applied
to data whose truth we happen to know — which means you can check whether your
method recovered it. You cannot do that with real data, ever.

> **Every DOI below was resolved before it was published here** — Dataverse
> packages against the Dataverse API, articles against Crossref. If one fails to
> resolve, tell me: it means something moved, and the table is wrong.

---

## The table

| S | Topic | Article | Data |
|---|---|---|---|
| 02 | Geometry of least squares | Topalova & Khandelwal, *Trade Liberalization and Firm Productivity: The Case of India* | **Real** — [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) · CC0 |
| 03 | Inference and diagnostics | Bertrand, Duflo & Mullainathan, *How Much Should We Trust Differences-in-Differences Estimates?* QJE 2004 · [10.1162/003355304772839588](https://doi.org/10.1162/003355304772839588) | Synthetic — spine |
| 04 | Bias–variance and CV | Mullainathan & Spiess, *Machine Learning: An Applied Econometric Approach*, JEP 2017 · [10.1257/jep.31.2.87](https://doi.org/10.1257/jep.31.2.87) | Synthetic — spine |
| 05 | Ridge, lasso, elastic net | Wang, Zhu & Yu, *Variable Selection in Macroeconomic Forecasting with Many Predictors*, Econometrics and Statistics · [10.1016/j.ecosta.2023.01.003](https://doi.org/10.1016/j.ecosta.2023.01.003) | Synthetic — spine |
| 06 | Classification | Shukla, *Credit Scoring of Thin File Consumers* | **Real** — [10.7910/DVN/EGAIKO](https://doi.org/10.7910/DVN/EGAIKO) · CC BY 4.0 |
| 07 | Trees, forests, boosting | Athey & Imbens, *Machine Learning Methods That Economists Should Know About*, Annual Review of Economics 2019 · [10.1146/annurev-economics-080217-053433](https://doi.org/10.1146/annurev-economics-080217-053433) | Synthetic — spine |
| 08 | PCA and factor models | Koopman & Mesters, *Empirical Bayes Methods for Dynamic Factor Models* | **Real** — [10.7910/DVN/NKWMQM](https://doi.org/10.7910/DVN/NKWMQM) · CC0 |
| 09 | Clustering and text | Bennani & Romelli, *Exploring the informativeness and drivers of tone during committee meetings* | **Real** — [10.7910/DVN/TZEN38](https://doi.org/10.7910/DVN/TZEN38) · CC BY 4.0 |
| 10 | Causal machine learning | Huber, *Evaluating (weighted) dynamic treatment effects by double machine learning* | **Real** — [10.7910/DVN/FS0KBA](https://doi.org/10.7910/DVN/FS0KBA) · CC0 |
| 11 | Forecasting and governance | Mullainathan & Spiess (above), read a second time for its last section | Your group's own project data |

---

## Why some sessions have no real data

I searched Harvard Dataverse for a usable replication package on every topic.
For sessions 03, 04, 05, 07 and 11 there was none that was simultaneously
(a) on the session's method, (b) economics with an international dimension, and
(c) openly licensed with data a student can actually open.

Harvard Dataverse is dominated by political science. Most economics replication
material sits in openICPSR, because the American Economic Association requires
it there. That is a fact about where the discipline deposits its work, not a
judgement about any of it.

Rather than attach a weak paper to a session for the sake of symmetry, those
sessions read a **strong methodological article** and replicate its argument on
the spine. In every case the spine was generated to carry exactly the pathology
the article is about.

---

## What "replicate" means here

Not "re-run their code and confirm the number." That teaches nothing except that
computers are deterministic.

For each session you will be asked to do some subset of:

1. **State the estimand.** What quantity is the paper trying to learn? Write it
   before you open the data.
2. **Reproduce one result.** One table cell, one coefficient, one figure.
3. **Break it.** Change the specification in a way the authors did not, and
   report what moved. This is where the learning is.
4. **Say what it now supports.** In three sentences, what may be claimed on the
   basis of what you produced — and what may not.

Step 4 is the graded one.

---

## Getting a replication package

Dataverse serves files over a plain URL. From your repository root:

```bash
# the whole package as a zip
curl -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/8WEXYD" \
     -o data/topalova.zip
unzip data/topalova.zip -d data/topalova/
```

**The bulk download gives you the authors' original files, not the `.tab`
versions the Dataverse web page lists.** In economics that usually means Stata.
Pandas reads it without Stata being installed:

```python
import pandas as pd

firms = pd.read_stata("data/topalova/prod_dataregression.dta")
print(firms.shape)        # (32422, 63) — firm-year panel
print(firms[["companyname", "yr", "industrycode"]].head())

industry = pd.read_stata("data/topalova/industrydata.dta")
print(industry.shape)     # (138, 20)
```

::: note
If a `.dta` is too old or too new for pandas, ask Dataverse for the archival
copy instead by appending `&format=tab` to a single-file download URL.
:::

::: note
Download **once**, into `data/`, which is git-ignored for anything large. Never
put a download inside a lab script — the lab must run with the wifi off.
:::

---

## Licences

Every package listed above is CC0 or CC BY 4.0, so you may use and redistribute
it with attribution. Cite the *article* and the *data* separately — they are
different contributions, and the data has its own DOI for that reason.

See [`LICENSING.md`](LICENSING.md) for how this repository is licensed, and
[`CITATION.cff`](CITATION.cff) for how to cite the course.
