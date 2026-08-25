# Session 10 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey & Robins (2018), 'Double/Debiased Machine Learning for Treatment and Structural Parameters', Econometrics Journal 21(1)**  
Source: https://doi.org/10.1111/ectj.12097  
*Why:* The central paper. Read the introduction and section 1 carefully; the intuition in section 1.1 is the lecture.

**Athey & Imbens (2019), 'Machine Learning Methods That Economists Should Know About', Annual Review of Economics 11**  
Source: https://doi.org/10.1146/annurev-economics-080217-053433  
*Why:* Situates DML among the alternatives.

**Wager & Athey (2018), 'Estimation and Inference of Heterogeneous Treatment Effects using Random Forests', JASA 113(523)**  
Source: https://doi.org/10.1080/01621459.2017.1319839  
*Why:* Causal forests, for the second half of the practice.


---

## Step 2 — Concepts to review

Return to Session 2 and re-read the **Frisch-Waugh-Lovell** theorem. Today's method is FWL with
machine learning in the residualisation steps, plus one crucial extra ingredient (cross-fitting)
that makes it work.

If you can state FWL from memory, this session will feel inevitable rather than magical.

Also settle the vocabulary: $Y_i(1)$ and $Y_i(0)$ are the potential outcomes; we observe
$Y_i = D_iY_i(1) + (1-D_i)Y_i(0)$. The **fundamental problem of causal inference** is that we never
observe both. Everything else is an argument about how to fill in the missing one.

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

**Before class:** Nominate a treatment with a date, and name the confounder you are most worried about. If you cannot name one, you have not thought hard enough about it.

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

**401(k) eligibility and financial wealth (the DML canonical example), or the NSW/LaLonde job-training data**

Source: Available via the `doubleml` Python package; LaLonde via `causaldata`
URL: <https://docs.doubleml.org/stable/examples/py_double_ml_pension.html>

```python
from doubleml.datasets import fetch_401K
df = fetch_401K(return_type="DataFrame")
df.to_parquet("data/pension401k.parquet")
```

The 401(k) example is ideal: eligibility is plausibly exogenous conditional on income and
demographics, the sample is large, and the literature gives a benchmark estimate to compare against.
The LaLonde data is the harder, more humbling case - the experimental benchmark is known, and most
observational methods miss it.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. State the three assumptions needed for the ATE to be identified from observational data under conditional ignorability.
2. Why does regularisation bias, which is harmless for prediction, become fatal for treatment-effect estimation?
3. In the DML score $\psi = (Y - \ell(X) - \theta(D - m(X)))(D - m(X))$, verify that the Gateaux derivative with respect to the nuisance functions is zero at the truth.
4. Why must the fold used to estimate the nuisance functions differ from the fold used to estimate $\theta$?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Explain why two nuisance functions each converging at n^{-1/4} is enough for root-n inference on theta. Show the product structure."
- "My DML estimate changes a lot depending on the random split. Is that a bug or a feature? What should I report?"
- "Give me the strongest argument that 401(k) eligibility is NOT conditionally ignorable."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 10](../README.md)
