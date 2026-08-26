# Session 08 — Lecture (first half, ~90 min)

# K-Nearest Neighbours and the Bias–Variance Trade-off

> **Flexible, or just unstable?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-08-lecture.html)** ·
> source: [`MATH60033A-S08-Lecture.qmd`](MATH60033A-S08-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

1. **Bias--Variance Trade-off**
2. **Classification**
3. **The Bayes Classifier**
4. **K-Nearest Neighbors**
5. **KNN by hand (you are the algorithm)**
6. **KNN by hand**
7. **KNN in R code (you are not longer the algorithm)**
8. **Machine Learning: using KNN as an example**
9. **Big lessons from ML**
10. **Big lessons**

---

## Learning objectives

By the end of the session you should be able to:

- State the **Bayes classifier** and say why no rule can beat it
- Compute a Euclidean distance and find nearest neighbours **by hand**
- Explain why KNN requires **standardised** predictors
- Choose $k$ by cross-validation, and read the trade-off the curve shows
- Say what happens to KNN as the number of predictors grows

---

## The data

**The course spine, plus the smarket returns used in the lecture**

```python
import qmib
data = qmib.load("core")
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

- Running KNN on unstandardised predictors
- Choosing $k$ on the test set
- Reporting accuracy with no benchmark
- Treating a low training error as evidence of anything

---

[Back to session 08](../README.md) · [On to the practice ->](../02-practice/README.md)
