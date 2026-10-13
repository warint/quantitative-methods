# Midterm practice questions

**Quantitative Methods in International Business · Sessions 1–6**

---

These questions train for the [midterm](EXAM.md) under its conditions: **2 hours 30 minutes, on
paper, in pen, with a non-programmable calculator, and nothing else**. The midterm tests your
**understanding** — what a method does, what a number means, and what it does not license — not
your ability to carry out long calculations. The practice follows the exam's six parts:

| Part | What it asks | Here |
|---|---|---|
| **I — Europe 2031** | answer in words: what AI the scenario is about, and Europe's options | 9 prompts |
| **II — The readings** | research question, model, critiques and an alternative model, for each paper | 5 readings |
| **A — multiple choice** | one correct answer out of four | 40 questions |
| **B — short answers** | state a concept precisely, in two or three sentences | 21 questions |
| **C — reading output** | interpret an output in words, or find the planted error | 8 items |
| **D — judgement** | say what a number does *not* license | 5 prompts |

**To print:** [questions](https://warint.github.io/quantitative-methods/midterm-practice.pdf) · [answer key](https://warint.github.io/quantitative-methods/midterm-practice-answers.pdf) (PDF).

Each question carries its session and its difficulty in brackets, so you can train one session at a
time, and build up from easy to difficult:

- **easy** (25 questions) — recall a definition, or recognise the right reading of a result;
- **medium** (44) — combine two ideas, or explain why a tempting reading is wrong;
- **difficult** (19) — a subtle distinction, an argued position, or several faults to find at once.

> **How to use it.** Answer first, on paper, without notes. Only then open the
> [answer key](PRACTICE-ANSWERS.md). An answer you recognise is not an answer you can produce; the
> exam asks you to produce it. The [midterm summary](MIDTERM-SUMMARY.pdf) holds the ideas you are
> expected to carry in your head.

---

# Part I — Europe 2031

*Answer in words, from the scenario and our Session 1 conversation, "what AI actually is". No
calculation is needed. Half a page each.*

**I1.** *(S1 · easy)* *Europe 2031* is a **scenario**, not a **forecast**. What is the difference?
Where does the fact-based part of the text end and the speculative part begin, and why does that
seam matter for anyone who quotes it?

**I2.** *(S1 · medium)* In Session 1 you downloaded a language model of a few gigabytes. What is in
that file, and what computation runs when it answers a question? Where does its competence come
from, and where does it stop?

**I3.** *(S1 · medium)* The scenario measures a region's AI power in **gigawatts of compute** (255.1 GW
for the United States in 2031, 20.9 GW for Europe). What do these numbers represent, and what does
the choice of that unit assume about what makes AI powerful?

**I4.** *(S1 · medium)* Compute, data and mathematics (the algorithms) are the three ingredients of
an AI system. Explain each in your own words, and say on which of the three Europe is best placed
to compete.

**I5.** *(S1 · medium)* What is **vertical AI**? Give two examples in European industry, and say
whether vertical AI is a way for Europe to escape the frontier race the scenario describes.

**I6.** *(S1 · medium)* What is a **small language model**? Give two advantages and two limits for a
European firm that chooses one over a frontier model run by a US provider.

**I7.** *(S1 · medium)* Why does the scenario propose **Special Compute Zones** — faster permits,
dedicated teams, grid connections from retired power plants? What could go wrong with a strategy
built around data centres?

**I8.** *(S1 · difficult)* The scenario contrasts **compute sovereignty** (Europe builds and controls
its own AI stack) with **governed interdependence** (Europe works with US providers but anchors
critical infrastructure under European law). Which do you find more realistic, and why?

**I9.** *(S1 · difficult)* "What in this course is AI, and what is a hundred-year-old statistical
method with a new name?" Answer the question for the methods of sessions 2 to 5, and say whether
the distinction matters.

---

# Part II — The readings

*For each required reading, answer the same four questions: **(a)** the research question; **(b)**
the model — the outcome, the unit of observation, the explanatory variables and the method; **(c)**
two distinct critiques a referee could raise; **(d)** another model from this course that could
answer the question, and what it would report.*

**II1.** *(S2 · medium)* **Fraiberger, Lee, Puy and Sahay (2021)**, *Media sentiment and international
asset prices*.

**II2.** *(S3 · medium)* **Amsili, van Es and Schindelbeck (2024)**, *Pedotransfer functions for field
capacity, permanent wilting point, and available water capacity*.

**II3.** *(S4 · difficult)* **Saganowski et al. (2019)**, *Analysis of group evolution prediction in
complex networks*.

