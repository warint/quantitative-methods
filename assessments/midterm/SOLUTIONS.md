# Midterm: worked solutions

**Every numerical answer here was verified programmatically.**

> Use this to practise, not to read. Sit the paper first — closed book, two hours, pen and a
> non-programmable calculator — and only then open this file. Marks are shown per sub-part so you
> can see exactly where credit is earned.

---

## How the marks are awarded

Three principles, applied throughout.

1. **Precision beats length.** A correct two-sentence answer scores full marks. A page that circles
   the right idea without stating it does not.
2. **A justified refusal earns full marks.** Particularly in Part D. *"This cannot be claimed, and
   here is what would be needed"* demonstrates the thing the course is trying to build. A confident
   causal claim drawn from a lasso does not.
3. **Follow-through credit is generous in Part B.** An arithmetic slip early should not cost the
   later parts. Mark the method.

---

# Part A — Definitions *(24)*

**A1** *(3)* — Regressing $y$ on $x_j$ **and** the other regressors $X_{-j}$ gives the same
$\hat\beta_j$ as: residualise $x_j$ on $X_{-j}$, residualise $y$ on $X_{-j}$, then regress one
residual on the other. So $\hat\beta_j$ measures the relationship between $y$ and the part of $x_j$
that the other regressors **cannot explain** — a partial, not a marginal, relationship.

> *2 marks for the residual-on-residual statement, 1 for the interpretation. An answer that says
> only "it controls for the other variables", without the partialling-out mechanism, earns 1.*

**A2** *(3)* — As $K$ rises each training set is larger, so the **bias** of the CV estimate falls:
each fit is closer to the model you will actually deploy on all $n$ rows. The **variance** rises,
because the $K$ training sets overlap more and the fold estimates become highly correlated — and the
cost rises linearly in $K$. $K = 5$ or $10$ sits where the bias is already small and neither the
variance nor the cost has yet blown up.

> *1 for bias falling, 1 for variance rising, 1 for the trade-off as the reason for the convention.
> Accept computational cost as part of the third mark.*

**A3** *(3)* — Linearity in parameters, strict exogeneity $\mathbb{E}[\varepsilon\mid X]=0$, and
full column rank of $X$. **Homoskedasticity is not needed** — it is required for efficiency
(Gauss–Markov), not for unbiasedness.

> *The second sentence is the discriminating one. Listing the assumptions without saying which is
> dispensable earns 1.*

**A4** *(3)* — $h_{ii}$ is the $i$-th diagonal element of $H = X(X^\top X)^{-1}X^\top$; it measures
how much $\hat y_i$ moves when $y_i$ moves, i.e. $\partial \hat y_i / \partial y_i$. Range
$[0,1]$. $\sum_i h_{ii} = \mathrm{tr}(H) = p$, the number of parameters.

**A5** *(3)* — Optimism is the expected difference between in-sample error on new outcomes at the
same $x_i$ and the training error:
$\mathbb{E}[\mathrm{Err}_{\text{in}}] - \mathbb{E}[\mathrm{err}] = \frac{2}{n}\sum_i \mathrm{Cov}(\hat y_i, y_i)$.
It is the degree to which the model chases its own training labels.

**A6** *(3)* — $\mathrm{df}(\lambda) = \sum_{j=1}^p \dfrac{d_j^2}{d_j^2 + \lambda}$. As
$\lambda \to 0$ it tends to $p$; as $\lambda \to \infty$ it tends to 0.

**A7** *(3)* — $\sigma'(z) = \sigma(z)\big(1 - \sigma(z)\big)$. Score:
$\nabla\ell(\beta) = X^\top(y - p)$ — the residual is orthogonal to every regressor at the optimum,
exactly as in OLS with fitted probabilities in place of fitted values.

> *Full credit requires both the identity and the score. Noticing the OLS parallel earns no extra
> marks, but it is the right instinct.*

**A8** *(3)* — **Discrimination** is the ability to rank: does the model give higher scores to
positives than negatives (AUC)? **Calibration** is whether the number means what it says: among
cases with $\hat p \approx 0.3$, do about 30% turn out positive? A model whose scores are a strictly
increasing transformation of the true probabilities — say $\hat p = p^2$ — has perfect
discrimination and is badly miscalibrated.

---

# Part B — Calculations *(36)*

