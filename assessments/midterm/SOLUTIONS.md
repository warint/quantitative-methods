# Midterm sample paper — worked solutions

**MATH60033A · Quantitative Methods in IB**

> Use this to practise, not to read. Sit the paper first — closed book, 2 hours 30 minutes, pen and
> a non-programmable calculator — and only then open this file. Marks are shown per sub-part so you
> can see exactly where credit is earned.

**Printable:** [the paper](https://warint.github.io/quantitative-methods/midterm-sample.pdf) · [this answer key](https://warint.github.io/quantitative-methods/midterm-sample-answers.pdf) (PDF).

---

## How the marks are awarded

Three principles, applied throughout.

1. **Precision beats length.** A correct two-sentence answer scores full marks. A page that circles
   the right idea without stating it does not.
2. **A justified refusal earns full marks.** Particularly in Parts II, C and D. *"This cannot be
   claimed, and here is what would be needed"* demonstrates the thing the course is trying to build.
3. **Your own words.** The answers below are model answers. Any precise formulation earns the marks;
   in Part I there is no single right answer, and a well-argued position that disagrees with the
   scenario scores as well as one that agrees.

---

# Part I — Europe 2031 *(15)*

**I(a)** *(3)* — A **forecast** says what will probably happen and can carry a probability; a
**scenario** is a coherent *if–then* story, built to expose assumptions and dependencies, and
carries none *(1)*. The seam is between the prologue (to June 2026, drawn from the observed record)
and the main narrative (from August 2026, constructed) *(1)*. 255.1 GW and 20.9 GW describe 2031:
they are **parameters of the story**, chosen by its authors, with nothing to verify them against —
quotable only as "what the scenario assumes" *(1)*.

**I(b)** *(4)* — The file holds the model's **parameters**: billions of numbers learned in training,
plus the vocabulary that turns text into tokens *(1)*. When it answers, it computes, token after
token, a probability for every possible next token given the text so far, and picks one — a very
large prediction from patterns in its training data *(1.5)*. "Understands" overstates it: it can be
fluent about a subject without a representation of it, and it is unreliable where its training data
were thin or out of date — prediction is not understanding *(1.5)*.

**I(c)** *(4)* — Two examples of each *(2)*: "AI" — large language models, the lasso and other
machine-learning methods tuned by cross-validation; older statistics — the mean and variance,
least squares (early nineteenth century), the logistic model, maximum likelihood. Whether it matters
*(2)*: the label does not change what a result licenses — a regression called "AI" is still an
association, and an "AI" prediction still needs out-of-sample evidence. What matters is whether the
method's assumptions are stated and checked, not its age or name.

**I(d)** *(4)* — A position *(2)* and one argument against it *(2)*. *Sovereignty*: control over
critical infrastructure, data and security, no rents leaving Europe — against: very costly, chips
and much of the stack still come from abroad, and Europe may lose a race it starts late.
*Governed interdependence*: access to frontier capability now, at lower cost, with European law
anchoring the critical parts — against: dependence on foreign firms and governments, leverage that
can be used against Europe, rules that are hard to enforce. Credit either, if argued with reference
to the scenario.

---

# Part II — The reading *(10)*

**II(a)** *(2)* — Can cheap soil properties that labs already measure (texture, organic matter)
predict a soil's water-holding capacity — field capacity, permanent wilting point, available water
capacity — well enough to replace slow, expensive direct measurement, and does a random forest do
better than a linear regression? *(1)* It matters because water-holding capacity drives irrigation
and soil-health decisions, and measuring it directly is costly *(1)*.

**II(b)** *(3)* — Outcome: field capacity, wilting point and available water capacity (g of water
per g of soil) *(1)*. Unit: one topsoil sample sent to the Cornell Soil Health Laboratory, about
7,200 samples from across the continental US *(0.5)*. Predictors: sand, clay and soil organic matter
(and, for the full random forest, other routine lab measurements) *(0.5)*. Models compared: a
multiple linear regression, a reduced random forest on the same inputs, and a full random forest *(1)*.
The full random forest predicts best; the linear regression does about as well as the reduced one.

**II(c)** *(3)* — Any two distinct critiques, 1.5 each:

- **The comparison is not like for like**: the regression's fit is measured in-sample (adjusted
  $R^2$), the random forests' out-of-bag; a fair comparison scores all models on the same held-out
  data.
- **Generalisation**: one US laboratory, topsoils only, soils above 10% organic matter excluded —
  the functions may not hold for other regions, depths or soils, and predicting outside that range
  is extrapolation.
- **Reproducibility**: the validation dataset behind the headline gain is not in the replication
  package, so that result cannot be checked.
