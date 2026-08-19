# Session 05 — teaching plan (first half, 90 min)

# Regularisation: Ridge, Lasso, and the Elastic Net

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · lab follows on
*Of two hundred indicators, which few actually carry the signal?*

---

## Opening

Write on the board: *"OLS is the best linear unbiased estimator."* Then: *"today we are going to do better than best."* Wait for the objection. The resolution — we leave the unbiased class — is the whole session in one sentence.

---

## Board plan

| Minutes | |
|---|---|
| **0–06** | The hook and the Gauss–Markov callback. |
| **06–32** | Ridge. Closed form, existence for $p > n$, then **the SVD reading**: $\hat y = \sum_j u_j \frac{d_j^2}{d_j^2+\lambda}u_j^\top y$. Make the point that ridge is *targeted*: it damps exactly the directions where the data carry least information. Effective df. |
| **32–52** | Lasso. Draw the diamond and the ellipse. The corner argument. Then contrast with the smooth $\ell_2$ ball — no corners, no zeros. |
| **52–70** | **Derive soft-thresholding** from the subgradient condition at zero. This is the derivation of the session; do it properly. Land on $S_\lambda(\rho) = \operatorname{sign}(\rho)(|\rho|-\lambda)_+$ and read it aloud in words. |
| **70–82** | Elastic net. Strict convexity, the grouping effect, why it matters for macro panels where a dozen series measure one construct. |
| **82–90** | Choosing $\lambda$: the path, $\lambda_{\min}$ vs $\lambda_{1se}$, and the warning that post-selection standard errors are invalid. |

---

## Worked example — do this live

Soft-threshold $\rho = (0.42, -0.18, 0.09, 0.31)$ at $\lambda = 0.20$: $(0.22, 0, 0, 0.11)$ — two survive. Then elastic net, $\alpha = 0.5$: threshold at 0.10, divide by 1.10, giving $(0.291, -0.073, 0, 0.191)$ — three survive. The contrast in one minute is worth twenty minutes of discussion.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Two predictors are correlated at 0.99 and both matter. What does the lasso do?"* It picks one, roughly arbitrarily, and a different one on a resampled dataset. That instability is the lab.

---

## Misconception to pre-empt

> That the lasso selects the *true* model. It does so only under strong conditions, and never reliably under correlation. Never let a lasso path be presented as variable identification — this is the single most common over-claim in applied work.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

$S_\lambda(\rho)$ and the two constraint regions side by side.

---

## If you are running short

Compress the effective-df discussion. The soft-thresholding derivation is the point of the session and Session 06 builds directly on it.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 5`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 05](../README.md) · [Lab](../02-lab/README.md)
