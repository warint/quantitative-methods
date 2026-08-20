# Session 08 — Group lab (second half, ~90 min)

# Building a diffusion index and nowcasting with it

---

## The theme of this session

> # How many independent things are we actually measuring?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

Extract factors from your own columns, report the Bai-Ng criteria, label your leading factor and then argue against your own label. **Collective step:** the five leading factors are pooled and the class examines their correlation structure — a direct test of the scenario's premise that compute is the dominant measure of capability.

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

Groups of 3-4 on FRED-MD. You will implement PCA from the SVD, select the number of
factors three ways, interpret them, and produce an honest out-of-sample forecast.

---

## Tasks

1. Implement `pca_svd(X, k)` returning scores, loadings and variance ratios. Verify against `sklearn.decomposition.PCA` (allowing for sign indeterminacy - explain why signs may flip).
2. Extract factors from the standardised, stationary FRED-MD panel. Plot the scree curve and cumulative variance.
3. Implement the Bai-Ng $IC_{p1}$, $IC_{p2}$ and $IC_{p3}$ criteria. Report $\hat r$ under each. Add the Ahn-Horenstein eigenvalue ratio. Do they agree?
4. **Interpret.** For each of the first four factors, list the 10 series with the largest absolute loadings. Propose an economic label - then argue against your own label using the rotation-indeterminacy point.
5. Plot the first factor against NBER recession shading. Comment.
6. Build the diffusion-index forecast of industrial production 3 months ahead. Compare out-of-sample RMSE against (a) an AR(4) benchmark and (b) your Session 5 elastic net on raw series.
7. **The look-ahead test.** Deliberately extract factors once on the full sample and re-run the backtest. Report the RMSE improvement you obtain illegitimately. This number is your leakage budget - remember it.
8. Reconstruct the panel from $k$ factors and report the Frobenius error. Confirm it matches $\sqrt{\sum_{j>k} d_j^2}$.

---

## Deliverable

`02-lab/submissions/group-XX/` with the factor-selection comparison table, the
loadings interpretation with its self-critique, the three-way forecast comparison, and a 300-word
note quantifying the look-ahead bias and explaining to a non-technical reader why it is fraud rather
than optimism.

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

- "My PCA loadings have the opposite sign from the textbook figure. Is my code wrong?"
- "Explain why more predictor series improves factor estimation but hurts an unregularised regression. Reconcile the two intuitions."
- "Write the Bai-Ng IC_p2 criterion and explain what property the penalty term must satisfy."

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

[Back to session 08](../README.md) · [<- Lecture notes](../01-lecture/README.md)
