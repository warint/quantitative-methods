# Session 03 — teaching plan (first half, 90 min)

# Linear Regression: Inference, Diagnostics, and Interpretation

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · lab follows on
*Which of these differences would survive a referee?*

---

## Opening

Project a regression table with three stars on a coefficient. Ask: *"under what conditions does that number mean anything?"* Then reveal that the data are 27 countries over 14 years with classical standard errors. Let someone object.

---

## Board plan

| Minutes | |
|---|---|
| **0–05** | The hook. |
| **05–20** | $\hat\beta = \beta + (X^\top X)^{-1}X^\top\varepsilon$. Write it large. Say: *everything in regression inference follows from what you assume about $\varepsilon$.* Unbiasedness needs only exogeneity. |
| **20–42** | Variance. Derive $\sigma^2(X^\top X)^{-1}$, then expand to $\sigma^2 / (n \operatorname{Var}(x_j)(1 - R_j^2))$ and **read off the four levers** — noise, sample size, variation, redundancy. This single expression explains collinearity, and it motivates Session 05. |
| **42–56** | Gauss–Markov. Sketch the proof. Then the caveat that matters: BLUE is a guarantee *within unbiased estimators*, and Session 05 will deliberately leave that class. |
| **56–75** | The sandwich. Robust (HC1), cluster-robust, and the rule: cluster at the level at which treatment is assigned. Warn about few clusters. |
| **75–90** | Omitted variable bias. Derive $\mathbb{E}[\hat\beta_1] = \beta_1 + \delta\beta_2$ and give the two-question recipe for signing it. |

---

## Worked example — do this live

OVB with numbers. True $\beta_2 = 0.08$, auxiliary $\delta_1 = 0.6$, so the bias is $+0.048$. If the short regression reports 0.112, the implied $\beta_1$ is 0.064. Have the room sign it before you compute it.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Your robust standard errors come out SMALLER than the classical ones. Is that possible?"* Yes — robust SEs are not uniformly larger. Students who think otherwise are pattern-matching rather than understanding the sandwich.

---

## Misconception to pre-empt

> That clustering always inflates standard errors, and that a large standard error is evidence of a small coefficient. Failure to reject is not acceptance. Say it twice; it is the most common error in their write-ups.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

$\operatorname{Var}(\hat\beta_j) = \sigma^2 / (n\operatorname{Var}(x_j)(1-R_j^2))$ and the OVB formula.

---

## If you are running short

Compress Gauss–Markov to the statement plus the caveat. The variance decomposition and OVB are both load-bearing later.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 3`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 03](../README.md) · [Lab](../02-lab/README.md)