## B1 *(6)*

**(a)** $t = \dfrac{0.42}{0.10} = \mathbf{4.20}$. Interval:
$0.42 \pm 1.96(0.10) = 0.42 \pm 0.196 = \mathbf{[0.224,\, 0.616]}$. Since $|t| > 1.96$ and the
interval excludes zero, it **is** significant at 5%.

**(b)** $t = \dfrac{0.42}{0.25} = \mathbf{1.68}$. Interval:
$0.42 \pm 1.96(0.25) = 0.42 \pm 0.49 = \mathbf{[-0.070,\, 0.910]}$. The point estimate has **not
moved** — clustering changes the standard error, not the coefficient. But the standard error is
$2.5\times$ larger, the interval now **contains zero**, and the result is no longer significant.

**(c)** "It is significant" is not a reason to prefer one standard error over another — that is
choosing the method by the answer it gives. The **clustered** standard error is the right one here:
30 countries observed over 12 years means the 360 rows are not independent, and errors within a
country are almost certainly correlated across years. Classical standard errors assume independence
and are therefore too small. The honest report is the clustered one.

> *Marking: (a) 2 — 1 for the $t$, 1 for the interval. (b) 2 — 1 for both recomputed values, 1 for
> noting the coefficient is unchanged while the interval now covers zero. (c) 2 — 1 for naming the
> circularity, 1 for clustering with the dependence argument.*
>
> *Full marks in (c) also for noting that 30 clusters is on the low side, so a wild bootstrap or a
> small-sample correction would be prudent.*

## B2 *(6)*

**(a)** $\det(X^\top X) = 10(8) - 4(4) = 80 - 16 = 64$.

$$(X^\top X)^{-1} = \tfrac{1}{64}\begin{pmatrix} 8 & -4 \\ -4 & 10\end{pmatrix},
\qquad
\hat\beta = \tfrac{1}{64}\begin{pmatrix} 8(26) - 4(20) \\ -4(26) + 10(20)\end{pmatrix}
= \tfrac{1}{64}\begin{pmatrix}128 \\ 96\end{pmatrix}
= \begin{pmatrix} \mathbf{2.00} \\ \mathbf{1.50}\end{pmatrix}$$

**(b)** $X^\top X + 2I = \begin{pmatrix}12 & 4\\ 4 & 10\end{pmatrix}$, $\det = 120 - 16 = 104$.

$$\hat\beta^{\text{ridge}} = \tfrac{1}{104}\begin{pmatrix}10(26) - 4(20) \\ -4(26) + 12(20)\end{pmatrix}
= \tfrac{1}{104}\begin{pmatrix}180 \\ 136\end{pmatrix}
= \begin{pmatrix}\mathbf{1.7308} \\ \mathbf{1.3077}\end{pmatrix}$$

**(c)** Shrinkage **13.5%** and **12.8%** respectively. Ridge remains well-defined under singularity
because $X^\top X + \lambda I \succ 0$ for any $\lambda > 0$ — regularisation is not only a
bias–variance device, it makes the problem well-posed, including when $p > n$.

> *Marking: (a) 2 — 1 for the determinant, 1 for the coefficients. (b) 2, follow-through from a
> wrong (a). (c) 2 — 1 for the percentages, 1 for the positive-definiteness point.*

## B3 *(6)*

**(a)** $S_{0.20}(\rho)$:

| $\rho_j$ | $\|\rho_j\| - 0.20$ | $\hat\beta_j$ |
|---|---|---|
| 0.42 | 0.22 | **0.22** |
| −0.18 | −0.02 → 0 | **0** |
| 0.09 | −0.11 → 0 | **0** |
| 0.31 | 0.11 | **0.11** |

Variables **1 and 4** are selected.

**(b)** $\lambda\alpha = 0.10$; denominator $1 + 0.20(0.5) = 1.10$.

| $\rho_j$ | $S_{0.10}(\rho_j)$ | $\div 1.10$ |
|---|---|---|
| 0.42 | 0.32 | **0.2909** |
| −0.18 | −0.08 | **−0.0727** |
| 0.09 | 0 | **0** |
| 0.31 | 0.21 | **0.1909** |

**(c)** The elastic net retains **three** variables rather than two; variable 2 survives. The
relevant property is the **grouping effect** — the strictly convex $\ell_2$ component means
correlated predictors receive similar coefficients rather than the lasso's arbitrary choice of one.

