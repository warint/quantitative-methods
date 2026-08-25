# Session 07 — teaching plan (first half, 90 min)

# Trees, Forests, and Gradient Boosting

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · practice follows on
*Is the relationship non-linear — and can you still explain it to a minister?*

---

## Opening

Draw a step function over a scatter. Ask: *"what kind of economic relationship is naturally a step function, and what kind is distorted by one?"* Trees are not a model of the world; they are a partition of it.

---

## Board plan

| Minutes | |
|---|---|
| **0–06** | The hook and the framing. |
| **06–26** | Recursive binary splitting. The greedy objective, why the global problem is infeasible, the $O(pn\log n)$ scan. Impurity measures and why misclassification error is a poor *growing* criterion but the right *pruning* one. |
| **26–40** | Cost-complexity pruning, weakest-link, and the callback: another complexity dial, selected by CV, exactly as $\lambda$ was. |
| **40–60** | **The variance formula.** $\rho\sigma^2 + \frac{1-\rho}{B}\sigma^2$. Derive it, then read the limit: increasing $B$ cannot help past $\rho\sigma^2$. *That* is why random forests subsample features. OOB error. |
| **60–80** | Gradient boosting as functional gradient descent. Pseudo-residuals; show that under squared loss they are the residual and under logistic loss they are $y - p$ from Session 06. Shrinkage and the $\nu$–$M$ trade. |
| **80–90** | Interpretation table. Emphasise that permutation importance breaks under correlation, and that SHAP describes the model, not the world. |

---

## Worked example — do this live

Variance of the average with $\sigma^2 = 1$: at $\rho = 0.6$ and $B = 100$ you get $0.604$; at $B = \infty$, $0.600$. At $\rho = 0.1$: $0.109$ and $0.100$. Two lines of arithmetic that make the entire random-forest design obvious.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Why do impurity-based importances favour continuous and high-cardinality variables?"* More candidate split points, more chances to reduce impurity by noise.

---

## Misconception to pre-empt

> That a large SHAP value means the feature causes the outcome. It means the model relies on it. Say it now, because Session 10 depends on the distinction being already uncomfortable.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the practice

The bagging variance formula and the interpretation-tools table.

---

## If you are running short

Compress impurity measures. The variance formula and the pseudo-residual connection are the two things that must land.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 7`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- **every member has pushed** before they leave the room

---

[Student notes](README.md) · [Session 07](../README.md) · [Practice](../02-practice/README.md)
