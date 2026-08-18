# Session 02 — Group lab (second half, ~90 min)

# OLS from scratch, and where it breaks

---

## The theme of this session

> # How much of the measured gap is real, and how much is composition?

All ten groups attack this question. Each answers it with **its own angle** and its own slice of the
data spine, and the last twenty minutes assemble the five answers into one.

Regress your headline indicator on structural controls, then use Frisch-Waugh-Lovell to isolate what survives. Your angle's row in [RESEARCH-MANDATES.md](../../RESEARCH-MANDATES.md#session-02--how-much-of-the-gap-is-composition) names your outcome and what to partial out.

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

Groups of 3-4, working in VS Codium on the Ames Housing data. You will build the
estimator three ways, agree to machine precision where you should, and then deliberately break it.

---

## Tasks

1. Load `data/ames.parquet`. Select `GrLivArea`, `OverallQual`, `YearBuilt`, `TotalBsmtSF` as predictors and `SalePrice` as outcome. Drop rows with missing values and report how many you lost.
2. Implement `ols_normal_equations(X, y)` using an explicit inverse. Implement `ols_qr(X, y)` using `numpy.linalg.qr`. Compare coefficients to `statsmodels.api.OLS`. Report the maximum absolute difference for each.
3. Compute the hat matrix diagonal. Plot leverage against residual. Identify the three highest-leverage sales and look up what makes them unusual.
4. Verify Pythagoras numerically: does `TSS == ESS + RSS` hold to floating-point tolerance? What happens if you omit the intercept?
5. **Break it.** Add a column equal to `GrLivArea * 1.0000001 + 1e-8 * noise`. Re-run both implementations. Which one survives? Report the condition number of X before and after.
6. **FWL check.** Regress `SalePrice` on all predictors. Separately, residualise `SalePrice` and `OverallQual` on the other three, then regress the residuals. Confirm the coefficients match.

---

## Deliverable

A commented script or notebook `02-lab/submissions/group-XX/` that runs
end-to-end from the cached parquet file, plus a 250-word note answering: *why did the QR route
survive the collinearity you introduced, and what does that tell you about interpreting
coefficients when predictors are nearly redundant?*

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

- "I get a LinAlgError: Singular matrix. Explain what this means about the geometry of my design matrix, without giving me code."
- "Walk me through the Frisch-Waugh-Lovell theorem using a two-regressor example with numbers."
- "Explain the difference between numpy.linalg.inv, numpy.linalg.solve and numpy.linalg.lstsq in terms of numerical stability."

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

[Back to session 02](../README.md) · [<- Lecture notes](../01-lecture/README.md)
