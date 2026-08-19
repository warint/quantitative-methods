# Session 06 — teaching plan (first half, 90 min)

# Classification: Logistic Regression, Regularisation, and Decision Thresholds

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · lab follows on
*Can we flag a country or sector falling behind one year ahead — and what does a false alarm cost?*

---

## Opening

Announce: *"my model is 97% accurate."* Pause. *"The base rate is 2%."* Let the room work out that predicting 'never' scores 98%. Then say: today is about the difference between a probability and a decision.

---

## Board plan

| Minutes | |
|---|---|
| **0–05** | The hook. |
| **05–20** | **Part A.** Two routes to the logistic model — the link function, and the latent random-utility formulation. Economists should see the second. |
| **20–42** | Likelihood, score $X^\top(y-p)$, Hessian $-X^\top W X$, **concavity**. Point out that the score is the OLS orthogonality condition with fitted probabilities. Note that no later method in this course has this guarantee. |
| **42–52** | IRLS. Show the Newton step rearranging into weighted least squares on the adjusted response. Then perfect separation — the MLE does not exist. **Leave this unresolved; Part B disposes of it in one line.** |
| **52–62** | Interpretation: log-odds, odds ratio, marginal effect, average marginal effect. Insist on the last one. |
| **62–75** | Evaluation. Confusion matrix, ROC/AUC, precision–recall under imbalance, and **derive $\tau^\star = c_{FP}/(c_{FP}+c_{FN})$**. Then calibration as a property distinct from discrimination. |
| **75–84** | **Part B.** Add the Session 05 penalty. One line: the penalty dominates the likelihood's drive to infinity, so separation is cured. Then the composition — outer IRLS, inner coordinate descent, same soft-thresholding operator. |
| **84–90** | Imbalance: the three interventions table, and the recommendation. Stability reporting. |

---

## Worked example — do this live

$x^\top\hat\beta = -3.2 + 0.045(40) + 0.8 = -0.60$, so $p = 0.354$. Odds ratio $e^{0.8} = 2.23$. Marginal effect $0.045 \times 0.354 \times 0.646 = 1.03$ percentage points. With $c_{FN} = 4c_{FP}$, $\tau^\star = 0.20$ — and since $0.354 > 0.20$, this applicant is flagged, where the default 0.5 would have passed them. **That reversal is the session.**

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"AUC is 0.93 and precision at the operating threshold is 0.11. Explain how both can be true."* AUC is threshold-free ranking; precision is one threshold under a 2% base rate.

---

## Misconception to pre-empt

> That resampling or class weights 'fix' imbalance for free. They shift the prior and destroy calibration. Fit unweighted, verify calibration, move the threshold. If you teach one thing from Part B, teach this.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

$\tau^\star = c_{FP}/(c_{FP}+c_{FN})$ and the three-interventions table.

---

## If you are running short

This is the densest session — Part B is deliberately short because the room derived both halves already. If you are behind, compress interpretation (6.4) to the average-marginal-effect recommendation and keep the threshold derivation.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 6`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 06](../README.md) · [Lab](../02-lab/README.md)