**II4.** *(S5 · medium)* **Blonigen and Piger (2014)**, *Determinants of foreign direct investment*.

**II5.** *(S6 · difficult)* **Topalova and Khandelwal (2011)**, *Trade liberalization and firm
productivity*.

---

# Part A — Multiple choice

*Tick one answer. On the exam, each correct answer earns the same marks and a wrong answer costs
nothing.*

### Session 2 · Describing a variable

**A1.** *(S2 · medium)* The sample variance divides by $n - 1$ rather than $n$ because:

- **A.** it makes the variance larger, which is safer
- **B.** the formula would otherwise not have the units of $x^2$
- **C.** the deviations from $\bar x$ sum to zero, so only $n - 1$ of them are free
- **D.** one observation is always an outlier

**A2.** *(S2 · easy)* A 5% trimmed mean is:

- **A.** the mean of the 5% largest values
- **B.** the mean computed after dropping 5% of the observations from each tail
- **C.** the median plus 5%
- **D.** the mean multiplied by 0.95

**A3.** *(S2 · easy)* Household income is strongly right-skewed. To describe a "typical" household,
you report:

- **A.** the median
- **B.** the mean
- **C.** the maximum
- **D.** the variance

**A4.** *(S2 · medium)* The 68–95–99.7 rule may be applied to a variable that is:

- **A.** strictly positive
- **B.** symmetric, whatever its tails
- **C.** measured in percent
- **D.** roughly normal

**A5.** *(S2 · medium)* A variable's skewness is −1.4, well beyond its threshold. Then:

- **A.** it is roughly normal
- **B.** its mean is above its median
- **C.** it has a long left tail, and its mean is below its median
- **D.** it has no extreme values

### Session 3 · Can the regression be trusted?

**A6.** *(S3 · easy)* Ordinary least squares chooses the line that:

- **A.** minimises the sum of the squared residuals
- **B.** passes through the largest number of points
- **C.** minimises the largest residual
- **D.** maximises the slope

**A7.** *(S3 · easy)* A residual is:

- **A.** the slope of the line
- **B.** the predicted value
- **C.** the average of $y$
- **D.** the observed value minus the fitted value

**A8.** *(S3 · difficult)* In a multiple regression, the coefficient on $x_j$ measures the
relationship between $y$ and:

- **A.** $x_j$, ignoring the other regressors
- **B.** the part of $x_j$ that the other regressors do not explain
- **C.** the sum of all the regressors
- **D.** $x_j$ in the observations where the other regressors are zero

**A9.** *(S3 · difficult)* For OLS to be unbiased, which of these is **not** needed?

- **A.** the model is linear in its parameters
- **B.** the errors have mean zero given the regressors
- **C.** the errors have constant variance
- **D.** no regressor is an exact combination of the others

**A10.** *(S3 · easy)* A regression of GDP per capita on a productivity index has an intercept of
−€86,000. The index runs from 72 to 129 in the data. The intercept should be:

- **A.** left uninterpreted: it is a prediction at an index of 0, far outside the data
- **B.** reported as the income of the least productive country
- **C.** read as proof that the model is wrong
- **D.** removed from the model

**A11.** *(S3 · medium)* A regressor has a variance inflation factor of 15. This means:

- **A.** its coefficient is 15 times too large
- **B.** it explains 15% of $y$
- **C.** it should be multiplied by 15
- **D.** it is almost a combination of the other regressors, so its coefficient is unstable

**A12.** *(S3 · medium)* An observation's **leverage** depends on:

- **A.** its residual only
- **B.** how unusual its values of the regressors are
- **C.** its value of $y$ only
- **D.** the number of regressors only

**A13.** *(S3 · easy)* Cook's distance flags one country-year far above all the others. You:

- **A.** delete it and report the new fit only
- **B.** ignore it: one row cannot matter
- **C.** find out which row it is and why, and report the fit with and without it
- **D.** add a dummy for it and say nothing

**A14.** *(S3 · medium)* AIC and BIC disagree: AIC prefers the larger model, BIC the smaller one.
The usual reason is that:

- **A.** BIC charges more for each extra parameter once the sample is not tiny
- **B.** AIC is computed on different data
- **C.** BIC ignores the fit of the model
- **D.** one of them must be miscalculated

**A15.** *(S3 · easy)* Two models may be compared on AIC only if they are:

- **A.** both significant
- **B.** both linear
- **C.** both estimated by the same person
- **D.** fitted on the same rows

