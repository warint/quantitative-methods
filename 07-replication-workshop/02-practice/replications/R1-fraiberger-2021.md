# Paper 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)

> **Reuses:** OLS (session 03) and the binary, ordinal and multinomial logits (session 04), line for line ·
> **Time:** about 40 minutes ·
> **Script:** [`starter/r1_fraiberger_2021.py`](../starter/r1_fraiberger_2021.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r1_fraiberger_2021.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## The data

Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices*, Journal
of International Economics — the authors' replication package (Harvard Dataverse,
doi:10.7910/DVN/QNKFJF), file
`02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta`.

- **One row** = one country on one **calendar** day, 25 countries, 1991–2017, weekends included.
  After dropping rows without a return or a predictor: **135,082** country-days.
- **Variables used:**
  - `F0_index` — today's stock-index return, in %;
  - `L1_sent1_best` — yesterday's news-sentiment index, in standard deviations (a z-score within
    each country);
  - `L1_vix` — yesterday's VIX, the market's measure of global risk;
  - `up` — built in step 1: 1 if today's return is positive, 0 otherwise.

We do not follow the paper's design. We take its data and plug it into the models of the course.

## The models, and where the code comes from

Every step copies a code cell from a lecture, **line for line**, with only the data and the
variable names changed:

| Step | Model | Copied from |
|---|---|---|
| 2 | OLS, one predictor | session 03 lecture, *Three lines of Python* |
| 3 | R² | session 03 lecture, *How much did the line explain?* |
| 4 | OLS, two predictors | session 03 lecture, *Two predictors: what "controlling for" means* |
| 5 | residuals vs fitted | session 03 lecture, *The residual plot is the instrument* |
| 6 | binary logit, log-odds | session 04 lecture, *LR 6 · Log-odds* |
| 7 | odds ratio | session 04 lecture, *LR 7 · Odds* |
| 8 | predicted probability | session 04 lecture, *LR 8 · Predicted probability* |
| 9 | ordinal logit: the day in thirds, down < flat < up | session 04 lecture, *OLR 3 · The code* |
| 10 | log-odds and proportional-odds ratios | session 04 lecture, *OLR 4* |
| 11 | probabilities | session 04 lecture, *OLR 5* |
| 12 | multinomial logit: the same three days, unordered | session 04 lecture, *MLR 3 · The code* |
| 13 | log-odds and relative risk ratios | session 04 lecture, *MLR 4* |
| 14 | probabilities | session 04 lecture, *MLR 5* |

## Steps

### Step 1 · Load the data

Read only the columns the models use, drop incomplete rows, and build the 0/1 outcome for the logit.

```python
path = "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
d = pd.read_stata(path, columns=["iso", "DATE", "F0_index", "L1_sent1_best", "L1_vix"])
d = d.dropna(subset=["F0_index", "L1_sent1_best", "L1_vix"])
d["up"] = (d["F0_index"] > 0).astype(int)            # 1 if the market rose that day
print(f"{len(d):,} country-days, {d['iso'].nunique()} countries, share of up days {d['up'].mean():.3f}")
```

**You should see:** `135,082 country-days, 25 countries, share of up days 0.519`.

### Step 2 · Three lines of Python

Today's return explained by yesterday's news sentiment.

```python
model = smf.ols("F0_index ~ L1_sent1_best", data=d).fit()
print(model.params)
```

**You should see:** `Intercept 0.056254`, `L1_sent1_best 0.071903`.

### Step 3 · How much did the line explain?

```python
print(f"R-squared = {model.rsquared:.3f}")
```

**You should see:** `R-squared = 0.001`.

### Step 4 · Two predictors

Add yesterday's VIX: the sentiment slope now holds global risk fixed.

```python
model2 = smf.ols("F0_index ~ L1_sent1_best + L1_vix", data=d).fit()
print(model2.params)
```

**You should see:** `Intercept 0.156209`, `L1_sent1_best 0.068528`, `L1_vix -0.005005`.

### Step 5 · The residual plot

```python
plt.scatter(model2.fittedvalues, model2.resid, s=12, alpha=0.6)
plt.axhline(0, color="black", lw=1)
plt.xlabel("Fitted values"); plt.ylabel("Residuals")
plt.show()
```

**You should see:** fitted values squeezed between about −0.7 and +0.8 (the model predicts almost
the same return every day), and residuals spread far above and below zero — from −39 to +105
percentage points on the most extreme days.

### Step 6 · Log-odds: does the market go up today?

```python
m2 = smf.logit("up ~ L1_sent1_best", data=d).fit(disp=0)
print(m2.params.round(4))
```

