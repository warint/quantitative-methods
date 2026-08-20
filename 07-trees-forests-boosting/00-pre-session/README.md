# Session 07 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 8**  
Source: https://www.statlearning.com/  
*Why:* Trees, bagging, random forests, boosting.

**ESL sec. 9.2, 10.1-10.10, 15**  
Source: https://hastie.su.domains/ElemStatLearn/  
*Why:* The gradient-boosting derivation and the random-forest variance analysis.

**Molnar, *Interpretable Machine Learning*, ch. on PDP, permutation importance and SHAP**  
Source: https://christophm.github.io/interpretable-ml-book/  
*Why:* The interpretation half of the practice.


---

## Step 2 — Concepts to review

A conceptual point to settle before class: **trees are not a model of the world, they are a
partition of it.** A regression tree approximates $f$ by a step function on axis-aligned boxes.
This is why they handle interactions and non-monotonicity effortlessly, and why they extrapolate
terribly and produce discontinuous predictions.

Ask yourself: for which economic quantities is a step-function approximation a natural
representation, and for which is it a distortion?

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

**Before class:** Re-run your Session 05 elastic net and save the fold indices. You need identical folds for the comparison, and re-splitting invalidates it.

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

**Ames Housing (regression) + Bank Marketing (classification)**

Source: OpenML / UCI
URL: <https://archive.ics.uci.edu/dataset/222/bank+marketing>

Reusing Ames lets you compare directly against your Session 2-5 linear results on identical
folds - which is the point of the practice. Keep the same random seed and the same CV splits.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Why is finding the globally optimal tree NP-hard, and what does the greedy algorithm give up?
2. Bagging $B$ trees each with variance $\sigma^2$ and pairwise correlation $\rho$: what is the variance of the average, and what is its limit as $B \to \infty$?
3. Random forests choose $m < p$ features at each split. Which term in that variance formula does this target?
4. Why do impurity-based feature importances favour high-cardinality and continuous variables?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Explain why permutation importance is misleading when two features are correlated at 0.95. Use a concrete example."
- "My gradient boosting model has training RMSE near zero and test RMSE worse than OLS. List the three most likely causes in order."
- "What is the difference between a partial dependence plot and an ICE plot, and when does the difference matter?"

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 07](../README.md)
