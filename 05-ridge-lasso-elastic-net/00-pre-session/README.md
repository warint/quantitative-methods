# Session 05 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-05-pre-session.html)** ·
> source: [`MATH60033A-S05-Pre-Session.qmd`](MATH60033A-S05-Pre-Session.qmd)


**Blonigen & Piger (2014), 'Determinants of foreign direct investment', Canadian Journal of
Economics 47(3), 775–812**  
Source: https://doi.org/10.1111/caje.12091 · free preprint: https://www.nber.org/papers/w16704  
*Why:* This is the session's question asked of a real international-business problem. Eight
prior studies disagree about which variables belong in an FDI regression (their table 1); the
authors collect 56 candidates and report which survive (their table 3). Read those two tables
first. The practice puts the lasso on the same 56 variables, two decades later.

*Optional background, if you want the mathematics:* ISLR ch. 6.2 (https://www.statlearning.com/)
for the tuning-parameter picture, and Zou & Hastie (2005),
https://doi.org/10.1111/j.1467-9868.2005.00503.x, for the elastic net's original argument.
Neither is examinable; the lecture derives what it needs.


---

## Step 2 — Concepts to review

You need the **singular value decomposition** at your fingertips: any $X \in \mathbb{R}^{n\times p}$
can be written $X = UDV^\top$ with $U^\top U = V^\top V = I$ and $D = \mathrm{diag}(d_1 \ge \dots \ge d_p \ge 0)$.

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

**Before class:** Count your candidate predictors and compute their correlation matrix. Report the maximum off-diagonal absolute correlation. If it is above 0.9, note which pair. Do the same for the 56 FDI candidates — that number is what decides lasso versus elastic net.

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
<summary>The paper's dataset — required, not optional</summary>

**56 candidate determinants of bilateral FDI, 2019**

The data behind Blonigen & Piger (2014), rebuilt from the sources the paper names: OECD bilateral
FDI positions, the CEPII gravity database, the World Development Indicators and Freedom House.
7,051 directed country pairs. Every number is real — unlike the rest of the spine, this file is
not a teaching fixture.

```python
import qmib

fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
print(fdi.shape, len(cov))          # (7051, 60) 56
```

Nothing to download: the file is committed to the repository. The
[data dictionary](../../data/spine/dictionaries/S05-fdi.md) names every source, every trap, and
the six places where the rebuild had to substitute for a series the original publisher has since
withdrawn.

This is a genuinely wide problem: 56 candidates, many of them correlated, and a sample that
shrinks fast once you require them all. Exactly where regularisation earns its keep.

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
