# Midterm practice questions — answer key

**Quantitative Methods in International Business · Sessions 2–6**

---

> Open this only after answering the [questions](PRACTICE.md) on paper. The answers are model
> answers: on the exam, any precise formulation earns the marks, and **working is marked** — a
> correct derivation with an arithmetic slip earns most of them.

---

# Part A — Definitions and short answers

**A1.** The mean is the sum divided by $n$, the balance point; the median is the middle value once
sorted. The median is robust: an extreme value moves the mean (it enters the sum) but not the
middle position.

**A2.** The mean computed after dropping a fixed share (say 5% or 10%) of observations from each
tail. Report it when a few extreme values distort the mean but you want to use more of the data than
the median does.

**A3.** The deviations from $\bar x$ sum to zero, because $\bar x$ was estimated from the same data:
only $n - 1$ of them are free. Dividing by $n$ would systematically underestimate the variance.

**A4.** The SD measures the spread of the **observations**; the SE, $s/\sqrt n$, measures the spread
of the **mean** across repeated samples. A larger sample shrinks the SE (the mean is estimated more
precisely) but not the SD (the observations are as spread out as before).

**A5.** $IQR = Q_3 - Q_1$, the width of the middle 50% of the data. It ignores both tails, so a long
tail does not inflate it the way it inflates the SD.

**A6.** A long **right** tail: a few large values. They pull the mean above the median.

**A7.** How heavy the tails are compared with a normal distribution: $g_2 > 0$ means more extreme
values than a normal. A normal has excess kurtosis $0$.

**A8.** Not necessarily. The rule holds for a roughly **normal** variable; a symmetric distribution
can still have heavy or light tails (check $g_2$).

**A9.** The sum of squared residuals, $\sum_i (y_i - \hat y_i)^2$. Squaring makes every miss
positive, so misses above and below cannot cancel, punishes one large miss more than several small
ones, and gives a closed-form solution, $(X^\top X)^{-1}X^\top y$.

**A10.** "Comparing countries with the same investment, a one-percentage-point higher tertiary
education share is associated with a 0.31-percentage-point higher GDP growth." Units, "holding
investment fixed", and "associated with", not "causes".

**A11.** $\hat\beta_j$ equals the slope from regressing the part of $y$ not explained by the other
regressors on the part of $x_j$ not explained by them. It is a **partial** relationship: what is left
of the association after the other regressors have taken their share.

**A12.** $R^2 = 1 - SSR/SST$, the share of the variance of $y$ the model accounts for. It does not
say the relationship is causal, nor that the model's assumptions hold (a curved cloud can have a
high $R^2$), nor that it will predict new data well.

**A13.** $R^2$ never falls when a regressor is added, even a useless one. The adjusted $R^2$
penalises each extra regressor and falls when the new one improves the fit by less than chance would.

**A14.** $RSE = \sqrt{SSR/(n-k-1)}$: the typical size of a residual, in the **units of $y$** — the
typical miss of the model.

**A15.** Linearity in the parameters, exogeneity $\mathbb{E}[\varepsilon \mid X] = 0$, and no
perfect collinearity (full column rank). Constant variance (homoskedasticity) is **not** needed for
unbiasedness — only for the classical standard errors and for efficiency.

**A16.** The variance of the errors changes with the fitted values: the residual plot **fans out**.
The coefficients stay unbiased, but the classical standard errors are wrong, so tests and intervals
are wrong. Use robust (HC) standard errors.

**A17.** An **outlier** has a large residual (unusual $y$ given $x$). A **leverage point** has an
unusual $x$. An **influential point** changes the fit when removed — typically high leverage **and**
a large residual.

**A18.** How much all the fitted values move when that observation is deleted; it combines leverage
and residual. Investigate it — find which row it is and why — and report the fit with and without
it. Never delete it silently.

**A19.** $VIF_j = 1/(1 - R_j^2)$, where $R_j^2$ is from regressing $x_j$ on the other regressors.
Above about 10, $x_j$ is almost a combination of the others: its standard error is inflated and its
sign can be unstable (multicollinearity).

**A20.** BIC, because its penalty per parameter, $\ln n$, exceeds AIC's 2 as soon as $n > 7$. The
models must be fitted on **the same rows**; otherwise the likelihoods are not comparable.

**A21.** It can predict probabilities below 0 or above 1, and it forces the effect on the
probability to be the same everywhere (a straight line), which is implausible near 0 and 1. Its
errors are also heteroskedastic by construction.

**A22.** $\text{odds} = p/(1-p)$. For $p = 0.20$: $0.20/0.80 = 0.25$, "one event for every four
non-events".

