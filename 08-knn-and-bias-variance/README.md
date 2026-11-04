# Session 08 — K-Nearest Neighbours and the Bias–Variance Trade-off

> **Flexible, or just unstable?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-08-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S08-Lecture.qmd`](01-lecture/MATH60033A-S08-Lecture.qmd).

> **Python cheatsheets for this session**, one per package, functions explained with
> pictures: [pandas](https://warint.github.io/quantitative-methods/python-cheatsheets/pandas.pdf) · [NumPy](https://warint.github.io/quantitative-methods/python-cheatsheets/numpy.pdf) · [matplotlib](https://warint.github.io/quantitative-methods/python-cheatsheets/matplotlib.pdf) · [scikit-learn](https://warint.github.io/quantitative-methods/python-cheatsheets/sklearn.pdf)

**Wednesday 4 November 2026** · 15:30–18:30 · Décelles — Victoriaville

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
| **After class** | At home, optional | The **QMIB Lab** — a knowledge check on this session | [warin.ca/qmib-labs](https://warin.ca/qmib-labs/qmib-lab-08.html) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**The Jordà–Schularick–Taylor Macrohistory Database — 18 economies, 1870–2020, 88 financial crises, with the paper's predictors already derived** — read by URL, in a folder of your own, with nothing but pandas:

```python
import pandas as pd

SITE = "https://warint.github.io/quantitative-methods/data/"
jst  = pd.read_csv(SITE + "session-08/jst_crises.csv")   # the paper's data
core = pd.read_csv(SITE + "core.csv")                    # shared by every group
mine = pd.read_csv(SITE + "angle_c_country.csv")         # YOUR angle — see your dictionary
```

The practice starter, [`02-practice/starter/session08_practice.py`](02-practice/starter/session08_practice.py), does this and the rest.

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## What you leave with

Nothing to hand in — this is practice. In your own folder: a KNN classifier on a binary outcome from your angle, with $k$ chosen by cross-validation, compared against a sensible benchmark, and a note on whether the flexibility earned its keep.

---

[<- [Session 07: Replication Workshop: Five Papers, One Toolkit](../07-replication-workshop/README.md)](../07-replication-workshop/README.md) | [[Session 09: Structural Equation Modelling](../09-structural-equation-modelling/README.md) ->](../09-structural-equation-modelling/README.md)
