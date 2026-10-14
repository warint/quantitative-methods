# Midterm practice questions — answer key

**Quantitative Methods in International Business · Sessions 1–6**

---

> Open this only after answering the [questions](PRACTICE.md) on paper. The answers are model
> answers: on the exam, any precise formulation in your own words earns the marks. In Parts I, II
> and D there is no single right answer — a precise concept and an argued position are what count.

---

# Part I — Europe 2031

**I1.** *(easy)* A forecast says what will probably happen and can carry a probability; a scenario
is a coherent, conditional story — *if* these things, *then* those — used to expose assumptions and
prepare decisions, with no probability attached. The prologue (January 2025 – June 2026) draws on
the observed record; from August 2026 the narrative is constructed. Anyone who quotes a post-seam
event or number as evidence is citing a story as a fact.

**I2.** *(medium)* The file holds the model's learned parameters (weights) — billions of numbers set
during training. When it answers, it computes, token by token, a probability for the next piece of
text from the text so far, and picks one: pattern completion learned from its training data. Its
competence comes from that training text; it stops where the text was thin, wrong or out of date
(a library version released after training), and fluency is not understanding.

**I3.** *(medium)* A scenario is a set of choices: a foundation with a mission, named authors and a
moment (June 2026) decide which risks to dramatise and which to leave out. Read it as an argument
for attention and action, not a neutral description. Possible absences: other regions (India, the
Gulf, Africa), slower AI progress or regulation that bites, energy or climate limits, public
resistance, open-source models, the role of small firms. A good answer names one and says how the
story would change.

**I4.** *(medium)* Any claim stated early enough to be observed: the pace of AI adoption by firms,
the build-out of data centres and grid connections, European investment in compute, wage growth or
job losses in exposed occupations, trade dependence on US clouds or Chinese hardware. The answer
says what would move belief either way and names a publisher — Eurostat surveys, national
statistics offices, the IEA, the OECD, company reports. A scenario is not proved by one
observation; the point is to know what to watch.

**I5.** *(medium)* Flexicurity combines flexibility for employers (easier hiring and adjustment) with
security for workers (income support, retraining, help to move to new jobs) — protecting people
rather than particular jobs. It answers the scenario's labour shock if displaced workers can be
retrained for jobs that exist; it does not, on its own, solve the fiscal problem — falling tax
revenue — and it is expensive exactly when revenues fall. A good answer takes a position.

**I6.** *(difficult)* No single right answer. Sovereignty: full control, but very costly and slow,
and still dependent on foreign chips and tools. Governed interdependence: faster and cheaper, keeps
access to frontier models, but leaves leverage with US firms and governments. A strong answer
names the trade-off, takes a side, and says what would make the chosen path fail.

**I7.** *(difficult)* Sessions 2–5 are largely statistics — means, least squares, logistic
regression (decades old), penalised regression (ridge from the 1970s, the lasso from 1996); what is
new is scale, computing power and the use of the same ideas for prediction. The distinction
matters because the old methods come with known assumptions and diagnostics — the questions of this
course apply to "AI" just as well.

---

# Part II — The readings

*Pointers, not full answers. Credit any precise research question, a correct description of the
model, two distinct critiques and a coherent alternative.*

**II1.** *(medium)* **Fraiberger et al. (2021).** (a) Does a better-than-usual news day for a country
go with higher stock returns in that country over the following days, and does global news matter
more than local news? (b) Outcome: a country's stock returns over the following days. Unit: a
country-day, for 25 countries. Main variable: a daily news-sentiment index built from Reuters
articles (share of positive minus negative words, standardised within each country); controls for
past returns, volume, volatility and global risk; a linear regression. (c) The index is a
constructed measure that assumes word counts capture sentiment; news may react to markets rather
than the reverse; a common cause may move both. (d) A logistic regression of whether the market
rises or falls the next day, reporting odds ratios and predicted probabilities; or a lasso on many
text-based measures to see which predict returns out of sample.

**II2.** *(difficult)* **Saganowski et al. (2019).** (a) Can a group's current structure in a social
network predict which of six events — dissolve, shrink, grow, continue, merge, split — happens to it
next? (b) Outcome: the next event, six unordered categories. Unit: a group in a time window. Predictors:
about 90 network measures (size, density, centrality…). Methods: 15 classifiers compared; tree-based
ones (bagging, random forest) do best, scored by the average of the per-class F-measures rather than
accuracy, because accuracy rewards predicting the common events. (c) Strong class imbalance; many
correlated features, so the feature ranking is unstable; results vary across data sets. (d) A
multinomial logit — six unordered categories, one baseline — reporting relative risk ratios and
predicted probabilities; with a lasso-type penalty to handle 90 correlated features.

