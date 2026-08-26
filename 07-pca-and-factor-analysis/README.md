# Session 07 — Principal Component and Factor Analyses

> **How many independent things are actually being measured?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-07-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S07-Lecture.qmd`](01-lecture/MATH60033A-S07-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### How many distinct dimensions does your angle really have?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Explain why PCA requires **standardised** inputs, and what happens if you forget
- Read a **scree plot** and defend the number of components you retained
- Distinguish a **loading** from a **score**, and say what each is for
- State the difference between **PCA** and **factor analysis**, and when each applies
- Say why a factor is identified only **up to rotation**

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: eigenvalues, loadings, scree plots, rotation, FAMD | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**45,000 films — budget, popularity, revenue, runtime and votes** — one line to load it:

```python
import qmib
data = qmib.load("movies")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a dimension-reduction of your project's indicators: the scree plot, the number retained with its justification, the loadings interpreted, and a note on what you are *not* entitled to call the components.

---

[<- [Session 06: Regression: Advanced Considerations](../06-advanced-regression/README.md)](../06-advanced-regression/README.md) | [[Session 08: K-Nearest Neighbours and the Bias–Variance Trade-off](../08-knn-and-bias-variance/README.md) ->](../08-knn-and-bias-variance/README.md)