> *Marking: (a) 2, all four values needed. (b) 3 — 1 for the halved threshold, 1 for the
> denominator, 1 for the values. (c) 1.*
>
> *Common error: applying $\lambda = 0.20$ rather than $\lambda\alpha = 0.10$ as the threshold.
> Deduct 1, follow through.*

## B4 *(6)*

**(a)** $g_1 = \dfrac{1}{30}\cdot\dfrac{62,208}{12.0^3}
= \dfrac{2,073.6}{1,728} = \mathbf{1.20}$.

Threshold: $2\sqrt{6/30} = 0.894$. Since $1.20 > 0.894$, the variable is
**substantially skewed**, and $g_1 > 0$ means a **long right tail**.

**(b)** $g_2 = \dfrac{1}{30}\cdot\dfrac{1,140,480}{12.0^4} - 3
= \dfrac{38,016}{20,736} - 3 = \mathbf{-1.167}$.

Threshold: $4\sqrt{6/30} = 1.789$. Since $|-1.167| < 1.789$, it is **not** substantially
kurtic.

**(c)** A long right tail pulls the **mean** away from the bulk of the data while leaving the
**median** where most observations sit — so mean $>$ median is exactly what (a) predicts. The gap
here is 4.0, about a third of a standard deviation, which is large enough to matter.

Report the **median** as the measure of centre — or report all three (mean, trimmed mean, median)
and let the disagreement be the finding. What you must not do is report the mean alone and call it
"the average", having just established the distribution is skewed.

> *Marking: (a) 2 — 1 for the value, 1 for the comparison **and** the direction. (b) 2 — 1 for the
> value, 1 for the comparison. (c) 2 — 1 for linking the gap to the right tail, 1 for a defended
> choice of summary.*
>
> *A common error is comparing $|g_2|$ against the skewness threshold. Deduct 1, follow through.*
>
> *Note the pattern: **substantially skewed, ordinary tails**. Asymmetry and heavy tails are
> different defects, and a student who says "it is skewed, therefore non-normal, therefore
> heavy-tailed" has conflated them.*

## B5 *(6)*

**(a)** $\mathbb{E}[\hat\beta_1^{\text{short}}] = \beta_1 + \delta_1\beta_2$.

**(b)** Both $\delta_1 = 0.6 > 0$ and $\beta_2 = 0.08 > 0$, so the bias is **positive (upward)**,
of magnitude $0.6 \times 0.08 = \mathbf{0.048}$.

**(c)** $\beta_1 \approx 0.112 - 0.048 = \mathbf{0.064}$.

**(d)** **Not necessarily.** Classical measurement error in the proxy attenuates its own coefficient
and leaves part of the confounding uncontrolled, so the bias on $\hat\beta_1$ is reduced but not
eliminated; with a poor proxy the improvement can be negligible. In some configurations — a proxy
correlated with the regressor but weakly with the true confounder — adding it can make matters
worse.

> *(d) 1 mark, for "not necessarily" **with** a mechanism — attenuation, or partial control.
> Either mechanism earns it; "not necessarily" alone does not.*

## B6 *(6)*

**(a)** $x^\top\hat\beta = -3.2 + 0.045(40) + 0.8(1) = -3.2 + 1.8 + 0.8 = \mathbf{-0.60}$.

$$p(x) = \frac{1}{1 + e^{0.60}} = \frac{1}{1 + 1.8221} = \mathbf{0.3543}$$

**(b)** $e^{0.8} = \mathbf{2.2255}$ — holding collateral multiplies the odds of default by about
2.23. *(A student may reasonably remark that this sign is economically odd; note it, do not
penalise. The point is the arithmetic.)*

**(c)** $0.045 \times p(1-p) = 0.045 \times 0.3543 \times 0.6457 = \mathbf{0.0103}$, i.e. about
**1.03 percentage points** per additional thousand of income.

**(d)** $\tau^\star = \dfrac{c_{FP}}{c_{FP} + c_{FN}} = \dfrac{1}{1+4} = \mathbf{0.20}$. Since
$p = 0.354 > 0.20$, **classify as default**. At the default threshold of 0.5 this applicant would
have been passed — which is the point.