**A23.** In **log-odds**: one more unit of $x$ raises the log-odds by 0.26. $e^{0.26} = 1.30$ is the
**odds ratio**: the odds are multiplied by 1.30, i.e. 30% higher. The wrong reading: "the
**probability** is 30% higher".

**A24.** The probability is an S-shaped function of $x$: its slope, $p(1-p)\beta$, depends on where
you evaluate it, largest at $p = 0.5$ and small near 0 or 1. A constant odds ratio moves the
probability by different amounts depending on the starting point.

**A25.** The parameter values that make the observed data — here, the 0s and 1s actually observed —
as probable as possible.

**A26.** Wald: $z = \hat\beta/SE$, one coefficient at a time, from one model. Likelihood ratio:
$LR = 2(\ell_{full} - \ell_{restricted}) \sim \chi^2_q$, comparing two nested models. Use the LR test
for several coefficients **jointly**, such as all the dummies of one categorical variable.

**A27.** $1 - \ell_{model}/\ell_{null}$: how far the model's log-likelihood improves on the
intercept-only model. It is not a share of variance, and its values run lower than an OLS $R^2$;
0.2–0.4 already indicates a good fit.

**A28.** The cutpoints $c_1 < c_2 < \dots$ are the thresholds between categories, one per cut; they
act as intercepts. Proportional odds: each predictor has **one** coefficient, so the same odds ratio
applies at every cut. Check it by fitting a binary logit at each cut and comparing the slopes.

**A29.** The category every other one is compared with; each equation models
$\ln[P(k)/P(\text{baseline})]$. An RRR of 0.80: a one-unit rise in $x$ multiplies the ratio
$P(\text{vocational})/P(\text{academic})$ by 0.80 — 20% fewer vocational students per academic one.
It does not say the probability of vocational falls by 20%.

**A30.** Discrimination: does the model **rank** positives above negatives (AUC)? Calibration: when
the model says 20%, does the event happen about 20% of the time? AUC depends only on the ranking, so
a model can rank perfectly while every probability is, say, twice too high — useless for pricing or
thresholds.

**A31.** With a 2% base rate, predicting "never" is 98% accurate and finds nothing. Precision
$= TP/(TP+FP)$: of those flagged, the share that are positive. Recall $= TP/(TP+FN)$: of the
positives, the share flagged.

**A32.** Test error $= \text{bias}^2 + \text{variance} + \text{noise}$. With few rows and many
correlated predictors, OLS is unbiased but its variance is enormous; a little bias that cuts the
variance a lot lowers the total.

**A33.** It makes one in-or-out decision at a time, each depending on the previous ones; resampling
the rows changes the path and the final model, and noise variables get in. The selection reflects
this sample, not a property of the world, and the $p$-values computed afterwards are invalid.

**A34.** It shrinks every coefficient toward zero, more where predictors are collinear, but never to
exactly zero. $X^\top X + \lambda I$ is invertible for any $\lambda > 0$, even when $X^\top X$ is
singular ($p > n$).

**A35.** It sets weak coefficients to **exactly zero** (the corners of its diamond-shaped budget),
so it selects variables. Limits: with $p > n$ it keeps at most $n$ variables; among correlated
predictors it keeps one, almost arbitrarily; the selected set is not "the true model".

**A36.** A ridge component: correlated predictors are kept or dropped **together** instead of one
standing in for the group — the **grouping effect**.

**A37.** The penalty compares coefficient sizes, which depend on units: unstandardised, a variable
in euros and one in thousands of euros are punished differently. Inside each fold, because
standardising on all rows lets the held-out fold's information into the training, which makes the CV
score optimistic (leakage).

**A38.** $\lambda_{min}$ minimises the CV error. $\lambda_{1se}$ is the largest $\lambda$ whose error
is within one standard error of that minimum. It gives a simpler (more shrunk) model whose error is
indistinguishable from the best.

**A39.** FE remove everything constant within a country over time (geography, history,
institutions); the cost is that the effect of any time-invariant variable cannot be estimated, and
only within-country variation identifies the slopes. RE assume the country effects are uncorrelated
with the regressors. The Hausman test compares the two; choose on whether the RE assumption holds,
never on which gives the significant answer.

**A40.** Observations of the same country are correlated over time, so the sample carries less
independent information than $n$ suggests. Cluster the standard errors by country.

---

# Part B — Calculations