**A16.** *(S3 · medium)* A firm's management quality raises its exports **and** is higher in firms
that invest more. A regression of exports on investment alone will:

- **A.** be unbiased
- **B.** overstate the effect of investment
- **C.** understate the effect of investment
- **D.** always give a negative coefficient

**A17.** *(S3 · easy)* More educated regions have higher wages. Which sentence is licensed?

- **A.** "Education causes higher wages."
- **B.** "Raising education will raise wages."
- **C.** "Education is associated with higher wages."
- **D.** "Wages do not affect education."

### Session 4 · Categorical outcomes

**A18.** *(S4 · easy)* A probability of 0.25 corresponds to odds of:

- **A.** 1 to 3, about 0.33
- **B.** 0.25
- **C.** 3 to 1
- **D.** 0.75

**A19.** *(S4 · medium)* Odds of 4 (four to one) correspond to a probability of:

- **A.** 0.25
- **B.** 4
- **C.** 0.40
- **D.** 0.80

**A20.** *(S4 · easy)* An odds ratio of 0.70 for a training programme means that the programme:

- **A.** lowers the probability by 70%
- **B.** multiplies the odds by 0.70 — 30% lower odds
- **C.** has no effect
- **D.** lowers the probability by 0.70 points

**A21.** *(S4 · easy)* A logistic regression is estimated by:

- **A.** least squares on the 0/1 outcome
- **B.** soft-thresholding
- **C.** maximum likelihood
- **D.** cross-validation

**A22.** *(S4 · medium)* You want to test whether four region dummies matter **jointly** in a logit.
You use:

- **A.** a likelihood-ratio test comparing the models with and without them
- **B.** the largest of the four $z$-statistics
- **C.** the $R^2$
- **D.** the odds ratio of the first dummy

**A23.** *(S4 · medium)* A logit has a McFadden pseudo-$R^2$ of 0.25. This means:

- **A.** the model explains 25% of the variance of the outcome
- **B.** 25% of the predictions are correct
- **C.** the model is useless
- **D.** a reasonable improvement over the intercept-only model; it is not a share of variance

**A24.** *(S6 · medium)* Export values are strongly right-skewed. Before regressing them on firm
size, an analyst takes their logarithm. This:

- **A.** removes every outlier
- **B.** pulls in the long tail, and a coefficient then reads approximately as a percentage change
- **C.** makes the regression causal
- **D.** is forbidden in a linear regression

**A25.** *(S4 · medium)* An ordinal logit for four ordered categories has:

- **A.** four cutpoints and four coefficients per predictor
- **B.** no cutpoints
- **C.** three cutpoints and one coefficient per predictor
- **D.** one equation per category against a baseline

**A26.** *(S4 · difficult)* The **proportional-odds** assumption says that:

- **A.** each predictor has the same odds ratio at every cut between categories
- **B.** every category has the same probability
- **C.** the odds always equal the probability
- **D.** the cutpoints are equally spaced

**A27.** *(S4 · difficult)* In a multinomial logit, you change the baseline category from
*academic* to *general*. Then:

- **A.** the predicted probabilities change
- **B.** the model can no longer be estimated
- **C.** nothing changes at all
- **D.** the coefficients change meaning, but the predicted probabilities stay the same

**A28.** *(S4 · easy)* **Precision** is:

- **A.** the share of all cases classified correctly
- **B.** among the cases flagged, the share that are truly positive
- **C.** among the true positives, the share that are flagged
- **D.** the area under the ROC curve

**A29.** *(S4 · easy)* **Recall** is:

- **A.** the share of all cases classified correctly
- **B.** among the cases flagged, the share that are truly positive
- **C.** among the true positives, the share that are flagged
- **D.** the threshold used

**A30.** *(S4 · medium)* A model is **well calibrated** when:

- **A.** among the cases it gives a probability of 20%, about 20% are positive
- **B.** it ranks every positive above every negative
- **C.** its accuracy exceeds 90%
- **D.** it uses a threshold of 0.5

**A31.** *(S4 · difficult)* A default model has an AUC of 0.93, but its predicted probabilities are
all about twice the observed default rates. This is:

- **A.** impossible
- **B.** a sign of a coding error
- **C.** a perfectly calibrated model
- **D.** possible: it ranks well (discrimination) but its probabilities are wrong (calibration)

**A32.** *(S4 · medium)* Missing a default costs a bank far more than a false alarm. Compared with
0.5, the threshold for flagging a borrower should be:

- **A.** higher
- **B.** lower
- **C.** the same: 0.5 is always optimal
- **D.** set to the base rate whatever the costs

