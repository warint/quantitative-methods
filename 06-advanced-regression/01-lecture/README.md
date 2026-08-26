# Session 06 — Lecture (first half, ~90 min)

# Regression: Advanced Considerations

> **Does the relationship hold across countries, and across years?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-06-lecture.html)** ·
> source: [`MATH60033A-S06-Lecture.qmd`](MATH60033A-S06-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("panel")`.

---

## What the lecture covers

1. **Goals**
2. **Getting your hands dirty with Money Ball**
3. **1. Panel data analysis**
4. **Step 1. Running a TSCS model**
5. **Step 2. Fixed effects versus random effects**
6. **2. To go further**
7. **2.2 Binary and categorical independent variables**
8. **2.3 Interaction terms**
9. **3. Comparing models**
10. **Automatic model selection**

---

## Learning objectives

By the end of the session you should be able to:

- State what a **panel** is, and why pooling it with OLS understates uncertainty
- Distinguish **fixed** from **random** effects, and say what each assumes
- Fit a quadratic term and interpret a **non-linear** relationship in units
- Read an **interaction** as a slope that differs between groups
- Compare non-nested models on information criteria rather than an F-test

---

## The data

**A country panel of government debt and economic-freedom indices**

```python
import qmib
data = qmib.load("panel")
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

- Pooling a panel with ordinary standard errors
- Choosing fixed or random effects because one gave the significant answer
- Reporting an interaction without stating the slope in each group
- Adding a quadratic term and interpreting only its coefficient

---

[Back to session 06](../README.md) · [On to the practice ->](../02-practice/README.md)
