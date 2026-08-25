# Session 10 — Causal Machine Learning: Double/Debiased ML and Heterogeneous Effects

> **You have a superb predictive model. Why can you still not use it to choose a policy?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Did the policy do anything, or did we just measure the countries that were already ahead?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- State the potential-outcomes framework and the identifying assumptions for conditional ignorability.
- Explain why naively plugging an ML estimate of the nuisance function into a treatment-effect regression fails.
- Derive the Neyman-orthogonal score for the partially linear model and show why it is insensitive to first-stage error.
- Explain cross-fitting and why it removes the overfitting bias term.
- Estimate an average treatment effect with DML and explore heterogeneity with a causal forest.

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

**401(k) eligibility and financial wealth (the DML canonical example), or the NSW/LaLonde job-training data**

Source: Available via the `doubleml` Python package; LaLonde via `causaldata`
URL: https://docs.doubleml.org/stable/examples/py_double_ml_pension.html

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-practice/submissions/group-XX/` with your from-scratch DML implementation, the
estimator comparison table (naive / OLS / DML with three learners / package), the split-sensitivity
plot, the heterogeneity projection, and a 500-word memo whose *first* paragraph is the
identification argument and whose last sentence states what would change your conclusion.

---

## Before the next session

- Mitchell et al. (2019), 'Model Cards for Model Reporting', before Session 11.
- Bring a draft of your final-project analysis to Session 11 - the practice is a workshop on it.

---

[<- Session 09: Unsupervised Learning II: Clustering, Embeddings, and Text as Data](../09-structural-equation-modelling/README.md) | [Session 11: Forecasting, Distribution Shift, and Model Governance ->](../11-causal-inference-did/README.md)
