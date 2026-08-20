# Session 07 — Lecture (first half, ~90 min)

# Trees, Forests, and Gradient Boosting

> **If we abandon linearity, what do we lose - and is interpretability recoverable?**

---

### 7.1 Regression trees

Partition the feature space into $M$ regions $R_1,\dots,R_M$ and predict a constant in each:
$\hat f(x) = \sum_m c_m \mathbb{1}\{x \in R_m\}$. Under squared loss the optimal constant is the
region mean, $\hat c_m = \operatorname{ave}(y_i \mid x_i \in R_m)$.

Finding the optimal partition is computationally infeasible, so we proceed **greedily**. At each
node, search over splitting variable $j$ and split point $s$ to solve

$$\min_{j,s}\ \Big[ \min_{c_1}\sum_{x_i \in R_1(j,s)}(y_i - c_1)^2 + \min_{c_2}\sum_{x_i \in R_2(j,s)}(y_i - c_2)^2 \Big],$$

where $R_1(j,s) = \{x : x_j \le s\}$ and $R_2(j,s) = \{x: x_j > s\}$. The inner minimisations are
just means, so a single scan over sorted values of each feature suffices; the cost is
$O(p\, n \log n)$ per node.

For classification, replace variance with an impurity measure on the node class proportions
$\hat p_{mk}$:

$$\text{Gini} = \sum_{k} \hat p_{mk}(1-\hat p_{mk}), \qquad
\text{Entropy} = -\sum_k \hat p_{mk}\log \hat p_{mk}, \qquad
\text{Misclassification} = 1 - \max_k \hat p_{mk}.$$

Gini and entropy are differentiable and strictly concave, so they reward splits that produce
*purer* nodes even when the majority class does not change. Misclassification error is insensitive
to this and makes a poor growing criterion - though it is the right criterion for **pruning**.

### 7.2 Cost-complexity pruning

Grow a large tree $T_0$, then choose a subtree minimising

$$C_\gamma(T) = \sum_{m=1}^{|T|} \sum_{x_i \in R_m}(y_i - \hat c_m)^2 + \gamma|T| .$$

**Weakest-link pruning:** as $\gamma$ increases from 0, the sequence of optimal subtrees is nested
and obtained by successively collapsing the internal node with the smallest per-leaf increase in
error. This gives a one-dimensional family indexed by $\gamma$ - which we then select by
cross-validation, exactly as we selected $\lambda$ in Session 5. The structural parallel is worth
noticing: *every* method in this course has a complexity dial and a CV procedure for setting it.

### 7.3 Bagging and the variance argument

Average $B$ trees fitted on bootstrap samples. If each has variance $\sigma^2$ and any two have
correlation $\rho$, the average has variance

$$\operatorname{Var}\Big(\frac1B\sum_b \hat f_b\Big) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2
\;\xrightarrow[B\to\infty]{}\; \rho\sigma^2 .$$

Increasing $B$ kills the second term but leaves $\rho\sigma^2$ untouched. **This is the entire
motivation for random forests.** If one predictor is strongly dominant, every bagged tree splits on
it first and the trees are nearly identical: $\rho \approx 1$ and bagging buys almost nothing.

**Random forests** decorrelate by restricting each split to a random subset of $m$ features
(defaults: $m = \lfloor \sqrt p \rfloor$ for classification, $\lfloor p/3\rfloor$ for regression).
Lower $m$ lowers $\rho$ but raises individual-tree bias - a bias-variance tradeoff *within* the
ensemble, tuned by CV.

Bagging also gives a free error estimate: each observation is out-of-bag for roughly
$(1 - 1/n)^n \to e^{-1} \approx 36.8\%$ of trees, so the **OOB error** approximates CV error at no
extra cost.

### 7.4 Gradient boosting as functional gradient descent

Instead of averaging independent trees, build them **sequentially**, each correcting its
predecessor. Think of minimising $\sum_i L(y_i, F(x_i))$ over the *function* $F$, by gradient
descent in function space.

At stage $m$, the negative gradient evaluated at the current fit is the "pseudo-residual"

$$r_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F = F_{m-1}} .$$

For squared loss, $r_{im} = y_i - F_{m-1}(x_i)$: literally the residual. For logistic loss,
$r_{im} = y_i - p_{m-1}(x_i)$: the same probability residual as in Session 6. Fit a small tree
$h_m$ to the pseudo-residuals and update

$$F_m(x) = F_{m-1}(x) + \nu\, \gamma_m h_m(x), \qquad 0 < \nu \le 1 .$$

The **shrinkage** $\nu$ (learning rate) is essential: small $\nu$ (0.01-0.1) with many trees
generalises far better than large $\nu$ with few. There is a direct trade: halving $\nu$ roughly
doubles the required $M$. Three tuning parameters interact - $\nu$, $M$, and tree depth $d$ (which
controls the maximum interaction order captured: $d=1$ is additive, $d=2$ allows two-way
interactions).

Modern implementations (XGBoost, LightGBM) add a second-order expansion and an explicit penalty:

$$\mathcal{L}^{(m)} \approx \sum_i \Big[g_i h_m(x_i) + \tfrac12 h_i h_m(x_i)^2\Big] + \Omega(h_m),
\qquad \Omega(h) = \gamma |T| + \tfrac12 \lambda \|w\|^2,$$

with $g_i, h_i$ the first and second derivatives of the loss. Solving for the optimal leaf weights
gives $w_j^\star = -G_j/(H_j+\lambda)$ - regularisation reappearing, in a third guise.

### 7.5 Recovering interpretation

| Method | What it answers | Key assumption / caveat |
|---|---|---|
| Impurity importance | how often and how usefully a feature was split on | Biased toward high-cardinality features; computed in-sample |
| **Permutation importance** | how much test error rises when the feature is scrambled | **Breaks down under correlated features** - creates impossible data points |
| Partial dependence $\hat f_S(x_S) = \frac1n\sum_i \hat f(x_S, x_{C,i})$ | average marginal relationship | Assumes $x_S \perp x_C$; hides heterogeneity |
| ICE curves | per-observation version of PDP | Reveals the heterogeneity PDP averages away |
| **SHAP** | additive attribution per prediction, from cooperative game theory | Unique under efficiency/symmetry/dummy/additivity axioms; costly; still assumes a value function |

**The honest summary:** these tools describe the *model*, not the world. A large SHAP value means
the model relies on that feature, not that the feature causes the outcome. Session 10 is where we
finally take causality seriously.

---

## Notation reminders used throughout the course

| Symbol | Meaning |
|---|---|
| $n$, $p$ | number of observations, number of predictors |
| $X$ | $n \times p$ design matrix (first column ones, unless stated) |
| $y$ | $n$-vector of outcomes |
| $\hat\beta$ | estimated coefficient vector |
| $\hat y = X\hat\beta$ | fitted values |
| $H = X(X^\top X)^{-1}X^\top$ | hat (projection) matrix |
| $\lambda$, $\alpha$ | penalty strength, elastic-net mixing parameter |
| $L(y,\hat y)$ | loss function |

> **Rendering the mathematics.** These notes use LaTeX. In VS Codium, install the
> *Markdown+Math* or *Markdown Preview Enhanced* extension and open the preview with
> `Ctrl/Cmd+K V`. See the [setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).

---

[Back to session 07](../README.md) · [On to the practice ->](../02-practice/README.md)
