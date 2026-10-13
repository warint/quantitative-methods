# Midterm practice questions

**Quantitative Methods in International Business · Sessions 2–6**

---

These questions train for the [midterm](EXAM.md) under its conditions: **on paper, in pen, with a
non-programmable calculator, and nothing else**. They follow its four parts, so you practise each
kind of thinking it marks:

| Part | What it asks | Here |
|---|---|---|
| **A — definitions** | state a concept precisely, in two or three sentences | 40 questions |
| **B — calculations** | derive and compute, showing the working | 24 exercises |
| **C — diagnosis** | find the planted error in an output or a procedure | 8 items |
| **D — judgement** | say what a number does *not* license | 5 prompts |

**To print:** [questions](https://warint.github.io/quantitative-methods/midterm-practice.pdf) · [answer key](https://warint.github.io/quantitative-methods/midterm-practice-answers.pdf) (PDF).

Each question carries its session and its difficulty in brackets, so you can train one session at a
time, and build up from easy to difficult:

- **easy** (25 questions) — recall a definition, or apply one formula directly;
- **medium** (39) — combine two ideas, or carry a calculation through several steps;
- **difficult** (13) — a subtle distinction, a longer derivation, or several faults to find at once.

> **How to use it.** Answer first, on paper, without notes. Only then open the
> [answer key](PRACTICE-ANSWERS.md). An answer you recognise is not an answer you can produce; the
> exam asks you to produce it. The [midterm summary](MIDTERM-SUMMARY.pdf) holds every formula you
> are expected to carry in your head.

---

# Part A — Definitions and short answers

*Two or three sentences each. Be precise, not lengthy.*

### Session 2 · Describing a variable

**A1.** *(S2 · easy)* Define the mean and the median. Which is robust to an extreme value, and why?

**A2.** *(S2 · easy)* What is a trimmed mean, and when would you report it?

**A3.** *(S2 · medium)* Why does the sample variance divide by $n - 1$ rather than $n$?

**A4.** *(S2 · medium)* Distinguish the **standard deviation** from the **standard error of the mean**. Which
one shrinks when the sample grows, and why?

**A5.** *(S2 · easy)* Define the interquartile range. Why is it preferred to the standard deviation for a
skewed variable?

**A6.** *(S2 · easy)* What does a positive skewness $g_1$ tell you about the shape of a distribution, and
about the order of its mean and median?

**A7.** *(S2 · easy)* What does **excess** kurtosis measure, and what value does a normal distribution have?

**A8.** *(S2 · medium)* A variable is symmetric. Can you apply the 68–95–99.7 rule to it? Explain.

### Session 3 · Can the regression be trusted?

**A9.** *(S3 · easy)* What does ordinary least squares minimise? Why squares, rather than the absolute
distances?

**A10.** *(S3 · medium)* Interpret a slope $\hat\beta_1 = 0.31$ in a regression of GDP growth (in %) on
tertiary education (in % of the population) with a control for investment. Write the full sentence.

**A11.** *(S3 · difficult)* What does "holding the other regressors fixed" mean, according to the
Frisch–Waugh–Lovell result?

**A12.** *(S3 · easy)* Define $R^2$. Give two things a high $R^2$ does **not** tell you.

**A13.** *(S3 · medium)* Why does the adjusted $R^2$ exist, and when can it fall as you add a regressor?

**A14.** *(S3 · easy)* What is the residual standard error (RSE), and in what units is it expressed?

**A15.** *(S3 · difficult)* State the assumptions needed for OLS to be unbiased. Which classical assumption is
**not** among them?

**A16.** *(S3 · medium)* What is heteroskedasticity, how do you see it in a residual plot, and what does it do
to the coefficients and to their standard errors?

**A17.** *(S3 · medium)* Distinguish an **outlier**, a **leverage point** and an **influential point**.

**A18.** *(S3 · medium)* What does Cook's distance measure? What do you do with an observation that has a
large one?

**A19.** *(S3 · medium)* Define the variance inflation factor. What value signals a problem, and what is the
problem?

**A20.** *(S3 · medium)* AIC and BIC disagree. Which one prefers the smaller model, and why? On what condition
may two models be compared at all?

### Session 4 · Binary, ordinal and multinomial outcomes

**A21.** *(S4 · easy)* Give two reasons why a linear regression is a poor model for a 0/1 outcome.

**A22.** *(S4 · easy)* Define the **odds** of an event. Convert a probability of 0.20 into odds, and say it
in words.

**A23.** *(S4 · medium)* A logit coefficient is $\hat\beta = 0.26$. What is it measured in? What is
$e^{0.26} \approx 1.30$, and what is the **wrong** way to read it?

**A24.** *(S4 · medium)* Why does a logistic regression have no single "effect on the probability"?

**A25.** *(S4 · easy)* What does maximum likelihood choose, in one sentence?

**A26.** *(S4 · medium)* Distinguish a **Wald** test from a **likelihood-ratio** test. When must you use the
second?

**A27.** *(S4 · medium)* What is McFadden's pseudo-$R^2$? Why is 0.25 already a good value?

**A28.** *(S4 · difficult)* In an ordinal logit, what are the cutpoints, and what is the **proportional-odds**
assumption? How would you check it?

**A29.** *(S4 · difficult)* In a multinomial logit, what is the **baseline**, and what does a relative risk ratio
of 0.80 for "vocational versus academic" mean?

**A30.** *(S4 · difficult)* Distinguish **discrimination** from **calibration**. Why does a high AUC not make
the predicted probabilities usable?

**A31.** *(S4 · easy)* Why is accuracy uninformative when the outcome is rare? Define precision and recall.

### Session 5 · Regularisation

**A32.** *(S5 · medium)* Write the bias–variance decomposition of the test error, and explain why a biased
estimator can predict better than OLS.

**A33.** *(S5 · medium)* Why is stepwise selection unstable, and why is "the data selected these variables"
not a finding?

**A34.** *(S5 · medium)* What does ridge do to the coefficients? Why is it well defined even when there are
more predictors than observations?

**A35.** *(S5 · medium)* What does the lasso do that ridge does not, and why? State two of its limitations.

**A36.** *(S5 · easy)* What does the elastic net add to the lasso? Name the property.

**A37.** *(S5 · difficult)* Why must predictors be standardised before penalising, and why must the
standardisation happen **inside** each cross-validation fold?

**A38.** *(S5 · medium)* Define $\lambda_{min}$ and $\lambda_{1se}$. Why might you report the second?

### Session 6 · Panels, interactions, curvature

**A39.** *(S6 · difficult)* What do **fixed effects** remove in a panel of countries, what do they cost you, and
what do **random effects** assume instead? Which test compares them, and on what basis may you choose?

**A40.** *(S6 · medium)* Why do classical standard errors understate uncertainty in a panel, and what is the
fix?

---

# Part B — Calculations

*Show every step. Use 1.96 for the 95% critical value. Critical values of $\chi^2$ at 5%:*
$\chi^2_1 = 3.84$, $\chi^2_2 = 5.99$, $\chi^2_3 = 7.81$, $\chi^2_4 = 9.49$.

### Session 2

**B1.** *(S2 · easy)* Five observations: $4,\ 8,\ 6,\ 10,\ 7$.
**(a)** Compute the mean and the median. **(b)** Compute $s^2$ and $s$, showing the deviations.
**(c)** Compute the standard error of the mean.

**B2.** *(S2 · easy)* A sample of $n = 36$ has $\bar x = 50$ and $s = 12$.
**(a)** Compute $SE(\bar x)$ and a 95% confidence interval for the mean. **(b)** What happens to
the SE, and to $s$, if the sample is four times larger?

**B3.** *(S2 · medium)* An indicator observed on $n = 36$ country-years gives $\bar x = 120$,
$\text{median} = 105$, $s = 30$, $\sum (x_i - \bar x)^3 = 1{,}166{,}400$ and
$\sum (x_i - \bar x)^4 = 116{,}640{,}000$.
**(a)** Compute $g_1$ and test it against $2\sqrt{6/n}$. **(b)** Compute $g_2$ and test it against
$4\sqrt{6/n}$. **(c)** Which centre would you report, and why?

### Session 3

**B4.** *(S3 · medium)* Five observations: $x = (1, 2, 3, 4, 5)$, $y = (2, 4, 5, 4, 5)$.
**(a)** Compute $\hat\beta_1 = \sum (x_i-\bar x)(y_i-\bar y) / \sum (x_i-\bar x)^2$ and $\hat\beta_0$.
**(b)** Compute the five residuals and the SSR. **(c)** Compute $R^2$ and the RSE (with $k = 1$).

**B5.** *(S3 · easy)* A regression gives $\hat\beta_1 = 0.85$ with $SE = 0.34$, on $n = 50$ observations and
$k = 4$ regressors, with $R^2 = 0.40$.
**(a)** Compute the $t$-statistic and the 95% interval. Is it significant at 5%?
**(b)** Compute the adjusted $R^2$.

**B6.** *(S3 · medium)* The true model is $y = \beta_0 + \beta_1 x + \beta_z z + u$ with $\beta_z = -0.3$, and
$z = \delta_0 + 0.5\,x + v$. The short regression of $y$ on $x$ alone gives $\hat\beta_1 = 0.45$.
**(a)** Sign and size the omitted-variable bias. **(b)** What is the implied $\beta_1$?

**B7.** *(S3 · medium)* A regression has $n = 40$ observations and $p = 3$ parameters.
**(a)** What is $\sum_i h_{ii}$, and the average leverage? **(b)** Observation 17 has $h_{ii} = 0.21$:
is that high? **(c)** What is the usual screening line for Cook's distance here?

**B8.** *(S3 · easy)* A regressor's $R_j^2$ from the regression on the other regressors is 0.92. Compute
its VIF and interpret it.

**B9.** *(S3 · medium)* On the same $n = 100$ rows, model A has $\ell = -210$ with $p = 4$ parameters, model B
has $\ell = -205$ with $p = 7$ (use $\ln 100 = 4.605$).
**(a)** Compute AIC and BIC for both. **(b)** Which model does each criterion prefer, and why do they
disagree?

### Session 4

**B10.** *(S4 · medium)* An export model gives, for (intercept, productivity index, foreign-owned),
$\hat\beta = (-3.0,\ 0.04,\ 0.9)$. A firm has productivity 50 and is foreign-owned.
**(a)** Compute $x^\top\hat\beta$, the odds and the probability of exporting.
**(b)** Report the odds ratio for foreign ownership and say it in words.
**(c)** Compute the marginal effect of one more point of productivity, in percentage points.

**B11.** *(S4 · medium)* A borrower's probability of default is 0.20. A characteristic has an odds ratio of
1.5. **(a)** Compute the new odds and the new probability. **(b)** By how many percentage points did
the probability rise? Why is it not "50% higher"?

**B12.** *(S4 · medium)* A logit with three extra dummies has $\ell = -412.6$; without them,
$\ell = -418.9$; the intercept-only model has $\ell = -450$.
**(a)** Compute the likelihood-ratio statistic and test the three dummies jointly at 5%.
**(b)** Compute McFadden's pseudo-$R^2$ of the full model.

**B13.** *(S4 · easy)* A missed default costs nine times a false alarm. **(a)** Compute the cost-minimising
threshold. **(b)** Should an applicant with $p = 0.15$ be flagged? With the default threshold of 0.5?

**B14.** *(S4 · difficult)* An ordinal logit with three ordered categories has cutpoints $c_1 = 1.0$ and
$c_2 = 3.0$, and a student has linear index $\eta = x^\top\hat\beta = 1.5$. Using
$F(z) = 1/(1 + e^{-z})$, compute the three category probabilities.
($F(-0.5) = 0.378$, $F(1.5) = 0.818$.)

**B15.** *(S4 · medium)* A multinomial logit with baseline *academic* gives, for one student, the linear
indices $\eta_{general} = -0.5$ and $\eta_{vocation} = 0.2$. Compute the three probabilities.
($e^{-0.5} = 0.607$, $e^{0.2} = 1.221$.)

**B16.** *(S4 · easy)* Among 1,000 firms, 50 fail. A model flags 100 firms, of which 30 fail.
**(a)** Fill in the confusion matrix. **(b)** Compute accuracy, precision and recall.
**(c)** What accuracy does "never fails" achieve?

### Session 5

**B17.** *(S5 · difficult)* With standardised predictors and no intercept,
$X^\top X = \begin{pmatrix} 6 & 3 \cr 3 & 4 \end{pmatrix}$ and
$X^\top y = \begin{pmatrix} 12 \cr 10 \end{pmatrix}$.
**(a)** Compute $\hat\beta^{OLS}$. **(b)** Compute $\hat\beta^{ridge}$ with $\lambda = 2$.
**(c)** Report the shrinkage of each coefficient, in %.

**B18.** *(S5 · medium)* Five standardised predictors have $\rho = (0.60,\ -0.35,\ 0.15,\ -0.05,\ 0.28)$.
**(a)** Compute the lasso updates with $\lambda = 0.25$. **(b)** Compute the elastic-net updates with
$\lambda = 0.25$, $\alpha = 0.5$, using $S_{\lambda\alpha}(\rho_j) / (1 + \lambda(1-\alpha))$.
**(c)** Compare the selected sets.

**B19.** *(S5 · medium)* A 5-fold cross-validation gives:

| $\lambda$ | 0.01 | 0.05 | 0.1 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|---|---|
| mean CV error | 2.10 | 1.95 | 1.90 | 1.98 | 2.05 | 2.40 |
| SE of the error | 0.12 | 0.10 | 0.11 | 0.10 | 0.11 | 0.13 |

Find $\lambda_{min}$ and $\lambda_{1se}$, and say which model is smaller.

### Session 6

**B20.** *(S6 · easy)* $\hat y = 20 + 3.0\,x - 0.05\,x^2$, where $x$ is a firm's age in years.
**(a)** Compute the effect of one more year at $x = 10$ and at $x = 40$. **(b)** Find the turning
point. **(c)** Why must you not read 3.0 alone?

**B21.** *(S6 · medium)* $\widehat{\text{wage}} = 30 + 1.5\,\text{exp} + 4\,\text{female} - 0.5\,(\text{exp} \times \text{female})$.
**(a)** Give the slope of experience for men and for women. **(b)** Compute the gender gap at 0
and at 10 years. **(c)** At what experience does the gap vanish?

**B22.** *(S6 · easy)* A panel regression gives $\hat\beta = 0.30$ with a classical SE of 0.08 and an SE
clustered by country of 0.18. Compute both $t$-statistics and both 95% intervals. Which do you
report, and what changes?

**B23.** *(S6 · easy)* A Hausman test comparing fixed and random effects on three coefficients gives
$H = 14.2$. Test at 5% and state the consequence.

**B24.** *(S6 · easy)* A categorical variable *region* has five levels. How many dummies enter the
regression? What happens if you include five, with an intercept?

---

# Part C — Diagnosis: find the planted error

*Every item contains at least one error. Name it, say why it is wrong, and give the correction.*

**C1.** *(S2 · medium)* "Household income in our sample has a mean of €58,000 and a standard deviation of
€41,000. By the 68–95–99.7 rule, 95% of households earn between −€24,000 and €140,000."

**C2.** *(S3 · easy)* A regression of exports on distance reports $\hat\beta = -0.82$ ($p = 0.31$). The
analyst writes: *"Distance has no effect on exports."*

**C3.** *(S3 · medium)* The residual-versus-fitted plot fans out to the right. The analyst keeps the classical
standard errors "because the coefficients are unbiased anyway".

**C4.** *(S3 · medium)* Model A (all 1,200 rows) has AIC 3,410; model B adds a variable missing for 300
country-years and, on the remaining 900 rows, has AIC 2,780. *"Model B is much better."*

**C5.** *(S4 · medium)* *"The odds ratio for collateral is 1.40, so borrowers with collateral are 40% more
likely to default."*

**C6.** *(S4 · medium)* A fraud model is reported with **accuracy 0.99**. Fraud occurs in 1% of transactions.
The threshold is 0.5 and a missed fraud costs fifty times a false alarm.

**C7.** *(S5 · difficult)*
```python
X = StandardScaler().fit_transform(X_all)          # all rows
lasso = LassoCV(cv=5).fit(X, y)
kept = X_all.columns[lasso.coef_ != 0]
print(smf.ols("y ~ " + " + ".join(kept), data=df).fit().summary())   # p-values reported
```

**C8.** *(S6 · difficult)* *"We ran fixed and random effects. Fixed effects made our key variable insignificant,
so we report random effects."* A Hausman test was not run.

---

# Part D — Interpretation and judgement

*A well-argued paragraph. A well-argued refusal earns full marks. Structure: what the number is,
what it does not license and why, what evidence would change your answer, what to do meanwhile.*

**D1.** *(S3 · medium)* Across 30 countries, a regression finds that one more point of a "digital
government" index is associated with €410 higher GDP per capita ($p < 0.01$, $R^2 = 0.58$). A
minister wants to announce that digitalising government services "will raise income by €410 per
point". Write your reply.

**D2.** *(S4 · difficult)* A bank's logit finds that applicants from one region have an odds ratio of default of
2.1, significant at 1%. A manager proposes refusing all loans from that region. Write your reply.

**D3.** *(S5 · medium)* A lasso keeps 6 of 120 candidate indicators to predict export success. A consultant
writes: *"The other 114 have no effect on exports."* Write your reply.

**D4.** *(S6 · difficult)* Firm fixed effects show that when a firm's training budget rises, its productivity
rises. A policy maker reads this as evidence that firms with larger training budgets are more
productive than other firms. Explain why the estimate does not answer that question, and which one
it does answer.

**D5.** *(S2–S3 · easy)* A report states: *"The average firm in our sample has 250 employees, so the
typical firm is medium-sized."* The median is 18 and the skewness is 6.4. What would you correct,
and what would you report instead?

---

*Answers: [`PRACTICE-ANSWERS.md`](PRACTICE-ANSWERS.md) · the exam itself: [`EXAM.md`](EXAM.md) ·
the summary: [`MIDTERM-SUMMARY.pdf`](MIDTERM-SUMMARY.pdf)*
