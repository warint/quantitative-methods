# Paper 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)

> **Reuses:** describing a variable (session 02), OLS and "controlling for" (session 03), the
> binary logit (session 04) · **Time:** about 30 minutes ·
> **Script:** [`starter/r1_fraiberger_2021.py`](../starter/r1_fraiberger_2021.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r1_fraiberger_2021.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## Citation

Fraiberger, S. P., Lee, D., Puy, D. & Ranciere, R. (2021). Media sentiment and international asset prices. *Journal of International Economics*, 133, 103526. https://doi.org/10.1016/j.jinteco.2021.103526. Replication package: Harvard Dataverse, doi:10.7910/DVN/QNKFJF.

## The paper in brief

The authors turn millions of Reuters news articles about 25 countries (9 advanced, 16 emerging) into a daily "news sentiment" number for each country. For each article they take the share of positive words minus the share of negative words, then average over the day's articles. They standardise the result within each country, so it is measured in standard deviations. They then ask whether a better-than-usual news day predicts higher stock returns in the following days, and whether global news matters more than local news.

## The research question

Does a one-standard-deviation rise in a country's news sentiment go with higher stock-market returns in that country over the following days, once past returns, volume, volatility and global risk are held fixed?

## Data

- **File:** `02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta` (Stata, 119 columns; we load 7 of them).
- **Unit of observation:** one country-**calendar day**, weekends included. 25 countries × 9,862 days (1 Jan 1991 to 31 Dec 2017) = 246,550 rows.
- **Variables we use:**
  - `F0_index`: today's stock-index return, in %.
  - `L1_sent1_best`: yesterday's news sentiment, a z-score within each country (in standard deviations).
  - `L1_returns`: the previous trading day's return, in %.
  - `L1_vix`: yesterday's VIX, the US "fear index", in index points.
- **Rows for the models:** 135,082 country-days with a return and all three predictors.

## The simple model and why

We do not try to reproduce the paper's number. We fit the models you typed in class, on the authors'
data, and read them:

| Step | Model | Session |
|---|---|---|
| 3 | describe the return and the sentiment index | 02 |
| 4 | OLS: today's return on yesterday's sentiment | 03 |
| 5 | the same, **controlling for** yesterday's return and the VIX | 03 |
| 6–7 | binary logit: does the market go **up** today? | 04 |

The paper's own regression is much richer: eight lags of sentiment, article counts, returns, volume,
volatility and the VIX, country effects, weekday dummies and dummies for extreme days, with standard
errors built for a panel. Step 8 sets our slopes next to its headline number, **0.049**, to talk
about the difference, not to match it.

## Steps

### Step 1 · Load the few columns the simple models need

Asking `read_stata` for a list of columns keeps the load fast.

```python
path = "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
cols = ["iso", "DATE", "F0_index", "sent1_best", "L1_sent1_best", "L1_returns", "L1_vix"]
d = pd.read_stata(path, columns=cols)
print("rows:", len(d), "| countries:", d["iso"].nunique(),
      "| dates:", d["DATE"].min().date(), "to", d["DATE"].max().date())
```

**You should see:** `rows: 246550 | countries: 25 | dates: 1991-01-01 to 2017-12-31`.

### Step 2 · One row is a country-day, weekends included: keep days with a return

News exists every day; markets trade on weekdays. So most weekend rows have no return.

```python
d["weekend"] = d["DATE"].dt.dayofweek >= 5
print(pd.crosstab(d["weekend"], d["F0_index"].notna(), rownames=["weekend"], colnames=["has return"]))
m = d.dropna(subset=["F0_index", "L1_sent1_best", "L1_returns", "L1_vix"]).copy()
m["up"] = (m["F0_index"] > 0).astype(int)            # 1 on a day the market rose
print("rows for the models:", len(m))
```

**You should see:** 163,830 weekdays with a return and 12,270 without (holidays, early years);
70,115 weekend days without a return and 335 with one (mostly Korean Saturday sessions in the 1990s).
Then `rows for the models: 135082`.

### Step 3 · Describe the outcome and the predictor before modelling (session 02)

```python
r = m["F0_index"]
print(f"return  : mean {r.mean():.3f}  median {r.median():.3f}  sd {r.std():.2f}  "
      f"skew {stats.skew(r):.2f}  excess kurtosis {stats.kurtosis(r):.0f}")
s = m["L1_sent1_best"]
print(f"sentiment (yesterday): mean {s.mean():.2f}  sd {s.std():.2f}  median {s.median():.2f}")
print(f"share of up days: {m['up'].mean():.3f}")
```

**You should see:**

```
return  : mean 0.057  median 0.049  sd 1.94  skew 3.59  excess kurtosis 151
sentiment (yesterday): mean 0.01  sd 0.95  median 0.07
share of up days: 0.519
```

A typical day moves the market by about 0.05%, but the spread is 1.94 points: a few extreme days
(+105% in China on 21 May 1992) give the returns enormous tails. The market rises on 52% of days.

### Step 4 · OLS: today's return on yesterday's sentiment (session 03)

```python
ols1 = smf.ols("F0_index ~ L1_sent1_best", data=m).fit()
print(ols1.params.round(4))
print(f"p-value on sentiment: {ols1.pvalues['L1_sent1_best']:.1e}   R2 = {ols1.rsquared:.4f}")
```

**You should see:** intercept 0.0563, slope **0.0719**, p-value about 1e-38, R² = **0.0012**.

### Step 5 · OLS with two controls: yesterday's return and yesterday's VIX

```python
ols2 = smf.ols("F0_index ~ L1_sent1_best + L1_returns + L1_vix", data=m).fit()
print(ols2.params.round(4))
print(f"p-value on sentiment: {ols2.pvalues['L1_sent1_best']:.1e}   R2 = {ols2.rsquared:.4f}")
```

**You should see:** sentiment **0.0668**, yesterday's return 0.0061, VIX −0.0049, R² = 0.0017.
The sentiment slope falls a little once yesterday's market and global fear are held fixed.

### Step 6 · Binary logit: does the market go up today? (session 04)

```python
logit = smf.logit("up ~ L1_sent1_best + L1_returns + L1_vix", data=m).fit(disp=0)
print(pd.DataFrame({"log-odds": logit.params, "odds ratio": np.exp(logit.params)}).round(4))
print(f"p-value on sentiment: {logit.pvalues['L1_sent1_best']:.1e}")
```

**You should see:** sentiment log-odds **0.0666**, odds ratio **1.0688**; yesterday's return 1.0234;
VIX 0.9938.

### Step 7 · Predicted probability of an up day, at three levels of yesterday's sentiment

The other two predictors are held at their averages.

```python
grid = pd.DataFrame({"L1_sent1_best": [-1.0, 0.0, 1.0],
                     "L1_returns": m["L1_returns"].mean(), "L1_vix": m["L1_vix"].mean()})
grid["P(up day)"] = logit.predict(grid)
print(grid[["L1_sent1_best", "P(up day)"]].round(4).to_string(index=False))
```

**You should see:** 0.5021 after a bad news day (−1 sd), 0.5187 after an ordinary one, **0.5353**
after a good one (+1 sd).

### Step 8 · Our simple slopes next to the paper's, in words not in a match

```python
print(pd.Series({"Step 4 · sentiment only": ols1.params["L1_sent1_best"],
                 "Step 5 · + yesterday's return and VIX": ols2.params["L1_sent1_best"],
                 "Paper · 8 lags of everything, country effects, extreme days": 0.049}).round(3))
```

**You should see:** 0.072, 0.067, 0.049.

## Interpretation

- **The OLS slope, in units.** Comparing two country-days, the one that follows a news day one
  standard deviation better has a stock return about **0.07 percentage points higher**, on average
  (0.067 holding yesterday's return and the VIX fixed).
- **The logit, in odds.** One standard deviation better news multiplies the odds of an up day by
  **1.07** — about 7% higher odds, not a 7% higher probability.
- **The logit, in probabilities.** The chance of an up day goes from about **50% to 54%** between a
  bad and a good news day. Real, but small.
- **The fit.** R² is about **0.001**: yesterday's news explains a tenth of a percent of the variation
  in today's returns. With 135,082 rows, a tiny effect is still very significant.

## How it differs from the paper

- The paper controls for **eight days** of past sentiment, article counts, returns, volume,
  volatility and the VIX, plus **country effects**, weekdays and **extreme-return days**. We use
  yesterday's return and the VIX only.
- That richer set of controls brings the slope down from our 0.07 to their **0.049**: much of the
  gap comes from a few hundred extreme days, which our simple model leaves in.
- The paper also traces the effect over the following days (an impulse response) and compares local
  with global news; we look at one day only.
- The logit is ours: the paper models the size of the return, not whether it is positive.

## What this does not license

- **No causal claim.** Returns are higher on days after good news. That does not say the news
  *causes* the move: the same economic event can drive both, and a one-day lag does not rule it out.
- **No trading rule.** 0.07 points a day, with R² ≈ 0.001, is far below the daily noise (sd ≈ 1.9
  points), and before transaction costs.
- **No claim to have reproduced the paper.** Our model is deliberately simpler; its slope is not the
  paper's estimate.

## Pitfalls

- **Calendar days, not trading days.** The panel has weekend rows. `L1_sent1_best` is the previous
  *calendar* day, so Monday's regressor is Sunday's news, but `L1_returns` is the previous *trading*
  day's return. Use the authors' lag columns; don't rebuild lags with a one-row shift.
- **Mean 0 and sd 1 are not findings.** The index is a z-score by construction. Describe its median
  and tails instead.
- **Extreme returns** (China 21 May 1992: +105%; Turkey 1991: +77% / −39%) dominate the return's
  spread and kurtosis. They are why the median is a safer "typical day" than the mean.
- **Significant is not large.** With over 100,000 rows, almost any slope has a tiny p-value. Read the
  size in units, and the R².
- Runtime is about one second end to end.