**B1.** **(a)** Mean $= 35/5 = 7$; sorted $4, 6, 7, 8, 10$, median $= 7$.
**(b)** Deviations $-3, 1, -1, 3, 0$; squares $9, 1, 1, 9, 0$, sum $20$; $s^2 = 20/4 = 5$,
$s = 2.236$. **(c)** $SE = 2.236/\sqrt 5 = 1.00$.

**B2.** **(a)** $SE = 12/\sqrt{36} = 2$; interval $50 \pm 1.96 \times 2 = (46.08,\ 53.92)$.
**(b)** $n = 144$: $SE = 12/12 = 1$, halved; $s$ stays about 12 — more data does not make the
observations less spread out.

**B3.** **(a)** $g_1 = \frac{1}{36} \cdot \frac{1{,}166{,}400}{30^3} = \frac{1{,}166{,}400}{972{,}000} = 1.20$;
threshold $2\sqrt{6/36} = 0.816$ → substantially **right**-skewed, consistent with mean $>$ median.
**(b)** $g_2 = \frac{1}{36} \cdot \frac{116{,}640{,}000}{30^4} - 3 = 4.00 - 3 = 1.00$; threshold
$4\sqrt{6/36} = 1.633$ → not substantially kurtic. **(c)** The median (105): the right tail pulls
the mean up.

**B4.** **(a)** $\bar x = 3$, $\bar y = 4$; $\sum (x-\bar x)(y-\bar y) = 4 + 0 + 0 + 0 + 2 = 6$,
$\sum (x - \bar x)^2 = 10$; $\hat\beta_1 = 0.6$, $\hat\beta_0 = 4 - 0.6 \times 3 = 2.2$.
**(b)** Fitted $2.8, 3.4, 4.0, 4.6, 5.2$; residuals $-0.8, 0.6, 1.0, -0.6, -0.2$ (they sum to 0);
$SSR = 0.64 + 0.36 + 1 + 0.36 + 0.04 = 2.4$. **(c)** $SST = 4 + 0 + 1 + 0 + 1 = 6$;
$R^2 = 1 - 2.4/6 = 0.60$; $RSE = \sqrt{2.4/3} = 0.894$.

**B5.** **(a)** $t = 0.85/0.34 = 2.50$; interval $0.85 \pm 0.666 = (0.184,\ 1.516)$; significant
at 5% ($|t| > 1.96$; the interval excludes 0). **(b)** $\bar R^2 = 1 - 0.60 \times 49/45 = 0.347$.

**B6.** **(a)** Bias $= \beta_z \delta_1 = -0.3 \times 0.5 = -0.15$: negative, the short regression
**understates** $\beta_1$. **(b)** $0.45 = \beta_1 - 0.15$, so $\beta_1 = 0.60$.

**B7.** **(a)** $\sum h_{ii} = p = 3$; average $3/40 = 0.075$. **(b)** Yes: 0.21 is 2.8 times the
average, above the usual $2p/n = 0.15$ flag. High leverage alone is not influence: check its residual
and its Cook's distance. **(c)** $4/n = 0.10$.

**B8.** $VIF = 1/(1 - 0.92) = 12.5$: the coefficient's variance is 12.5 times what it would be with
uncorrelated regressors, its SE $\sqrt{12.5} \approx 3.5$ times larger. Above 10: a problem.

**B9.** **(a)** $AIC_A = 420 + 8 = 428$, $AIC_B = 410 + 14 = 424$;
$BIC_A = 420 + 4 \times 4.605 = 438.4$, $BIC_B = 410 + 7 \times 4.605 = 442.2$.
**(b)** AIC prefers B (lower), BIC prefers A. BIC charges $\ln 100 = 4.6$ per parameter instead of
2, so B's three extra parameters cost more than its gain in fit.

**B10.** **(a)** $x^\top\hat\beta = -3.0 + 0.04 \times 50 + 0.9 = -0.1$; odds $= e^{-0.1} = 0.905$;
$p = 0.905/1.905 = 0.475$. **(b)** $e^{0.9} = 2.46$: a foreign-owned firm has 2.46 times the odds
of exporting of an otherwise identical domestic firm (146% higher odds). **(c)**
$p(1-p)\beta = 0.475 \times 0.525 \times 0.04 = 0.0100$: about **1.0 percentage point** per point of
productivity, at this firm.

**B11.** **(a)** Odds $0.20/0.80 = 0.25$; new odds $0.25 \times 1.5 = 0.375$; new probability
$0.375/1.375 = 0.273$. **(b)** $+7.3$ percentage points (from 20% to 27.3%), a 36% relative rise. An
odds ratio multiplies the **odds**, not the probability.