- **Influential observations**: a few extreme soils (very high clay) can move the linear model's
  coefficients — check Cook's distance.
- **Prediction, not explanation**: a good predictive fit does not say why texture and organic matter
  matter; the coefficients should not be read as causal effects.

**II(d)** *(2)* — The **lasso** or the **elastic net** (session 5) on all the routine lab
measurements, standardised, with $\lambda$ chosen by cross-validation *(1)*. It would select the
measurements that help prediction, shrink the others, and report its **out-of-sample error** —
comparable with the random forests' on the same held-out data *(1)*. (A regression with a squared
term, to capture curvature, is also accepted if justified.)

---

# Part A — Multiple choice *(30)*

1.5 points per correct answer.

| Q | Answer | Session | Why |
|---|---|---|---|
| 1 | **B** | S2 | The SD is in the units of the variable; the variance is in squared units. |
| 2 | **C** | S2 | The deviations from $\bar x$ sum to zero; dividing by $n$ would underestimate the variance. |
| 3 | **D** | S2 | Symmetric is not normal; heavy tails put more mass far from the mean. |
| 4 | **A** | S2 | The middle of the sorted values; the 40 moves the mean (14), not the median. |
| 5 | **A** | S3 | OLS minimises $\sum_i (y_i - \hat y_i)^2$. |
| 6 | **C** | S3 | The intercept is the prediction at $x = 0$, a value no observation is near. |
| 7 | **D** | S3 | A large sample makes the estimate precise; it does nothing about causality. |
| 8 | **B** | S3 | Multicollinearity: the coefficient is hard to pin down and its sign can be unstable. |
| 9 | **B** | S3 | BIC's penalty per parameter, $\ln n$, exceeds AIC's 2 as soon as $n > 7$. |
| 10 | **A** | S3 | A log compresses the long right tail; slopes then read as proportional changes. |
| 11 | **C** | S4 | Odds = $p/(1-p) = 3$ gives $p = 3/4$. |
| 12 | **D** | S4 | It chooses the coefficients that make the observed 0s and 1s most probable. |
| 13 | **B** | S4 | The S-curve is steepest at 0.5: the slope is $p(1-p)\beta$. |
| 14 | **A** | S4 | When misses are costly, flag at lower probabilities: $\tau^\star = c_{FP}/(c_{FP}+c_{FN})$. |
| 15 | **C** | S4 | AUC is discrimination (ranking), not calibration and not accuracy. |
| 16 | **D** | S4 | Precision $= TP/(TP + FP)$; recall is the share of failures that were flagged. |
| 17 | **A** | S5 | More shrinkage: further from the truth on average, but more stable. |
| 18 | **C** | S5 | $X^\top X + \lambda I$ is invertible for any $\lambda > 0$, even when $p > n$. |
| 19 | **B** | S5 | Without it, a variable in euros and one in thousands of euros would be penalised differently. |
| 20 | **D** | S5 | Each fold is held out once; each observation sits in one fold. |

---

# Part B — Short answers *(18)*

**B1** *(3)* — The description shows what a model will have to cope with: skew, outliers,
implausible values, missing data *(1)*. It can change the analysis by leading you to report the
median rather than the mean, to model the logarithm of a skewed variable, to investigate or
correct an error, or to treat extreme observations with care *(2, any two)*.

**B2** *(3)* — It plots each residual (what the model missed) against its fitted value *(1)*. When
the model is adequate, the points scatter at random around zero, with the same spread everywhere
*(1)*. Problems: a **curve** (the relationship is not linear — try a squared term or a
transformation) and a **fan** (the spread grows with the fitted values) *(1)*.

**B3** *(3)* — When a variable that affects $y$ and is correlated with $x$ is left out, the
coefficient on $x$ absorbs part of its effect *(1)*. Example: regressing firms' exports on
productivity without management quality *(1)*. Good management raises both exports and
productivity, so the productivity coefficient is pushed **upward** — it takes credit for management
*(1)*. (The direction is the sign of the omitted effect times the sign of its correlation with $x$.)

**B4** *(3)* — The cutpoints are the thresholds that separate the ordered categories, one between
each pair of neighbouring categories; they play the role of intercepts *(1.5)*. Proportional odds:
each predictor has **one** coefficient, the same at every cut — a predictor shifts the whole
distribution up or down the scale by the same amount in log-odds *(1.5)*.

**B5** *(3)* — Leakage is when information from the held-out fold reaches the model during training
*(1)*. Example: standardising, imputing or selecting variables on **all** the rows before splitting
into folds; or shuffling time-series data so the model trains on the future *(1)*. It makes the
cross-validation error **optimistic**: the model looks better than it will on genuinely new data *(1)*.

