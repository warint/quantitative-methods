# Session 03 — Lecture (first half, ~90 min)

# Linear Regression: Inference, Diagnostics, and Interpretation

> **Your coefficient has a standard error. Under what conditions does that number mean anything?**

---

### 3.1 Sampling distribution of the OLS estimator

Substituting $y = X\beta + \varepsilon$ into $\hat\beta = (X^\top X)^{-1}X^\top y$:

$$\hat\beta = \beta + (X^\top X)^{-1} X^\top \varepsilon .$$

This decomposition is the whole of regression inference. Everything follows from what you are
willing to assume about $\varepsilon$.

**Unbiasedness.** $\mathbb{E}[\hat\beta \mid X] = \beta + (X^\top X)^{-1}X^\top \mathbb{E}[\varepsilon \mid X] = \beta$, using only strict exogeneity.

**Variance.** Under homoskedasticity,

$$\mathrm{Var}(\hat\beta \mid X) = (X^\top X)^{-1} X^\top \mathrm{Var}(\varepsilon\mid X) X (X^\top X)^{-1} = \sigma^2 (X^\top X)^{-1} .$$

For a single coefficient this expands into a form worth memorising:

$$\mathrm{Var}(\hat\beta_j) = \frac{\sigma^2}{n \cdot \mathrm{Var}(x_j) \cdot (1 - R_j^2)},$$

where $R_j^2$ is the $R^2$ from regressing $x_j$ on all other regressors. Read off the four levers:
noise, sample size, variation in the regressor, and **redundancy**. The factor $1/(1-R_j^2)$ is the
*variance inflation factor*. It is the price of collinearity - and it is precisely what
regularisation (Session 5) proposes to pay differently.

### 3.2 Gauss-Markov

**Theorem.** Under assumptions 1-4, $\hat\beta_{OLS}$ has the smallest variance in the class of
linear unbiased estimators.

*Proof sketch.* Let $\tilde\beta = Cy$ be any linear unbiased estimator; write $C = (X^\top X)^{-1}X^\top + D$.
Unbiasedness forces $DX = 0$. Then
$\mathrm{Var}(\tilde\beta) = \sigma^2\big[(X^\top X)^{-1} + DD^\top\big] \succeq \mathrm{Var}(\hat\beta)$,
since $DD^\top \succeq 0$. $\blacksquare$

**The crucial caveat.** BLUE is a guarantee *within the class of unbiased estimators*. Sessions 4
and 5 show that deliberately accepting bias can lower total error. Gauss-Markov does not forbid
this; it simply does not apply.

### 3.3 When assumption 4 fails

The **sandwich** form is always correct:

$$\mathrm{Var}(\hat\beta \mid X) = (X^\top X)^{-1} \Big( X^\top \Omega X \Big) (X^\top X)^{-1}, \qquad \Omega = \mathrm{Var}(\varepsilon \mid X).$$

- **Heteroskedasticity-robust (White / HC1):** estimate $\Omega$ by $\mathrm{diag}(\hat\varepsilon_i^2)$, with a small-sample correction $n/(n-p)$.
- **Cluster-robust:** if errors are correlated within groups $g$ (firms, regions, countries), use $\hat\Omega = \sum_g \hat\varepsilon_g \hat\varepsilon_g^\top$. Requires *many* clusters; with fewer than roughly 40, inference is unreliable.
- **Practical rule:** cluster at the level at which treatment is assigned.

### 3.4 Omitted variable bias

Suppose the true model is $y = X_1\beta_1 + X_2\beta_2 + u$ but you estimate $y$ on $X_1$ alone.
Let $\delta$ be the coefficient matrix from regressing $X_2$ on $X_1$. Then

$$\mathbb{E}[\hat\beta_1] = \beta_1 + \delta \beta_2 .$$

**Sign the bias with two questions:** (i) how does the omitted variable relate to my regressor
($\delta$)? (ii) how does it relate to the outcome ($\beta_2$)? Same sign in both: upward bias.

### 3.5 What a Mincer coefficient identifies

$$\log w_i = \alpha + \rho\, S_i + \gamma_1 X_i + \gamma_2 X_i^2 + \varepsilon_i$$

$\rho$ is often read as "the return to a year of schooling". Strictly, it is the mean log-wage
difference associated with an additional year of schooling **among people who are otherwise
identical on the included covariates**. Unobserved ability, selection into schooling, and
measurement error all break the causal reading. Session 11 gives us tools that take this seriously.
Today, the discipline is simply to say precisely what we have estimated.

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

[Back to session 03](../README.md) · [On to the practice ->](../02-practice/README.md)
