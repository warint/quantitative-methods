# Session 11 — Causal Inference II: Difference-in-Differences

> **What would have happened otherwise?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-11-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S11-Lecture.qmd`](01-lecture/MATH60033A-S11-Lecture.qmd).

**Wednesday 25 November 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### What is your counterfactual, and would anyone believe it?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Set up a **difference-in-differences** design and identify the four cells
- Read the **interaction coefficient** as the estimate
- State the **parallel-trends** assumption and how you would probe it
- Explain what an **instrument** must satisfy, and why good ones are rare
- Say what neither design can rescue

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: parallel trends, the interaction as the estimate, instrumental variables | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**The spine's post-2021 structural break, treated as a policy change** — one line to load it:

```python
import qmib
data = qmib.load("core")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a difference-in-differences estimate on your angle, with the parallel-trends evidence shown rather than asserted, and a note on the threat you consider most serious.

---

[<- [Session 10: Causal Inference I: Counterfactuals, Randomisation, Matching](../10-causal-inference-foundations/README.md)](../10-causal-inference-foundations/README.md) | [[Session 12: Final Group Presentations](../12-group-presentations/README.md) ->](../12-group-presentations/README.md)