**B6** *(3)* — To let the effect of $x$ change with its level — to accelerate, level off or reverse —
when the residual plot shows a curve *(1)*. With $y = \beta_0 + \beta_1 x + \beta_2 x^2$, the effect
of one more unit of $x$ is $\beta_1 + 2\beta_2 x$: it depends on $x$, so $\beta_1$ alone must not be
read *(1)*. The turning point is the value of $x$ where that effect is zero, $x^\star =
-\beta_1/(2\beta_2)$, where the curve peaks (if $\beta_2 < 0$) or bottoms out *(1)*.

---

# Part C — Reading output *(15)*

## C1 *(5)*

**C1(a)** *(2)* — "Comparing firms of the same size, a one-point higher productivity index is
associated with an export share 0.29 percentage points higher." Units *(1)*; "holding size fixed"
and "associated with" *(1)*.

**C1(b)** *(1.5)* — Larger firms are both more productive and more export-oriented. In Model 1,
productivity took part of the credit for size (omitted-variable bias); Model 2 compares firms of the
same size, so the coefficient answers a different, narrower question.

**C1(c)** *(1.5)* — No. It is the predicted export share of a firm with productivity 0 and log
employees 0 (one employee) — far outside the data, and a negative share is impossible. It anchors
the line; it is not a finding.

## C2 *(5)*

**C2(a)** *(2)* — "A large firm has three times the **odds** of adopting AI of a small firm with the
same R&D status."

**C2(b)** *(2)* — An odds ratio multiplies the **odds**, not the probability *(1)*. The same
multiplier moves the probability more where it is closer to 0.5: from 0.25 a large firm has more
room to move than a small firm starting from 0.10 *(1)*.

**C2(c)** *(1)* — No. Without R&D, 0.25 against 0.10 is 2.5 times as likely; "three times" is the
**odds** ratio, read as if it were a ratio of probabilities.

## C3 *(5)*

**C3(a)** *(2)* — $\lambda = 0.1$: it has the lowest **cross-validation** error (1.05), the error on
data the model did not see *(1)*. The training error must not be used to choose: it always prefers
the least penalised model *(1)*.

**C3(b)** *(2)* — A larger penalty restrains the model, so it fits the training rows less closely:
training error rises *(1)*. On new data, a small $\lambda$ overfits (low bias, high variance) and a
large one underfits (high bias): the cross-validation error is lowest in between — the bias–variance
trade-off *(1)*.

**C3(c)** *(1)* — With no predictor kept, it predicts the **mean** R&D intensity for every country.

---

# Part D — Judgement *(12)*

- **What the numbers are (3):** an AUC of 0.93 says that, on past data, the model ranks risky markets
  above safe ones well. The feature ranking says which indicators the model leans on for those
  predictions.
- **What they do not license (3):** AUC is not calibration — it does not say the predicted
  probabilities are right, nor which threshold to use; it says nothing about costs or about how the
  model performs on future markets. And an important **predictive** feature is not a **cause**:
  political instability may stand in for income, conflict or currency risk, and the model was never
  designed to identify causes.
- **Evidence needed (3):** a calibration check and a validation on later years (out-of-time); a
  threshold set from the costs of a missed failure and of a refused contract; for any causal claim,
  a design that isolates the effect of instability — not a feature ranking.
- **Meanwhile (3):** use the model as a **screening tool** with human review, not an automatic
  ban; set the threshold from the costs; report the predictive performance without "causes"; and
  monitor how the flagged markets actually perform.

*Full marks for a well-argued refusal that covers the four elements.*

---

## Score yourself by part, not in total

The parts diagnose different failures, and the total hides which one is yours. Add up each part
separately and read the row that applies:

| Weak in | What it means | What to do next |
|---|---|---|
| **I** | You repeat the scenario instead of reasoning about it | Re-read the Session 1 brief and the "What AI actually is" questions |
| **II** | You read papers for their results, not their design | Take any paper and write its question, model, two critiques and an alternative in ten lines |
| **A or B** | You are working from impressions, not definitions | Re-do the pre-session self-checks in writing |
| **C** | You accept output as given | Interpret one of your own practice outputs in words, sentence by sentence |
| **D** | You over-claim | Re-read your Session 1 memo. This is the row that matters most for the final paper |

---

*The paper: [the sample paper](EXAM.md) · more practice: [the practice questions](PRACTICE.md) and its
[answer key](PRACTICE-ANSWERS.md) · the
[midterm summary](https://warint.github.io/quantitative-methods/midterm-summary.pdf)*
