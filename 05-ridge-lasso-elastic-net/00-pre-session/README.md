# Session 05 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 6.2**  
Source: https://www.statlearning.com/  
*Why:* Ridge, lasso, and the tuning-parameter picture.

**Zou & Hastie (2005), 'Regularization and variable selection via the elastic net', JRSS-B 67(2)**  
Source: https://doi.org/10.1111/j.1467-9868.2005.00503.x  
*Why:* The original argument for combining the two penalties. Read the motivation and section 2.

**ESL sec. 3.4**  
Source: https://hastie.su.domains/ElemStatLearn/  
*Why:* The SVD treatment of shrinkage.


---

## Step 2 — Concepts to review

You need the **singular value decomposition** at your fingertips: any $X \in \mathbb{R}^{n\times p}$
can be written $X = UDV^\top$ with $U^\top U = V^\top V = I$ and $D = \operatorname{diag}(d_1 \ge \dots \ge d_p \ge 0)$.

Convince yourself before class that $X^\top X = VD^2V^\top$, so the eigenvalues of $X^\top X$ are
the squared singular values of $X$. This one fact makes the entire lecture transparent.

Also note: **all penalised methods require standardised predictors.** A penalty on $\beta_j$ is
otherwise a penalty on your choice of measurement units. The intercept is never penalised.

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

**Before class:** Count your candidate predictors and compute their correlation matrix. Report the maximum off-diagonal absolute correlation. If it is above 0.9, note which pair.

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

**FRED-MD: a monthly US macroeconomic panel (~127 series)**

Source: Federal Reserve Bank of St. Louis (McCracken & Ng)
URL: <https://www.stlouisfed.org/research/economists/mccracken/fred-databases>

Download `current.csv` from the FRED-MD page. The first row contains the
transformation codes (1 = level, 2 = first difference, 5 = log difference, ...). Apply them before
modelling - the series are not stationary in levels.

```python
import pandas as pd
raw = pd.read_csv("data/fred_md_current.csv")
tcode = raw.iloc[0, 1:].astype(int)
df = raw.iloc[1:].set_index("sasdate")
```

This is a genuinely wide problem: many correlated series, a short sample. Exactly where
regularisation earns its keep.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Why does the ridge solution exist even when $p > n$, while OLS does not?
2. Sketch the $\ell_1$ and $\ell_2$ constraint regions in two dimensions with an RSS contour. Explain the corner argument in one sentence.
3. Two predictors are correlated at 0.99 and both matter. What does the lasso do? What does the elastic net do instead?
4. As $\lambda \to \infty$, what happens to bias and to variance? Where is the optimum?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Derive the soft-thresholding operator from the subgradient condition. Show every step."
- "My lasso selected 4 variables; when I drop one observation it selects a different 4. Is my code wrong, or is this expected? Explain."
- "Explain why standardising predictors is mandatory for penalised regression but irrelevant for OLS coefficients' interpretation."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 05](../README.md)
