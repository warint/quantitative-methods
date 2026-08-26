# Session 08 — K-Nearest Neighbours and the Bias–Variance Trade-off

> **Flexible, or just unstable?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-08-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S08-Lecture.qmd`](01-lecture/MATH60033A-S08-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Does flexibility buy you anything on your own data?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- State the **Bayes classifier** and say why no rule can beat it
- Compute a Euclidean distance and find nearest neighbours **by hand**
- Explain why KNN requires **standardised** predictors
- Choose $k$ by cross-validation, and read the trade-off the curve shows
- Say what happens to KNN as the number of predictors grows

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: the Bayes classifier, distance, choosing $k$ by cross-validation | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**The course spine, plus the smarket returns used in the lecture** — one line to load it:

```python
import qmib
data = qmib.load("core")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a KNN classifier on a binary outcome from your angle, with $k$ chosen by cross-validation, compared against a sensible benchmark, and a note on whether the flexibility earned its keep.

---

[<- [Session 07: Principal Component and Factor Analyses](../07-pca-and-factor-analysis/README.md)](../07-pca-and-factor-analysis/README.md) | [[Session 09: Structural Equation Modelling](../09-structural-equation-modelling/README.md) ->](../09-structural-equation-modelling/README.md)
