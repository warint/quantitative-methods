# Session 09 — Lecture (first half, ~90 min)

# Structural Equation Modelling

> **Can you measure something you cannot observe?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-09-lecture.html)** ·
> source: [`MATH60033A-S09-Lecture.qmd`](MATH60033A-S09-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("efa")`.

---

## What the lecture covers

1. **Part I: SEM Basics**
2. **What is SEM?**
3. **Why use SEM?**
4. **Key Terminology in SEM**
5. **Components of a SEM**
6. **Example 1**
7. **Example Dataset: HolzingerSwineford1939**
8. **🔹 **Dataset overview****
9. **🔹 **Latent and observed variables****
10. **🔹 **Typical CFA model specification****

---

## Learning objectives

By the end of the session you should be able to:

- Distinguish the **measurement** model from the **structural** model
- Write a model description and read `=~` as "is measured by"
- Interpret a **standardised loading**, and say when an indicator is weak
- Report **CFI, TLI and RMSEA**, and say what each would have to be
- State why good fit is not evidence that the model is correct

---

## The data

**A 14-item questionnaire on purchase decisions, plus semopy's bundled examples**

```python
import qmib
data = qmib.load("efa")
```

Run it once before class; it caches locally and then works offline.

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

[Back to session 09](../README.md) · [On to the practice ->](../02-practice/README.md)
