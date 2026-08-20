# Session 02 — Data, Vectors, and the Geometry of Least Squares

> **Why is the most-used estimator in economics a right-angle triangle?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### How much of the measured gap is real, and how much is composition?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive the OLS estimator from first-order conditions **and** from an orthogonal projection argument.
- Interpret the hat matrix, fitted values, and residuals geometrically.
- Explain the role of $\mathrm{rank}(X)$ and diagnose multicollinearity as near-rank-deficiency.
- Implement OLS from scratch in NumPy and reconcile it, to numerical precision, with `statsmodels`.
- Explain why the normal equations are numerically dangerous and what QR decomposition does instead.

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

**Ames Housing (2,930 residential sales, 79 features)**

Source: OpenML / scikit-learn `fetch_openml`
URL: https://www.openml.org/d/42165

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

A commented script or notebook `02-practice/submissions/group-XX/` that runs
end-to-end from the cached parquet file, plus a 250-word note answering: *why did the QR route
survive the collinearity you introduced, and what does that tell you about interpreting
coefficients when predictors are nearly redundant?*

---

## Before the next session

- ISLR ch. 3.3 before Session 3.
- Optional: Angrist & Pischke, *Mostly Harmless Econometrics*, ch. 3 on regression anatomy.

---

[<- Session 01: Foundations: Scenarios, Tools, and the Supervised Learning Problem](../01-foundations-scenarios-and-tools/README.md) | [Session 03: Linear Regression: Inference, Diagnostics, and Interpretation ->](../03-inference-diagnostics-interpretation/README.md)
