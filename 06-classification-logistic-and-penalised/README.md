# Session 06 — Classification: Logistic Regression, Regularisation, and Decision Thresholds

> **Your classifier is 97% accurate. Should anyone be impressed?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Can we flag a country or sector falling behind one year ahead — and what does a false alarm cost?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your angle, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive the logistic model from the log-odds link and from a latent-variable formulation.
- Write the log-likelihood, derive the score and Hessian, prove concavity, and explain IRLS.
- Explain what perfect separation does to the MLE and why a penalty cures it.
- Compose the Session 5 elastic-net penalty with the logistic likelihood, and state the resulting coordinate update.
- Interpret coefficients as log-odds, odds ratios, and average marginal effects.
- Choose a decision threshold from an explicit cost ratio, and assess calibration and selection stability.

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | Reading, concept review, data download, self-check | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: the mathematics of the method | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-lab/`](02-lab/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive with the reading done and
a working environment; the lab assumes you arrive with the data already downloaded.

---

## Data for this session

**Statlog German Credit (1,000 applicants, 20 features) + Polish/Taiwanese company bankruptcy (wide and severely imbalanced)**

Source: UCI Machine Learning Repository
URL: https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-lab/submissions/group-XX/` containing: the IRLS implementation, the
three-metric coefficient table, the cost curve with the optimal threshold marked, the reliability
diagram, and (Track B) the calibration comparison and stability plot.

Plus a **400-word memo to a credit committee** that (a) states the recommended threshold and its
cost justification, (b) names which features are *robustly* selected and explicitly refuses to
over-claim about the others, and (c) raises the group-disparity finding without resolving it
prematurely.

---

## Before the next session

- ISLR ch. 8 (tree-based methods) before Session 7.

---

[<- Session 05: Regularisation: Ridge, Lasso, and the Elastic Net](../05-ridge-lasso-elastic-net/README.md) | [Session 07: Trees, Forests, and Gradient Boosting ->](../07-trees-forests-boosting/README.md)
