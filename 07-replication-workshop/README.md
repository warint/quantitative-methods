# Session 07 — Four Papers, One Toolkit

> **What do the course's models say on the papers' data?**

> **[Open the workshop slides](https://warint.github.io/quantitative-methods/session-07-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S07-Lecture.qmd`](01-lecture/MATH60033A-S07-Lecture.qmd).

> **Python cheatsheets for this session**, one per package, functions explained with
> pictures: [pandas](https://warint.github.io/quantitative-methods/python-cheatsheets/pandas.pdf) · [NumPy](https://warint.github.io/quantitative-methods/python-cheatsheets/numpy.pdf) · [matplotlib](https://warint.github.io/quantitative-methods/python-cheatsheets/matplotlib.pdf) · [statsmodels](https://warint.github.io/quantitative-methods/python-cheatsheets/statsmodels.pdf) · [scikit-learn](https://warint.github.io/quantitative-methods/python-cheatsheets/sklearn.pdf)

**Wednesday 14 October 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00 · **in autonomy, alone or in teams**

---

## What this session is

No new method. You take the data of four papers you read before sessions 2 to 6 and plug it into
the models of the course, in Python, in VS Codium, **with exactly the code you typed in class** —
only the variable names change: OLS, the binary, ordinal and multinomial logits, ridge, the lasso
and the elastic net. You do not follow the papers; you read each output precisely, in words. Every
paper has a script cut into numbered steps and a guide that says, for every step, which session's
cell it copies and the numbers you should see.

It is also the revision session for the **midterm on 28 October**, which covers sessions 1 to 6.

| # | Paper | The simple models, with the code of | Guide |
|---|---|---|---|
| 1 | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* | OLS, the three logits · sessions 03–04 | [Paper 1](02-practice/replications/R1-fraiberger-2021.md) |
| 2 | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* | binary, ordinal and multinomial logits · session 04 | [Paper 2](02-practice/replications/R2-saganowski-2019.md) |
| 3 | Blonigen & Piger (2014), *Determinants of foreign direct investment* | OLS, ridge, lasso, elastic net · sessions 03 and 05 | [Paper 3](02-practice/replications/R3-blonigen-piger-2014.md) |
| 4 | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* | OLS, the three logits, ridge, lasso, elastic net · sessions 03, 04 and 05 | [Paper 4](02-practice/replications/R4-topalova-khandelwal-2011.md) |

---

## The three hours

| | Where | What |
|---|---|---|
| **Before** | [`00-pre-session/`](00-pre-session/README.md) | 30 minutes: set up a session-07 folder of your own, re-read four abstracts |
| **0:00 – 0:15** | [`02-practice/`](02-practice/README.md), Part 0 | Your folder in VS Codium, run `check_setup.py` |
| **0:15 – 3:00** | [`02-practice/replications/`](02-practice/replications/) | The four papers, 30 to 45 minutes each, with a break |

The opening slides ([`01-lecture/`](01-lecture/README.md)) show how the afternoon works and what
each paper's models should find; the step-by-step work is in [`02-practice/`](02-practice/README.md).

---

## By the end of the session you should be able to

- Choose which of the course's models fits a new outcome — a number, a yes/no, ordered or unordered categories
- Run OLS, the three logits, ridge, the lasso and the elastic net on the papers' data, with **exactly the code seen in class**
- Read every result as a sentence, in units — slopes, odds ratios, probabilities, what a penalty kept
- Compare OLS with the penalised models on data they did not see
- Say what each result does **not** license

---

## Nothing to hand in

The afternoon is practice, and revision for the midterm: the work is to read each output in words,
with units, and to say what it does not license.

## What loses marks on the midterm

- A coefficient with no sentence, no units, or no "holding the others fixed"
- An odds ratio read as a probability, or a lasso zero read as "no effect"
- Presenting a number from a simple model as the paper's finding
- Pasting output with no sentence saying what it means

---

> **Where did PCA and factor analysis go?** They are now
> [session 13, "One more thing"](../13-one-more-thing/README.md) — after the course, for
> self-study, and not on the midterm. The book's chapter 7 still covers them.

---

[<- [Session 06: Regression: Advanced Considerations](../06-advanced-regression/README.md)](../06-advanced-regression/README.md) | [[Session 08: K-Nearest Neighbours and the Bias–Variance Trade-off](../08-knn-and-bias-variance/README.md) ->](../08-knn-and-bias-variance/README.md)
