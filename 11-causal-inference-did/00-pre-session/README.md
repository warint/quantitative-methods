<!-- authored: do not regenerate -->

# Session 11 — Pre-session preparation

> **What would have happened otherwise?**

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-11-pre-session.html)** ·
> source: [`MATH60033A-S11-Pre-Session.qmd`](MATH60033A-S11-Pre-Session.qmd)

Three things to do before class, and each one is a step of the practice.
Budget **75–90 minutes**.

| | Before class | Objective | Used in the practice for |
|---|---|---|---|
| **1** | Read the paper | find the difference-in-differences inside it | step 1, reproducing its number |
| **2** | Get the data, map your project | have everything run, and know your four columns | steps 2 and 3 |
| **3** | Self-check | know what the lecture will build on | the lecture |

---

## 1. The reading — 45–60 min

**Cavallo, Gopinath, Neiman & Tang (2021), *Tariff Passthrough at the Border and at the Store: Evidence from US Trade Policy*, American Economic Review: Insights 3(1)**
[Read the article](https://doi.org/10.1257/aeri.20190536)

**Objective:** find the difference-in-differences inside the paper. Read for the **argument**, not for
coverage, and annotate the answers to five questions; the practice opens with them.

| | Question | Why it matters |
|---|---|---|
| **1** | What is **treated**, and what is the **control** group? | the second difference is only as good as the controls |
| **2** | What are the **dates**: before, after, and is adoption staggered? | decides which comparisons exist |
| **3** | Which **coefficient** is the estimate, and in what **units**? | the number you will reproduce |
| **4** | What evidence do they show for **parallel trends**? | an event study, a pre-period, an argument? |
| **5** | What could **change at the same time** as the treatment? | the first objection a referee would raise |

A question the paper leaves open is a finding: write it down.

---

## 2. The data, and your project — 15 min

### a) The paper's data

**Objective:** spend the first twenty minutes of the practice reproducing a number, not downloading one.

**Harvard Dataverse: [10.7910/DVN/JV7FCH](https://doi.org/10.7910/DVN/JV7FCH)**

Unzip it here — the folder is git-ignored, so nothing large is committed:

```text
11-causal-inference-did/data/replication/
```

Keep the authors' own folder structure and README.

> **Note.** This deposit sits behind a Dataverse **guestbook**, so a scripted download returns an
> error. Open the DOI in a browser, click **Access Dataset -> Download ZIP**, accept the terms once,
> and unzip it to the folder above.

### b) The course data, and the estimators

**Objective:** check that the practice's data and estimators run on your machine.

```python
import qmib
import diff_diff as dd

ai = qmib.load("angle_c_country")           # the practice ground: AI strategies, 30 countries
print(ai.shape, ai["has_ai_strategy"].sum(), "country-years with a strategy")
print("diff-diff", dd.__version__)          # the estimators of the lecture and the practice
```

You should see `(330, 33) 61 country-years with a strategy` and `diff-diff` 3.11 or later. It
downloads once and caches as parquet. `ModuleNotFoundError: diff_diff` means
`pip install -r requirements.txt` from the repository root, with the environment active.

### c) Your project, on paper

**Objective:** know whether a difference-in-differences can apply to your project before the practice
asks. Every estimator needs four columns:

| Column | On the course data | On your project |
|---|---|---|
| **unit** | `geo`, the country | ? |
| **time** | `time`, the year | ? |
| **outcome** | `ai_use_any`, % of firms using AI | ? |
| **adoption year**, 0 if never | from `has_ai_strategy` | which policy, which date, for which units? |

If no unit is ever treated, none stays untreated, or none is observed **before** its treatment, the
design cannot apply. Knowing that is a full answer ([`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md),
section 5).

---

## 3. Self-check — 15 min

Answer on paper. If you cannot, that is what the lecture is for.

1. **Compute one.** Full-time staff per fast-food restaurant: New Jersey went from 20.44 to 21.03 after
   its minimum wage rose; Pennsylvania, which did not change its wage, from 23.33 to 21.17. What is the
   difference-in-differences, and what would New Jersey have reached without the rise?
2. **Name the differences.** Which of the two subtractions removes what is **constant** about the
   treated group, and which removes what happened to **everyone**?
3. **The assumption.** Parallel trends is about which years: before the policy, or after? Why can no
   test prove it?
4. **Session 10 against session 11.** Matching needed every confounder measured. What does
   difference-in-differences need instead?
5. **The paper.** Which claim rests on the difference-in-differences, and how hard does it lean on it?

---

## Arrive with

- [ ] The paper annotated against the five questions
- [ ] The replication package downloaded and unzipped
- [ ] The check in 2b run once, so the cache exists
- [ ] Your project mapped onto four columns, or the reason it cannot be
- [ ] Your self-check answers, on paper

---

[Session 11 overview](../README.md) · [The lecture](../01-lecture/README.md) ·
[The practice](../02-practice/README.md)
