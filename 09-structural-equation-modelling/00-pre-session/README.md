# Session 09 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 12.4**  
Source: https://www.statlearning.com/  
*Why:* k-means and hierarchical clustering.

**Gentzkow, Kelly & Taddy (2019), 'Text as Data', Journal of Economic Literature 57(3)**  
Source: https://doi.org/10.1257/jel.20181020  
*Why:* The canonical economics survey. Read sections 1-3.

**Baker, Bloom & Davis (2016), 'Measuring Economic Policy Uncertainty', QJE 131(4)**  
Source: https://doi.org/10.1093/qje/qjw024  
*Why:* The practice replicates the logic of this index. Note especially the *validation* section.


---

## Step 2 — Concepts to review

**The central methodological problem of text as data is validation, not estimation.** Any procedure
will produce numbers. The question is whether those numbers measure the construct you named.

Baker, Bloom and Davis validate their EPU index by human audit of thousands of articles - a step
that is expensive, unglamorous, and the reason the index is credited. Come to class prepared to
argue: *what would count as evidence that a text-derived index measures what it claims?*

Also note: clustering has **no ground truth**. Every clustering algorithm will return clusters,
including on pure noise. The burden is entirely on you.

---

## Step 3 — Your data this week

Your data are **already cleaned and cached**. There is nothing to download.

| Group | Angle | Your file | Unit | Columns |
|---|---|---|---|---|
| **G01** | A | `angle_a_country.parquet` | country × time | [dictionary](../../data/spine/dictionaries/G01.md) |
| **G02** | A | `angle_a_sector.parquet` | country × sector × time | [dictionary](../../data/spine/dictionaries/G02.md) |
| **G03** | B | `angle_b_occupation.parquet` | occupation × country × time | [dictionary](../../data/spine/dictionaries/G03.md) |
| **G04** | B | `angle_b_sector.parquet` | sector × country × time | [dictionary](../../data/spine/dictionaries/G04.md) |
| **G05** | C | `angle_c_country.parquet` | country × time | [dictionary](../../data/spine/dictionaries/G05.md) |
| **G06** | C | `angle_c_sector_size.parquet` | country × sector × size × time | [dictionary](../../data/spine/dictionaries/G06.md) |
| **G07** | D | `angle_d_partner.parquet` | reporter × partner × time | [dictionary](../../data/spine/dictionaries/G07.md) |
| **G08** | D | `angle_d_product.parquet` | reporter × product × time | [dictionary](../../data/spine/dictionaries/G08.md) |
| **G09** | E | `angle_e_centralbank.parquet` | document | [dictionary](../../data/spine/dictionaries/G09.md) |
| **G10** | E | `angle_e_national.parquet` | document | [dictionary](../../data/spine/dictionaries/G10.md) |

```python
import pandas as pd
core = pd.read_parquet("data/spine/core.parquet")
mine = pd.read_parquet("data/spine/<your file>.parquet")
df   = mine.merge(core, on=["geo", "time"], how="left")   # not for angle E
```

**Before class:** Decide what your unit of clustering is — country, sector, occupation, document — and what features describe it. For angle E: choose your seed vocabulary before you see any output.

> Read your [data dictionary](../../data/spine/dictionaries/) first. Its **Traps** section lists
> the things that have cost somebody a week, and its **First look** items take ten minutes. Knowing
> that a series is survey-based, breaks in 2021, or is structurally absent before a given year is
> part of your answer — not a footnote.
>
> ⚠️ The spine currently holds **teaching fixtures**: real schema, real coverage, real flags and
> real pathologies, generated from a known structure. Every method behaves as it would on the
> genuine sources, but no number in them is a fact about Europe. See
> [`PROVENANCE.md`](../../data/spine/PROVENANCE.md).

<details>
<summary>Teaching dataset for the method exercise (optional)</summary>

**A corpus of central bank communications (ECB / Bank of Canada / Fed statements) + a regional economic panel**

Source: ECB press releases; Eurostat regional accounts
URL: <https://www.ecb.europa.eu/press/pr/date/html/index.en.html>

The instructor will supply `data/cb_statements.parquet` (date, institution, text) so
that the practice has no scraping dependency. If you extend the corpus yourself, respect each site's
terms of use and record your collection date - provenance is part of the deliverable.

The regional panel (Eurostat `nama_10r_2gdp`, `lfst_r_lfu3rt`) supports the clustering half.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Show that, holding assignments fixed, the k-means objective is minimised by setting each centroid to its cluster mean.
2. Why does k-means implicitly assume spherical, equally-sized clusters? Which step of the algorithm creates that assumption?
3. What does a silhouette value of -0.2 for an observation tell you?
4. Why is cosine similarity usually preferred to Euclidean distance for document vectors?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "My silhouette score says k=2 and my gap statistic says k=6. How should I proceed, and what should I report?"
- "Explain why running k-means on random uniform data still produces tight-looking clusters."
- "I am building a text index of policy uncertainty. Play the referee: give me your three strongest objections to its validity."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 09](../README.md)
