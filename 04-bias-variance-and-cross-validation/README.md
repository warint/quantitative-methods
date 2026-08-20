# Session 04 — The Bias-Variance Tradeoff, Overfitting, and Cross-Validation

> **Your model fits the past perfectly. Why is that bad news?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Are we predicting, or only describing the past?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive the bias-variance decomposition of expected prediction error, term by term.
- Explain why in-sample error is a *biased* estimate of out-of-sample error, and quantify the optimism.
- Implement K-fold and leave-one-out cross-validation correctly, including the pitfalls of leakage.
- Read a learning curve and a validation curve, and say what each diagnoses.
- Explain why cross-validation must respect the dependence structure of economic data.

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

**Ames Housing (continued) + a synthetic polynomial DGP**

Source: Cached from Session 2 + generated locally
URL: https://www.openml.org/d/42165

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-lab/submissions/group-XX/` containing the bias-variance figure, a table
reporting CV error under correct and leaked procedures (with the optimism in each case), and a
200-word note: *which leak was most dangerous, and why is it the hardest one to notice in a
referee report?*

---

## Before the next session

- ISLR ch. 6.2 (shrinkage methods) before Session 5. Read it twice.

---

[<- Session 03: Linear Regression: Inference, Diagnostics, and Interpretation](../03-inference-diagnostics-interpretation/README.md) | [Session 05: Regularisation: Ridge, Lasso, and the Elastic Net ->](../05-ridge-lasso-elastic-net/README.md)
