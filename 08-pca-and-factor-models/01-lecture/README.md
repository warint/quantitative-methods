# Session 08 — Lecture (first half, ~90 min)

# Unsupervised Learning I: PCA, the SVD, and Factor Models in Macroeconomics

> **Two hundred macro series move together. How many things are actually happening?**

---

### 8.1 PCA as variance maximisation

Let $X$ be $n \times p$, columns centred (and standardised). Seek a unit vector $v_1$ maximising
the variance of the projection $Xv$:

$$ v_1 = \arg\max_{\|v\|=1} \; v^\top \hat\Sigma\, v, \qquad \hat\Sigma = \tfrac{1}{n}X^\top X . $$

Lagrangian: $\mathcal{L} = v^\top\hat\Sigma v - \phi(v^\top v - 1)$; first-order condition
$\hat\Sigma v = \phi v$. So $v$ must be an **eigenvector**, and since the objective at an
eigenvector equals its eigenvalue, we take the largest. Subsequent components solve the same
problem subject to orthogonality to those already found, giving the eigenvectors in decreasing
eigenvalue order.

**Via the SVD** (cleaner, and what software actually computes): $X = UDV^\top$. Then
$\hat\Sigma = \frac1n VD^2V^\top$, so the loadings are the columns of $V$, the scores are
$Z = XV = UD$, and the variance explained by component $j$ is $d_j^2/\sum_k d_k^2$.

Note the connection to Session 5: ridge shrank along the same $V$ basis, damping small-$d_j$
directions. **PCA truncates exactly the directions ridge shrinks.** Principal components
regression is, in this light, a hard-thresholded ridge.

### 8.2 Eckart-Young: best low-rank approximation

**Theorem.** Among all matrices of rank $\le k$, the one minimising $\|X - \tilde X\|_F$ is
$\tilde X_k = U_k D_k V_k^\top$, the truncated SVD, and the minimum equals
$\big(\sum_{j>k} d_j^2\big)^{1/2}$.

This is the formal sense in which "the first $k$ components capture the most information": they
give the best rank-$k$ reconstruction in Frobenius norm. It also tells you exactly what you lose -
the discarded singular values.

### 8.3 The approximate factor model

Stock and Watson's insight: a large macro panel is well described by a few common shocks plus
idiosyncratic noise.

$$ X_{it} = \lambda_i^\top F_t + e_{it}, \qquad i = 1,\dots,N,\ t = 1,\dots,T, $$

with $F_t \in \mathbb{R}^r$ the common factors and $\lambda_i$ the loadings. The **approximate**
factor model (Chamberlain-Rothschild) allows weak cross-sectional and serial correlation in $e_{it}$,
which is essential for real data.

**Key result:** the principal-component estimator $\hat F_t$ is consistent for the space spanned by
$F_t$ as **both** $N \to \infty$ and $T \to \infty$, at rate $\min(\sqrt N, \sqrt T)$. Crucially,
if $\sqrt T / N \to 0$, the estimated factors can be treated as *known* in a second-stage
regression - the generated-regressor problem vanishes. **More series genuinely helps.** This is the
opposite of the intuition you built in Sessions 5 and 6, and understanding why is the heart of this
session: there, extra predictors added variance; here, extra *measurements of the same latent
object* average noise away.

**Normalisation.** To pin down the rotation, impose $F^\top F/T = I_r$ and $\Lambda^\top\Lambda$
diagonal. This is a choice, not a discovery.

### 8.4 How many factors?

- **Scree plot:** look for the elbow. Informal, and often ambiguous.
- **Cumulative variance:** retain enough for 80-90%. Arbitrary but transparent.
- **Bai-Ng criteria:** minimise
  $$ IC_{p1}(k) = \log V(k, \hat F^k) + k\left(\frac{N+T}{NT}\right)\log\left(\frac{NT}{N+T}\right), $$
  where $V(k,\hat F^k)$ is the average residual sum of squares from a $k$-factor fit. The penalty
  must vanish slower than $\min(N,T)^{-1}$; $IC_{p2}$ and $IC_{p3}$ use alternative penalty forms.
  Report all three - if they disagree, say so.
- **Onatski's test** or the eigenvalue-ratio criterion of Ahn & Horenstein
  ($\hat r = \arg\max_k d_k/d_{k+1}$) are useful cross-checks.

### 8.5 Diffusion-index forecasting

Two stages:

1. Extract $\hat F_t$ by PCA from the standardised, stationary panel of $N$ series.
2. Forecast the target with a small regression on the factors:
   $$ \hat y_{t+h} = \hat\alpha + \sum_{j=1}^{r}\hat\beta_j \hat F_{jt} + \sum_{\ell=0}^{L}\hat\gamma_\ell y_{t-\ell} . $$

**The rule you must not break:** factors must be re-estimated at each forecast origin using only
data available at that time. Extracting factors from the full sample and then backtesting is
look-ahead bias, and it is the single most common flaw in student factor-model projects. Session 4's
rolling-origin discipline applies to *every* step, including the unsupervised one.

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

[Back to session 08](../README.md) · [On to the lab ->](../02-lab/README.md)
