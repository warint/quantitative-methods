# Session 11 — Lecture (first half, ~90 min)

# Forecasting, Distribution Shift, and Model Governance

> **What are you responsible for when someone acts on your model?**

---

### 11.1 Backtesting time-dependent models

Random K-fold CV is invalid whenever observations are ordered in time. Three valid designs:

- **Rolling origin, expanding window:** train on $1..t$, predict $t+h$; increment $t$. Uses all
  history; the training size grows, so early and late errors are not comparable.
- **Rolling origin, fixed window:** train on $t-w..t$. Constant training size; adapts to structural
  change; discards old information.
- **Blocked CV with a purge and an embargo:** leave a gap of at least $h$ observations between train
  and test to prevent leakage through overlapping horizons or through serially correlated features.
  Essential whenever features are constructed from rolling windows.

**Two rules that are violated constantly.**

1. *Point-in-time data.* Macroeconomic series are **revised**. A backtest using today's vintage of
   GDP gives your model information no forecaster had at the time. Use real-time vintages
   (ALFRED / the Philadelphia Fed's real-time dataset) or state clearly that you have not.
2. *Every* preprocessing step - standardisation, factor extraction (Session 8!), feature selection,
   hyperparameter choice - must be inside the loop.

### 11.2 Comparing forecasts honestly

Compare against a benchmark that is hard to beat: a random walk, an AR($p$), or the consensus
forecast. A lower RMSE without a significance statement is an anecdote.

**Diebold-Mariano.** Let $e_{1t}, e_{2t}$ be the forecast errors of two models and
$d_t = L(e_{1t}) - L(e_{2t})$ the loss differential. Under the null of equal predictive accuracy,
$\mathbb{E}[d_t] = 0$, and

$$\mathrm{DM} = \frac{\bar d}{\sqrt{\widehat{\mathrm{Var}}(\bar d)}} \;\xrightarrow{d}\; N(0,1),$$

where the variance must be estimated with a **HAC** (Newey-West) estimator because $d_t$ is
serially correlated at multi-step horizons — use a lag truncation of at least $h-1$.

Two cautions: the test is not valid for *nested* models estimated on the same sample (use Clark-West
instead), and with small samples the Harvey-Leybourne-Newbold correction is advisable.

### 11.3 Distribution shift

Let $P_{\text{train}}$ and $P_{\text{deploy}}$ be the joint distributions.

| Type | What changes | Detection | Fix |
|---|---|---|---|
| **Covariate shift** | $P(X)$; $P(Y\mid X)$ stable | Train a classifier to distinguish train from deploy — if it succeeds, you have shift | Importance weighting by $P_{\text{deploy}}(x)/P_{\text{train}}(x)$; often just retrain |
| **Label shift** | $P(Y)$; $P(X\mid Y)$ stable | Compare predicted marginal to observed | Reweight, or correct the intercept (Session 6) |
| **Concept drift** | $P(Y\mid X)$ | Only detectable once outcomes arrive | Retraining is necessary but not sufficient — the model form may be wrong |
| **Feedback** | your model changes the world it predicts | Requires causal reasoning, not monitoring | Redesign; see below |

The classifier-based diagnostic is worth internalising: pool training and deployment features, label
them by period, and try to predict the label. **If a classifier can tell your two periods apart, so
can your model's errors.** An AUC near 0.5 is reassuring; near 1.0 is an alarm.

**Goodhart's law**, stated precisely for this course: *when a measure becomes a target, the
relationship the model learned between measure and outcome is exactly the relationship agents have
an incentive to break.* A credit-scoring feature that predicts default only until applicants learn
it is used is not a stable feature. This is a **causal** problem (Session 10), not a monitoring
problem, and no amount of retraining solves it.

### 11.4 Model governance

A deployable model is accompanied by a document that a competent successor could act on. Minimum
contents:

1. **Intended use and out-of-scope uses.** What decision does it support? What must it *not* be used for?
2. **Data lineage.** Sources, vintages, collection dates, licences, known quality issues, checksums.
3. **Preprocessing.** Every transformation, in order, with the code that performs it.
4. **Validation.** Design (including why the CV scheme matches deployment), metrics, benchmark comparison, subgroup performance.
5. **Limitations.** Where does it perform worst? What populations are under-represented? What assumptions are load-bearing?
6. **Monitoring plan.** Which quantities are tracked, at what frequency, and what threshold triggers review.
7. **Ownership.** Who is accountable, and what is the retirement criterion.

This is not bureaucracy. Sections 5 and 6 are where the intellectual content of the whole course
finally has to be written down for someone else. A template is provided in
[`governance-file-template.md`](../02-practice/governance-file-template.md).

### 11.5 The arc, in one table

| Session | The dial you learned to turn | The self-deception it prevents |
|---|---|---|
| 2-3 | Which variables enter, and how errors are modelled | "My standard errors are correct because the software printed them" |
| 4 | Model complexity, via CV | "It fits the data well" |
| 5-6 | $\lambda$ and $\alpha$ | "The model identified the true drivers" |
| 6 | The decision threshold | "It is 97% accurate" |
| 7 | Depth, learning rate, $m$ | "The important feature is the cause" |
| 8 | The number of factors | "I extracted factors, then backtested" |
| 9 | $k$, and the representation of text | "The algorithm found clusters, so clusters exist" |
| 10 | Nothing — identification is not a dial | "A better predictor is a better policy guide" |
| 11 | The monitoring threshold | "It worked last year" |

Session 10 is the exception that defines the course: **no tuning parameter buys you
identification.**

### 11.6 Returning to *Europe 2031*

The scenario's numbers — a US:EU compute ratio near 12.2 in 2031, buildout ratio near 15.7 — were
introduced in Session 1 as *parameters of a narrative*. You can now ask sharper questions of them:

- What would a **factor model** (S8) say about how many independent dimensions "technological
  capacity" actually has? Is compute one factor, or a proxy for several?
- Is the labour-displacement mechanism a **prediction** or a **causal** claim (S10)? Which would you
  need to justify the policy responses in the narrative?
- The scenario's policy menu implies **decisions under cost asymmetry**. What are the $c_{FP}$ and
  $c_{FN}$ of acting on a false signal of European decline versus missing a true one (S6)?
- Its indicators would be **monitored** over years. Which are vulnerable to Goodhart, and which to
  concept drift (S11)?

The purpose of a stress test is not to be right. It is to make you specify what you would need to
know. That is also the purpose of a model — and it is what you will be examined on next week.

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

[Back to session 11](../README.md) · [On to the practice ->](../02-practice/README.md)
