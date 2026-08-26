# Session 11 — Lecture (first half, ~90 min)

# Causal Inference II: Difference-in-Differences

> **What would have happened otherwise?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-11-lecture.html)** ·
> source: [`MATH60033A-S11-Lecture.qmd`](MATH60033A-S11-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

1. **The key concept**
2. **The statistical model**
3. **The coefficients**
4. **The counterfactual**
5. **A Difference-in-Difference model**
6. **Data**
7. **Analysis**
8. **Discussion of the results**
9. **Instrumental Variables: Your turn!**

---

## Learning objectives

By the end of the session you should be able to:

- Set up a **difference-in-differences** design and identify the four cells
- Read the **interaction coefficient** as the estimate
- State the **parallel-trends** assumption and how you would probe it
- Explain what an **instrument** must satisfy, and why good ones are rare
- Say what neither design can rescue

---

## The data

**The spine's post-2021 structural break, treated as a policy change**

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

- A DiD with no evidence on parallel trends
- Reading the post-treatment dummy as the effect
- An instrument justified only by its first stage
- Claiming a causal effect the design cannot deliver

---

[Back to session 11](../README.md) · [On to the practice ->](../02-practice/README.md)
