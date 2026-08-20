# Session 03 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**ISLR ch. 3.3**  
Source: https://www.statlearning.com/  
*Why:* Potential problems in regression: non-linearity, correlated errors, outliers, collinearity.

**Mincer (1974), *Schooling, Experience and Earnings* - concept summary**  
Source: Any labour economics text; or ask your local LLM for the functional form and check it  
*Why:* The lab estimates this equation. Know why log wages and why experience enters as a quadratic.


---

## Step 2 — Concepts to review

Come to class able to state, without notes, the five classical assumptions:

1. **Linearity in parameters:** $y = X\beta + \varepsilon$.
2. **Strict exogeneity:** $\mathbb{E}[\varepsilon \mid X] = 0$.
3. **No perfect collinearity:** $\operatorname{rank}(X) = p$.
4. **Homoskedasticity and no autocorrelation:** $\operatorname{Var}(\varepsilon \mid X) = \sigma^2 I_n$.
5. **(For exact inference)** $\varepsilon \mid X \sim \mathcal{N}(0, \sigma^2 I_n)$.

Note carefully which results need which assumption. Unbiasedness needs 1-3. Efficiency needs 4.
$t$ and $F$ distributions in finite samples need 5.

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

**Before class:** Decide, before class, at which level you will cluster your standard errors, and write one sentence defending it. Then name one variable that is missing from your file and would plausibly confound your Session 02 result.

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

**CPS / IPUMS-style wage microdata (use the Wooldridge `wage2` or CPS 1985 extract)**

Source: `statsmodels` datasets, or the Wooldridge R package data mirrored as CSV
URL: <https://cran.r-project.org/package=wooldridge>

A clean, dependency-free option:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/JeffSackmann/.../cps85.csv"  # replace with your mirror
```

**Recommended:** the instructor will place `data/wages.csv` in the shared repo before class so the
lab has no network dependency. Verify with `md5sum` against the value in `data/CHECKSUMS.txt`.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Which assumption fails if you regress euro-area country GDP growth on a common EU-level policy variable using country-year data? What is the practical consequence?
2. Show that $\mathbb{E}[\hat\beta \mid X] = \beta$ requires only assumptions 1-3.
3. You suspect an omitted variable positively correlated with schooling and positively affecting wages. Sign the bias on the schooling coefficient.
4. Why is $R^2$ not a measure of whether a model is *correct*?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "My robust standard errors are SMALLER than my classical ones. Is that possible? Under what conditions?"
- "Critique this sentence as a hostile referee: '<paste your interpretation paragraph>'"
- "Explain the difference between clustering at the individual level and at the industry level for panel wage data."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 03](../README.md)
