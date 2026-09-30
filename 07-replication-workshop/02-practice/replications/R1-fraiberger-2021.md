# Replication 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)

> **Reuses:** exploratory data analysis (session 02) · **Time:** about 30 minutes ·
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

## The published target

- **Target:** the coefficient on **yesterday's sentiment (`L1_sent1_best`)** at horizon 0 in the panel regression for all 25 countries: **0.049 (s.e. 0.007), N = 102,665**.
- **Where it is:** `public/results/figure_2b.csv`, column (1) `F0_index`, row `L1_sent1_best`. The file is written by `code/6_figure_2.do` (the `xtscc ... , fe pooled` loop). This coefficient is the first point (h = 0) of the impulse response in Figure 2, panel B.
- For comparison, the US-only version (Figure 2A, `figure_2a.csv`, column 1) is 0.064 (0.019), N = 6,016.
- **Caveat:** these numbers come from the package's CSV output, not from the printed article. The readme says the package's sentiment index is "an updated version" (Reuters 1991 to 2019), while the article used 1991 to 2015. So the printed Figure 2 may differ slightly from the CSV.

## Data

- **File:** `02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta` (Stata, 119 columns; we load 57 of them). The package also has `news_sentiment.csv` (the three sentiment indices only, 259,002 rows). We don't use it because it has no returns.
- **Unit of observation:** one country-**calendar day**, weekends included. 25 countries × 9,862 days (1 Jan 1991 to 31 Dec 2017) = 246,550 rows.
- **Key variables:** `sent1_best` is the news sentiment index, a z-score within each country. `L1_sent1_best` is its value the previous calendar day. `F0_index` is today's stock-index return in %, identical to `returns`. `L1..L8_` are lags of sentiment, article counts (`art1_best`), returns, detrended volume (`vlm_ma60_adj`), volatility (`vol_ma60`) and the VIX. `dow2`–`dow5` are weekday dummies.
- **Rows after cleaning:** 172,690 non-missing sentiment values (profile). 138,913 rows for the simple regression. 104,073 rows for the full regression, i.e. rows where the return and all 48 lags are present.

## Steps

### Step 1 · Load the columns you need

Reading only 57 of the 119 columns makes the 100 MB file load in well under a second. This is the first habit of EDA: know what is in the file before you compute anything.

```python
path = "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
lags = range(1, 9)                                   # the paper uses 8 lags
controls = ["sent1_best", "art1_best", "returns", "vlm_ma60_adj", "vol_ma60", "vix"]
lag_cols = [f"L{i}_{v}" for v in controls for i in lags]
cols = ["iso", "DATE", "sent1_best", "returns", "F0_index", "dow2", "dow3", "dow4", "dow5"] + lag_cols
d = pd.read_stata(path, columns=cols)
print("rows, columns:", d.shape)
print("countries:", d["iso"].nunique(), "| dates:", d["DATE"].min().date(), "to", d["DATE"].max().date())
```

**You should see:**
```
rows, columns: (246550, 57)
countries: 25 | dates: 1991-01-01 to 2017-12-31
```

### Step 2 · What is one row, and what is missing?

Session 02 insists that you know the window and the missingness before you profile anything. News appears every day, but markets trade only on weekdays. So sentiment and returns are missing on different rows.

```python
d["weekday"] = d["DATE"].dt.dayofweek               # 0 = Monday ... 6 = Sunday
d["weekend"] = d["weekday"] >= 5
print(d[["sent1_best", "returns"]].notna().sum())
print(pd.crosstab(d["weekend"], d["returns"].notna(), rownames=["weekend"], colnames=["has return"]))
s = d["sent1_best"].dropna()                         # the sentiment index we profile
n = len(s)
```

**You should see:**
```
sent1_best    172690
returns       164179
has return  False   True
weekend
False       12256  163844
True        70115     335
```
(The 335 weekend returns are real. 252 of them are Korean Saturday sessions from the 1990s.)

### Step 3 · Centre: mean, trimmed mean, median

