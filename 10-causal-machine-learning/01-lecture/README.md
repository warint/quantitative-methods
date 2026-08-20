# Session 10 — Lecture (first half, ~90 min)

# Causal Machine Learning: Double/Debiased ML and Heterogeneous Effects

> **You have a superb predictive model. Why can you still not use it to choose a policy?**

---

### 10.1 The setup

Partially linear model:

$$Y = \theta_0 D + g_0(X) + U, \qquad \mathbb{E}[U \mid X, D] = 0,$$
$$D = m_0(X) + V, \qquad \mathbb{E}[V \mid X] = 0 .$$

$\theta_0$ is the parameter of interest; $g_0$ and $m_0$ are **nuisance functions** we do not care
about but must handle. In classical econometrics we would assume $g_0$ linear. The premise of DML
is that we would rather estimate $g_0$ and $m_0$ flexibly with the tools of Sessions 5-7 - because
functional-form error in $g_0$ contaminates $\theta_0$.

**Identification** requires: (i) *conditional ignorability*, $\{Y(1), Y(0)\} \perp D \mid X$;
(ii) *overlap*, $0 < P(D=1\mid X) < 1$ almost surely; (iii) *SUTVA*. No amount of machine learning
substitutes for these. They are assumptions about the world, defended with institutional knowledge,
not with cross-validation.

### 10.2 Why the naive plug-in fails

Suppose you estimate $\hat g_0$ by, say, a lasso or a random forest on the full sample, then
regress $Y - \hat g_0(X)$ on $D$. Decomposing the estimation error of the resulting $\hat\theta$
yields, schematically,

$$\sqrt n(\hat\theta - \theta_0) = \underbrace{a}_{\to N(0,\Sigma)}
+ \underbrace{b}_{\text{regularisation bias}} + \underbrace{c}_{\text{overfitting bias}} .$$

- Term $b$ scales like $\sqrt n \times \|\hat g_0 - g_0\|$. ML estimators converge at rates *slower*
  than $n^{-1/2}$ (that is the price of flexibility), so $b$ **diverges**. The estimator is not even
  consistent at the parametric rate, and confidence intervals are meaningless.
- Term $c$ arises because $\hat g_0$ was fitted using the same observations at which it is evaluated,
  inducing correlation between the estimated nuisance and the residual.

Two distinct problems requiring two distinct fixes.

### 10.3 Fix 1 - Neyman orthogonality

Instead of the naive score, use the **partialling-out** (FWL) score:

$$\psi(W; \theta, \eta) = \big(Y - \ell_0(X) - \theta\,(D - m_0(X))\big)\big(D - m_0(X)\big),$$

with nuisances $\eta = (\ell_0, m_0)$, $\ell_0(X) = \mathbb{E}[Y\mid X]$, $m_0(X)=\mathbb{E}[D\mid X]$.
Solving $\mathbb{E}[\psi]=0$ gives

$$\theta_0 = \frac{\mathbb{E}\big[(Y-\ell_0(X))(D-m_0(X))\big]}{\mathbb{E}\big[(D-m_0(X))^2\big]}
= \frac{\operatorname{Cov}(\tilde Y, \tilde D)}{\operatorname{Var}(\tilde D)} ,$$

which is precisely FWL: regress residualised $Y$ on residualised $D$.

**The orthogonality property.** The Gateaux (directional) derivative of $\mathbb{E}[\psi]$ with
respect to $\eta$, evaluated at the truth, is zero:

$$\partial_\eta \, \mathbb{E}\big[\psi(W;\theta_0,\eta_0)\big][\eta - \eta_0] = 0 .$$

Consequently, small errors in $\hat\eta$ have only a **second-order** effect on $\hat\theta$. The
bias term becomes of order $\sqrt n \times \|\hat\ell - \ell_0\| \times \|\hat m - m_0\|$, so it
vanishes provided each nuisance converges faster than $n^{-1/4}$ - a rate that lasso, random
forests and boosting can achieve under reasonable conditions. **Note the structure: two slow rates
multiply into one fast enough rate.** That is the whole trick, and it is why the method is called
*double*.

### 10.4 Fix 2 - cross-fitting

Split the sample into $K$ folds. For each $k$:

1. Estimate $\hat\ell^{(-k)}$ and $\hat m^{(-k)}$ on all folds **except** $k$.
2. Form residuals on fold $k$: $\tilde Y_i = Y_i - \hat\ell^{(-k)}(X_i)$, $\tilde D_i = D_i - \hat m^{(-k)}(X_i)$.

Then pool:

$$\hat\theta = \frac{\sum_{i} \tilde Y_i \tilde D_i}{\sum_{i} \tilde D_i^2}, \qquad
\hat\sigma^2 = \frac{\frac1n \sum_i \tilde D_i^2 (\tilde Y_i - \hat\theta \tilde D_i)^2}
{\big(\frac1n\sum_i \tilde D_i^2\big)^2} .$$

Because the nuisance was never fitted on the observation where it is evaluated, term $c$ vanishes.
Repeat the whole procedure over several random splits and take the median of $\hat\theta$ to remove
split sensitivity.

**Result.** $\sqrt n(\hat\theta - \theta_0) \to N(0, \sigma^2)$, so ordinary confidence intervals
are valid - despite having used black-box learners for the nuisances. This is the reconciliation of
Sessions 5-7 with Session 3.

### 10.5 Heterogeneous treatment effects

Often the interesting question is not the average but *for whom*: $\tau(x) = \mathbb{E}[Y(1)-Y(0)\mid X=x]$.

**Causal forests** (Wager & Athey) adapt random forests in three ways: splits are chosen to
maximise heterogeneity in the treatment effect rather than in the outcome; **honesty** requires
that the observations used to choose splits be disjoint from those used to estimate the leaf
effects; and the resulting estimator is shown to be asymptotically normal and pointwise consistent,
so confidence intervals are available.

**Discipline in reporting heterogeneity.** Searching over subgroups for large effects is
multiple testing, and it will find something. Pre-specify subgroups where possible; otherwise use
the **best linear projection** of $\hat\tau(X)$ on a small set of covariates, or a calibration test
(the GATES / CLAN procedures of Chernozhukov et al.), and report them as exploratory.

### 10.6 What this does not fix

DML delivers valid inference **conditional on the identifying assumptions**. If treatment is
confounded by something not in $X$, DML estimates a precisely-quantified wrong number, and its
narrow confidence interval will make the wrong number look authoritative. Flexible nuisance
estimation removes functional-form error; it does not remove omitted-variable bias. Return here to
Session 3's OVB formula: it still governs everything.

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

[Back to session 10](../README.md) · [On to the practice ->](../02-practice/README.md)
