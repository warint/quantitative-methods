# Session 10 — Lecture (first half, ~90 min)

# Causal Inference I: Counterfactuals, Randomisation, Matching

> **Did the policy do anything, or were the groups different to begin with?**

---

> **Python cheatsheet — [session 10](https://warint.github.io/quantitative-methods/python-cheatsheet-10.pdf)** (PDF) ·
> source: [`PYTHON-CHEATSHEET.qmd`](../PYTHON-CHEATSHEET.qmd)
>
> How to start Python in VS Codium on your platform, how to make a file and run it,
> the DataFrame basics, and every name taught in sessions 1 to 10 with a
> line showing it in use. Print it.

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-10-lecture.html)** ·
> source: [`MATH60033A-S10-Lecture.qmd`](MATH60033A-S10-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every cell runs on its own when
pasted into a file: the data is either simulated in the cell or read from a URL.

---

## What the lecture covers

1. **The question, in pictures** — two potential outcomes per unit, the fundamental problem, ATE and
   ATT, and the naive difference written as effect plus selection bias
2. **A world where we know the truth** — 1,000 simulated firms: a coin flip recovers the effect,
   self-selection does not, and a balance check shows why
3. **Matching, tested on real data** — LaLonde's job-training experiment, its controls swapped for a
   survey: naive estimate, balance, propensity score, overlap, nearest-neighbour matching, a better
   score, and the ATT against the experiment's answer
4. **What matching does not fix** — unmeasured confounders, bad controls, overlap, standard errors
5. **Your recipe** — seven steps, one cell to copy, what to report, and the same test with a second
   survey

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

**A simulation, and LaLonde's job-training data (Dehejia and Wahba's version)**

```python
import pandas as pd
url = "https://users.nber.org/~rdehejia/data/"
nsw = pd.read_stata(url + "nsw_dw.dta")            # the experiment: 185 trained, 260 controls
cps = pd.read_stata(url + "cps_controls.dta")      # 15,992 people from a survey
```

Nothing to download by hand; the cells read the files directly.

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

[Back to session 10](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-10.html)
