# Session 08 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 12.1-12.2**  
Source: https://www.statlearning.com/  
*Why:* PCA, proportion of variance explained, the scree plot.

**Stock & Watson (2002), 'Forecasting Using Principal Components from a Large Number of Predictors', JASA 97(460)**  
Source: https://doi.org/10.1198/016214502388618960  
*Why:* The diffusion-index method the practice reproduces.

**Bai & Ng (2002), 'Determining the Number of Factors in Approximate Factor Models', Econometrica 70(1)**  
Source: https://doi.org/10.1111/1468-0262.00273  
*Why:* The selection criteria you will implement.


---

## Step 2 — Concepts to review

Three preliminaries.

**1. Standardisation is not optional.** PCA on a covariance matrix is dominated by whichever series
has the largest units. Unemployment in percent and money supply in billions are not comparable.
Use the correlation matrix (i.e. standardise) unless every variable shares a unit and you *want*
scale to matter.

**2. PCA is a rotation, not a selection.** Each component is a linear combination of *all*
variables. It reduces dimension without reducing the number of series you must collect - a point
that matters enormously in practice and is routinely forgotten.

**3. The identification problem you are about to meet.** In $X = F\Lambda^\top + e$, for any
invertible $H$ we have $F\Lambda^\top = (FH)(\Lambda H^{-\top})^\top$. Factors are identified only
up to rotation. So "Factor 1 is the business cycle" is an *interpretation*, never an estimate.

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

**Before class:** List the columns in your file that plausibly measure the same underlying construct. That guess is your prior on how many factors you will find.

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

**FRED-MD (revisited, from Session 5) + a target series for nowcasting**

Source: Federal Reserve Bank of St. Louis
URL: <https://www.stlouisfed.org/research/economists/mccracken/fred-databases>

You already have the transformed panel from Session 5. Reuse it - and this time, exploit
its correlation structure instead of penalising it.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Show that the first principal component direction is the eigenvector of the sample covariance matrix with the largest eigenvalue.
2. If $X = UDV^\top$, what are the principal component scores and what are the loadings?
3. Your first component explains 40% of variance and loads positively on all 127 series. What is it, economically?
4. Why does adding more (noisy) series to a factor model sometimes *improve* factor estimation?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "My PCA loadings have the opposite sign from the textbook figure. Is my code wrong?"
- "Explain why more predictor series improves factor estimation but hurts an unregularised regression. Reconcile the two intuitions."
- "Write the Bai-Ng IC_p2 criterion and explain what property the penalty term must satisfy."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 08](../README.md)
