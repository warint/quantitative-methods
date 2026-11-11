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
what loses marks. Every code example in the deck is **Python**. The first cell of each design
simulates its data and writes a small CSV in your folder; every later cell starts from that file, so
each runs on its own once the first has run.

---

## What the lecture covers

The lecture is built on **four examples**, with no code on screen while they are taught. The code
comes at the end and does not replay the examples: it explains the two designs,
difference-in-differences and an instrument, and has you carry each one out on new data.

1. **The language of difference-in-differences (DiD)** — the two differences, the interaction
   regression, the words you will need, and parallel trends stated exactly
2. **Example 1 · Did affordable housing lower nearby prices?** — 1,000 simulated houses, two periods:
   after-only, before-after and DiD against a known effect, the four means and the counterfactual
3. **Example 2 · Were the trends parallel?** — the same city over six years, in two versions: the event
   study is flat when the trends were parallel and slopes when they were not
4. **Example 3 · Do national AI strategies raise firms' AI use?** — the course data, adopted in different
   years: the adoption table, two-way fixed effects against Callaway–Sant'Anna, and how much violation of
   parallel trends the result survives
5. **Example 4 · Does exporting raise productivity?** — 2,000 simulated firms, management unobserved:
   distance to the nearest port as an instrument, the first stage and the reduced form, two-stage least
   squares against the truth, and what happens when the exclusion fails
6. **Wrapping up** — matching, DiD or an instrument; what DiD cannot fix; the seven steps
7. **In class · The two designs, done in Python** — what each design is and why it removes
   selection, then:
   - **a difference-in-differences study, step by step** (export desks opened in 40 regions, in two
     waves): the panel and the adoption table, the plot, one clean 2×2, an event study by regression,
     two-way fixed effects against Callaway–Sant'Anna, and a sensitivity analysis
   - **an instrument, step by step** (a randomly drawn voucher for a trade fair): the naive answer,
     balance and the first stage, the reduced form and the ratio, two-stage least squares, and whom
     the estimate describes
   - a *Your turn* for each

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

**The four examples: three simulations, and the course data on national AI strategies**

```python
import qmib
wide = qmib.load("angle_c_country")    # Example 3: AI use and AI strategies, by country and year
```

The lecture's charts are drawn from these. Examples 1, 2 and 4 are simulated.

**The in-class code: two new simulations, each with a known effect**

- `export_desks.csv` — 40 regions, 2014–2023; export desks open in 12 regions in 2018 and 10 more in
  2021 (true effect: 2 points of exporting firms per year open)
- `trade_fair.csv` — 3,000 firms, half of which were sent a voucher for a trade fair at random (true
  effect of attending: +12, \$ thousand of exports)

The first cell of each design writes its file; nothing is downloaded.

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