**II3.** *(medium)* **Blonigen and Piger (2014).** (a) Of 56 candidate determinants of bilateral FDI,
which few actually carry the signal? Hard because earlier studies each picked their own short list
and disagree. (b) Outcome: bilateral FDI between a parent and a host country. Unit: a country pair.
Candidates: 56 variables (gravity, cultural distance, trade agreements, income, skills, institutions,
costs…). Method: Bayesian model averaging, which weights every combination of variables and gives
each an inclusion probability. Robust: gravity, cultural distance, parent income, some trade
agreements, host skill; not robust: host business costs, infrastructure, financial depth,
institutions. (c) Association, not causation; correlated candidates share the credit, so a low
inclusion probability is not "no effect"; results depend on the priors and on the candidate list.
(d) The lasso or, with correlated candidates, the elastic net, with λ chosen by cross-validation: a
short list of shrunken coefficients and its out-of-sample error.

**II4.** *(difficult)* **Topalova and Khandelwal (2011).** (a) Did India's tariff cuts of 1991 — on a
firm's output and on its inputs — raise its productivity? (b) Outcome: a firm's productivity. Unit:
a firm in a year — about 3,000 listed manufacturing firms followed over several years. Main
variables: the tariffs on the firm's industry output and on its inputs; a linear regression that
compares each firm with itself as its tariffs change. Both cuts raise productivity, the input
channel more. (c) Tariff cuts might have targeted industries already improving (the paper argues
the IMF-imposed reform rules this out); productivity is estimated, not observed; listed firms are
not all firms. (d) A logistic regression of whether a firm starts exporting or exits after the
reform, reporting odds ratios and probabilities. *(The design that follows the same firms over time
is not examined on the midterm.)*

---

# Part A — Multiple choice

| Q | Answer | Level | Why |
|:--|:--|:---|:------------------------|
| A1 | **C** | medium | $\bar x$ is estimated from the same data, so the deviations sum to zero: only $n-1$ are free. |
| A2 | **B** | easy | A trimmed mean drops a fixed share from each tail before averaging. |
| A3 | **A** | easy | The median is not pulled by the long right tail. |
| A4 | **D** | medium | The rule holds for a roughly normal variable; symmetric is not enough. |
| A5 | **C** | medium | Negative skewness: a long left tail pulls the mean below the median. |
| A6 | **A** | easy | OLS minimises the sum of squared residuals. |
| A7 | **D** | easy | Residual = observed − fitted. |
| A8 | **B** | difficult | Frisch–Waugh–Lovell: a partial relationship, net of the other regressors. |
| A9 | **C** | difficult | Constant variance is not needed for unbiasedness. |
| A10 | **A** | easy | Never interpret an intercept you have no data near. |
| A11 | **D** | medium | A VIF above about 10 signals near-collinearity: an unstable coefficient. |
| A12 | **B** | medium | Leverage depends only on how unusual the regressor values are. |
| A13 | **C** | easy | Investigate; report with and without; never delete silently. |
| A14 | **A** | medium | BIC's penalty per parameter ($\ln n$) exceeds AIC's 2 once $n > 7$. |
| A15 | **D** | easy | Likelihoods are only comparable on the same rows. |
| A16 | **B** | medium | The omitted variable raises exports and moves with investment: the short regression gives investment its credit. |
| A17 | **C** | easy | Without a design that isolates a cause, write "associated with". |
| A18 | **A** | easy | $0.25 / 0.75 = 1/3$: one event for every three non-events. |
| A19 | **D** | medium | $p = \text{odds}/(1 + \text{odds}) = 4/5 = 0.80$. |
| A20 | **B** | easy | An odds ratio multiplies the odds, not the probability. |
| A21 | **C** | easy | Logits are fitted by maximum likelihood. |
| A22 | **A** | medium | Several coefficients jointly: a likelihood-ratio test of the nested models. |
| A23 | **D** | medium | McFadden's pseudo-$R^2$ compares log-likelihoods; 0.2–0.4 is already good. |
| A24 | **B** | medium | The log compresses the tail; a coefficient on a logged outcome reads roughly as a % change. |
| A25 | **C** | medium | $J$ ordered categories: $J - 1$ cutpoints, one slope per predictor. |
| A26 | **A** | difficult | Proportional odds: the same odds ratio at every cut. |
| A27 | **D** | difficult | The baseline changes what each coefficient compares, not the fitted probabilities. |
| A28 | **B** | easy | Precision: of those flagged, the share truly positive. |
| A29 | **C** | easy | Recall: of the true positives, the share flagged. |
| A30 | **A** | medium | Calibration: predicted probabilities match observed frequencies. |
| A31 | **D** | difficult | AUC measures ranking only; probabilities can be wrong while the ranking is right. |
| A32 | **B** | medium | When misses are costly, flag at a lower probability. |
| A33 | **C** | medium | Bias–variance trade-off: a little bias, much less variance. |
| A34 | **A** | easy | A huge penalty shrinks every coefficient to zero: predict the mean. |
| A35 | **D** | difficult | The penalty makes the problem solvable even with more predictors than rows. |
| A36 | **B** | easy | The penalty is scale-dependent. |
| A37 | **C** | medium | Leakage: the held-out folds influenced the scaling, so the error is optimistic. |
| A38 | **A** | medium | The usual compromise between using enough data per fit and cost or instability. |
| A39 | **D** | medium | Post-selection $p$-values are invalid. |
| A40 | **B** | difficult | With more predictors than rows, the lasso keeps at most $n$ variables. |

