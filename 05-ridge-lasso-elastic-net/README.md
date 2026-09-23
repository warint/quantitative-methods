# Session 05 — Regularisation: Ridge, Lasso, and the Elastic Net

> **When is a deliberately biased estimator the better one?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-05-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S05-Lecture.qmd`](01-lecture/MATH60033A-S05-Lecture.qmd).

**Wednesday 23 September 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Of two hundred indicators, which few actually carry the signal?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive the ridge estimator in closed form and show how it shrinks the SVD spectrum.
- Explain geometrically why the lasso produces exact zeros and ridge does not.
- State the elastic net objective and explain what the $\ell_2$ component adds under correlated predictors.
- Derive the coordinate-descent update for the lasso, including the soft-thresholding operator.
- Select $(\alpha, \lambda)$ by cross-validation and interpret the resulting model honestly.

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | Reading, concept review, data download, self-check | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: the mathematics of the method | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |
| **After class** | At home, optional | The **QMIB Lab** — a knowledge check on this session | [warin.ca/qmib-labs](https://warin.ca/qmib-labs/qmib-lab-05.html) |

The pre-session work is **not optional**. The lecture assumes you arrive with the reading done and
a working environment; the practice session assumes you arrive with the data already downloaded.

---

## Data for this session

**56 candidate determinants of bilateral FDI, 2019**

The dataset behind Blonigen & Piger (2014), rebuilt from the sources the paper names.
7,051 directed country pairs; every number real.

```python
import qmib
fdi = qmib.load("fdi")
```

Sources: OECD (FDI positions) · CEPII Gravity · World Development Indicators · Freedom House
Built by [`scripts/build_fdi_determinants.py`](../scripts/build_fdi_determinants.py) ·
[data dictionary](../data/spine/dictionaries/S05-fdi.md)

---

## Deliverable

`groups/A2026/group-XX/session-NN/` with the coordinate-descent implementation,
the CV surface, the stability plot, and a 300-word note answering: *a trade ministry asks which
factors attract foreign direct investment. Given your stability results, what can you honestly
tell them, and what must you refuse to claim?*

---

## Before the next session

- Read the Session 06 article and download its Dataverse package before the next lecture.

---

[<- Session 04: The Bias-Variance Tradeoff, Overfitting, and Cross-Validation](../04-logistic-ordinal-multinomial/README.md) | [Session 06: Classification: Logistic Regression, Regularisation, and Decision Thresholds ->](../06-advanced-regression/README.md)
