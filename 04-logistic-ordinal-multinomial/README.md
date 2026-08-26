# Session 04 — Logistic Regression: Binary, Ordinal, and Multinomial

> **The outcome is a category, not a number. Now what?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-04-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S04-Lecture.qmd`](01-lecture/MATH60033A-S04-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Can we predict a discrete outcome honestly?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Say why the **linear probability model** fails, and where it fails worst
- Interpret a logistic coefficient as a **log-odds**, and its exponential as an odds ratio
- Compute a fitted probability by hand from $x^\top\hat\beta$
- Compare nested models with a **likelihood-ratio test**
- Extend the model to **ordinal** and **multinomial** outcomes, and say what each assumes

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: maximum likelihood, odds ratios, pseudo-$R^2$, likelihood-ratio tests | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**Lending club — 9,578 three-year loans, fico scores and default** — one line to load it:

```python
import qmib
data = qmib.load("loans")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a logistic model of a binary outcome in your own project data, with the odds ratios interpreted in words, one nested comparison tested, and a note on what the model does not license you to say.

---

[<- [Session 03: Regression: Adequacy, Validity, and Robustness](../03-regression-adequacy-and-validity/README.md)](../03-regression-adequacy-and-validity/README.md) | [[Session 05: Regularisation: Ridge, Lasso, and the Elastic Net](../05-ridge-lasso-elastic-net/README.md) ->](../05-ridge-lasso-elastic-net/README.md)
