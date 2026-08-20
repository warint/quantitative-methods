# Session 04 — Lecture (first half, ~90 min)

# The Bias-Variance Tradeoff, Overfitting, and Cross-Validation

> **Your model fits the past perfectly. Why is that bad news?**

---

### 4.1 The decomposition

Fix a test point $x_0$. Let $\hat f$ be estimated on a random training sample. The expected
squared error at $x_0$, averaging over training samples and over the new noise draw, is

$$\mathbb{E}\big[(y_0 - \hat f(x_0))^2\big]
= \underbrace{\operatorname{Var}\big(\hat f(x_0)\big)}_{\text{variance}}
+ \underbrace{\big(\mathbb{E}[\hat f(x_0)] - f(x_0)\big)^2}_{\text{bias}^2}
+ \underbrace{\sigma^2}_{\text{irreducible}} .$$

*Derivation.* Write $y_0 = f(x_0) + \varepsilon_0$ and add and subtract $\mathbb{E}[\hat f(x_0)]$
inside the square. Three cross terms vanish: one because $\mathbb{E}[\varepsilon_0]=0$ and
$\varepsilon_0$ is independent of the training sample; two because
$\mathbb{E}\big[\hat f(x_0) - \mathbb{E}[\hat f(x_0)]\big] = 0$. $\blacksquare$

**The economics of this equation.** Bias is what you get for imposing structure you believe in.
Variance is what you pay for letting the data speak. Flexibility trades one for the other, and
there is generally an interior optimum. The rest of this course is a catalogue of ways to sit at
that optimum deliberately rather than by accident.

### 4.2 In-sample error is optimistic - by how much?

Let $\operatorname{err} = \frac1n\sum_i (y_i - \hat f(x_i))^2$ be training error and
$\operatorname{Err}_{\text{in}}$ the error on new outcomes at the *same* $x_i$. Then

$$\mathbb{E}[\operatorname{Err}_{\text{in}}] - \mathbb{E}[\operatorname{err}]
= \frac{2}{n}\sum_{i=1}^n \operatorname{Cov}(\hat y_i, y_i) .$$

The **optimism** is exactly twice the average covariance between fitted value and its own outcome:
the degree to which the model chases its own training labels. For a linear fit with $p$ parameters
this covariance sum equals $p\sigma^2$, giving optimism $2p\sigma^2/n$ and motivating

$$C_p = \operatorname{err} + \frac{2p\hat\sigma^2}{n}, \qquad
\mathrm{AIC} = -\frac{2}{n}\log\mathcal{L} + \frac{2p}{n}, \qquad
\mathrm{BIC} = -2\log\mathcal{L} + p\log n .$$

Note that BIC penalises more heavily for $n > e^2 \approx 7.4$; it is consistent for model
selection, whereas AIC is efficient for prediction. They answer different questions.

The quantity $\mathrm{df}(\hat f) = \frac{1}{\sigma^2}\sum_i \operatorname{Cov}(\hat y_i, y_i)$ is
the **effective degrees of freedom**, and it generalises "number of parameters" to methods where
counting parameters makes no sense - which we need from Session 5 onward.

### 4.3 Cross-validation

Partition the data into $K$ folds. For each $k$, fit on the complement and predict the held-out
fold:

$$\mathrm{CV}_K = \frac{1}{n}\sum_{k=1}^{K}\sum_{i \in \mathcal{F}_k} L\big(y_i, \hat f^{-k}(x_i)\big).$$

- $K = n$ (LOOCV): nearly unbiased for $\operatorname{Err}$, but high variance (the $n$ training
  sets are almost identical, so the errors are highly correlated) and usually expensive - except
  for linear smoothers, where the shortcut
  $\mathrm{CV}_{(n)} = \frac1n\sum_i \left(\frac{y_i - \hat y_i}{1 - h_{ii}}\right)^2$
  makes it free once you have the hat matrix.
- $K = 5$ or $10$: the standard compromise. Some upward bias (each model is trained on less data),
  much lower variance.

### 4.4 Three ways to get cross-validation wrong

1. **Leakage through preprocessing.** Any step that uses the outcome or the *full* feature
   distribution - standardisation, imputation, feature selection, target encoding - must be fitted
   **inside** each training fold. Use a `Pipeline`. This is the single most common serious error in
   applied ML papers.
2. **Leakage through selection.** Choosing a model by CV and then reporting that same CV error as
   the model's performance is optimistic. You need a **nested** design: an outer loop for
   evaluation, an inner loop for tuning.
3. **Ignoring dependence.** Random folds assume exchangeability. Economic data are rarely
   exchangeable:
   - *Time series:* use rolling-origin / expanding-window CV. Never train on the future.
   - *Panel or clustered data:* use `GroupKFold` so all observations of a firm or region stay together.
   - *Spatial data:* use blocked CV, because neighbouring units are correlated.

**Rule of thumb:** the CV split must mimic the way the model will actually be deployed.

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

[Back to session 04](../README.md) · [On to the practice ->](../02-practice/README.md)