**B12.** **(a)** $LR = 2(-412.6 + 418.9) = 12.6 > 7.81$ ($\chi^2_3$): the three dummies jointly
improve the model; reject the null that all three are zero. **(b)** $1 - 412.6/450 = 0.083$.

**B13.** **(a)** $\tau^\star = c_{FP}/(c_{FP} + c_{FN}) = 1/(1 + 9) = 0.10$. **(b)** $0.15 > 0.10$:
flag. With 0.5 the applicant would not be flagged — the default threshold ignores the costs.

**B14.** $P(Y \le 1) = F(1.0 - 1.5) = F(-0.5) = 0.378$; $P(Y \le 2) = F(3.0 - 1.5) = F(1.5) = 0.818$.
So $P(1) = 0.378$, $P(2) = 0.818 - 0.378 = 0.440$, $P(3) = 1 - 0.818 = 0.182$ (they sum to 1).

**B15.** Denominator $e^0 + e^{-0.5} + e^{0.2} = 1 + 0.607 + 1.221 = 2.828$.
$P(\text{academic}) = 1/2.828 = 0.354$, $P(\text{general}) = 0.607/2.828 = 0.215$,
$P(\text{vocation}) = 1.221/2.828 = 0.432$.

**B16.** **(a)** $TP = 30$, $FP = 70$, $FN = 20$, $TN = 880$. **(b)** Accuracy $= 910/1000 = 0.91$;
precision $= 30/100 = 0.30$; recall $= 30/50 = 0.60$. **(c)** $950/1000 = 0.95$ — higher than the
model's accuracy, although it finds no failure at all.

**B17.** **(a)** $\det = 24 - 9 = 15$; $(X^\top X)^{-1} = \frac{1}{15}\begin{pmatrix} 4 & -3 \cr -3 & 6 \end{pmatrix}$;
$\hat\beta^{OLS} = \frac{1}{15}(48 - 30,\ -36 + 60) = (1.200,\ 1.600)$.
**(b)** $X^\top X + 2I = \begin{pmatrix} 8 & 3 \cr 3 & 6 \end{pmatrix}$, $\det = 39$;
$\hat\beta^{ridge} = \frac{1}{39}(72 - 30,\ -36 + 80) = (1.077,\ 1.128)$.
**(c)** $1 - 1.077/1.2 = 10.3\%$ and $1 - 1.128/1.6 = 29.5\%$.

**B18.** **(a)** Subtract 0.25 from $|\rho_j|$, keep the sign, set to 0 if negative:
$(0.35,\ -0.10,\ 0,\ 0,\ 0.03)$ — variables 1, 2 and 5 selected. **(b)** Threshold
$\lambda\alpha = 0.125$, divisor $1 + 0.25 \times 0.5 = 1.125$:
$(0.475,\ -0.225,\ 0.025,\ 0,\ 0.155)/1.125 = (0.422,\ -0.200,\ 0.022,\ 0,\ 0.138)$ — variables 1, 2,
3 and 5. **(c)** The elastic net keeps one more (variable 3): its lower threshold lets weaker
predictors in, and its ridge part shrinks the survivors proportionally.

**B19.** $\lambda_{min} = 0.1$ (error 1.90). One-SE bound $1.90 + 0.11 = 2.01$. The largest $\lambda$
with error $\le 2.01$ is $0.5$ (1.98; at 1.0 the error 2.05 is above). $\lambda_{1se} = 0.5$: more
shrinkage, so a smaller model, with an error indistinguishable from the best.

**B20.** **(a)** Effect $= 3.0 - 2 \times 0.05\,x = 3.0 - 0.1\,x$: $+2.0$ at 10 years, $-1.0$ at 40.
**(b)** $x^\star = 3.0/0.1 = 30$ years (a maximum, since the square term is negative).
**(c)** 3.0 is the effect only at $x = 0$; with a square term the effect depends on $x$.

**B21.** **(a)** Men: 1.5 per year; women: $1.5 - 0.5 = 1.0$ per year. **(b)** Gap (women − men)
$= 4 - 0.5\,\text{exp}$: $+4$ at 0 years, $4 - 5 = -1$ at 10. **(c)** $4 - 0.5\,\text{exp} = 0$ at
8 years.

**B22.** Classical: $t = 3.75$, interval $(0.143,\ 0.457)$. Clustered: $t = 1.67$, interval
$(-0.053,\ 0.653)$. Report the clustered one: the panel's observations are not independent. The
estimate did not change; what you may claim did — no longer significant at 5%.

