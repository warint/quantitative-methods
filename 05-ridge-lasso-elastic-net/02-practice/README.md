# Session 05 — Group practice (second half, ~90 min)

# Elastic net on a wide macro panel

> **[Open the practice slides](https://warint.github.io/quantitative-methods/session-05-practice.html)** ·
> source: [`MATH60033A-S05-Practice.qmd`](MATH60033A-S05-Practice.qmd)


---

## The theme of this session

> # Of two hundred indicators, which few actually carry the signal?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

Throw your full column family at the elastic net. Report both $\lambda_{\min}$ and $\lambda_{1se}$, and run the bootstrap stability analysis. **Collective payoff:** five stability plots side by side reveal whether robustness is a property of the method or of the data domain.

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

Groups of 3-4, on FRED-MD. You will implement the core of the algorithm yourself
before using the library, and you will confront the stability question head-on.

---

## Tasks

1. Apply the FRED-MD transformation codes to obtain stationary series. Document what you did to each code. Handle the resulting missing values explicitly.
2. Build the design: predict industrial production growth $h$ = 3 months ahead from all available series at $t$ (plus 3 lags). Report $n$ and $p$.
3. Implement `soft_threshold(rho, lam)` and a coordinate-descent lasso in ~30 lines. Verify against `sklearn.linear_model.Lasso` on a small subset. Report the max coefficient difference.
4. Fit ridge, lasso, and elastic net over a grid of $\alpha \in \{0, 0.25, 0.5, 0.75, 1\}$ and 100 values of $\lambda$, using **rolling-origin** CV (Session 4 rules apply). Plot the CV surface.
5. Report both $\lambda_{\min}$ and $\lambda_{1se}$ models. How many non-zero coefficients does each retain? Name them.
6. **Stability check.** Bootstrap the sample 200 times. For each predictor, record the share of bootstrap replicates in which it is selected. Plot the selection frequencies for lasso vs. elastic net. Which is more stable?
7. Plot effective degrees of freedom against $\lambda$ for ridge using the SVD formula. Confirm it decreases from $p$ toward 0.

---

## Deliverable

`groups/A2026/group-XX/session-NN/` with the coordinate-descent implementation,
the CV surface, the stability plot, and a 300-word note answering: *a policymaker asks which
indicators drive industrial production. Given your stability results, what can you honestly tell
them, and what must you refuse to claim?*

Create your group's folder as `groups/A2026/group-XX/session-NN/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this practice requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "Derive the soft-thresholding operator from the subgradient condition. Show every step."
- "My lasso selected 4 variables; when I drop one observation it selects a different 4. Is my code wrong, or is this expected? Explain."
- "Explain why standardising predictors is mandatory for penalised regression but irrelevant for OLS coefficients' interpretation."

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

[Back to session 05](../README.md) · [<- Lecture notes](../01-lecture/README.md)
