# Session 09 — Lecture (first half, ~90 min)

# Structural Equation Modelling

> **Can you measure something you cannot observe?**

---

> **Python cheatsheet — [session 09](https://warint.github.io/quantitative-methods/python-cheatsheet-09.pdf)** (PDF) ·
> source: [`PYTHON-CHEATSHEET.qmd`](../PYTHON-CHEATSHEET.qmd)
>
> How to start Python in VS Codium on your platform, how to make a file and run it,
> the DataFrame basics, and every name taught in sessions 1 to 9 with a
> line showing it in use. Print it.

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-09-lecture.html)** ·
> source: [`MATH60033A-S09-Lecture.qmd`](MATH60033A-S09-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. The lecture is built on **three examples**, with no code on screen while they are
taught; the code for all three comes at the end, for you to run in class. Every cell runs on its own
when pasted into a file: the data either ship with semopy or are simulated in the cell.

---

## What the lecture covers

1. **The language of SEM** — a construct and its indicators, the five symbols, five words (observed,
   latent, exogenous and endogenous, path, error), the two halves, and corr = λᵢλⱼ
2. **Example 1 · Nine tests, three abilities** — Holzinger and Swineford's 301 children: the
   correlations, the drawing, the loadings, the fit, where the model misses, and three competing models
3. **Example 2 · Does industrialisation bring democracy?** — Bollen's 75 countries: structural
   paths, R², direct and indirect effects, the same-question covariances, and an arrow turned around
4. **Example 3 · Will this firm export?** — the theory of planned behaviour on a simulated survey of
   400 managers, where the true paths are known: SEM recovers them, averaging the items shrinks them
5. **What a good fit does not prove** — equivalent models, confounding, small samples, invariance
6. **In class · The code behind the three examples** — every cell, and a *Your turn* task per example

---

## Learning objectives

By the end of the session you should be able to:

- Distinguish the **measurement** model from the **structural** model
- Write a model description and read `=~` as "is measured by"
- Interpret a **standardised loading**, and say when an indicator is weak
- Report **CFI, TLI and RMSEA**, and say what each would have to be
- Decompose a **mediation** into direct and indirect paths
- Explain why averaging noisy items **shrinks** a path, and why SEM does not
- State why good fit is not evidence that the model is correct

---

## The data

**Three examples, nothing to download**

```python
from semopy.examples import holzinger39, political_democracy
data = holzinger39.get_data()                 # Example 1: 301 children, nine tests
countries = political_democracy.get_data()    # Example 2: 75 countries, 1960 and 1965
# Example 3 is simulated in the deck's cell: 400 managers, eight survey items
```

Your group's own measurement model, in the practice, uses `qmib.load("efa")`.

---

## Running the code

Everything in the deck runs in the **VS Codium terminal** with the project environment active:

```bash
source .venv/bin/activate        # macOS / Linux
python
```

If a package is missing, `pip install -r requirements.txt` from the repository root.

---

## What loses marks

- Reporting fit indices without saying which threshold you applied
- Treating good fit as confirmation of the causal structure
- Adding correlated residuals until the model fits
- Naming a latent variable without defending the name

---

[Back to session 09](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-09.html)
