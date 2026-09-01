# Session 06 — Regression: Advanced Considerations

> **Does the relationship hold across countries, and across years?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-06-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S06-Lecture.qmd`](01-lecture/MATH60033A-S06-Lecture.qmd).

**Wednesday 7 October 2026** · 15:30–18:30 · Décelles — Victoriaville · **asynchronous**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Does your finding survive the structure of your data?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- State what a **panel** is, and why pooling it with OLS understates uncertainty
- Distinguish **fixed** from **random** effects, and say what each assumes
- Fit a quadratic term and interpret a **non-linear** relationship in units
- Read an **interaction** as a slope that differs between groups
- Compare non-nested models on information criteria rather than an F-test

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: panel data, fixed and random effects, non-linearity, interactions | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**A country panel of government debt and economic-freedom indices** — one line to load it:

```python
import qmib
data = qmib.load("panel")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `groups/A2026/group-XX/session-06/`: a panel specification of your project's core relationship, fitted with both fixed and random effects, plus a 250-word note on which you would report and why.

---

[<- [Session 05: Regularisation: Ridge, Lasso, and the Elastic Net](../05-ridge-lasso-elastic-net/README.md)](../05-ridge-lasso-elastic-net/README.md) | [[Session 07: Principal Component and Factor Analyses](../07-pca-and-factor-analysis/README.md) ->](../07-pca-and-factor-analysis/README.md)
