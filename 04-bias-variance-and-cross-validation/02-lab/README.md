# Session 04 — Group lab (second half, ~90 min)

# Building a cross-validation harness that does not lie to you

---

## The theme of this session

> # Are we predicting, or only describing the past?

All ten groups attack this question. Each answers it with **its own angle** and its own slice of the
data spine, and the last twenty minutes assemble the five answers into one.

Build the cross-validation harness that matches your data's dependence structure — `GroupKFold` by country for cross-sections, rolling-origin for time series, both for panels. Then hunt your own leakage and report the size of the gap.

Your angle, your unit of analysis and your data are fixed for the semester:
**[RESEARCH-MANDATES.md](../../RESEARCH-MANDATES.md)**.

> **If your angle cannot answer the theme this week, say so and show why.** That is a contribution,
> not a failure — and it is graded as one.

---

## Method exercise

The tasks below build the machinery. Do them on the teaching dataset if you need to see the method
work on known ground first, then turn it on your own angle. The reported result must be from **your
angle**.

## Brief

Groups of 3-4. First you will *see* the decomposition on data where you know the
truth. Then you will deliberately commit each of the three leakage errors and measure how much
optimism each one buys.

---

## Tasks

1. Generate 500 datasets from $y = \sin(2\pi x) + \varepsilon$, $\varepsilon \sim N(0, 0.3^2)$, $n = 50$. For polynomial degrees 1..15, estimate squared bias, variance, and total error at a grid of test points. Plot all three against degree. Mark the minimum.
2. Verify that total error equals bias^2 + variance + 0.09 to within Monte Carlo noise. Report the discrepancy.
3. On Ames, build a `sklearn.pipeline.Pipeline` with imputation + standardisation + polynomial features + linear regression. Run 10-fold CV correctly.
4. **Leak 1:** standardise and impute on the full dataset *before* CV. Report the CV error. How much did leakage flatter you?
5. **Leak 2:** select the 10 features most correlated with the outcome using all the data, then CV on those 10. Compare to doing selection inside each fold.
6. **Leak 3:** sort Ames by `YrSold`, treat it as a time series, and compare random 10-fold CV to a rolling-origin split. Which is honest?
7. Implement the LOOCV shortcut using the hat matrix diagonal from Session 2. Confirm it matches brute-force LOOCV.

---

## Deliverable

`02-lab/submissions/group-XX/` containing the bias-variance figure, a table
reporting CV error under correct and leaked procedures (with the optimism in each case), and a
200-word note: *which leak was most dangerous, and why is it the hardest one to notice in a
referee report?*

Create your group's folder as `submissions/group-XX/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this lab requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "Review this scikit-learn code for data leakage. Point to specific lines: <paste>"
- "Explain why LOOCV has higher variance than 10-fold CV, even though it has lower bias."
- "Design a cross-validation scheme for quarterly euro-area data where I want to forecast 4 quarters ahead. Justify each choice."

**Required in every deliverable:** at least one instance where you identified an LLM output as
wrong, unverifiable, or misleading — with an explanation of how you established that.

---

## The two-minute report

> **The presenter is drawn at random when your group is called.** Any of the three of you may have
> to give this report, so all three must understand the analysis, the number, and what would
> undermine it. See [`GROUP-ASSESSMENT.md`](../../GROUP-ASSESSMENT.md).

**One slide. Three sentences.**

1. **What I did.** *"We regressed X on Y for [our unit], partialling out [Z]."*
2. **The number.** One figure or estimate, with its uncertainty or its benchmark.
3. **The catch.** What surprised you, what you cannot claim, or where your data failed you.

No method exposition — everyone learned it ninety minutes ago. No code on the slide. **Sentence 3
earns the slot:** a result plus what would undermine it is worth more than a result alone.

## Before you leave the room

Fill in this session's row of your group's role log
(`assessment/role-logs/gXX.md`): who was **Driver** (wrote the code), **Analyst** (decided the
specification and owns the interpretation), **Reporter** (wrote the three sentences). Roles rotate
every week.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis on your angle |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + instructor synthesis |

---

[Back to session 04](../README.md) · [<- Lecture notes](../01-lecture/README.md)
