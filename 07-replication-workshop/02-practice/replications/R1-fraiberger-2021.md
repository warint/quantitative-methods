# Paper 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)

> **Reuses:** OLS (session 03) and the binary logit (session 04), line for line ·
> **Time:** about 30 minutes ·
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

## What this does not license

- **No causal claim.** The same event can move both the news and the market; a one-day lag does not
  rule that out.
- **No trading rule.** A slope of 0.07 points against a daily return that varies by about 2 points,
  and a probability that moves from 50% to 54%, is small — and before transaction costs.
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
