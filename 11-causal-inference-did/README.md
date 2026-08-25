# Session 11 — Forecasting, Distribution Shift, and Model Governance

> **What are you responsible for when someone acts on your model?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-11-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S11-Lecture.qmd`](01-lecture/MATH60033A-S11-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### If this were a monitoring dashboard for a European agency, would you sign it?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Design an honest backtest for a time-dependent economic forecasting problem.
- Apply the Diebold-Mariano test to compare forecasts against a hard benchmark.
- Detect and diagnose distribution shift, and distinguish covariate shift from concept drift.
- Explain why Goodhart's law is a causal problem rather than a monitoring problem.
- Complete a model governance file that a competent successor could act on.

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

**Your group's own final-project data**

Source: Chosen by Session 10 and approved by the instructor


Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

By the end of this session, `02-practice/submissions/group-XX/` should contain a
draft **governance file**, your **backtest results with the DM test**, and the **shift diagnostic**.
These carry forward directly into the Session 12 submission — nothing here is thrown away.

---

## Before the next session

- Nothing new. Finish the deck, the governance file and the revised memo. See Session 12 for the schedule and rubric.

---

[<- Session 10: Causal Machine Learning: Double/Debiased ML and Heterogeneous Effects](../10-causal-inference-foundations/README.md) | [Session 12: Final Group Presentations ->](../12-group-presentations/README.md)
