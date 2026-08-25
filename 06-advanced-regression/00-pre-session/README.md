# Session 06 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 4.1-4.3**  
Source: https://www.statlearning.com/  
*Why:* Why not linear probability; the logistic model; multiple logistic regression.

**ESL sec. 4.4 and 18.3**  
Source: https://hastie.su.domains/ElemStatLearn/  
*Why:* The IRLS derivation in full, and regularised logistic regression in the p >> n regime.

**Friedman, Hastie & Tibshirani (2010), 'Regularization Paths for Generalized Linear Models via Coordinate Descent', J. Stat. Software 33(1)**  
Source: https://doi.org/10.18637/jss.v033.i01  
*Why:* The glmnet paper. Read sections 2-3 only - it is exactly the algorithm we assemble in class.


---

## Step 2 — Concepts to review

**This session composes two things you already have.** From Session 5: the soft-thresholding
operator and the elastic-net coordinate update. From today's first hour: the reformulation of
logistic regression as weighted least squares. Sketch, before class, how you think they combine.
Most of you will guess correctly - which is the point. You are now able to *derive* a method rather
than look it up.

Two further preliminaries.

**Why not just run OLS on a 0/1 outcome?** The linear probability model is not absurd - its
coefficients are directly interpretable as marginal effects, and it is still widely used in applied
economics. Its defects are: fitted values outside $[0,1]$, inherent heteroskedasticity
($\mathrm{Var}(y|x) = p(x)(1-p(x))$), and a functional form that cannot respect the natural
compression of probabilities near the boundaries. Come with an opinion on when you would use it
anyway.

**Concavity.** Recall that a twice-differentiable function is concave iff its Hessian is negative
semi-definite. We use this to prove that the logistic MLE has no local optima to trap us - a
guarantee most later methods in this course do not enjoy.

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

**Before class:** Merge `falling_behind_next` from `core.parquet` onto your file. Report the base rate in your sample, and think about what a false alarm would cost a European agency in your domain.

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

**Statlog German Credit (1,000 applicants, 20 features) + Polish/Taiwanese company bankruptcy (wide and severely imbalanced)**

Source: UCI Machine Learning Repository
URL: <https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data>

**German Credit** ships with an explicit **cost matrix**: classifying a bad customer
as good is stated to be five times worse than the reverse. This is unusual and pedagogically
valuable - it forces the threshold question into the open rather than letting 0.5 pass unexamined.

```python
from sklearn.datasets import fetch_openml
d = fetch_openml("credit-g", version=1, as_frame=True, parser="auto")
d.frame.to_parquet("data/credit_g.parquet")
```

**Bankruptcy data** (<https://archive.ics.uci.edu/dataset/365/polish+companies+bankruptcy+data>)
supplies the high-dimensional half: 64 highly correlated financial ratios, 2-5% positive rate,
substantial missingness. Every pathology in the lecture appears in it.

```python
from scipy.io import arff
import pandas as pd
data, meta = arff.loadarff("data/3year.arff")
pd.DataFrame(data).to_parquet("data/polish_3y.parquet")
```

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Derive $p(x) = \frac{e^{x^\top\beta}}{1 + e^{x^\top\beta}}$ from the assumption that $\log\frac{p}{1-p} = x^\top\beta$.
2. A coefficient is 0.7. State its meaning as a log-odds and as an odds ratio, and explain why you cannot read it as a probability change without more information.
3. A dataset has 2% positives. A model predicts 'negative' always. What is its accuracy, and what is its recall?
4. Why can the penalised logistic MLE exist under perfect separation, where the unpenalised one does not?
5. You oversample the minority class 5:1. What happens to your predicted probabilities?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "My logistic regression has a coefficient of 24 with a standard error of 4000. Diagnose the problem."
- "Explain the difference between an odds ratio of 2 and a doubling of probability. Give a numerical example where they diverge sharply."
- "My AUC is 0.93 but my precision at the operating threshold is 0.11. Explain how both can be true."
- "Derive the intercept correction for a logistic model fitted on an oversampled training set."
- "Argue both sides: should a credit model be required to equalise false positive rates across nationality groups?"

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 06](../README.md)