These three answer different questions. Here the mean is zero **by construction**, because the authors z-scored the index. The informative comparison is therefore the median against the mean.

```python
print(f"n = {n:,}")
print(f"mean     {s.mean():+.3f}")
print(f"trim 5%  {stats.trim_mean(s, 0.05):+.3f}")
print(f"median   {s.median():+.3f}")
```

**You should see:**
```
n = 172,690
mean     -0.000
trim 5%  +0.019
median   +0.066
```
The median sits above the mean, so the typical day is slightly positive and a long tail of very bad news days drags the mean down. The gap is small, 0.066 sd.

### Step 4 · Spread, and the empirical rule

The standard deviation is 1 by construction. So check the IQR, the extremes and the 68/95/99.7 rule, and confirm the z-scoring country by country.

```python
print(f"sd  {s.std(ddof=1):.3f}   IQR  {s.quantile(0.75) - s.quantile(0.25):.3f}"
      f"   min {s.min():.2f}   max {s.max():.2f}")
for k, normal in ((1, 0.68), (2, 0.95), (3, 0.997)):
    share = ((s - s.mean()).abs() <= k * s.std()).mean()
    print(f"within {k} sd: {share:.1%}   (normal: {normal:.1%})")
print(d.groupby("iso")["sent1_best"].agg(["mean", "std"]).round(3).head(5))   # z-scored by country
```

**You should see:**
```
sd  1.000   IQR  1.049   min -11.56   max 12.49
within 1 sd: 76.4%   (normal: 68.0%)
within 2 sd: 94.8%   (normal: 95.0%)
within 3 sd: 98.6%   (normal: 99.7%)
     mean  std
iso
AR    0.0  1.0
BR   -0.0  1.0
CL    0.0  1.0
CN    0.0  1.0
DE   -0.0  1.0
```
The rule passes at 2 sd, as the chapter warns it can. It fails in the centre (too many days within 1 sd) and in the tails (1.4% beyond 3 sd against 0.3%). Days 11 to 12 sd from the mean exist.

### Step 5 · Shape, tested against the thresholds

This is the session's shape function, with $g_1$ tested against $2\sqrt{6/n}$ and $g_2$ against $4\sqrt{6/n}$. Returns are tested alongside for comparison.

```python
def shape(x):
    x = pd.Series(x).dropna().to_numpy(float)
    n, xbar, sd = len(x), x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / sd ** 3
    g2 = ((x - xbar) ** 4).mean() / sd ** 4 - 3
    print(f"n = {n:,}   g1 = {g1:+.3f} (threshold ±{2 * np.sqrt(6 / n):.3f})"
          f"   g2 = {g2:+.3f} (threshold ±{4 * np.sqrt(6 / n):.3f})")
shape(s)            # the sentiment index
shape(d["returns"])  # daily returns, for comparison
```

**You should see:**
```
n = 172,690   g1 = -0.413 (threshold ±0.012)   g2 = +4.836 (threshold ±0.024)
n = 164,179   g1 = +3.784 (threshold ±0.012)   g2 = +161.069 (threshold ±0.024)
```
Sentiment is significantly left-skewed and strongly heavy-tailed. Returns are far worse: $g_2 = 161$ comes from a handful of extreme days, such as China on 21 May 1992 (+105%) and Turkey in 1991 (−39% to +77%). With $n$ this large, the thresholds are tiny, so everything "fails". The size of $g$ matters more than the test.

### Step 6 · Look at it

The session rule is to trust the picture, and check that it agrees with $g_1$ and $g_2$.

```python
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].hist(s, bins=100)
ax[0].axvline(s.mean(), color="black"); ax[0].axvline(s.median(), color="red", linestyle="--")
ax[0].set_xlabel("News sentiment (z-score within country)")
ax[1].hist(d["returns"].dropna(), bins=100, range=(-10, 10))
ax[1].set_xlabel("Daily stock-index return (%), shown from -10 to +10")
plt.savefig(OUTPUT / "fig_s02_distributions.png", dpi=120)
plt.close()
```

