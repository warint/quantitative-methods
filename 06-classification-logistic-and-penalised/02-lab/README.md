# Session 06 — Group lab (second half, ~90 min)

# Credit scoring and bankruptcy prediction: from probability to decision

---

## The theme of this session

> # Can we flag a country or sector falling behind one year ahead — and what does a false alarm cost?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

Define a binary 'falling behind' label appropriate to your project, predict it one period ahead, then do the decision analysis: what does a false alarm cost a European agency relative to a missed signal, and what threshold follows?

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

Groups of 3-4. **Track A** (German Credit) is compulsory and covers estimation,
interpretation and the threshold decision. **Track B** (bankruptcy data) is the high-dimensional
extension. Attempt Track A completely before starting Track B; a thorough A plus a partial B scores
better than two rushed halves.

The technical work is straightforward. The difficulty - and the grade - is in the decision analysis
and the honesty of the reporting.

---

## Tasks

1. **A1.** Implement `logistic_irls(X, y, tol, max_iter)` from scratch, returning coefficients and $(X^\top W X)^{-1}$. Verify against `statsmodels.Logit` to 6 decimal places.
2. **A2.** Report coefficients, odds ratios and average marginal effects in one table. Write one sentence interpreting the largest effect in each of the three metrics.
3. **A3. Induce separation.** Construct a feature that perfectly predicts a subset of outcomes. Show your IRLS diverges. What does `statsmodels` report? What does `sklearn.LogisticRegression` report, and why is its answer different?
4. **A4.** Plot the ROC and precision-recall curves. Report AUC and average precision, and explain the divergence between the two visual impressions.
5. **A5.** Apply the dataset's 5:1 cost matrix. Plot total expected cost against $\tau$ over a grid; find the minimiser; compare to the analytical $\tau^\star = 1/6$ and to the default 0.5. Report the cost saving.
6. **A6.** Plot a reliability diagram with 10 bins. Is the model calibrated? Apply Platt scaling or isotonic regression and re-plot.
7. **A7. Fairness.** Split recall and FPR by the `age` and `foreign_worker` attributes at your chosen $\tau$. Are they equal? Should they be?
8. **B1.** Add the elastic-net penalty to your IRLS by wrapping it around your Session 5 coordinate-descent routine. Clamp the weights. Verify against `sklearn.LogisticRegression(penalty='elasticnet', solver='saga')`.
9. **B2.** On the bankruptcy data, tune $(\alpha,\lambda)$ by stratified 10-fold CV optimising **average precision**, not accuracy. Justify that choice in one sentence. Report the $\lambda_{1se}$ model and map each retained ratio to its financial meaning.
10. **B3. Compare the three imbalance interventions** - unweighted, class-weighted, SMOTE. For each, plot a reliability diagram and report the Brier score. Which preserves calibration? Apply the analytical intercept correction to the resampled model and re-plot.
11. **B4. Stability selection.** 500 subsamples at $n/2$; plot selection frequency for the top 20 variables; mark your $\pi_{thr}=0.6$ line.

---

## Deliverable

`02-lab/submissions/group-XX/` containing: the IRLS implementation, the
three-metric coefficient table, the cost curve with the optimal threshold marked, the reliability
diagram, and (Track B) the calibration comparison and stability plot.

Plus a **400-word memo to a credit committee** that (a) states the recommended threshold and its
cost justification, (b) names which features are *robustly* selected and explicitly refuses to
over-claim about the others, and (c) raises the group-disparity finding without resolving it
prematurely.

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

- "My logistic regression has a coefficient of 24 with a standard error of 4000. Diagnose the problem."
- "Explain the difference between an odds ratio of 2 and a doubling of probability. Give a numerical example where they diverge sharply."
- "My AUC is 0.93 but my precision at the operating threshold is 0.11. Explain how both can be true."
- "Derive the intercept correction for a logistic model fitted on an oversampled training set."
- "Argue both sides: should a credit model be required to equalise false positive rates across nationality groups?"

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

[Back to session 06](../README.md) · [<- Lecture notes](../01-lecture/README.md)
