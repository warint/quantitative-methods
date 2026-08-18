# Session 08 — teaching plan (first half, 90 min)

# Unsupervised Learning I: PCA, the SVD, and Factor Models in Macroeconomics

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

`MATH60033A` · lecture 90 min · lab follows on
*How many independent things are we actually measuring?*

---

## Opening

List a dozen macro series on the board — industrial production, new orders, capacity utilisation, employment, hours, shipments. Ask: *"how many distinct things are being measured here?"* Nobody says twelve.

---

## Board plan

| Minutes | |
|---|---|
| **0–06** | The hook. Note that standardisation is not optional and PCA is a rotation, not a selection. |
| **06–26** | PCA as variance maximisation. Lagrangian, first-order condition, $\hat\Sigma v = \phi v$ — so the answer must be an eigenvector. |
| **26–44** | Via the SVD. Loadings $V$, scores $UD$, variance ratios. **Then the callback worth the whole session:** ridge shrank along this same basis; PCA truncates exactly the directions ridge damps. Eckart–Young. |
| **44–68** | The approximate factor model. $X_{it} = \lambda_i^\top F_t + e_{it}$, consistency as **both** $N, T \to \infty$, and the condition $\sqrt T / N \to 0$ under which estimated factors can be treated as known. **Make the contrast explicit:** in Session 05 more predictors added variance; here more measurements of one latent object average noise away. |
| **68–80** | How many factors: scree, cumulative variance, Bai–Ng $IC_{p1..3}$, Ahn–Horenstein. Report all and say when they disagree. |
| **80–90** | Diffusion-index forecasting, and the rule they will break: factors must be re-estimated at each forecast origin. |

---

## Worked example — do this live

Eigendecompose $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ by hand: eigenvalues 3 and 1, eigenvectors $(1,1)/\sqrt2$ and $(1,-1)/\sqrt2$. 75% of variance on the first component. Thirty seconds, and PCA stops being magic.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Why does adding more noisy series HELP factor estimation, when in Session 05 it hurt the regression?"* This is the best question of the semester. Make them work for it.

---

## Misconception to pre-empt

> That factors are identified. They are identified only up to rotation, so 'Factor 1 is the business cycle' is an interpretation, never an estimate. Require the self-critique in the lab.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

The rotation-indeterminacy statement and the Bai–Ng criterion.

---

## If you are running short

Compress Eckart–Young to the statement. The $N, T$ asymptotics contrast with Session 05 is the intellectual core.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 8`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 08](../README.md) · [Lab](../02-lab/README.md)
