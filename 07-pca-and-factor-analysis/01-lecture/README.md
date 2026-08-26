# Session 07 — Lecture (first half, ~90 min)

# Principal Component and Factor Analyses

> **How many independent things are actually being measured?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-07-lecture.html)** ·
> source: [`MATH60033A-S07-Lecture.qmd`](MATH60033A-S07-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("movies")`.

---

## What the lecture covers

1. **Multivariate statistics**
2. **Principal Component Analysis**
3. **Mathematical Model --- Maximize variance of the new components**
4. **The Netflix's Recommender System through a PCA**
5. **Netflix's Recommender System**
6. **Netflix's recommender System**
7. **Factor analysis**
8. **Two examples : the wine data and the cars questionnaire**
9. **FAMD: the wine data**
10. **Factor Analysis for Questionnaires**

---

## Learning objectives

By the end of the session you should be able to:

- Explain why PCA requires **standardised** inputs, and what happens if you forget
- Read a **scree plot** and defend the number of components you retained
- Distinguish a **loading** from a **score**, and say what each is for
- State the difference between **PCA** and **factor analysis**, and when each applies
- Say why a factor is identified only **up to rotation**

---

## The data

**45,000 films — budget, popularity, revenue, runtime and votes**

```python
import qmib
data = qmib.load("movies")
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

- Running PCA on unstandardised columns
- Retaining components by a rule you did not state
- Naming a component ("this is competitiveness") with no rotation caveat
- Reporting variance explained as though it measured correctness

---

[Back to session 07](../README.md) · [On to the practice ->](../02-practice/README.md)
