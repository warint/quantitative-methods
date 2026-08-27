# Midterm examination

**Quantitative Methods in International Business · Sessions 1–7**

---

|  |  |
|---|---|
| **Format** | **Paper. Handwritten, in pen.** |
| **Duration** | 2 hours |
| **Total** | 100 points |
| **Permitted** | a pen, and a **non-programmable calculator** |
| **Not permitted** | any computer, phone, tablet or smartwatch · any networked device · **no internet** · notes, textbooks, formula sheets |
| **Answer** | in the spaces provided; show your working |

> **No machine, and no assistant.** Every other assessment in this course assumes you have a
> language model beside you, because that is how the work is now done. This one deliberately does
> not. It is the only instrument that isolates what **you** can derive, unaided, on paper — which is
> the thing that lets you tell when the assistant is wrong for the rest of your career.
>
> Working is marked. A correct final answer with no derivation earns part marks; a correct
> derivation with an arithmetic slip earns most of them.

---

> ### What this paper is testing, and why
>
> The group project shows what three people and a language model can produce together. This paper is
> the only instrument in the course that isolates what **you** understand.
>
> The four parts test four different things, deliberately:
>
> **Part A — definitions.** Can you state a concept precisely? Imprecision here is not a
> presentational flaw; it is the thing itself. A person who cannot state what leverage *is* cannot
> notice when an outlier is driving a coefficient.
>
> **Part B — calculation.** Can you derive and compute? These are the formulas worth carrying in
> your head, because having them there is what lets you notice, mid-meeting, that a proposed
> analysis cannot be right.
>
> **Part C — diagnosis.** Given output, can you find the fault? This is the most common professional
> task in the whole discipline and the one least often taught. Every item in Part C contains a
> planted error.
>
> **Part D — judgement.** Knowing what a number does *not* license you to say. The hardest part,
> and the one that separates an analyst from a technician.
>
> Suggested timing: **A 20 min · B 40 min · C 35 min · D 20 min**, leaving five to check.

---

# Part A — Definitions and short answers

**24 points · 8 questions × 3 · two or three sentences each · be precise, not lengthy**

---

**A1.** *(3)* State the **Frisch–Waugh–Lovell** result, and say what it tells you a multiple-regression
coefficient $\hat\beta_j$ actually measures.

<br><br><br>

**A2.** *(3)* In $K$-fold cross-validation, state what rises and what falls as $K$ increases, and
say why $K = 5$ or $10$ became the convention.

<br><br><br>

**A3.** *(3)* State the assumptions under which $\mathbb{E}[\hat\beta \mid X] = \beta$ for the OLS
estimator. Which classical assumption is **not** needed for this result?

<br><br><br>

**A4.** *(3)* Define the leverage $h_{ii}$ of observation $i$. State its range, and state what
$\sum_i h_{ii}$ equals.

<br><br><br>

**A5.** *(3)* Define the **optimism** of the training error. Give the expression that relates it to
the covariance between fitted values and outcomes.

<br><br><br>

**A6.** *(3)* State what the first principal component **maximises**, why the inputs must be
**standardised** first, and the difference between a **loading** and a **score**.

<br><br><br>

**A7.** *(3)* State the identity satisfied by the logistic function $\sigma(z)$ that makes the score
and Hessian of the logistic log-likelihood take their simple forms. Write the score.

<br><br><br>

**A8.** *(3)* Distinguish **discrimination** from **calibration** for a probabilistic classifier.
Give one example of a model that has one without the other.

<br><br><br>

---

# Part B — Derivations and calculations

**36 points · show your working · a calculator is expected**

---

## B1. Standard errors and what they license *(6 points)*

On a panel of 30 countries observed over 12 years, a regression of productivity growth on ICT
investment gives $\hat\beta_1 = 0.42$ with a **classical** standard error of $0.10$.

> Use $1.96$ for the 95% critical value throughout.

**(a)** *(2)* Compute the $t$-statistic and the 95% confidence interval. Is the coefficient
significant at 5%?

**(b)** *(2)* Re-estimated with standard errors **clustered by country**, the standard error becomes
$0.25$. Recompute the $t$-statistic and the interval, and state what changed.

**(c)** *(2)* The analyst reports the classical result, "because it is significant". State what is
wrong with that, and say which standard error is the right one here and why.

