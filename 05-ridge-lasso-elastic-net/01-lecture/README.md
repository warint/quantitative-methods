# Session 05 — Lecture (first half, ~90 min)

# Regularisation: Ridge, Lasso, and the Elastic Net

> **When is a deliberately biased estimator the better one?**

---

### 5.1 Ridge regression

$$\hat\beta^{\text{ridge}} = \arg\min_\beta \Big\{ \|y - X\beta\|_2^2 + \lambda\|\beta\|_2^2 \Big\}
= (X^\top X + \lambda I)^{-1} X^\top y .$$

The added $\lambda I$ makes the matrix positive definite for any $\lambda > 0$, **even when $p > n$**.
Regularisation is not only a bias-variance device; it is what makes the problem well-posed at all.

**What ridge does, in the SVD basis.** With $X = UDV^\top$:

$$\hat y^{\text{ridge}} = \sum_{j=1}^{p} u_j \frac{d_j^2}{d_j^2 + \lambda} \, u_j^\top y .$$

Compare OLS, which is the same sum with every factor equal to 1. Ridge multiplies the $j$-th
principal component of the design by $d_j^2/(d_j^2+\lambda) \in (0,1)$. Directions with **large**
$d_j$ - where the data vary a lot - are barely touched. Directions with **small** $d_j$ - where the
data are nearly collinear and the OLS coefficient is wildly unstable - are shrunk hard.

Ridge is therefore not a blunt instrument. It is a *targeted* damping of exactly the directions in
which your data carry little information. The effective degrees of freedom are
$\mathrm{df}(\lambda) = \sum_j d_j^2/(d_j^2+\lambda)$, decreasing smoothly from $p$ to $0$.

**Bias-variance, explicitly.** $\mathrm{Var}(\hat\beta^{\text{ridge}})$ is decreasing in
$\lambda$ while $\mathrm{Bias}^2$ is increasing. There always exists $\lambda > 0$ whose MSE
is strictly lower than OLS - a result that surprised the profession in 1970 and should still shape
how you think about Gauss-Markov.

### 5.2 The lasso

$$\hat\beta^{\text{lasso}} = \arg\min_\beta \Big\{ \tfrac{1}{2n}\|y - X\beta\|_2^2 + \lambda\|\beta\|_1 \Big\} .$$

No closed form. But in the equivalent constrained formulation, minimise RSS subject to
$\|\beta\|_1 \le t$: the constraint region is a cross-polytope (a diamond in 2-D), which has
**corners on the axes**. The elliptical RSS contours expanding outward from $\hat\beta^{OLS}$ meet
this region, generically, at a corner - and a corner is a point where some coordinates are exactly
zero. The $\ell_2$ ball, by contrast, is smooth: it has no corners, so ridge shrinks but never
zeroes.

**Coordinate descent and soft-thresholding.** Hold all $\beta_k$, $k\neq j$, fixed. With
standardised columns ($\frac1n\sum_i x_{ij}^2 = 1$), the univariate problem is

$$\min_{\beta_j} \; \tfrac{1}{2}(\beta_j - \rho_j)^2 + \lambda|\beta_j|, \qquad
\rho_j = \tfrac1n \textstyle\sum_i x_{ij}\big(y_i - \sum_{k\neq j} x_{ik}\beta_k\big).$$

The objective is convex but non-differentiable at $0$. Using the subgradient of $|\beta_j|$ (which
is $[-1,1]$ at zero), the solution is the **soft-thresholding operator**

$$\hat\beta_j = S_\lambda(\rho_j) = \mathrm{sign}(\rho_j)\,\big(|\rho_j| - \lambda\big)_+ .$$

Read it directly: *if the partial correlation of $x_j$ with the residual is smaller in magnitude
than $\lambda$, set the coefficient to exactly zero; otherwise shrink it toward zero by $\lambda$.*
Cycling this update over $j$ converges, and it is why `glmnet` and scikit-learn are fast.

**Limitations you must know.** (i) With $p > n$, the lasso selects at most $n$ variables.
(ii) Among a group of highly correlated predictors, it tends to pick one arbitrarily and zero the
rest - which is unstable across samples and often economically absurd. (iii) Its selected set is
consistent only under strong conditions (the "irrepresentable condition"). Do not present a lasso
path as if it identified the true model.

### 5.3 The elastic net

$$\hat\beta^{\text{EN}} = \arg\min_\beta \Big\{ \tfrac{1}{2n}\|y-X\beta\|_2^2
+ \lambda\big[\alpha \|\beta\|_1 + \tfrac{1-\alpha}{2}\|\beta\|_2^2\big] \Big\}, \qquad \alpha \in [0,1].$$

$\alpha = 1$ is the lasso, $\alpha = 0$ is ridge. The mixed penalty is **strictly convex** whenever
$\alpha < 1$, which delivers the property Zou and Hastie call the *grouping effect*: for two
identical predictors, the elastic net assigns them identical coefficients, whereas the lasso must
choose. More generally, the difference in coefficients is bounded by a function of
$1 - \mathrm{corr}(x_j, x_k)$.

For macroeconomic panels - where dozens of series measure nearly the same underlying construct -
this is not a technicality. It is the difference between a model that says *"industrial production
matters"* and one that says *"industrial production of durable goods excluding motor vehicles,
specifically, and none of its neighbours."*

The coordinate update becomes $\hat\beta_j = \dfrac{S_{\lambda\alpha}(\rho_j)}{1 + \lambda(1-\alpha)}$
- soft-threshold, then divide.

### 5.4 Choosing the tuning parameters

Fit over a decreasing grid of $\lambda$ from $\lambda_{\max} = \max_j |x_j^\top y|/(n\alpha)$
(the smallest $\lambda$ giving the null model) down to $\varepsilon\lambda_{\max}$, using warm
starts. Cross-validate jointly over $(\alpha, \lambda)$.

Two conventions:
- $\lambda_{\min}$: the value minimising CV error.
- $\lambda_{1\text{se}}$: the largest $\lambda$ within one standard error of the minimum - a
  simpler model whose performance is statistically indistinguishable. Prefer it when the model must
  be explained to someone.

**Inference warning.** Standard errors reported after lasso selection are not valid, because
selection used the same data. Naive post-selection $p$-values are badly anti-conservative. This
motivates the debiased methods of Session 10.

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

[Back to session 05](../README.md) · [On to the practice ->](../02-practice/README.md)