*Correct letters: A ×10, B ×10, C ×10, D ×10.*

---

# Part B — Short answers

**B1.** *(easy)* The mean is the sum divided by $n$, the balance point; the median is the middle
value once sorted. The median is robust: an extreme value enters the sum and moves the mean, but
not the middle position.

**B2.** *(easy)* $IQR = Q_3 - Q_1$, the width of the middle 50% of the data. It ignores both tails,
so a long tail does not inflate it the way it inflates the standard deviation.

**B3.** *(easy)* A long **right** tail: a few large values, which pull the mean above the median.

**B4.** *(medium)* Not necessarily. The rule holds for a roughly **normal** variable; a symmetric
distribution can still have heavy or light tails (check the excess kurtosis).

**B5.** *(easy)* The sum of squared residuals. Squaring makes every miss positive, so misses above
and below cannot cancel, and punishes one large miss more than several small ones.

**B6.** *(medium)* "Comparing countries with the same investment, a one-percentage-point higher
tertiary education share is associated with GDP growth 0.31 percentage points higher." Units,
"holding investment fixed", and "associated with", not "causes".

**B7.** *(difficult)* The coefficient equals the slope from regressing the part of $y$ not explained
by the other regressors on the part of $x_j$ not explained by them: what is left of the association
once the other regressors have taken their share.

**B8.** *(easy)* The share of the variation in $y$ that the model accounts for. It does not say the
relationship is causal, nor that the model has the right shape, nor that it will predict new data.

**B9.** *(medium)* A **curve** (the straight line misses a non-linear relationship — try a squared
term or a transformation); a **fan** (the spread of the errors changes with the fitted values);
**isolated points** far from the rest (possible outliers or influential observations to
investigate). Random scatter around zero is the model behaving.

**B10.** *(medium)* BIC, because its penalty per parameter, $\ln n$, exceeds AIC's 2 once $n > 7$.
The models must be fitted on **the same rows**.

**B11.** *(easy)* It can predict probabilities below 0 or above 1, and it forces the effect on the
probability to be the same everywhere, which is implausible near 0 and 1.

**B12.** *(easy)* Odds $= p/(1-p)$. For $p = 0.75$: $0.75/0.25 = 3$, "three events for every
non-event".

**B13.** *(medium)* In **log-odds**: one more unit of $x$ raises the log-odds by 0.26. 1.30 is the
**odds ratio**: the odds are multiplied by 1.30, 30% higher. Wrong: "the probability is 30% higher".

**B14.** *(medium)* The probability is an S-shaped function of $x$: the same odds ratio moves the
probability a lot where it is near 0.5 and little near 0 or 1, so the effect depends on where you
start.

**B15.** *(medium)* Wald: one coefficient divided by its uncertainty, within one model.
Likelihood ratio: compares the log-likelihoods of two nested models. Use the second for several
coefficients **jointly**, such as all the dummies of one categorical variable.

**B16.** *(difficult)* The cutpoints are the thresholds between ordered categories, one per cut,
acting as intercepts. Proportional odds: each predictor has **one** coefficient, so the same odds
ratio applies at every cut. Check it by fitting a binary logit at each cut and comparing the slopes.

**B17.** *(difficult)* Discrimination: does the model **rank** positives above negatives (AUC)?
Calibration: when it says 20%, does the event happen about 20% of the time? A model can rank
perfectly while every probability is twice too high — useless for pricing or setting thresholds.

**B18.** *(medium)* It makes one in-or-out decision at a time, each depending on the previous ones;
resampling the rows changes the path and the final model, and noise variables get in. The
selection reflects this sample, not a property of the world.

**B19.** *(medium)* It sets weak coefficients to **exactly zero** (its absolute-value penalty), so
it selects variables. Limits: with more predictors than rows it keeps at most $n$; among
correlated predictors it keeps one, almost arbitrarily; the selected set is not "the true model".

**B20.** *(difficult)* Standardising on all the rows lets information from the held-out fold enter
the training; the held-out fold is then not truly unseen, and the cross-validated error is too
optimistic (leakage).

