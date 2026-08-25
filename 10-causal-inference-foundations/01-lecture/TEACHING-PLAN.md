# Session 10 — teaching plan (first half, 90 min)

# Causal Machine Learning: Double/Debiased ML and Heterogeneous Effects

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · practice follows on
*Did the policy do anything, or did we just measure the countries that were already ahead?*

---

## Opening

*"You have built a model that predicts regional decline with an AUC of 0.94. A minister asks which programme to fund. What do you tell her?"* Let the room try. The honest answer — that nothing you have done so far licenses an answer — is today.

---

## Board plan

| Minutes | |
|---|---|
| **0–08** | The hook. Potential outcomes, the fundamental problem, the three identifying assumptions. State plainly that no amount of ML substitutes for them. |
| **08–28** | **Why the naive plug-in fails.** Write the three-term decomposition and take the terms one at a time: regularisation bias diverges because ML rates are slower than $n^{-1/2}$; overfitting bias arises from evaluating the nuisance where it was fitted. Two problems, two fixes. |
| **28–55** | **Neyman orthogonality.** The partialling-out score, the FWL reading, and the Gateaux derivative vanishing at the truth. Then the rate arithmetic: $n^{-1/4} \times n^{-1/4} = n^{-1/2}$. **Two slow rates multiply into one fast enough rate — that is why it is called *double*.** |
| **55–70** | Cross-fitting. The algorithm, why term $c$ vanishes, and the median over splits. |
| **70–82** | Heterogeneous effects, causal forests, honesty, and the discipline of reporting subgroup findings as exploratory. |
| **82–90** | **What this does not fix.** DML removes functional-form error, not omitted variables. Return to the Session 03 OVB formula and leave it on the board. |

---

## Worked example — do this live

Do the rate arithmetic explicitly. If $\|\hat\ell - \ell_0\| = O(n^{-1/4})$ and the same for $\hat m$, the bias term is $\sqrt n \cdot n^{-1/4} \cdot n^{-1/4} = \sqrt n \cdot n^{-1/2} = O(1)$ — and with a little more care, $o(1)$. Three lines that make the whole method obvious.

### What the fixtures will give them

The Session 10 treatment (`has_ai_strategy`) has a **true effect of +2.40 pp**, and the fixtures are built so that the control set is the whole lesson:

| Estimator | Estimate | 95% CI | Truth inside? |
|---|---|---|---|
| Naive difference in means | **+6.01** | — | no — 2.5× the truth |
| DML, digital proxies only | **+3.30** | [2.67, 3.92] | **no** |
| DML, + core structural controls | **+2.94** | [2.16, 3.71] | yes |

> **This is the moment of the session.** The middle row is a *tight confidence interval around a wrong number* — precisely what section 10.6 warns about. Cross-fitting and orthogonality removed the ML-induced bias; they did nothing about the confounder the student failed to include. Let a group present the middle row before you reveal the third.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"State Frisch–Waugh–Lovell from memory."* They saw it in Session 02. If they can, today feels inevitable rather than magical — say so.

---

## Misconception to pre-empt

> That flexible machine learning reduces confounding. It reduces functional-form error. A confounded DML estimate is a precisely-quantified wrong number, and its narrow interval makes it *more* dangerous, not less.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the practice

The DML score and the OVB formula, side by side.

---

## If you are running short

Compress causal forests to the three modifications. The orthogonality argument and the rate product are the session.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 10`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- **every member has pushed** before they leave the room

---

[Student notes](README.md) · [Session 10](../README.md) · [Practice](../02-practice/README.md)