**You should see:** `fig_s02_distributions.png`. Both histograms are single-peaked and much more pointed than a normal curve, with long thin tails. Sentiment's left tail is visibly longer. Mean and median lines almost overlap, because the gap is 0.07 sd.

### Step 7 · The simplest return regression, and the slope in units

This is the course's simple regression. Today's return (%) is regressed on yesterday's sentiment (sd units), with HC1 standard errors.

```python
m1 = smf.ols("F0_index ~ L1_sent1_best", data=d).fit(cov_type="HC1")
print(f"slope {m1.params['L1_sent1_best']:.4f}  (se {m1.bse['L1_sent1_best']:.4f})"
      f"  n = {int(m1.nobs):,}  R2 = {m1.rsquared:.4f}")
```

**You should see:**
```
slope 0.0738  (se 0.0058)  n = 138,913  R2 = 0.0013
```
**In units:** a day after news sentiment one standard deviation above its country average, the stock index return is on average 0.074 **percentage points** higher. Sentiment explains 0.13% of the day-to-day variance in returns.

### Step 8 · Add what the paper controls for

This step reuses "controlling for" from the chapter. It adds country fixed effects (`C(iso)`), eight lags each of sentiment, article counts, returns, volume, volatility and the VIX, and weekday dummies, which is everything in `6_figure_2.do` that the package ships. Standard errors are clustered by date.

```python
dd = d.dropna(subset=["F0_index"] + lag_cols).copy()
rhs = " + ".join(lag_cols) + " + dow2 + dow3 + dow4 + dow5 + C(iso)"
m2 = smf.ols("F0_index ~ " + rhs, data=dd).fit(cov_type="cluster",
                                               cov_kwds={"groups": dd["DATE"].astype("int64")})
print(f"slope {m2.params['L1_sent1_best']:.4f}  (se {m2.bse['L1_sent1_best']:.4f})  n = {int(m2.nobs):,}")
```

**You should see:**
```
slope 0.0697  (se 0.0087)  n = 104,073
```

### Step 9 · Add dummies for extreme-return days

The do-file also includes `F0_d_returns_h` and `F0_d_returns_l`, which are dummies for days with extreme returns. They are **not in the package**. We rebuild them using the only "large move" definition the package gives: `5_figure_1.do` flags returns more than 3 country standard deviations from the country mean.

```python
by_country = dd.groupby("iso")["F0_index"].agg(["mean", "std"])      # one row per country
dd = dd.merge(by_country, left_on="iso", right_index=True)          # adds columns mean, std
dd["big_up"] = (dd["F0_index"] > dd["mean"] + 3 * dd["std"]).astype(int)
dd["big_down"] = (dd["F0_index"] < dd["mean"] - 3 * dd["std"]).astype(int)
m3 = smf.ols("F0_index ~ " + rhs + " + big_up + big_down", data=dd).fit(
    cov_type="cluster", cov_kwds={"groups": dd["DATE"].astype("int64")})
print(f"slope {m3.params['L1_sent1_best']:.4f}  (se {m3.bse['L1_sent1_best']:.4f})"
      f"  big_up {m3.params['big_up']:.2f}  big_down {m3.params['big_down']:.2f}")
print("days flagged:", dd["big_up"].sum(), "up,", dd["big_down"].sum(), "down")
```

**You should see:**
```
slope 0.0491  (se 0.0068)  big_up 8.35  big_down -6.98
days flagged: 804 up, 820 down
```

### Step 10 · Compare with the published number

```python
print(pd.DataFrame({
    "slope on L1 sentiment": [m1.params["L1_sent1_best"], m2.params["L1_sent1_best"],
                              m3.params["L1_sent1_best"], 0.049],
    "n": [int(m1.nobs), int(m2.nobs), int(m3.nobs), 102665]},
    index=["(7) simple", "(8) + FE and lags", "(9) + extreme-day dummies", "paper, Fig. 2B h=0"]).round(3))
```

