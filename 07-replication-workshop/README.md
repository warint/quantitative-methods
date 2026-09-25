# Session 07 — Replication Workshop: Five Papers, One Toolkit

> **Can you reproduce what the papers claim, with only what you have learned?**

> **[Open the workshop slides](https://warint.github.io/quantitative-methods/session-07-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S07-Lecture.qmd`](01-lecture/MATH60033A-S07-Lecture.qmd).

**Wednesday 14 October 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00 · **in autonomy, alone or in teams**

---

## What this session is

No new method. You go back to the five papers you read before sessions 2 to 6, open the authors'
own replication data, and rebuild a published result in Python, in VS Codium, **using only the code
you saw in class**. Every paper has a script cut into numbered steps and a guide that says, for every
step, what to run, why, and the numbers you should see.

It is also the revision session for the **midterm on 28 October**, which covers sessions 1 to 6.

| # | Paper | Reuses | Guide |
|---|---|---|---|
| 1 | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* | Session 02 · describing a variable, the first regression | [R1](02-practice/replications/R1-fraiberger-2021.md) |
| 2 | Amsili, van Es & Schindelbeck (2024), *Pedotransfer functions …* | Session 03 · regression diagnostics | [R2](02-practice/replications/R2-amsili-2024.md) |
| 3 | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* | Session 04 · logistic and multinomial regression | [R3](02-practice/replications/R3-saganowski-2019.md) |
| 4 | Blonigen & Piger (2014), *Determinants of foreign direct investment* | Session 05 · ridge, lasso, elastic net | [R4](02-practice/replications/R4-blonigen-piger-2014.md) |
| 5 | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* | Session 06 · panel data, fixed and random effects | [R5](02-practice/replications/R5-topalova-khandelwal-2011.md) |

---

## The three hours

| | Where | What |
|---|---|---|
| **Before** | [`00-pre-session/`](00-pre-session/README.md) | 30 minutes: check the four data packages are on your machine, re-read five tables |
| **0:00 – 0:15** | [`02-practice/`](02-practice/README.md), Part 0 | Set up in VS Codium, run `check_setup.py` |
| **0:15 – 2:50** | [`02-practice/replications/`](02-practice/replications/) | The five replications, about 30 minutes each, with a break |
| **2:50 – 3:00** | [`02-practice/replication-log.md`](02-practice/replication-log.md) | The log: fill it in, commit, push |

The opening slides ([`01-lecture/`](01-lecture/README.md)) show how the afternoon works and what
each replication should find; the step-by-step work is in [`02-practice/`](02-practice/README.md).

---

## By the end of the session you should be able to

- State each paper's **research question**, and the result it rests on, in one sentence
- Rebuild a published result from the authors' own files, with **only the Python seen in class**
- Say how close the replication came, and **where** and **why** it differs
- Re-read each result through the course's diagnostics — thresholds, residuals, odds ratios, penalties, fixed effects
- Say what each published result does **not** license

---

## Deliverable

In `groups/A2026/group-XX/session-07/`: a replication log — for each paper attempted, the published
number, yours, the gap and its explanation, and one sentence on what the result does not license.
The template is [`02-practice/replication-log.md`](02-practice/replication-log.md).

## What loses marks

- Reporting a replicated number without the published one beside it
- Calling a replication failed without saying where it breaks
- Reaching for a method the course has not taught to force a match
- Pasting output with no sentence saying what it means

---

> **Where did PCA and factor analysis go?** They are now
> [session 13, "One more thing"](../13-one-more-thing/README.md) — after the course, for
> self-study, and not on the midterm. The book's chapter 7 still covers them.

---

[<- [Session 06: Regression: Advanced Considerations](../06-advanced-regression/README.md)](../06-advanced-regression/README.md) | [[Session 08: K-Nearest Neighbours and the Bias–Variance Trade-off](../08-knn-and-bias-variance/README.md) ->](../08-knn-and-bias-variance/README.md)
