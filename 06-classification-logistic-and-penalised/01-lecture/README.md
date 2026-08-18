# Session 06 — Lecture (first half, ~90 min)

# Classification: Logistic Regression, Regularisation, and Decision Thresholds

> **Your classifier is 97% accurate. Should anyone be impressed?**

---

> **Structure of this lecture.** Part A (~50 min) builds the logistic model and its estimation.
> Part B (~40 min) adds the Session 5 penalty and confronts what happens when $p$ is large and the
> classes are unbalanced. Part B is short precisely because Part A and Session 5 have done the work.

---

# Part A — Logistic regression

### 6.1 Two routes to the same model

**Route A - the link function.** Model the log-odds as linear:

$$ \log\frac{p(x)}{1-p(x)} = x^\top\beta \quad\Longleftrightarrow\quad
p(x) = \frac{1}{1 + e^{-x^\top\beta}} = \sigma(x^\top\beta). $$

The logistic function satisfies $\sigma'(z) = \sigma(z)(1-\sigma(z))$ - an identity we use
repeatedly.

**Route B - a latent variable.** Suppose an unobserved index $y_i^* = x_i^\top\beta - u_i$ with
$y_i = \mathbb{1}\{y_i^* > 0\}$. If $u_i$ is standard logistic, then
$P(y_i = 1\mid x_i) = \sigma(x_i^\top\beta)$ exactly; if $u_i$ is standard normal, you get probit.

Route B is the economist's route: $y^*$ is a latent utility difference, and the model is a random
utility model. The logit/probit choice is a choice about the distribution of unobserved
heterogeneity, and in practice the two give nearly identical fitted probabilities.

### 6.2 The likelihood, the score, and concavity

$$ \ell(\beta) = \sum_{i=1}^n \Big[ y_i x_i^\top\beta - \log\big(1 + e^{x_i^\top\beta}\big) \Big]. $$

**Score.** Using $\sigma' = \sigma(1-\sigma)$:

$$ \nabla \ell(\beta) = \sum_i \big(y_i - p(x_i)\big)x_i = X^\top (y - p). $$

Beautifully simple: *at the optimum, the residual $y - p$ is orthogonal to every regressor* -
exactly the OLS condition from Session 2, with fitted probabilities in place of fitted values.

**Hessian.**

$$ \nabla^2\ell(\beta) = -\sum_i p_i(1-p_i)\,x_i x_i^\top = -X^\top W X, \qquad
W = \operatorname{diag}\big(p_i(1-p_i)\big). $$

Since $W \succeq 0$, we have $-X^\top W X \preceq 0$: **the log-likelihood is concave.** Any
stationary point is a global maximum. There are no local optima.

### 6.3 Newton-Raphson = iteratively reweighted least squares

The Newton step $\beta^{(t+1)} = \beta^{(t)} + (X^\top W X)^{-1}X^\top(y-p)$ rearranges to

$$ \beta^{(t+1)} = (X^\top W X)^{-1} X^\top W z, \qquad
z = X\beta^{(t)} + W^{-1}(y - p) . $$

This is exactly **weighted least squares** of the *adjusted response* $z$ on $X$ with weights $W$.
Hence IRLS. Two consequences: you reuse all the linear algebra of Session 2, and the asymptotic
covariance is $\widehat{\operatorname{Var}}(\hat\beta) = (X^\top W X)^{-1}$, the inverse observed
information.

**Perfect separation.** If a hyperplane separates the classes exactly, the likelihood increases
without bound as $\|\beta\| \to \infty$: **the MLE does not exist.** Symptoms are enormous
coefficients with enormous standard errors. This is more common with small samples and many dummies
than students expect. Hold that thought - Part B disposes of it in one line.

### 6.4 Interpretation: three quantities, three uses

| Quantity | Formula | Use it when |
|---|---|---|
| Log-odds change | $\beta_j$ | Reporting the raw model |
| Odds ratio | $e^{\beta_j}$ | Communicating to a clinical or credit audience |
| Marginal effect at $x$ | $\beta_j\, p(x)(1-p(x))$ | You need a probability change |
| **Average marginal effect** | $\frac1n\sum_i \beta_j\, p_i(1-p_i)$ | **Reporting to economists** |

The same $\beta_j$ implies a large probability change near $p=0.5$ and almost none near $p=0.01$.
**Report average marginal effects** unless you have a reason not to; a bare odds ratio invites
misreading.

*Aside on more than two classes.* The multinomial (softmax) extension is
$P(y=k\mid x) = e^{x^\top\beta_k}/\sum_\ell e^{x^\top\beta_\ell}$, with parameters identified only
up to adding a constant vector to every $\beta_k$ - hence the convention $\beta_K = 0$. The
likelihood is again concave and the same algorithm applies block by block. Note that multinomial
logit imposes **independence of irrelevant alternatives**, which matters greatly for discrete-choice
work and much less for pure classification.

### 6.5 Evaluation - and why accuracy is usually the wrong metric

A model produces $\hat p_i$; a **decision** requires a threshold $\tau$. These are separate acts,
and conflating them is the most common applied error.

|  | Predicted 1 | Predicted 0 |
|---|---|---|
| **Actual 1** | TP | FN |
| **Actual 0** | FP | TN |

$$ \text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall (TPR)} = \frac{TP}{TP+FN}, \quad
\text{FPR} = \frac{FP}{FP+TN}. $$

**ROC** plots TPR against FPR as $\tau$ sweeps $[0,1]$; **AUC** equals
$P(\hat p_{\text{positive}} > \hat p_{\text{negative}})$ for a random pair. AUC is threshold-free
and invariant to class balance - a virtue for comparing models, a *vice* for judging usefulness
under heavy imbalance. With 2% positives, prefer the **precision-recall curve** and average
precision.

