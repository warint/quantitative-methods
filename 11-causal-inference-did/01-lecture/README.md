# Session 11 — Lecture (first half, ~90 min)

# Causal Inference II: Difference-in-Differences

> **What would have happened otherwise?**

---

> **Python cheatsheet — [session 11](https://warint.github.io/quantitative-methods/python-cheatsheet-11.pdf)** (PDF) ·
> source: [`PYTHON-CHEATSHEET.qmd`](../PYTHON-CHEATSHEET.qmd)
>
> How to start Python in VS Codium on your platform, how to make a file and run it,
> the DataFrame basics, and every name taught in sessions 1 to 11 with a
> line showing it in use. Print it.

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-11-lecture.html)** ·
> source: [`MATH60033A-S11-Lecture.qmd`](MATH60033A-S11-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

The lecture is built on **three examples**, with no code on screen while they are taught; the code
for all three comes at the end, for you to run in class.

1. **The language of difference-in-differences (DiD)** — the two differences, the interaction
   regression, the words you will need, and parallel trends stated exactly
2. **Example 1 · Did affordable housing lower nearby prices?** — 1,000 simulated houses, two periods:
   after-only, before-after and DiD against a known effect, the four means and the counterfactual
3. **Example 2 · Were the trends parallel?** — the same city over six years, in two versions: the event
   study is flat when the trends were parallel and slopes when they were not
4. **Example 3 · Do national AI strategies raise firms' AI use?** — the course data, adopted in different
   years: the adoption table, two-way fixed effects against Callaway–Sant'Anna, and how much violation of
   parallel trends the result survives
5. **Wrapping up** — matching or DiD, what DiD cannot fix, and instrumental variables when neither works
6. **In class · The code behind the three examples** — every cell, and a *Your turn* per example

---

## Learning objectives

By the end of the session you should be able to:

- Set up a **difference-in-differences** design and identify the four cells
- Read the **interaction coefficient** as the estimate
- State the **parallel-trends** assumption and how you would probe it
- Explain why **two-way fixed effects** can mislead under staggered adoption
- Explain what an **instrument** must satisfy, and why good ones are rare
- Say what neither design can rescue

---

## The data

**Two simulations, and the course data on national AI strategies**

```python
import qmib
wide = qmib.load("angle_c_country")    # Example 3: AI use and AI strategies, by country and year
```

Run it once before class from the repository root; it caches locally and then works offline.
Examples 1 and 2 are simulated inside their cells.

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

[Back to session 11](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-11.html)
