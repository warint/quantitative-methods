# Paper 4 · Session 06 · Topalova & Khandelwal (2011)

> **Reuses:** OLS (session 03) · ridge, lasso, elastic net (session 05) · **Time:** about 30 minutes ·
> **Script:** [`starter/r4_topalova_khandelwal_2011.py`](../starter/r4_topalova_khandelwal_2011.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

## How to work through it

Open `r4_topalova_khandelwal_2011.py` in VS Codium. Each step below is one block of the script,
marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read the
output, and check it against **You should see** before moving on.

The code is **the course's own**, line for line: the OLS cells of the session 03 lecture and the
ridge, lasso and elastic-net cells of session 05. Only the data and the variable names change.
You are not reproducing the paper — you are plugging its data into the models you know.

Topalova, P. & Khandelwal, A. (2011). Trade liberalization and firm productivity: the case of India.
*Review of Economics and Statistics* 93(3), 995–1009. https://doi.org/10.1162/REST_a_00095

## The data

- **File:** `06-advanced-regression/data/replication/prod_dataregression.dta` (the authors'
  replication package, Harvard Dataverse doi:10.7910/DVN/8WEXYD).
- **One row:** one Indian manufacturing firm in one year. We keep 1989–1996: **14,648 firm-years,
  3,077 firms**.
- **Outcome:** `tfp1000`, the firm's log total factor productivity (mean 0.051, sd 0.303).
- **Candidates:** `lagtariff` (last year's tariff on the firm's output; 0.65 = 65%), `laginputariff`
  (on its inputs), ownership dummies `prgroup`, `govown`, `foreign`, size dummies `medium`, `small`,
  `age` and its square `age2`, and seven year dummies (1989 is the base).

## The models, and where the code comes from

| Steps | Model | Copied from |
|---|---|---|
| 2–5 | OLS: productivity on the output tariff, then on both tariffs; the residual plot | session 03 lecture: *Three lines of Python*, *How much did the line explain?*, *Two predictors*, *The residual plot is the instrument* |
| 6–10 | Ridge, lasso, elastic net on 16 candidates, then the four models on held-out rows | session 05 lecture: *The Python: four ways to choose*; the `test_rmse` cell as reviewed in session 06 |

## Steps

### Step 1 · Load the firms

```python
firms = pd.read_stata("06-advanced-regression/data/replication/prod_dataregression.dta")
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age"]
d = firms[firms["yr"] < 1997].dropna(subset=cols)
```

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

The session 03 cell, with `fit = model2`. The figure is saved as `output/s06_resid_vs_fitted.png`.

**You should see:** a cloud centred on zero, with long tails on both sides (productivity runs from
−4.2 to 3.6) — a few firms far more or far less productive than any tariff level predicts.

### Step 6 · The candidates

Year dummies and the square of age are built as columns, so the penalised models can use them.

**You should see:** `16 candidates: ['lagtariff', 'laginputariff', 'prgroup', 'govown', 'foreign',
'medium', 'small', 'age', 'age2', 'yr_1990', …, 'yr_1996']`.

### Step 7 · Ridge

**You should see:** `λ = 47.64` and `ridge kept 16 of 16 — it never drops a predictor`.

### Step 8 · Lasso

**You should see:** `λ = 0.0003` and `lasso kept 16 of 16`.

### Step 9 · Elastic net

**You should see:** `λ = 0.0006` and `elastic net kept 16 of 16`.

### Step 10 · The four, on rows they never saw

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
- **Steps 7–10:** cross-validation picks a penalty close to zero, the lasso and the elastic net drop
  nothing, and all four models predict new firm-years equally well (RMSE 0.296). With **14,648 rows
  for 16 candidates**, OLS does not overfit, so a penalty has nothing to fix. Regularisation pays
  when candidates are many and rows are few — session 05's FDI data, not this one.

## What this does not license

- **No causal claim.** The slopes compare different firms in different years; firms in industries
  whose tariffs fell more may differ in other ways.
- **No "every variable matters".** The lasso keeping all 16 says only that, with this much data,
  none hurts prediction — not that each one affects productivity.
- **No claim beyond these firms:** listed manufacturing firms that survived, 1989–1996.

## Pitfalls

- **Units.** Tariffs are fractions (0.65 = 65%): multiply a slope by 0.1 to read a 10-point change.
- **`read_stata` keeps Stata's types.** `companyname` arrives as text; that is fine here.
- **Year dummies.** `drop_first=True` leaves 1989 as the base; keeping all eight beside an intercept
  would make OLS perfectly collinear.
- **The figure** has 14,648 points; the long tails are real data, not a plotting error.
