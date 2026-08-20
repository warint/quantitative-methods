# Session 04 — teaching plan (first half, 90 min)

# The Bias-Variance Tradeoff, Overfitting, and Cross-Validation

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · practice follows on
*Are we predicting, or only describing the past?*

---

## Opening

Plot 20 points from a smooth function with noise. Fit a degree-19 polynomial through every one. $R^2 = 1$. Ask: *"is this a good model?"* Everyone says no. Then ask: *"prove it."* They cannot — yet. That is today.

---

## Board plan

| Minutes | |
|---|---|
| **0–08** | The hook, and the framing: **this session is the hinge of the course.** Before today, in-sample fit was evidence. After today it is not. |
| **08–35** | Derive the bias–variance decomposition in full. Add and subtract $\mathbb{E}[\hat f(x_0)]$, expand, kill the three cross terms one at a time and say why each vanishes. Do not rush; this is the most quoted and least understood result in the field. |
| **35–55** | Optimism. $\mathbb{E}[\mathrm{Err_{in}}] - \mathbb{E}[\mathrm{err}] = \frac{2}{n}\sum_i \operatorname{Cov}(\hat y_i, y_i)$. Read it aloud in words: *twice the degree to which the model chases its own labels.* Then $C_p$, AIC, BIC, and effective degrees of freedom as the generalisation of 'number of parameters' — needed from Session 05 on. |
| **55–72** | Cross-validation. The estimator, the bias–variance tradeoff in $K$, LOOCV and the hat-matrix shortcut $\frac1n\sum_i((y_i-\hat y_i)/(1-h_{ii}))^2$ — callback to Session 02. |
| **72–90** | **The three leaks.** Preprocessing, selection, dependence. Spend real time here: this is the content students most need and least expect. |

---

## Worked example — do this live

Fill in the bias–variance table live. $\sigma^2 = 0.09$; degree 3 gives $0.09+0.06+0.09 = 0.24$; degree 5 gives $0.02+0.14+0.09 = 0.25$. **Then make the point that the minimum is flat** — 0.24 vs 0.25 is inside Monte Carlo noise — and that this is why the one-standard-error rule exists.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"You standardise your features on the full dataset, then run 5-fold CV. What exactly has gone wrong?"* Push until someone says: the test fold influenced the mean and standard deviation used to transform the training rows.

---

## Misconception to pre-empt

> That the CV error of the *selected* model is an unbiased estimate of its performance. It is not — selection used the same data. Nested CV, or an untouched holdout. This is the error that most often survives peer review.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the practice

The decomposition, and the three leaks as a numbered list. Both are practice tasks.

---

## If you are running short

Compress AIC/BIC to a sentence. Do not cut the leaks — the whole rest of the course assumes them.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 4`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- **every member has pushed** before they leave the room

---

[Student notes](README.md) · [Session 04](../README.md) · [Practice](../02-practice/README.md)
