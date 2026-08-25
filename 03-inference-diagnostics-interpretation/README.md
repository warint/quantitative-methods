# Session 03 — Linear Regression: Inference, Diagnostics, and Interpretation

> **Your coefficient has a standard error. Under what conditions does that number mean anything?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Which of these differences would survive a referee?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- State the Gauss-Markov assumptions and prove that OLS is BLUE under them.
- Derive $\mathrm{Var}(\hat\beta)$ and explain each term's economic content.
- Explain heteroskedasticity- and cluster-robust standard errors, and know when each is required.
- Quantify omitted variable bias and sign it in a real application.
- Estimate and interpret a Mincer earnings equation, distinguishing what the coefficients do and do not identify.

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

**CPS / IPUMS-style wage microdata (use the Wooldridge `wage2` or CPS 1985 extract)**

Source: `statsmodels` datasets, or the Wooldridge R package data mirrored as CSV
URL: https://cran.r-project.org/package=wooldridge

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-practice/submissions/group-XX/mincer.md` with the three-column results table,
two diagnostic plots, your predicted-vs-actual OVB calculation, and the interpretation paragraph.
The paragraph is worth as much as the code.

---

## Before the next session

- ISLR ch. 5 (resampling methods) before Session 4. This is the pivot of the course.

---

[<- Session 02: Exploratory Data Analysis: Centre, Spread, and Shape](../02-exploratory-data-analysis/README.md) | [Session 04: The Bias-Variance Tradeoff, Overfitting, and Cross-Validation ->](../04-bias-variance-and-cross-validation/README.md)
