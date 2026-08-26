# Session 03 — Regression: Adequacy, Validity, and Robustness

> **You have fitted a regression. Can it be trusted?**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-03-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S03-Lecture.qmd`](01-lecture/MATH60033A-S03-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### Which model would survive a referee?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

- Read a **residuals-versus-fitted** plot and say what structure it reveals
- Diagnose non-constant variance from a **scale–location** plot
- Compute **leverage** and say which observations have the power to move the line
- Use **Cook's distance** to separate an outlier from an influential point
- Compare candidate models on **AIC**, and say why that is not model selection

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: residual diagnostics, leverage, Cook's distance, information criteria | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**The same regression session 02 fitted — gdp per capita on productivity** — one line to load it:

```python
import qmib
data = qmib.load("core")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: a diagnostic report on your group's own regression: four plots, the observations you investigated, and a 250-word note on which conclusions survived the diagnostics and which did not.

---

[<- [Session 02: Exploratory Data Analysis, and the First Model](../02-exploratory-data-analysis/README.md)](../02-exploratory-data-analysis/README.md) | [[Session 04: Logistic Regression: Binary, Ordinal, and Multinomial](../04-logistic-ordinal-multinomial/README.md) ->](../04-logistic-ordinal-multinomial/README.md)
