# Session 07 — Trees, Forests, and Gradient Boosting

> **If we abandon linearity, what do we lose - and is interpretability recoverable?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-07-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S07-Lecture.qmd`](01-lecture/MATH60033A-S07-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Is the relationship non-linear — and can you still explain it to a minister?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive recursive binary splitting and the impurity criteria (Gini, entropy, variance reduction).
- Explain cost-complexity pruning and the weakest-link algorithm.
- Show why bagging reduces variance, and quantify the limit imposed by inter-tree correlation.
- Derive gradient boosting as functional gradient descent in the space of predictors.
- Interpret a black-box model with permutation importance, partial dependence, and Shapley values - and state each method's assumptions.

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | Reading, concept review, data download, self-check | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: the mathematics of the method | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive with the reading done and
a working environment; the practice session assumes you arrive with the data already downloaded.

---

## Data for this session

**Ames Housing (regression) + Bank Marketing (classification)**

Source: OpenML / UCI
URL: https://archive.ics.uci.edu/dataset/222/bank+marketing

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-practice/submissions/group-XX/` with the five-model comparison table, the OOB-vs-$m$
curve, PDP/ICE and SHAP figures, and a 400-word note: *you must present one model to a municipal
housing authority. Which do you choose, and how do you defend the choice on grounds other than
RMSE?*

---

## Before the next session

- ISLR ch. 12.1-12.2 (PCA) before Session 8.

---

[<- Session 06: Classification: Logistic Regression, Regularisation, and Decision Thresholds](../06-advanced-regression/README.md) | [Session 08: Unsupervised Learning I: PCA, the SVD, and Factor Models in Macroeconomics ->](../08-knn-and-bias-variance/README.md)
