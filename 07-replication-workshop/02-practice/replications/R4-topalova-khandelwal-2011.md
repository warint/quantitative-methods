# Paper 4 · Session 06 · Topalova & Khandelwal (2011)

> **Reuses:** OLS (session 03) · binary, ordinal and multinomial logits (session 04) · ridge, lasso, elastic net (session 05) · **Time:** about 35 minutes ·
> **Script:** [`starter/r4_topalova_khandelwal_2011.py`](../starter/r4_topalova_khandelwal_2011.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

## How to work through it

Run it in **your own session-07 folder**, set up in Part 0 of the [practice README](../README.md) — not in the course repository. Open `r4_topalova_khandelwal_2011.py` in VS Codium. Each step below is one block of the script,
marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read the
output, and check it against **You should see** before moving on.

The code is **the course's own**, line for line: the OLS cells of the session 03 lecture, the three
logits of session 04, and the ridge, lasso and elastic-net cells of session 05. Only the data and the variable names change.
You are not reproducing the paper — you are plugging its data into the models you know.

Topalova, P. & Khandelwal, A. (2011). Trade liberalization and firm productivity: the case of India.
*Review of Economics and Statistics* 93(3), 995–1009. https://doi.org/10.1162/REST_a_00095

## The data

- **File:** the authors' `prod_dataregression.dta` (Harvard Dataverse doi:10.7910/DVN/8WEXYD,
  CC0); the script reads the columns it uses from the course site,
  [`paper4_topalova_khandelwal_2011.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper4_topalova_khandelwal_2011.csv).
- **One row:** one Indian manufacturing firm in one year. We keep 1989–1996: **14,648 firm-years,
  3,077 firms**.
- **Outcome:** `tfp1000`, the firm's log total factor productivity (mean 0.051, sd 0.303).
- **Three outcomes made from it for the logits:** above the median or not (binary); productivity in
  thirds, low < middle < high (ordinal); and, from the ownership dummies, who owns the firm —
  stand-alone, business group, state-owned, foreign (multinomial, no order).
- **Candidates:** `lagtariff` (last year's tariff on the firm's output; 0.65 = 65%), `laginputariff`
  (on its inputs), ownership dummies `prgroup`, `govown`, `foreign`, size dummies `medium`, `small`,
  `age` and its square `age2`, and seven year dummies (1989 is the base).

## The models, and where the code comes from

| Steps | Model | Copied from |
|---|---|---|
| 2–5 | OLS: productivity on the output tariff, then on both tariffs; the residual plot | session 03 lecture: *Three lines of Python*, *How much did the line explain?*, *Two predictors*, *The residual plot is the instrument* |
| 6–8 | Binary logit: is the firm above the median? | session 04 lecture: *LR 6 · Log-odds*, *LR 7 · Odds*, *LR 8 · Predicted probability* |
| 9–11 | Ordinal logit: productivity in thirds | session 04 lecture: *OLR 3 · The code*, *OLR 4*, *OLR 5* |
| 12–14 | Multinomial logit: who owns the firm | session 04 lecture: *MLR 3 · The code*, *MLR 4*, *MLR 5* |
| 15–19 | Ridge, lasso, elastic net on 16 candidates, then the four models on held-out rows | session 05 lecture: *The Python: four ways to choose*; the `test_rmse` cell as reviewed in session 06 |

## Steps

### Step 1 · Load the firms

```python
firms = pd.read_csv(DATA + "paper4_topalova_khandelwal_2011.csv")
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age"]
d = firms[firms["yr"] < 1997].dropna(subset=cols)
```

`DATA`, set at the top of the script, is the address of the course site's data folder: `https://warint.github.io/quantitative-methods/data/session-07/`.

**You should see:** `14,648 firm-years, 3,077 firms`. The output tariff averages 0.695 (69.5%),
the input tariff 0.261.

### Step 2 · Three lines of Python: productivity on the output tariff

```python
model = smf.ols("tfp1000 ~ lagtariff", data=d).fit()
print(model.params)
```

**You should see:** `Intercept 0.108335`, `lagtariff -0.083159`.

### Step 3 · How much did the line explain?

```python
print(f"R-squared = {model.rsquared:.3f}")
```

**You should see:** `R-squared = 0.004`.

### Step 4 · Two predictors

```python
model2 = smf.ols("tfp1000 ~ lagtariff + laginputariff", data=d).fit()
```

**You should see:** `lagtariff -0.065720`, `laginputariff -0.075279`, `R-squared = 0.005`.

### Step 5 · Residuals versus fitted

The session 03 cell, with `fit = model2`. The figure opens in a window, and is saved as `p4_resid_vs_fitted.png` in your folder.

**You should see:** a cloud centred on zero, with long tails on both sides (productivity runs from
−4.2 to 3.6) — a few firms far more or far less productive than any tariff level predicts.

### Step 6 · Binary logit: log-odds

The session 04 *LR 6* cell. `high_tfp` is 1 when the firm-year is more productive than the median.

**You should see:** `Intercept 0.5052`, `lagtariff -0.7278` — a higher output tariff goes with a
lower chance of being above the median (the sign is readable directly).

### Step 7 · Binary logit: odds

The *LR 7* cell.

**You should see:** `0.483` — one unit of tariff (100 percentage points) multiplies the odds of
being above the median by 0.48. For a 10-point step: e^(0.1 × −0.728) ≈ 0.93, odds 7% lower.

### Step 8 · Binary logit: predicted probability

The *LR 8* cell, at output tariffs of 0.4, 0.7 and 1.0 (the data run from 0.1 to 3.5).

**You should see:** `0.553`, `0.499`, `0.445`.

### Step 9 · Ordinal logit

The *OLR 3* cell. `pd.qcut` cuts productivity into three equal-sized groups, kept in order.

**You should see:** in the summary, `lagtariff −0.5092`, `laginputariff −0.5095`, `age −0.0077`,
all with p < 0.05, and the two cutpoints `low/middle` and `middle/high`.

### Step 10 · Ordinal logit: log-odds and odds

The *OLR 4* cells.

**You should see:** proportional-odds ratios `0.601`, `0.601`, `0.992`.

### Step 11 · Ordinal logit: probabilities

The *OLR 5* cell: the same 20-year-old firm (input tariff 0.3) under an output tariff of 1.0 and 0.4.

**You should see:**

```
              low  middle   high
tariff 1.0  0.365   0.335  0.300
tariff 0.4  0.297   0.335  0.367
```

### Step 12 · Multinomial logit

The *MLR 3* cell. Ownership is built from the three dummies; stand-alone private firms are the
baseline, large firms the size reference.

**You should see:** three blocks of coefficients, one per owner type against stand-alone.

### Step 13 · Multinomial logit: log-odds and relative risk ratios

The *MLR 4* cell.

**You should see:** for `tfp1000`, RRR `0.697` (group), `0.209` (state), `1.318` (foreign); for
`small`, `0.025`, `0.013`, `0.022`.

### Step 14 · Multinomial logit: probabilities

The *MLR 5* cell: large firms, at the median productivity, then from −0.5 to 0.5.

**You should see:** P(business group) about 0.64–0.69 throughout; P(state-owned) falls from 0.236
to 0.076 and P(foreign) rises from 0.087 to 0.177 as productivity rises.

### Step 15 · The candidates

Year dummies and the square of age are built as columns, so the penalised models can use them.

**You should see:** `16 candidates: ['lagtariff', 'laginputariff', 'prgroup', 'govown', 'foreign',
'medium', 'small', 'age', 'age2', 'yr_1990', …, 'yr_1996']`.

### Step 16 · Ridge

**You should see:** `λ = 47.64` and `ridge kept 16 of 16 — it never drops a predictor`.

### Step 17 · Lasso

**You should see:** `λ = 0.0003` and `lasso kept 16 of 16`.

### Step 18 · Elastic net

**You should see:** `λ = 0.0006` and `elastic net kept 16 of 16`.

### Step 19 · The four, on rows they never saw

```text
                     predictors kept  test RMSE
OLS, all predictors               16      0.296
ridge                             16      0.296
lasso                             16      0.296
elastic net                       16      0.296
```

## Interpretation

- **Step 2:** a tariff 10 percentage points lower goes with productivity about **0.83% higher**
  (0.1 × 0.083 log points), comparing firm-years across the sample.
- **Step 4:** holding the input tariff fixed, the output-tariff slope falls to −0.066; a 10-point
  lower input tariff, holding the output tariff fixed, goes with productivity about 0.75% higher.
- **Steps 3–4:** tariffs account for **half a percent** of the variation in productivity. Firms
  differ for many reasons a tariff does not capture.
- **Steps 6–8 (binary):** each 10 points of output tariff lowers the odds of being an above-median
  firm by about 7%; moving the tariff from 1.0 to 0.4 raises that probability from 0.45 to 0.55.
- **Steps 9–11 (ordinal):** lower tariffs push firms **up** the productivity thirds — the chance of
  the top third rises from 0.30 to 0.37 — and older firms sit slightly lower.
- **Steps 12–14 (multinomial):** relative to stand-alone firms, small and medium firms are far less
  likely to belong to a group, the state or a foreign owner; among large firms, the more productive
  are more often foreign-owned and less often state-owned. Everything is *relative to stand-alone*.
- **Steps 16–19:** cross-validation picks a penalty close to zero, the lasso and the elastic net drop
  nothing, and all four models predict new firm-years equally well (RMSE 0.296). With **14,648 rows
  for 16 candidates**, OLS does not overfit, so a penalty has nothing to fix. Regularisation pays
  when candidates are many and rows are few — session 05's FDI data, not this one.

## What this does not license

- **No causal claim.** The slopes compare different firms in different years; firms in industries
  whose tariffs fell more may differ in other ways. The ownership model describes who owns which
  firms — it does not say that productivity attracts or repels an owner.
- **No "every variable matters".** The lasso keeping all 16 says only that, with this much data,
  none hurts prediction — not that each one affects productivity.
- **No claim beyond these firms:** listed manufacturing firms that survived, 1989–1996.

## Pitfalls

- **Units.** Tariffs are fractions (0.65 = 65%): multiply a slope by 0.1 to read a 10-point change.
- **`read_stata` keeps Stata's types.** `companyname` arrives as text; that is fine here.
- **Year dummies.** `drop_first=True` leaves 1989 as the base; keeping all eight beside an intercept
  would make OLS perfectly collinear.
- **The figure** has 14,648 points; the long tails are real data, not a plotting error.
