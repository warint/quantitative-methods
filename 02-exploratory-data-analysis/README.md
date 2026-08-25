# Session 02 — Exploratory Data Analysis: Centre, Spread, and Shape

> **Before you model anything, what does the data actually look like?**

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Which summary of your project's key variable would you defend in print?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Compute and distinguish the **mean, median and trimmed mean**, and say which question each answers.
- Explain why the sample variance divides by $n-1$ rather than $n$.
- Apply the **empirical rule**, and state the precondition under which it is valid.
- Compute **skewness** and **excess kurtosis** from their definitions, and test each against its
  threshold $2\sqrt{6/n}$ and $4\sqrt{6/n}$.
- Show that skewness and kurtosis are **independent** — and that symmetry is not normality.
- Read a mean–median gap as evidence about shape rather than as a rounding artefact.

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | Git and GitHub setup, reading, self-check | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: centre, spread, shape | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. This is the session where your group repository is set
up, so arrive with git working and a GitHub account.

---

## Data for this session

**The course data spine** — thirty European countries, 2010–2024, already in the repository. No
download required.

```python
import pandas as pd
core = pd.read_parquet("data/spine/core.parquet")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

A commented script in `02-practice/submissions/group-XX/` that profiles your project's three most
important variables — centre, spread and shape, with the thresholds tested — plus a 250-word note
answering: *for the variable at the centre of your research question, which summary would you put
in a paper, and what does its shape tell you about the methods available to you later?*

---

## Before the next session

- Bring the profile of your variables. Session 03 fits a mean function to one of them.
- Optional: ISLR ch. 2 for the vocabulary Session 03 uses.

---

[<- Session 01: Foundations, Scenarios, and Tools](../01-foundations-scenarios-and-tools/README.md) | [Session 03: From Data to Models ->](../03-regression-adequacy-and-validity/README.md)