<br><br><br><br>

## B2. Least squares and ridge *(6 points)*

For a two-regressor problem (both predictors standardised, no intercept) you are given:

$$X^\top X = \begin{pmatrix} 10 & 4 \\ 4 & 8 \end{pmatrix}, \qquad
   X^\top y = \begin{pmatrix} 26 \\ 20 \end{pmatrix}$$

**(a)** *(2)* Compute $\hat\beta^{\text{OLS}}$. Show the determinant and the inverse.

**(b)** *(2)* Compute $\hat\beta^{\text{ridge}}$ with $\lambda = 2$.

**(c)** *(2)* Report the percentage shrinkage of each coefficient. In one sentence, explain why
regularisation would still be well-defined here even if $X^\top X$ were singular.

<br><br><br><br>

## B3. Soft-thresholding, lasso and elastic net *(6 points)*

With standardised columns, the partial correlations of four predictors with the current residual are

$$\rho = (0.42,\; -0.18,\; 0.09,\; 0.31)$$

**(a)** *(2)* Compute the lasso coordinate updates with $\lambda = 0.20$ (i.e. $\alpha = 1$).
Which variables are selected?

**(b)** *(3)* Compute the elastic net updates with $\lambda = 0.20$ and $\alpha = 0.5$, using
$\hat\beta_j = S_{\lambda\alpha}(\rho_j) \,/\, \big(1 + \lambda(1-\alpha)\big)$.

**(c)** *(1)* State the difference in the selected set, and name the property of the elastic net
that explains it.

<br><br><br><br>

## B4. Describing a variable before you model it *(6 points)*

A country indicator is observed for $n = 30$ country-years. From the sample:

$$\bar x = 42.0,\qquad \text{median} = 38.0,\qquad s = 12.0$$
$$\sum_i (x_i - \bar x)^3 = 62,208,\qquad \sum_i (x_i - \bar x)^4 = 1,140,480$$

> Recall $g_1 = \dfrac{1}{n}\dfrac{\sum_i (x_i-\bar x)^3}{s^3}$ and
> $g_2 = \dfrac{1}{n}\dfrac{\sum_i (x_i-\bar x)^4}{s^4} - 3$.

**(a)** *(2)* Compute $g_1$ and test it against $2\sqrt{6/n}$. Is the variable substantially
skewed, and in which direction?

**(b)** *(2)* Compute $g_2$ and test it against $4\sqrt{6/n}$. Is it substantially kurtic?

**(c)** *(2)* The mean exceeds the median. Reconcile that with your answer to (a), and say which
measure of centre you would report — and why.

<br><br><br><br>

## B5. Omitted variable bias *(6 points)*

The true model is

$$\log w_i = \beta_0 + \beta_1 \,\text{educ}_i + \beta_2 \,\text{ability}_i + u_i,
\qquad \beta_2 = 0.08$$

and the auxiliary regression of ability on schooling gives
$\text{ability}_i = \delta_0 + \delta_1 \,\text{educ}_i + v_i$ with $\delta_1 = 0.6$.

You estimate the **short** regression, omitting ability, and obtain $\hat\beta_1^{\text{short}} = 0.112$.

**(a)** *(2)* Write the formula for $\mathbb{E}[\hat\beta_1^{\text{short}}]$.

**(b)** *(2)* Sign the bias and compute its magnitude.

**(c)** *(1)* What is the implied value of $\beta_1$?

**(d)** *(1)* You now add a noisy proxy for ability. Does the bias necessarily fall? Explain in
one sentence.

<br><br><br><br>

## B6. Logistic regression and the decision threshold *(6 points)*

A credit model gives, for (intercept, income in thousands, has_collateral):

$$\hat\beta = (-3.2,\; 0.045,\; 0.8)$$

Consider an applicant with income 40 (thousand) and collateral = 1. The outcome $y = 1$ denotes
default.

**(a)** *(2)* Compute $x^\top\hat\beta$ and the fitted probability $p(x)$.

**(b)** *(1)* Report the odds ratio associated with holding collateral.

**(c)** *(1)* Compute the marginal effect of one additional thousand of income at this $x$, and
express it in percentage points.

