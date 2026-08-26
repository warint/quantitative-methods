# Session 10 — Causal Inference I: Counterfactuals, Randomisation, Matching

> **Did the policy do anything, or were the groups different to begin with?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-10-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S10-Lecture.qmd`](01-lecture/MATH60033A-S10-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Can your project support a causal claim at all?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- State the **fundamental problem of causal inference**
- Explain why **randomisation** solves it, and what it costs
- Estimate a **propensity score** and use it to match treated to control units
- Check **overlap** and **balance**, and say what to do when they fail
- Report an **ATT**, and state the assumption it rests on

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: potential outcomes, randomisation, propensity scores, matching | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**The spine's documented treatment, with a known effect to recover** — one line to load it:

```python
import qmib
data = qmib.load("core")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a matched comparison on your own data: the naive difference, the overlap check, the balance table, the matched estimate, and the paragraph defending conditional ignorability — that paragraph carries the marks.

---

[<- [Session 09: Structural Equation Modelling](../09-structural-equation-modelling/README.md)](../09-structural-equation-modelling/README.md) | [[Session 11: Causal Inference II: Difference-in-Differences](../11-causal-inference-did/README.md) ->](../11-causal-inference-did/README.md)
