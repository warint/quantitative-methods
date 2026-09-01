# Session 09 — Structural Equation Modelling

> **Can you measure something you cannot observe?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-09-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S09-Lecture.qmd`](01-lecture/MATH60033A-S09-Lecture.qmd).

**Wednesday 11 November 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### What is the construct behind your indicators?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Distinguish the **measurement** model from the **structural** model
- Write a model description and read `=~` as "is measured by"
- Interpret a **standardised loading**, and say when an indicator is weak
- Report **CFI, TLI and RMSEA**, and say what each would have to be
- State why good fit is not evidence that the model is correct

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: measurement and structural models, latent variables, fit indices | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**A 14-item questionnaire on purchase decisions, plus semopy's bundled examples** — one line to load it:

```python
import qmib
data = qmib.load("efa")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `groups/A2026/group-XX/session-09/`: a measurement model for one construct in your project, with the loadings reported, the fit indices stated, and a note on the indicators you would drop and why.

---

[<- [Session 08: K-Nearest Neighbours and the Bias–Variance Trade-off](../08-knn-and-bias-variance/README.md)](../08-knn-and-bias-variance/README.md) | [[Session 10: Causal Inference I: Counterfactuals, Randomisation, Matching](../10-causal-inference-foundations/README.md) ->](../10-causal-inference-foundations/README.md)