> *Marking: (a) 2, (b) 1, (c) 1 — the formula and the value together. (d) 2 — 1 for $\tau^\star$,
> 1 for the decision. Award the final mark only if they state the decision, not just the threshold.*

---

# Part C — Diagnosis *(24)*

## C1 *(8)*

**(a) and (b)** — three problems, three corrections:

| Problem | Correction |
|---|---|
| **Heteroskedasticity** — residuals fan out, so classical SEs are inconsistent | HC1 robust standard errors |
| **Within-country dependence** — 27 countries × 14 years, errors almost certainly correlated within country | Cluster at the country level. Note 27 clusters is near the lower limit for reliable cluster inference; wild bootstrap advisable |
| **Near-collinearity** — VIF 18.3 on `ict_investment` inflates $\mathrm{Var}(\hat\beta_j)$ by that factor | Not automatically a "fix": the estimator is unbiased. Options are to accept wide intervals, combine the collinear regressors, or regularise — while noting that penalised coefficients do not carry valid classical SEs |

**(c)** A large standard error is not evidence of a small coefficient. With VIF 18.3, the estimate
0.164 is compatible with a wide range of economically meaningful values; the confidence interval
almost certainly includes both zero and substantial effects. *Failure to reject is not acceptance* —
the correct statement is that the data are uninformative about this coefficient.

> *Marking: (a) 3, one per problem. (b) 3, one per correction. (c) 2 — 1 for the failure-to-reject
> logic, 1 for tying it to the VIF. Saying collinearity has no "fix" and explaining why also earns
> the mark in (b); that is the better answer.*

## C2 *(8)*

**(a)** Four sources of optimism:

1. **Imputation on the full dataset** — test-fold rows influence the means used to fill training rows.
2. **Standardisation on the full dataset** — same leakage, through the mean and standard deviation.
3. **Feature selection using $y$ on the full dataset** — the most serious. The top-20 correlation
   filter has already seen every outcome, including those in every test fold.
4. **Random $K$-fold on time-series panel data** — shuffled folds train on the future to predict the
   past, and with a four-quarter horizon adjacent observations overlap.

*A fifth, awarded as a bonus if noticed:* countries are not split as groups, so the same country
appears in train and test.

**(b)** Put imputation, standardisation and feature selection **inside** a pipeline fitted
separately on each training fold. Replace shuffled $K$-fold with a **rolling-origin** split that
never trains on data later than the forecast origin, with a **purge and embargo** of at least
$h - 1 = 3$ quarters between train and test. If country-level generalisation is the target, group
by country as well.

**(c)** **Feature selection leakage.** A paper reports "we selected the 20 most predictive features
and then cross-validated"; nothing in that sentence looks wrong, and the fold-level detail is almost
never published. Meanwhile it is the largest single source of optimism, because the selection step
has consumed the outcome information the CV is supposed to hold out.

> *Marking: (a) 4, one each, cap at 4. (b) 3 — 1 pipeline, 1 rolling origin, 1 purge/embargo or
> grouping. (c) 1.*

## C3 *(8)*

**(a)** With a 2% base rate, the trivial "never fails" classifier attains **98% accuracy** — better
than the model's 97.8%. Accuracy is dominated by the majority class and carries almost no
information under imbalance.

**(b)** **Not contradictory.** AUC is threshold-free and measures *ranking*: the probability that a
randomly chosen failing firm scores above a randomly chosen surviving one. Recall is measured at one
specific threshold — 0.5 — which under a 2% base rate almost no observation exceeds. The model ranks
well and is being *used* badly.

**(c)** $\tau^\star = \dfrac{1}{1 + 20} = \mathbf{0.0476}$. Lowering the threshold from 0.5 to about
0.048 will **raise recall substantially and lower precision**; many more firms are flagged, a larger
share of them are false alarms, and expected cost falls because false alarms are cheap relative to
missed failures.

**(d)** A **calibration check** — a reliability diagram, or a Brier score decomposition. AUC is
invariant to any strictly increasing transformation of the scores, so a model can rank perfectly and
still have $\hat p$ values that are systematically wrong. Since $\tau^\star$ is a statement about
*probabilities*, applying it to uncalibrated scores does not deliver the cost-minimising decision.

> *(d) is the discriminating part of C3. 2 marks: 1 for naming calibration, 1 for the invariance
> argument. "Check performance on a holdout" earns 1.*