**You should see:**
```
                           slope on L1 sentiment       n
(7) simple                                 0.074  138913
(8) + FE and lags                          0.070  104073
(9) + extreme-day dummies                  0.049  104073
paper, Fig. 2B h=0                         0.049  102665
```

## Compare with the paper

- **The simple regression (0.074) does not match the paper's number, and was not expected to.** It is a different regression. It shares the sign and order of magnitude, and a positive, highly significant slope of a few hundredths of a percentage point per sd.
- **Adding the controls the package ships (0.070)** barely moves it. The lags of returns, volume, volatility and the VIX are not what separates us from 0.049.
- **Adding the extreme-day dummies** brings the slope to **0.049 (s.e. 0.0068)**, against the package's **0.049 (0.007)**. That match is partly luck and should not be oversold:
  - Our dummy coefficients (8.35 and −6.98) are not the paper's (12.607 and −11.024), so our dummies are **not** the authors' variable.
  - The slope depends on the cut-off we chose. With the same code, a 2-sd cut-off gives 0.043, 2.5 sd gives 0.047, 3.5 sd gives 0.053 and 4 sd gives 0.055.
  - What is robust: most of the gap between 0.07 and 0.05 comes from controlling for a few hundred extreme days. This is Step 5's kurtosis showing up in the regression.
- **Remaining differences:**
  - Sample size: 104,073 rows against 102,665. The authors also control for eight lags of commodity returns (S&P GSCI) and world equity returns (Dow Jones World). Both are proprietary and commented out of the do-file, and their missing values plausibly account for the 1,408 rows we keep that the authors do not. I have not verified this, because the series are not in the package.
  - Standard errors: the authors use Driscoll–Kraay errors (`xtscc`), which are not taught in the course. We cluster by date instead. This changes the standard error but not the coefficient.

## What this does not license

- **No causal claim.** The slope says that returns are higher on days after good news, holding the listed controls fixed. It does not say news *causes* the move. The same economic event can drive both the news and prices, and a one-day lag does not rule that out.
- **No trading rule.** 0.05 percentage points a day, with an R² of about 0.001, is far below the day-to-day noise (return sd ≈ 1.9 pp). It is also before transaction costs.
- **No claim that our 3-sd dummies are the authors' dummies.** Step 9 matches the headline number but not the dummy coefficients. Report it as an approximation, not a replication of their exact specification.

## Pitfalls

- **File names in the readme.** The sentiment file is `news_sentiment.csv`, not `.tab`. The readme also points to `./indicator/`, but the file is in `public/data/`.
- **Calendar days, not trading days.** The panel has weekend rows. `L1_sent1_best` is the previous *calendar* day, so Monday's regressor is Sunday's news, but `L1_returns` is the previous *trading* day's return. Don't rebuild lags yourself with a one-row shift, or you will mix these up.
- **Mean 0 and sd 1 are not findings.** The index is z-scored within country on all calendar days. Reporting "mean ≈ 0, sd = 1" as a profile is the `describe()`-and-move-on error the practice warns against. Profile the median, the tails and the shape.
- **The thresholds are tiny at n = 172,690** (0.012 and 0.024). Every variable "fails", so report the size of $g_1$ and $g_2$, not only the verdict.
- **Extreme returns** (China 21 May 1992: +105%; Turkey 1991: +77% / −39%) dominate the return kurtosis. Clip the histogram's range, or the plot is one spike.
- **Missing columns.** `AE`, `F*_d_returns_h/l`, `commo` and `R_DJ_global` are referenced in the do-files but absent from `regression_sample.dta`. `pd.read_stata(..., columns=[...])` raises a `ValueError` naming them if you ask for them.
- **Clustering on dates:** statsmodels wants numbers for `groups`, hence `dd["DATE"].astype("int64")`.
- **Figures** are saved in `07-replication-workshop/02-practice/output/`, which git ignores.
- Runtime is about 2–3 seconds end to end.
