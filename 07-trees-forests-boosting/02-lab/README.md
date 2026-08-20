# Session 07 — Group lab (second half, ~90 min)

# Does flexibility pay? A controlled comparison

---

## The theme of this session

> # Is the relationship non-linear — and can you still explain it to a minister?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

Random forest and gradient boosting against your Session 05 elastic net on **identical folds**, then PDP, ICE and SHAP. The question is not which model wins but whether the gain justifies what you give up.

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

Groups of 3-4. Using the **same folds and the same seed** as your Session 5 elastic
net, you will find out whether the non-linear machinery earns its cost - and then explain the
winning model.

---

## Tasks

1. Implement `best_split(X, y)` for a single node under squared loss, in under 25 lines. Verify against a depth-1 `DecisionTreeRegressor`.
2. Fit a single deep tree on Ames, then prune by cost-complexity with CV over `ccp_alpha`. Plot CV error against $\gamma$ and against tree size.
3. Fit a random forest. Sweep $m$ from 1 to $p$; plot OOB error against $m$. Locate the minimum and relate it to the $\rho\sigma^2$ formula.
4. Fit gradient boosting. Grid over $\nu \in \{0.01, 0.05, 0.1\}$, depth $\in \{2,3,5\}$, with early stopping on a validation fold. Report the $(\nu, M)$ trade you observe.
5. **The comparison table.** On identical CV folds, report test RMSE for: OLS (S2), elastic net (S5), pruned tree, random forest, gradient boosting. Include fit time. Is the accuracy gain worth it?
6. Compute permutation importance twice: once on the full feature set, once after removing one member of each highly correlated pair. Explain the difference.
7. Produce PDP + ICE curves for `GrLivArea` and `OverallQual`. Find one feature where the ICE curves fan out - what does that heterogeneity mean economically?
8. Compute SHAP values for the five most expensive and five cheapest predicted houses. Do the explanations differ systematically?

---

## Deliverable

`02-lab/submissions/group-XX/` with the five-model comparison table, the OOB-vs-$m$
curve, PDP/ICE and SHAP figures, and a 400-word note: *you must present one model to a municipal
housing authority. Which do you choose, and how do you defend the choice on grounds other than
RMSE?*

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

- "Explain why permutation importance is misleading when two features are correlated at 0.95. Use a concrete example."
- "My gradient boosting model has training RMSE near zero and test RMSE worse than OLS. List the three most likely causes in order."
- "What is the difference between a partial dependence plot and an ICE plot, and when does the difference matter?"

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

[Back to session 07](../README.md) · [<- Lecture notes](../01-lecture/README.md)