### Session 5 · Regularisation

**A33.** *(S5 · medium)* Ridge regression can predict new data better than OLS because:

- **A.** it is unbiased
- **B.** it uses more data
- **C.** it accepts a little bias for a large cut in variance
- **D.** it removes every correlated predictor

**A34.** *(S5 · easy)* As the ridge penalty $\lambda$ grows very large, the coefficients:

- **A.** all shrink toward zero, and the model predicts the mean
- **B.** become the OLS coefficients
- **C.** grow without limit
- **D.** become exactly zero one at a time, like the lasso

**A35.** *(S5 · difficult)* With more predictors than observations, OLS has no unique solution but
ridge does, because:

- **A.** ridge drops half of the predictors
- **B.** ridge uses the median instead of the mean
- **C.** ridge needs no data
- **D.** adding the penalty makes the problem solvable for any $\lambda > 0$

**A36.** *(S5 · easy)* Predictors must be standardised before ridge or the lasso because:

- **A.** the software requires it
- **B.** the penalty compares coefficient sizes, which depend on each variable's units
- **C.** it makes the coefficients significant
- **D.** it removes outliers

**A37.** *(S5 · medium)* An analyst standardises the predictors on **all** the rows, then runs
5-fold cross-validation. The cross-validated error is:

- **A.** exactly right
- **B.** too pessimistic
- **C.** too optimistic: information from the held-out folds leaked into training
- **D.** unaffected, because standardising changes nothing

**A38.** *(S5 · medium)* In $K$-fold cross-validation, $K = 5$ or $10$ is the usual choice because:

- **A.** it balances using most of the data in each fit against the cost and instability of a very large $K$
- **B.** a larger $K$ is forbidden
- **C.** $K$ must divide the sample size
- **D.** a smaller $K$ always gives the lowest error

**A39.** *(S5 · medium)* After the lasso selects six variables, the analyst refits OLS on them and
reports the $p$-values. These $p$-values are:

- **A.** valid, because OLS is unbiased
- **B.** too large
- **C.** identical to the lasso's
- **D.** not valid: the same data chose the variables and then tested them

**A40.** *(S5 · difficult)* With 200 candidate predictors and 60 observations, the lasso can keep
at most:

- **A.** 200 variables
- **B.** 60 variables
- **C.** 6 variables
- **D.** 1 variable

---

# Part B — Short answers

*Two or three sentences each. Be precise, not lengthy.*

### Session 2 · Describing a variable

**B1.** *(S2 · easy)* Define the mean and the median. Which is robust to an extreme value, and why?

**B2.** *(S2 · easy)* Define the interquartile range. Why is it preferred to the standard deviation
for a skewed variable?

**B3.** *(S2 · easy)* What does a positive skewness tell you about the shape of a distribution, and
about the order of its mean and median?

**B4.** *(S2 · medium)* A variable is symmetric. Can you apply the 68–95–99.7 rule to it? Explain.

### Session 3 · Can the regression be trusted?

**B5.** *(S3 · easy)* What does ordinary least squares minimise? Why squares, rather than the
absolute distances?

**B6.** *(S3 · medium)* Interpret a slope of 0.31 in a regression of GDP growth (in %) on tertiary
education (in % of the population) with a control for investment. Write the full sentence.

**B7.** *(S3 · difficult)* What does "holding the other regressors fixed" mean, according to the
Frisch–Waugh–Lovell result?

**B8.** *(S3 · easy)* Define $R^2$. Give two things a high $R^2$ does **not** tell you.

**B9.** *(S3 · medium)* Name three things you look for in a plot of residuals against fitted values,
and what each would tell you about the model.

**B10.** *(S3 · medium)* AIC and BIC disagree. Which one prefers the smaller model, and why? On what
condition may two models be compared at all?

### Session 4 · Categorical outcomes

**B11.** *(S4 · easy)* Give two reasons why a linear regression is a poor model for a 0/1 outcome.

**B12.** *(S4 · easy)* Define the **odds** of an event. Convert a probability of 0.75 into odds, and
say it in words.

**B13.** *(S4 · medium)* A logit coefficient is 0.26, and $e^{0.26} \approx 1.30$. What is the
coefficient measured in, what is 1.30, and what is the **wrong** way to read it?

**B14.** *(S4 · medium)* Why does a logistic regression have no single "effect on the probability"?

**B15.** *(S4 · medium)* Distinguish a **Wald** test from a **likelihood-ratio** test. When must you
use the second?