---

# Part D — Judgement *(16)*

## D1 *(8)*

A full-credit answer contains, in substance:

- **What the seven variables are.** Predictors retained by a penalised fit at one value of a tuning
  parameter, on one sample. Nothing more. They are not "the drivers"; they are the variables whose
  partial correlation with the residual exceeded the threshold on this draw.
- **Why the causal language is unsupported.** Selection is a predictive operation. Nothing in the
  elastic net addresses confounding, reverse causation, or the possibility that a selected variable
  proxies an unmeasured one. Reallocating a budget is a causal act and requires a causal design.
- **The diagnostic to run first: selection stability.** Refit on several hundred subsamples of size
  $n/2$ and record the proportion of fits retaining each variable. Expected output: one or two
  variables selected in 80%+ of replicates and several selected in 30–50%, particularly where
  indicators are correlated — the lasso component picks one member of a correlated group more or
  less arbitrarily.
- **What to do meanwhile.** Publish the model as a *predictive* instrument with its stability
  frequencies attached; do not name drivers; and, if the causal question is the one that matters,
  commission a design that can answer it.

> *Marking, 2 marks each. A well-argued refusal earns full marks even if the recommended action
> differs, provided stability is raised. An answer that accepts the causal framing scores at most
> 3, however fluent.*
>
> *Bonus remark for anyone noting that post-selection standard errors are invalid — that is a
> Session 5 point and shows genuine attention.*

## D2 *(8)*

**(a)** *(3)* A testable restatement is something like: *"a country's or bloc's economic and
strategic outcomes are more strongly associated with its installed AI compute than with other
measures of capability."* Any indicator is acceptable if it is **observable, attributed to a named
publisher, and on a stated schedule** — for example data-centre electricity demand from IEA or
Eurostat energy balances, or accelerator import volumes under HS 8542 from UN Comtrade. A trigger
must have a number and a date: *"if the EU:US ratio of data-centre electricity demand falls below
0.10 before end-2029, the assumption gains support."*

> *Award 1 each for indicator, named publisher and frequency, and for a trigger with both a
> threshold and a horizon. A vague "look at compute investment" earns 1.*

**(b)** *(3)* The strongest answers name a method and say what the alternative would miss:

- **Session 2–3 (regression with FWL)** — to ask whether a compute gap survives after partialling
  out economic size and sector composition. *Preferred over raw comparison because the raw ratio
  confounds capability with the size of the economy.*
- **Session 5 (elastic net with stability)** — to ask whether compute is selected ahead of energy,
  talent, data and industrial-integration measures when all compete. *Preferred over a single
  bivariate regression, which cannot adjudicate between rival measures.*
- **Session 4 (honest out-of-sample evaluation)** — to ask whether compute has *predictive* content
  for the outcome or only in-sample fit.

> *3 marks: 1 for a named method, 2 for a comparative justification. A method named without
> justification earns 1.*

**(c)** *(2)* Acceptable falsifiers include: a country in the bottom quartile of compute achieving
top-quartile productivity growth over the horizon; or compute failing to be selected ahead of energy
and talent measures in a stability analysis.

**Also full marks:** arguing that the assumption *as stated in the scenario* is not falsifiable —
because "dominant measure of geopolitical power" names no outcome variable, so no observation can
contradict it — provided the student states what would have to be specified (a named outcome, a
horizon, a comparison class) to make it testable.

> *This is the best answer available on the paper. If you found it unprompted, you are ready for the
> final paper.*

---

## Score yourself by part, not in total

The four parts diagnose four different failures, and the total hides which one is yours. Add up each
part separately and read the row that applies:

| Weak in | What it means | What to do before Session 7 |
|---|---|---|
| **A** | You are working from impressions, not definitions | Re-do the pre-session self-checks in writing |
| **A1, A2 or B1** | Session 02–04 foundations: partialling out, and what cross-validation estimates | Re-derive FWL on paper, then re-run one of your own CV scripts and say what each fold is estimating |
| **B** | You can describe methods but not derive them | Re-derive B1, B2 and B3 from scratch, without notes |
| **C** | You accept output as given | Re-run your own Session 4 leakage practice and read the diagnostics |
| **D** | You over-claim | Re-read your Session 1 memo. This is the row that matters most for the final paper |
