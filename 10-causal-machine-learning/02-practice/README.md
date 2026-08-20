# Session 10 — Group practice (second half, ~90 min)

# Estimating a treatment effect three ways, and disagreeing productively

---

## The theme of this session

> # Did the policy do anything, or did we just measure the countries that were already ahead?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

Nominate a plausible treatment with a date and run DML with your columns as controls. **Most groups will find identification fails or the estimate is too imprecise to act on. Demonstrating that clearly, with the overlap diagnostic and a named unmeasured confounder, is a full-credit answer.**

Your project, its unit of analysis and the data you found for it are fixed for the semester:
**[RESEARCH-MANDATES.md](../../RESEARCH-MANDATES.md)**.

> **If your project cannot answer the theme this week, say so and show why.** That is a contribution,
> not a failure — and it is graded as one.

---

## Method exercise

The tasks below build the machinery. Do them on the teaching dataset if you need to see the method
work on known ground first, then turn it on your own project. The reported result must be from **your
project**.

## Brief

Groups of 3-4 on the 401(k) data. You will produce a naive estimate, a DML estimate,
and a heterogeneity analysis - and account for every difference between them.

---

## Tasks

1. Estimate the effect of 401(k) eligibility on net financial assets by (a) a difference in means, (b) OLS with linear controls. Report both.
2. Check overlap: estimate the propensity score and plot its distribution by treatment status. Are there regions with no common support? What do you do about them?
3. Implement DML yourself: 5-fold cross-fitting, with your Session 5 elastic net for both nuisances. Report $\hat\theta$ and its standard error. Do **not** use the `doubleml` package for this step.
4. Repeat with random forests, and then with gradient boosting, as nuisance learners. Present all estimates in one table. How sensitive is $\hat\theta$ to the learner?
5. Verify your implementation against `doubleml.DoubleMLPLR`. Reconcile any discrepancy.
6. **Show the failure.** Implement the naive (non-cross-fitted) version: fit nuisances on the full sample. Compare the point estimate and the standard error to your DML result. Quantify the bias.
7. Repeat DML over 20 different random splits. Plot the distribution of $\hat\theta$. Report the median and comment on split sensitivity.
8. Fit a causal forest (`econml` or `grf`). Plot $\hat\tau(x)$ against income. Report the best linear projection of $\hat\tau$ on income and age with confidence intervals.
9. Write the identification paragraph: state the assumptions, and name one plausible confounder not in $X$. Explain what its presence would do to your estimate, using the Session 3 OVB logic.

---

## Deliverable

`02-practice/submissions/group-XX/` with your from-scratch DML implementation, the
estimator comparison table (naive / OLS / DML with three learners / package), the split-sensitivity
plot, the heterogeneity projection, and a 500-word memo whose *first* paragraph is the
identification argument and whose last sentence states what would change your conclusion.

Create your group's folder as `submissions/group-XX/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this practice requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "Explain why two nuisance functions each converging at n^{-1/4} is enough for root-n inference on theta. Show the product structure."
- "My DML estimate changes a lot depending on the random split. Is that a bug or a feature? What should I report?"
- "Give me the strongest argument that 401(k) eligibility is NOT conditionally ignorable."

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

**Every member commits and pushes from their own machine.** There are no assigned roles — work on
it together — but all three of you appear in the history, every week:

```bash
git add -A && git commit -m "..." && git push
```

`python scripts/assess.py contributions` prints a per-member, per-week grid. A week where you
pushed nothing is visible, and it is the kind of thing worth fixing in week four rather than week
eleven.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis on your project |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + instructor synthesis |

---

[Back to session 10](../README.md) · [<- Lecture notes](../01-lecture/README.md)
