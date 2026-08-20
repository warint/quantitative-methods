# Session 02 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes, plus 45 for the setup below.

---

## ⚠️ Session 2 only — set up git and your group repository

Before the four steps, work through
**[`setup-git-and-github.md`](setup-git-and-github.md)**. Budget 45 minutes.

From this session onward you are assessed as a group, and your commit history is one of the four
records used to check that all three members did the work. That record only exists if git knows
who you are.

You must arrive with a private group repository that your teammates **and the instructor** can
see, and with at least one commit pushed from your own machine.

Slides: [`slides-github-and-teamwork.qmd`](slides-github-and-teamwork.qmd)

---

## Step 1 — Reading

**ISLR ch. 3.1-3.2**  
Source: https://www.statlearning.com/  
*Why:* Applied framing of the multiple regression model.

**Hastie, Tibshirani & Friedman, *Elements of Statistical Learning* (ESL), sec. 3.2**  
Source: https://hastie.su.domains/ElemStatLearn/  
*Why:* The projection-geometry treatment we develop in the lecture.


---

## Step 2 — Concepts to review

Refresh these before class - we will use them without re-deriving them.

- **Inner product and orthogonality.** $\langle a, b\rangle = a^\top b$; $a \perp b \iff a^\top b = 0$.
- **Column space.** $\mathcal{C}(X) = \{X\beta : \beta \in \mathbb{R}^p\}$, a subspace of $\mathbb{R}^n$.
- **Idempotent matrices.** $P$ is a projection iff $P^2 = P$; it is an *orthogonal* projection iff also $P^\top = P$.
- **Rank and invertibility.** $X^\top X$ is invertible iff $X$ has full column rank.

If any of these is unfamiliar, work through them with your local LLM *before* class, and bring your
worked notes.

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

**Before class:** Load your file, join to `core.parquet`, and identify **one outcome** and **three structural controls** you could partial out. Write the regression equation you intend to estimate. Bring it written down.

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

**Ames Housing (2,930 residential sales, 79 features)**

Source: OpenML / scikit-learn `fetch_openml`
URL: <https://www.openml.org/d/42165>

Download once and cache locally:

```python
from sklearn.datasets import fetch_openml
ames = fetch_openml(name="house_prices", as_frame=True, parser="auto")
ames.frame.to_parquet("data/ames.parquet")
```

Everything after the first run reads the local parquet file. **No network access is needed during
the lab.**

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Show that if $P = X(X^\top X)^{-1}X^\top$ then $P^2 = P$ and $P^\top = P$.
2. What is the trace of the hat matrix, and why does that number have a name you already know?
3. If two columns of $X$ are perfectly collinear, what fails - and does the *fitted value* $\hat y$ still exist?
4. Why does adding a variable never decrease $R^2$? Answer geometrically, not algebraically.

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "I get a LinAlgError: Singular matrix. Explain what this means about the geometry of my design matrix, without giving me code."
- "Walk me through the Frisch-Waugh-Lovell theorem using a two-regressor example with numbers."
- "Explain the difference between numpy.linalg.inv, numpy.linalg.solve and numpy.linalg.lstsq in terms of numerical stability."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 02](../README.md)
