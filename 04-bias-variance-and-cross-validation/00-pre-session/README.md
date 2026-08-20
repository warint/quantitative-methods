# Session 04 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 5.1**  
Source: https://www.statlearning.com/  
*Why:* Validation set, LOOCV, K-fold, and the bias-variance tradeoff for K.

**ESL sec. 7.1-7.5**  
Source: https://hastie.su.domains/ElemStatLearn/  
*Why:* The rigorous version: optimism, effective degrees of freedom, and why in-sample error misleads.


---

## Step 2 — Concepts to review

This session is the hinge of the course. Everything before it treats the model as given; everything
after it treats **model selection** as the central problem.

Come with a written answer to this question: *if a more flexible model always fits the observed data
at least as well, why would anyone ever choose a less flexible one?* One paragraph. We will collect
these and read three aloud.

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

**Before class:** Work out the dependence structure of your file: is it a panel, a repeated cross-section, a time series, a corpus? Write down which cross-validation scheme that implies, and why.

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

**Ames Housing (continued) + a synthetic polynomial DGP**

Source: Cached from Session 2 + generated locally
URL: <https://www.openml.org/d/42165>

The synthetic part lets you *see* bias and variance separately, because you know the truth.
The Ames part shows you what it looks like when you do not.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. In the decomposition $\mathbb{E}[(y_0 - \hat f(x_0))^2] = \operatorname{Var}(\hat f(x_0)) + [\operatorname{Bias}(\hat f(x_0))]^2 + \sigma^2$, which term can you drive to zero, and which can you not?
2. For LOOCV, is the bias of the error estimate high or low? What about its variance? Explain the tradeoff in K.
3. You standardise your features using the full dataset, then run 5-fold CV. What exactly has gone wrong?
4. Why is random K-fold CV inappropriate for quarterly GDP data?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Review this scikit-learn code for data leakage. Point to specific lines: <paste>"
- "Explain why LOOCV has higher variance than 10-fold CV, even though it has lower bias."
- "Design a cross-validation scheme for quarterly euro-area data where I want to forecast 4 quarters ahead. Justify each choice."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 04](../README.md)