**Choosing $\tau$ from costs.** If a false negative costs $c_{FN}$ and a false positive $c_{FP}$,
the expected-cost-minimising threshold is

$$ \boxed{\;\tau^\star = \frac{c_{FP}}{c_{FP} + c_{FN}}\;} $$

For German Credit's stated 5:1 ratio, $\tau^\star = 1/6 \approx 0.167$, not 0.5. **The default
threshold in every software package is a modelling assumption about costs that almost nobody states
out loud.**

**Calibration.** A model is calibrated if, among cases where $\hat p \approx 0.3$, about 30% are
positive. Discrimination (AUC) and calibration are *different properties*: a model can rank
perfectly and still be badly miscalibrated. Plot a reliability diagram whenever the probability
itself enters a decision.

---

# Part B — Adding the penalty

### 6.6 The composition

Combine Session 5's penalty with the likelihood above:

$$ \hat\beta = \arg\min_\beta \left\{ -\frac{1}{n}\sum_{i}\Big[ y_i x_i^\top\beta - \log(1+e^{x_i^\top\beta})\Big]
+ \lambda\Big[\alpha\|\beta\|_1 + \tfrac{1-\alpha}{2}\|\beta\|_2^2\Big] \right\}. $$

The negative log-likelihood is convex (6.2) and both penalties are convex, so the objective is
convex; for $\alpha < 1$ it is strictly convex and the minimiser is unique.

**The penalty cures separation.** The likelihood's drive toward $\|\beta\|\to\infty$ is dominated by
the penalty's growth, so a finite minimiser always exists. Regularisation is here a *regularity*
device, not merely a variance-reduction device. (Firth's bias-reduced logistic regression is an
alternative; dropping the offending variable, once you recognise it as a proxy for the outcome, is
usually the honest answer.)

### 6.7 The algorithm: two nested loops

**Outer loop.** At the current $\tilde\beta$, take the second-order Taylor expansion of the
log-likelihood. By 6.3 this *is* a weighted least-squares problem, with $w_i = \tilde p_i(1-\tilde p_i)$
and $z_i = x_i^\top\tilde\beta + (y_i - \tilde p_i)/w_i$.

**Inner loop.** Solve the penalised weighted least-squares problem by coordinate descent. The update
is the Session 5 formula with weights inserted:

$$ \beta_j \leftarrow \frac{S_{\lambda\alpha}\big(\frac1n\sum_i w_i x_{ij}(z_i - \tilde y_i^{(-j)})\big)}
{\frac1n\sum_i w_i x_{ij}^2 + \lambda(1-\alpha)} , $$

with $S_\lambda(\rho) = \operatorname{sign}(\rho)(|\rho|-\lambda)_+$ the soft-thresholding operator
you derived in Session 5. Iterate, recompute weights, repeat.

**Three practical points.** (i) Warm starts down a decreasing $\lambda$ grid make the whole path
cost little more than one fit. (ii) An *active set* strategy cycles only over currently non-zero
coefficients, checking the full set occasionally via the KKT conditions. (iii) **Clamp $w_i$ away
from zero** (e.g. at $10^{-5}$) or $z_i$ explodes for well-classified points - this is the bug you
will hit in the lab.

### 6.8 Class imbalance: three distinct interventions

Suppose positives are 2% of the sample. Three things are routinely confused.

| Intervention | What it changes | Effect on calibration |
|---|---|---|
| **Resampling** (SMOTE, over/under-sampling) | the empirical distribution | **Destroys** it - $\hat p$ now estimates the resampled prior |
| **Class weights** in the loss | the objective | Distorts it similarly; equivalent to a prior shift |
| **Threshold adjustment** | only the decision rule | **Preserves** it completely |

**The recommendation is unambiguous for most economic applications: fit an unweighted,
well-regularised model, verify calibration, then move the threshold using $\tau^\star$ from 6.5.**
You keep an interpretable probability *and* an optimal decision.

If you must resample, undo the prior shift analytically. With training positive rate $\pi'$ and
population rate $\pi$, correct the intercept by

$$ \beta_0 \leftarrow \beta_0 - \log\!\left(\frac{\pi'}{1-\pi'}\cdot\frac{1-\pi}{\pi}\right). $$

Very few practitioners do this. Be one who does.

*On SMOTE:* it interpolates between minority neighbours, so synthetic points lie in the convex hull
of observed minority cases. In high dimensions with correlated financial ratios, those interpolants
can be economically impossible firms. Treat with scepticism.

### 6.9 Selection stability - and how to report it

When $p \gg n$ with correlated predictors, the selected variable set is a high-variance object
(you saw this for the lasso in Session 5; it is worse for the logistic case).

- **Stability selection** (Meinshausen & Bühlmann): draw many subsamples of size $n/2$, fit on each,
  retain variables selected in at least $\pi_{\text{thr}}$ (e.g. 0.6) of them. Comes with a bound on
  the expected number of false selections.
- **Bootstrap selection frequencies:** simpler, and enough for a report.

**How to write it up.** Never: *"the model identified X, Y and Z as the drivers of bankruptcy."*
Instead: *"at $\lambda_{1se}$ the model retained X, Y and Z; across 500 subsamples these were
selected in 82%, 44% and 39% of fits respectively, indicating that only X is robustly selected."*
The second sentence is the one a referee will respect.

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

[Back to session 06](../README.md) · [On to the lab ->](../02-lab/README.md)
