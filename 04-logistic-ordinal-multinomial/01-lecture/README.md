# Session 04 — Lecture (first half, ~90 min)

# Logistic Regression: Binary, Ordinal, and Multinomial

> **The outcome is a category, not a number. Now what?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-04-lecture.html)** ·
> source: [`MATH60033A-S04-Lecture.qmd`](MATH60033A-S04-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("loans")`.

---

## What the lecture covers

1. **Let's start with an example**
2. **Lending Club**
3. **The basics of logistic regression**
4. **Let's use another example**
5. **FICO Score**
6. **Inference and goodness of fit**
7. **Let's see another example**
8. **Portugal's Red Wines**
9. **Comparing logistic models**
10. **Model selection**

---

## Learning objectives

By the end of the session you should be able to:

- Say why the **linear probability model** fails, and where it fails worst
- Interpret a logistic coefficient as a **log-odds**, and its exponential as an odds ratio
- Compute a fitted probability by hand from $x^\top\hat\beta$
- Compare nested models with a **likelihood-ratio test**
- Extend the model to **ordinal** and **multinomial** outcomes, and say what each assumes

---

## The data

**Lending club — 9,578 three-year loans, fico scores and default**

```python
import qmib
data = qmib.load("loans")
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

- Reporting log-odds as though they were probabilities
- Interpreting an odds ratio as a relative risk
- Comparing non-nested models with a likelihood-ratio test
- Reporting accuracy on an imbalanced outcome with no base rate

---

[Back to session 04](../README.md) · [On to the practice ->](../02-practice/README.md)