**(d)** *(2)* A missed default costs the lender four times what a false alarm costs. Compute the
cost-minimising threshold $\tau^\star$ and state the decision for this applicant.

<br><br><br><br>

---

# Part C — Diagnosis: read the output, find the fault

**24 points · each item contains at least one planted error**

---

## C1. A regression table *(8 points)*

A colleague estimates, on a panel of 27 countries observed 2010–2023, with **classical** standard
errors:

```
                    coef     std err        t      P>|t|
const             2.4180       0.412     5.869      0.000
gdp_pc_log        0.3120       0.041     7.610      0.000
ict_investment    0.1870       0.038     4.921      0.000
ict_capital       0.1640       0.145     1.131      0.259
educ_tertiary     0.0410       0.019     2.158      0.032
                                                      n = 378
```

They add: *"Residuals fan out markedly with fitted values. The variance inflation factor for
`ict_investment` is 18.3."*

**(a)** *(3)* Identify **three** distinct problems with the inference as reported.

**(b)** *(3)* For each, state the specific correction.

**(c)** *(2)* Your colleague concludes that `ict_capital` "has no effect". Why is this conclusion
unsupported by this table?

<br><br><br><br>

## C2. A cross-validation procedure *(8 points)*

```python
X = impute_column_means(X_all)
X = standardize(X)
selected = top_20_features_by_correlation_with(y)
scores = cross_val_score(model, X[selected], y, cv=KFold(10, shuffle=True))
print(scores.mean())
```

The data are quarterly observations of 27 countries, 2010–2023, and the model is intended to
forecast four quarters ahead.

**(a)** *(4)* Identify **four** distinct sources of optimism in this reported score.

**(b)** *(3)* Rewrite the procedure in words (no code required), stating what must move inside the
loop and what must change about the splitting.

**(c)** *(1)* Which of the four errors would a referee be least likely to detect from the paper
alone? Why does that make it the most dangerous?

<br><br><br><br>

## C3. A classifier report *(8 points)*

A firm-failure model is reported as follows. The base rate of failure is 2%.

```
accuracy   0.978        AUC        0.94
precision  0.31         recall     0.08     (at threshold 0.50)
```

The client states that a missed failure costs twenty times what a false alarm costs.

**(a)** *(2)* Why is the accuracy figure uninformative here? What accuracy does the trivial
"never fails" classifier achieve?

**(b)** *(2)* Reconcile an AUC of 0.94 with a recall of 0.08. Are they contradictory?

**(c)** *(2)* Compute the cost-minimising threshold and state the qualitative effect on precision
and recall of moving to it.

**(d)** *(2)* Before deploying, what single diagnostic would you require, and why does AUC not
substitute for it?

<br><br><br><br>

---

# Part D — Interpretation and judgement

**16 points · prose answers · a well-argued refusal earns full marks**

---

## D1. What a selected variable list licenses *(8 points)*

A European agency has run an elastic net on 180 candidate indicators and obtained a model with
seven non-zero coefficients at $\lambda_{1se}$. A senior official proposes a press release naming
those seven as "the drivers of regional divergence" and reallocating a programme budget accordingly.

Write the paragraph you would send in reply. It must state: what the seven variables *are*, what
evidence would be needed before the causal language could be used, what diagnostic you would run
first and what its output would look like, and what you would recommend the agency do in the
meantime.

<br><br><br><br><br><br>

## D2. From a narrative claim to a testable one *(8 points)*

The *Europe 2031* scenario assigns the United States roughly 12 times Europe's AI compute stock in
2031, and treats compute as the dominant measure of geopolitical capability.

**(a)** *(3)* State the assumption in a form that could be tested. Name one observable indicator,
its publishing institution, and a trigger point with a horizon.

**(b)** *(3)* Which method from Sessions 1–7 would you use, and why that one rather than the
obvious alternative?

**(c)** *(2)* State one observation that would count as evidence **against** the assumption. If you
believe the assumption is not falsifiable as stated, say so and explain what would have to change.

<br><br><br><br><br><br>

---

**End of examination.**

*Worked solutions, with the marks shown per sub-part: [`SOLUTIONS.md`](SOLUTIONS.md)*

> Sit the paper first, closed book and timed. The solutions are only worth reading against an
> attempt you have already made.
