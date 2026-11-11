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
what loses marks. Every code example in the deck is **Python**. The first cell of each solution
simulates its data and writes a small CSV in your folder; every later cell starts from that file, so
each runs on its own once the first has run.

---

## What the lecture covers

The lecture is built on **three examples**, with no code on screen while they are taught. The code
comes at the end and does not replay the examples: it explains the two solutions, a randomised
controlled trial and propensity-score matching, and has you carry each one out on new data.

1. **The language of causal inference** — two potential outcomes per unit, the fundamental problem,
   ATE and ATT, the words you will need, and the naive difference as effect plus selection bias
2. **Example 1 · Did the export programme work?** — 1,000 simulated firms: a coin flip recovers the
   effect, self-selection does not, and a balance check shows why
3. **Example 2 · LaLonde's test** — a job-training lottery, its controls swapped for a survey: naive
   estimate, balance, propensity score, overlap, matching, the love plot, and the ATT against the
   experiment's answer
4. **Example 3 · Does analytics training raise performance?** — 800 simulated employees: matching
   recovers the course's effect, then fails, with perfect balance, once motivation drives enrolment
5. **Wrapping up** — matching or regression, what matching does not fix, the seven steps
6. **In class · The two solutions, done in Python** — what each solution is and why it removes
   selection, then:
   - **a trial, step by step** (400 workshops offered export orders): the baseline file, power, a
     stratified draw, the balance check, the estimate with and without baseline controls, and what to
     do when firms refuse
   - **matching, step by step** (4,000 firms, some certified ISO 9001): the score, overlap, matching
     within a caliper, balance, the ATT with a bootstrap interval, and robustness
   - a *Your turn* for each, then both solutions on LaLonde's real data

---

## Learning objectives

By the end of the session you should be able to:

- State the **fundamental problem of causal inference**
- Explain why **randomisation** solves it, and what it costs
- **Run a trial**: size it, draw the treated, check the draw, and estimate the effect with its interval
- Estimate a **propensity score** and use it to match treated to control units
- Check **overlap** and **balance**, and say what to do when they fail
- Report an **ATT**, and state the assumption it rests on
- Say why matching and regression rest on the **same assumption**, and where they differ

---

## The data

**The three examples: two simulations, and LaLonde's job-training data (Dehejia and Wahba's version)**

```python
import pandas as pd
url = "https://users.nber.org/~rdehejia/data/"
nsw = pd.read_stata(url + "nsw_dw.dta")            # the experiment: 185 trained, 260 controls
cps = pd.read_stata(url + "cps_controls.dta")      # 15,992 people from a survey
```

Nothing to download by hand. The lecture's charts are drawn from these; you load them yourself in the
last *Your turn*.

**The in-class code: two new simulations, each with a known effect**

- `trial_baseline.csv`, then `trial_assigned.csv` — 400 workshops that applied for export orders; you
  draw the 200 that receive them (true effect: +\$150 of monthly profit)
- `certification.csv` — 4,000 firms, some of which chose a quality certification (true effect: +8,
  \$ thousand of exports)

The first cell of each solution writes its file; nothing is downloaded.

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

- Redrawing a randomisation until the groups "look right", or comparing by who took the treatment
  rather than by the draw
- Reporting a matched estimate with no overlap diagnostic
- Matching on a variable affected by the treatment
- Calling an association causal because you controlled for something
- Omitting the balance table

---

[Back to session 10](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-10.html)
