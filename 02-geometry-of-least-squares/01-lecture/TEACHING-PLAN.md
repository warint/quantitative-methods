# Session 02 — teaching plan (first half, 90 min)

# Data, Vectors, and the Geometry of Least Squares

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

`MATH60033A` · lecture 90 min · lab follows on
*How much of the measured gap is real, and how much is composition?*

---

## Opening

Draw $\mathbb{R}^3$ on the board. Draw a plane through the origin — that is $\mathcal{C}(X)$. Draw a vector $y$ sticking out of it. Ask: *"where is the closest point in the plane?"* Everyone knows: drop a perpendicular. Then say — that is the entire content of least squares, and we are going to spend ninety minutes on it.

---

## Board plan

| Minutes | |
|---|---|
| **0–05** | The picture. Leave it up all session. |
| **05–20** | Matrix setup, $S(\beta) = \|y - X\beta\|^2$, differentiate, normal equations. Quick — this is the route they have seen. |
| **20–45** | The geometric route. Projection theorem, orthogonality of the residual, $X^\top(y - X\hat\beta) = 0$. **Make the point explicitly: these are the same equation.** Students who see this once stop being confused by 'controlling for'. |
| **45–65** | Hat matrix. $\hat y = Hy$, idempotence, $\operatorname{tr}(H) = p$, leverage, Pythagoras and $R^2$ as a squared cosine. |
| **65–82** | **Frisch–Waugh–Lovell.** Derive it, then say the sentence they should remember: *a multiple-regression coefficient is a simple regression coefficient on the part of the variable orthogonal to everything else.* Flag that it returns in Session 10 as the foundation of double ML. |
| **82–90** | Numerical warning: $\kappa(X^\top X) = \kappa(X)^2$. Never invert. |

---

## Worked example — do this live

Do the 2×2 by hand on the board. $X^\top X = \begin{pmatrix}10&4\\4&8\end{pmatrix}$, $X^\top y = (26, 20)^\top$. Determinant 64, $\hat\beta = (2.00, 1.50)$. Two minutes, and it makes the algebra concrete. They meet these exact numbers again on the midterm.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Why does adding a variable never decrease $R^2$? Answer geometrically, not algebraically."* The answer — you enlarged the subspace, so the projection can only get closer — is the test of whether the picture landed.

---

## Misconception to pre-empt

> That multicollinearity **biases** coefficients. It does not. OLS remains unbiased under near-collinearity; what inflates is the variance. Say this explicitly, because half the room believes otherwise and it corrupts Session 03.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

The projection picture and the FWL sentence.

---

## If you are running short

Compress the calculus route to five minutes. Never cut FWL.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 2`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 02](../README.md) · [Lab](../02-lab/README.md)