**B23.** $14.2 > 7.81$ ($\chi^2_3$): reject. FE and RE differ by more than sampling noise, so the RE
assumption fails — use fixed effects.

**B24.** Four dummies; the omitted level is the reference. With five plus an intercept, the dummies
sum to the intercept column: perfect collinearity (the dummy-variable trap), and the model cannot be
estimated.

---

# Part C — Diagnosis

**C1.** The empirical rule is applied to a variable that is clearly skewed: income cannot be
negative, and an SD of 71% of the mean signals a long right tail. Report the median and the IQR
instead, and check $g_1$ against its threshold.

**C2.** "Not significant" is read as "no effect". With $p = 0.31$ the data cannot distinguish the
effect from zero, but the interval almost certainly also includes large negative values. Report the
interval and say the evidence is inconclusive.

**C3.** Unbiased coefficients do not save the inference: under heteroskedasticity the classical
standard errors, $t$-statistics and intervals are wrong. Use robust (HC) standard errors.

**C4.** AIC compared on different rows: 1,200 against 900. Likelihoods on different samples are not
comparable, and the drop mostly reflects fewer observations. Refit both on the same 900 rows.

**C5.** An odds ratio read as a probability ratio (relative risk), and the conclusion is that
collateral raises default risk. 1.40 means the **odds** are 40% higher; the change in probability
depends on the baseline. (And a positive association with collateral may reflect which borrowers are
asked to provide it — not causation.)

**C6.** Accuracy on a 1% outcome: "never fraud" is 99% accurate. Report the base rate, precision and
recall. And the threshold ignores the costs: $\tau^\star = 1/(1 + 50) \approx 0.02$, not 0.5.

**C7.** Three errors. Standardising on **all** rows before cross-validation (leakage). Treating the
lasso's selection as the true model. Reporting OLS $p$-values on the selected columns: the same data
chose and then tested them, so the $p$-values are invalid. Fix: put the scaler inside a pipeline,
report the selected set and its out-of-sample error, no post-selection $p$-values.

**C8.** The specification is chosen by which gives the significant result — specification search.
Choose on the assumption: run the Hausman test (or argue whether the country effects can be
correlated with the regressor). If RE is rejected, FE is the estimate, insignificant or not.

---

# Part D — Judgement (what a strong answer contains)

**D1.** **What it is:** a cross-country association, €410 per index point, holding nothing else
fixed that we know of. **Not licensed:** "will raise": richer countries can afford digital
government (reverse causality), and institutions or education can drive both (omitted variables);
$R^2 = 0.58$ says nothing about cause. **Evidence needed:** a design that isolates the change —
within-country change over time with fixed effects, a staggered rollout compared with
non-adopters, controls for the obvious confounders. **Meanwhile:** report the association with its
interval, and do not attach a euro figure to the policy.

**D2.** **What it is:** a predictive association in this bank's data. **Not licensed:** region may
stand in for income, sector or collateral; refusing a whole region also raises fairness and legal
issues. **Evidence:** does the odds ratio survive controls for the borrower's own risk factors? Is
the model calibrated for that region? **Meanwhile:** price risk on the borrower's characteristics, use
a cost-based threshold, and review the variable's legitimacy before using it.

**D3.** **What it is:** six variables that jointly predict well at one $\lambda$, on this sample.
**Not licensed:** a dropped variable is not "no effect" — the lasso keeps one of a correlated group
almost arbitrarily, and with $p > n$ it can keep at most $n$. **Evidence:** selection stability
across resamples, an elastic net to see whether groups enter together, a causal design for any
variable whose effect matters. **Meanwhile:** report the predictive performance, not a list of
"drivers".

**D4.** Fixed effects use only **within-firm** variation: the estimate answers "when **this** firm
raises its training budget, does **its** productivity rise?" It removes everything constant about
each firm, including whatever makes some firms both train more and be more productive. The question
"are high-training firms more productive than others?" is a **between-firm** comparison that FE
deliberately throws away; answering it needs the cross-sectional variation, with its own
confounding problems.

**D5.** The mean is pulled up by a few very large firms: $g_1 = 6.4$ is far above any threshold, and
the median (18) is a fourteenth of the mean. The typical firm has about 18 employees — small, not
medium. Report the median and the IQR, say the distribution is strongly right-skewed, and model the
log of employment if it enters a regression.

---

*Questions: [`PRACTICE.md`](PRACTICE.md) · the exam: [`EXAM.md`](EXAM.md) and its
[solutions](SOLUTIONS.md) · the summary: [`MIDTERM-SUMMARY.pdf`](MIDTERM-SUMMARY.pdf)*