**B21.** *(medium)* With a squared term the effect of $x$ is $b_1 + 2 b_2 x$: it depends on $x$, and
$b_1$ is the effect only at $x = 0$. A negative $b_2$ means the effect weakens as $x$ grows, and can
turn negative past a turning point.

---

# Part C — Reading output

**C1.** *(medium)* The empirical rule is applied to a variable that is clearly skewed: income cannot
be negative, and a standard deviation of 71% of the mean signals a long right tail. Report the
median and the IQR instead.

**C2.** *(easy)* "Not significant" is read as "no effect". With $p = 0.31$ the data cannot
distinguish the effect from zero, but large negative effects are not ruled out. Say the evidence is
inconclusive.

**C3.** *(medium)* AIC compared on different rows, 1,200 against 900: the likelihoods are not
comparable, and most of the drop comes from having fewer observations. Refit both on the same 900
rows.

**C4.** *(medium)* An odds ratio read as a ratio of probabilities. 1.40 means the **odds** are 40%
higher; the change in probability depends on the starting point. (And collateral may reflect which
borrowers are asked for it — not a cause.)

**C5.** *(medium)* Accuracy on a 1% outcome: predicting "never fraud" is 99% accurate and catches
nothing. Report the base rate, precision and recall. And with misses fifty times as costly, the
threshold should be far below 0.5.

**C6.** *(difficult)* Three errors. Standardising on **all** rows before cross-validation (leakage).
Treating the lasso's selection as the true model. Reporting OLS $p$-values on the selected columns:
the same data chose and then tested them. Fix: put the scaler inside a pipeline, report the selected
set and its out-of-sample error, no post-selection $p$-values.

**C7.** *(medium)* A high $R^2$ does not show the shape is right: the U-shaped residuals say the
straight line misses a curvature. Add a squared term (or transform the variables) and check the
residuals again.

**C8.** *(difficult)* A multinomial coefficient compares *general* with the **baseline** (academic),
not the probability of general itself. Every equation moves at once: here better writers leave the
vocational programme faster than the general one, so $P(\text{general})$ first rises. Report the
predicted probabilities, and say "relative to academic".

---

# Part D — Judgement (what a strong answer contains)

**D1.** *(medium)* **What it is:** a cross-country association: countries with more schooling
export more high-technology goods. **Not licensed:** "will raise" — richer countries both school
longer and export more technology (reverse causality and common causes: income, institutions,
foreign investment); $R^2$ says nothing about cause; and the effect of *compulsory* schooling on
those who would otherwise leave school may differ from the average difference between countries.
**Evidence needed:** a design that isolates the change — countries that extended schooling compared
with similar ones that did not, before and after, with the delay it takes for pupils to reach the
labour market. **Meanwhile:** report the association with its uncertainty, attach no export figure
to the policy, and plan an evaluation.

**D2.** *(difficult)* **What it is:** a predictive association in this bank's data. **Not
licensed:** region may stand in for income, sector or collateral; refusing a whole region also
raises fairness and legal issues. **Evidence:** does the odds ratio survive the borrower's own risk
factors? Is the model calibrated for that region? **Meanwhile:** price risk on the borrower's own
characteristics, use a cost-based threshold, and review whether region is a legitimate variable.

**D3.** *(medium)* **What it is:** six variables that jointly predict well at one $\lambda$, on this
sample. **Not licensed:** a dropped variable is not "no effect" — the lasso keeps one of a correlated
group almost arbitrarily. **Evidence:** how often each variable is kept across resamples; an elastic
net to see whether groups enter together; a causal design for any variable whose effect matters.
**Meanwhile:** report predictive performance, not a list of "drivers".

**D4.** *(difficult)* **What it is:** an AUC of 0.95 says the model **ranks** borrowers well.
**Not licensed:** pricing needs the probabilities themselves to be right, and AUC says nothing about
calibration — the probabilities could all be twice too high or too low. **Evidence:** a calibration
check on recent loans (predicted against observed default rates by group), on data the vendor did
not train on. **Meanwhile:** use the score to rank or screen, not to price, until it is calibrated.

**D5.** *(easy)* The mean is pulled up by a few very large firms: a skewness of 6.4 is far beyond
any threshold, and the median (18) is a fourteenth of the mean. The typical firm has about 18
employees — small, not medium. Report the median and the IQR, and say the distribution is strongly
right-skewed.

---

*Questions: [`PRACTICE.md`](PRACTICE.md) · the exam: [`EXAM.md`](EXAM.md) and its
[solutions](SOLUTIONS.md) · the summary: [`MIDTERM-SUMMARY.pdf`](MIDTERM-SUMMARY.pdf)*