**B16.** *(S4 · difficult)* In an ordinal logit, what are the cutpoints, and what is the
proportional-odds assumption? How would you check it?

**B17.** *(S4 · difficult)* Distinguish **discrimination** from **calibration**. Why does a high AUC
not make the predicted probabilities usable?

### Session 5 · Regularisation

**B18.** *(S5 · medium)* Why is stepwise selection unstable, and why is "the data selected these
variables" not a finding?

**B19.** *(S5 · medium)* What does the lasso do that ridge does not, and why? State two of its
limitations.

**B20.** *(S5 · difficult)* Why must the standardisation of the predictors happen **inside** each
cross-validation fold?

### Session 6 · Curvature

**B21.** *(S6 · medium)* In $\hat y = b_0 + b_1 x + b_2 x^2$, why must you not read $b_1$ on its own?
What does a negative $b_2$ mean for the effect of $x$?

---

# Part C — Reading output

*Every item contains at least one error, or one tempting wrong reading. Say what it is, why it is
wrong, and what you would write instead — in words.*

**C1.** *(S2 · medium)* "Household income in our sample has a mean of €58,000 and a standard
deviation of €41,000. By the 68–95–99.7 rule, 95% of households earn between −€24,000 and
€140,000."

**C2.** *(S3 · easy)* A regression of exports on distance reports a coefficient of −0.82 with
$p = 0.31$. The analyst writes: *"Distance has no effect on exports."*

**C3.** *(S3 · medium)* Model A (all 1,200 rows) has AIC 3,410; model B adds a variable missing for
300 country-years and, on the remaining 900 rows, has AIC 2,780. *"Model B is much better."*

**C4.** *(S4 · medium)* *"The odds ratio for collateral is 1.40, so borrowers with collateral are 40%
more likely to default."*

**C5.** *(S4 · medium)* A fraud model is reported with **accuracy 0.99**. Fraud occurs in 1% of
transactions. The threshold is 0.5, and a missed fraud costs fifty times a false alarm.

**C6.** *(S5 · difficult)*
```python
X = StandardScaler().fit_transform(X_all)          # all rows
lasso = LassoCV(cv=5).fit(X, y)
kept = X_all.columns[lasso.coef_ != 0]
print(smf.ols("y ~ " + " + ".join(kept), data=df).fit().summary())   # p-values reported
```

**C7.** *(S3 · medium)* A regression of house prices on floor area has $R^2 = 0.91$. The residual
plot shows a clear U-shape. The analyst writes: *"With an R² of 0.91, the straight line is clearly
the right model."*

**C8.** *(S4 · difficult)* A multinomial logit of programme choice (baseline: *academic*) gives a
negative coefficient on the writing score in the *general* equation. A report concludes: *"Better
writers are always less likely to choose the general programme."* Yet the predicted probability of
*general* rises from 0.19 to 0.23 as the writing score goes from 35 to 45, then falls.

---

# Part D — Interpretation and judgement

*A well-argued paragraph. A well-argued refusal earns full marks. Structure: what the number is,
what it does not license and why, what evidence would change your answer, what to do meanwhile.*

**D1.** *(S3 · medium)* Across 85 countries, a regression finds that countries with one more
year of average schooling export, on average, 6% more high-technology goods ($p < 0.01$,
$R^2 = 0.47$). A trade minister wants to announce that extending compulsory schooling by one year
"will raise high-technology exports by 6%". Write your reply.

**D2.** *(S4 · difficult)* A bank's logit finds that applicants from one region have an odds ratio of
default of 2.1, significant at 1%. A manager proposes refusing all loans from that region. Write
your reply.

**D3.** *(S5 · medium)* A lasso keeps 6 of 120 candidate indicators to predict export success. A
consultant writes: *"The other 114 have no effect on exports."* Write your reply.

**D4.** *(S4 · difficult)* A vendor sells a credit-scoring model with an AUC of 0.95 and proposes to
use its predicted probabilities directly to set each borrower's interest rate. The model has never
been checked against observed default rates. Write your reply.

**D5.** *(S2 · easy)* A report states: *"The average firm in our sample has 250 employees, so the
typical firm is medium-sized."* The median is 18 and the skewness is 6.4. What would you correct,
and what would you report instead?

---

*Answers: [`PRACTICE-ANSWERS.md`](PRACTICE-ANSWERS.md) · the exam itself: [`EXAM.md`](EXAM.md) ·
the summary: [`MIDTERM-SUMMARY.pdf`](MIDTERM-SUMMARY.pdf)*
