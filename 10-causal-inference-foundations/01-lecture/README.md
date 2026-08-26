# Session 10 — Lecture (first half, ~90 min)

# Causal Inference I: Counterfactuals, Randomisation, Matching

> **Did the policy do anything, or were the groups different to begin with?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-10-lecture.html)** ·
> source: [`MATH60033A-S10-Lecture.qmd`](MATH60033A-S10-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

1. **Causal Inference: Logic and Tools**
2. **Counterfactual Framework**
3. **The Rubin Causal Model**
4. **Why It Matters**
5. **Real Example of Observed and Counterfactual Outcomes**
6. **Observed vs. Counterfactual**
7. **The Missing Counterfactual**
8. **How to Proceed**
9. **Randomized Controlled Trials (RCTs)**
10. **Why Randomize?**

---

## Learning objectives

By the end of the session you should be able to:

- State the **fundamental problem of causal inference**
- Explain why **randomisation** solves it, and what it costs
- Estimate a **propensity score** and use it to match treated to control units
- Check **overlap** and **balance**, and say what to do when they fail
- Report an **ATT**, and state the assumption it rests on

---

## The data

**The spine's documented treatment, with a known effect to recover**

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

- Reporting a matched estimate with no overlap diagnostic
- Matching on a variable affected by the treatment
- Calling an association causal because you controlled for something
- Omitting the balance table

---

[Back to session 10](../README.md) · [On to the practice ->](../02-practice/README.md)
