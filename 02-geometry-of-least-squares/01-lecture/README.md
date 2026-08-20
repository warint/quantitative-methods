# Session 02 — Lecture (first half, ~90 min)

# Data, Vectors, and the Geometry of Least Squares

> **Why is the most-used estimator in economics a right-angle triangle?**

---

### 2.1 The model in matrix form

Stack the data: $y \in \mathbb{R}^n$, $X \in \mathbb{R}^{n \times p}$ (first column a vector of
ones), $\beta \in \mathbb{R}^p$, $\varepsilon \in \mathbb{R}^n$:

$$y = X\beta + \varepsilon.$$

We seek $\hat\beta$ minimising the residual sum of squares

$$S(\beta) = \|y - X\beta\|_2^2 = (y - X\beta)^\top (y - X\beta).$$

### 2.2 Route 1 - calculus

Expand: $S(\beta) = y^\top y - 2\beta^\top X^\top y + \beta^\top X^\top X \beta$. Differentiate:

$$\frac{\partial S}{\partial \beta} = -2X^\top y + 2X^\top X\beta \stackrel{!}{=} 0
\quad\Longrightarrow\quad \boxed{X^\top X \hat\beta = X^\top y}$$

- the **normal equations**. If $X$ has full column rank, $\hat\beta = (X^\top X)^{-1} X^\top y$.
The Hessian is $2X^\top X \succeq 0$, so the stationary point is a global minimum. $S$ is convex.

### 2.3 Route 2 - geometry (the one worth remembering)

$X\beta$ ranges over $\mathcal{C}(X)$, a $p$-dimensional subspace of $\mathbb{R}^n$. Minimising
$\|y - X\beta\|$ means: **find the point in $\mathcal{C}(X)$ closest to $y$.** By the projection
theorem, that point is the orthogonal projection of $y$ onto $\mathcal{C}(X)$, and it is
characterised by the residual being orthogonal to the subspace:

$$X^\top (y - X\hat\beta) = 0,$$

which *is* the normal equations. The two routes are the same statement in different clothes.

Define the **hat matrix** $H = X(X^\top X)^{-1}X^\top$. Then

$$\hat y = Hy, \qquad \hat\varepsilon = (I - H)y, \qquad H(I-H) = 0 .$$

Consequences worth internalising:

- $\operatorname{tr}(H) = p$: the projection uses exactly $p$ degrees of freedom.
- $h_{ii} \in [0,1]$ is observation $i$'s **leverage** - how much $\hat y_i$ moves when $y_i$ moves.
- $\|y\|^2 = \|\hat y\|^2 + \|\hat\varepsilon\|^2$ is Pythagoras. $R^2$ is a squared cosine.

### 2.4 Adding a regressor: Frisch-Waugh-Lovell

Partition $X = [X_1 \; X_2]$. Then $\hat\beta_2$ from the full regression equals the coefficient
from regressing $M_1 y$ on $M_1 X_2$, where $M_1 = I - X_1(X_1^\top X_1)^{-1}X_1^\top$.

**In words:** a multiple-regression coefficient is a *simple* regression coefficient on the part of
the variable that is orthogonal to everything else. This single theorem explains "controlling for",
it explains why collinearity inflates variance, and it will reappear in Session 11 as the
foundation of double machine learning. Learn it now.

### 2.5 Numerical warning

Never compute $(X^\top X)^{-1}$. Forming $X^\top X$ squares the condition number,
$\kappa(X^\top X) = \kappa(X)^2$, so you lose roughly twice as many digits of precision. Use the
QR decomposition $X = QR$ with $Q^\top Q = I$ and $R$ upper triangular; then

$$R\hat\beta = Q^\top y$$

is solved by back-substitution. This is what `numpy.linalg.lstsq` and `statsmodels` do internally.
You will verify the precision difference yourself in the lab.

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

[Back to session 02](../README.md) · [On to the lab ->](../02-lab/README.md)
