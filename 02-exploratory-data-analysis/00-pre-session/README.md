# Session 02 — Pre-session preparation

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-02-pre-session.html)** ·
> source: [`MATH60033A-S02-Pre-Session.qmd`](MATH60033A-S02-Pre-Session.qmd)

> Complete **all three steps** before class. Expect 90–120 minutes, plus 45 for the git setup below.

| | Before class | Used in the practice for |
|---|---|---|
| **1** | Read the paper | reproducing one of its results |
| **2** | Get **both** datasets | that, and profiling your own angle |
| **3** | Set up git and your group repository | pushing your work, this session and every session after |

---

## ⚠️ Session 2 only — set up git and clone the course repository

Before the three steps below, work through
**[`setup-git-and-github.md`](setup-git-and-github.md)**. Budget 45 minutes.

From this session onward you are assessed as a group, and your commit history is one of the four
records used to check that all three members did the work. That record only exists if git knows
who you are.

**Session 01 gave you a ZIP. A ZIP cannot push, so from here you work in a clone:**

```bash
cd ~/Desktop                     # Windows: Set-Location "$HOME\Desktop"
git clone https://github.com/warint/quantitative-methods.git
cd quantitative-methods

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -c "import qmib; print(qmib.load('core').shape)"   # expect (450, 11)
```

Then delete the unzipped Session 01 folder, so there is only one copy of the course on your
machine.

There is **no separate group repository**. Everyone works in this one, and each group has a
branch, `group-XX`. You must arrive having cloned it and pushed at least one commit to your
group's branch from your own machine — which needs you to be added as a **collaborator** first,
so send your GitHub username to the instructor if you have not.

Slides: [`slides-github-and-teamwork.qmd`](slides-github-and-teamwork.qmd) — the same material,
walked through.

---

## Step 1 — Reading

**Fraiberger et al. (2021), *Media sentiment and international asset prices***
[Read the article](https://doi.org/10.1016/j.jinteco.2021.103526)

You reproduce one of its results in the first twenty minutes of the practice, so read it with that
in mind.

Read for the **argument**, not for coverage. Annotate four things:

| | |
|---|---|
| **1** | The research question, in one sentence |
| **2** | How they build the sentiment measure |
| **3** | The strongest single piece of evidence |
| **4** | One limitation you would raise as a referee |

*Optional background:* **ISLR ch. 2** — <https://www.statlearning.com/> — for the vocabulary
Session 02 uses.

---

## Step 2 — Concepts to review

Refresh these before class; we will use them without re-deriving them.

- **Mean and median.** The mean is the balance point; the median is the middle of the ordering.
- **Variance and standard deviation.** $s^2 = \frac{1}{n-1}\sum_i (x_i - \bar x)^2$ — note the $n-1$.
- **Quantiles.** $\tilde q_p$ is the value below which about $100p\%$ of the data falls.
- **A straight line.** $y = \beta_0 + \beta_1 x$: what the intercept and the slope each mean.

If any of these is unfamiliar, work through it with your local LLM *before* class, and bring your
worked notes.

---

## Step 3 — Get both datasets

The practice uses **two**, and both should be on your machine before you arrive.

### a) The paper's replication package

This is what you reproduce in the first twenty minutes.

**Harvard Dataverse: [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF)**

Download once and unzip into `02-exploratory-data-analysis/data/replication/`. That folder is
git-ignored, so nothing large is committed. Keep the authors' own structure and README.

### b) The course data, for your own angle

This is what you apply the method to in the second half. It is **already cleaned and cached** —
one line, nothing to download.

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
import qmib

core = qmib.load("core")                 # shared by every group
mine = qmib.load("angle_c_country")      # YOUR file — see the table above
df   = core.merge(mine, on=["geo", "time"], how="inner")   # not for angle E

print(core.shape, mine.shape, df.shape)
```

> `qmib.load()` resolves the local cache first, so after the first run the practice works with the
> wifi off. `qmib.catalog()` lists everything available.

**Before class:** load your file, join it to `core`, and pick the **three variables** your research
question depends on most — the outcome, and the two you most expect to explain it. Write down one
sentence on why you chose each. That is what you profile in the practice.

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
the practice.**

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