**You should see:** `Intercept 0.0747`, `L1_sent1_best 0.0773`.

### Step 7 · Odds

```python
print(np.exp(m2.params["L1_sent1_best"]).round(4))
```

**You should see:** `1.0804`.

### Step 8 · Predicted probability

A bad, an ordinary and a good news day: sentiment at −1, 0 and +1 standard deviation.

```python
print(m2.predict(pd.DataFrame({"L1_sent1_best": [-1, 0, 1]})).round(3))
```

**You should see:** `0.499`, `0.519`, `0.538`.

### Step 9 · Ordinal logit: down < flat < up

`pd.qcut` cuts the day's return into three equal-sized groups; the *OLR 3* cell keeps their order.

**You should see:** in the summary, `L1_sent1_best 0.0761` and `L1_vix -0.0057` (both p < 0.001),
and the cutpoints `down/flat` and `flat/up`.

### Step 10 · Ordinal logit: log-odds and odds

**You should see:** proportional-odds ratios `1.079` (sentiment) and `0.994` (VIX).

### Step 11 · Ordinal logit: probabilities

A bad and a good news day (−1 and +1 sd), with the VIX at 20.

**You should see:**

```
            down   flat     up
bad news   0.351  0.333  0.316
good news  0.317  0.334  0.349
```

### Step 12 · Multinomial logit: the same three days, without their order

The *MLR 3* cell, with a flat day as the baseline. The categories are the ones of step 9, but the
multinomial does not use their order: down and up each get their own equation.

**You should see:** two blocks. Down vs flat: sentiment −0.0947, VIX +0.0403. Up vs flat: sentiment
+0.0065 (p = 0.36), VIX +0.0343.

### Step 13 · Multinomial logit: log-odds and relative risk ratios

**You should see:** RRR for sentiment `0.910` (down) and `1.007` (up); for the VIX `1.041` (down)
and `1.035` (up).

### Step 14 · Multinomial logit: probabilities

The VIX at 20, sentiment from −2 to +2 sd.

**You should see:** P(down) falls from 0.379 to 0.292; P(up) rises from 0.311 to 0.360; P(flat)
from 0.309 to 0.348.

## Interpretation

- **OLS:** comparing two days one standard deviation of sentiment apart, the day after the better
  news has, on average, a return **0.072 percentage points** higher. Holding yesterday's VIX fixed,
  it is **0.069** points.
- **R²:** yesterday's sentiment accounts for about **0.1%** of the day-to-day variation in returns.
  The residual plot shows why: almost everything that moves a market on a given day is not in the
  model.
- **Logit:** one more standard deviation of sentiment raises the **log-odds** of an up day by 0.077;
  the **odds** of an up day are multiplied by **1.08** — 8% higher. In **probabilities**: from
  **50%** after a bad news day to **54%** after a good one.
- **Ordinal logit:** one more standard deviation of sentiment multiplies the odds of being in a
  higher third (flat or up rather than down, or up rather than the rest) by **1.08**; a higher VIX
  pushes days slightly **down** the scale (0.994 per point).
- **Multinomial logit:** relative to a flat day, good news mostly makes a **down** day less likely
  (RRR 0.91); its effect on an up day is not detectable. And a higher VIX makes **both** extreme days
  more likely than a flat one (RRR 1.04 and 1.035): global risk means big moves either way. The
  ordinal model cannot show this — it forces every predictor to push all days in one direction.

## What this does not license

- **No causal claim.** The same event can move both the news and the market; a one-day lag does not
  rule that out.
- **No trading rule.** A slope of 0.07 points against a daily return that varies by about 2 points,
  and a probability that moves from 50% to 54%, is small — and before transaction costs.
- **No "the order is wrong".** The multinomial is not more correct than the ordinal: it asks a
  different question. Choose the model by the question — the direction of the day, or how far from
  flat it lands.
- **Significant is not large.** With 135,082 rows, almost any slope is statistically significant.
  Read its size in units, and the R².

## Pitfalls

- **Calendar days, not trading days.** The panel has weekend rows. `L1_sent1_best` is the previous
  *calendar* day, so Monday's regressor is Sunday's news. Use the authors' lag columns; don't rebuild
  lags with a one-row shift.
- **The sentiment index is a z-score.** Its mean is 0 and its sd 1 by construction, so "one unit" is
  one standard deviation.
- **Extreme returns** (China, 21 May 1992: +105%) sit far out in the residual plot. They are real
  days, not errors.
- The residual plot has 135,082 points and takes a few seconds to draw. Runtime is otherwise about
  one second.
