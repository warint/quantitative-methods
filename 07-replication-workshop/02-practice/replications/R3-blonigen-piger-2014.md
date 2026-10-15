# Paper 3 · Session 05 · Blonigen & Piger (2014)

> **Reuses:** OLS (session 03) · ridge, lasso, elastic net (session 05) · **Time:** about 30 minutes ·
> **Script:** [`starter/r3_blonigen_piger_2014.py`](../starter/r3_blonigen_piger_2014.py)

## How to work through it

Run it in **your own session-07 folder**, set up in Part 0 of the [practice README](../README.md) — not in the course repository. Open `r3_blonigen_piger_2014.py` in VS Codium. Each step below is one block of the script, marked
`# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read the output, and
check it against **You should see** before moving on. If a number differs, stop and find out why.

## The data

Blonigen, B. A. & Piger, J. (2014). Determinants of foreign direct investment. *Canadian Journal of
Economics* 47(3), 775–812. https://doi.org/10.1111/caje.12091

- **Source:** [`paper3_blonigen_piger_2014.csv`](https://warint.github.io/quantitative-methods/data/session-07/paper3_blonigen_piger_2014.csv), on the course site. Rebuilt by the course from the sources the paper names (OECD
  bilateral FDI positions, CEPII gravity, World Development Indicators, Freedom House), for **2019**
  — the paper used 2000. Every number is real.
- **One row:** one parent → host country pair.
- **Outcome:** `log_fdi`, the log of the FDI stock the parent country holds in the host.
- **Candidates:** 56 variables — market sizes (`parent_gdp`, `host_gdp`, in logs), `distance` (in
  logs), cultural ties (`common_language_official`, `colonial_link`), trade agreements, taxes,
  institutions, skills, infrastructure.
- **Rows used:** 765 pairs with positive FDI and all 56 candidates present.

We do not follow the paper. We take its data and fit the models of the course on it.

## The models, and where the code comes from

| Steps | Model | The code is copied from |
|---|---|---|
| 2–4 | OLS: one predictor, then two | session 03, *Three lines of Python*, *How much did the line explain?*, *Two predictors* |
| 5–7 | ridge, lasso, elastic net on all 56 | session 05, *The Python: four ways to choose* |
| 8 | the four models scored on held-out pairs | session 06, *Session 5 · Too many predictors* |

Only the data and the variable names change.

## Steps

### Step 1 · Load the data

Keep pairs with positive FDI (the log of zero does not exist) and all 56 candidates present, and put
the outcome and the gravity variables in logs.

```python
fdi = pd.read_csv(DATA + "paper3_blonigen_piger_2014.csv")
YCOL = "log_fdi"
XCOLS = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=XCOLS).copy()
d["log_fdi"] = np.log(d["fdi_stock_musd"])
for v in ["parent_gdp", "host_gdp", "distance"]:
    d[v] = np.log(d[v])
print(f"country pairs: {len(d)}   candidate predictors: {len(XCOLS)}")
```

`DATA`, set at the top of the script, is the address of the course site's data folder: `https://warint.github.io/quantitative-methods/data/session-07/`.

**You should see:** `country pairs: 765   candidate predictors: 56`.

### Step 2 · OLS: three lines of Python

```python
model = smf.ols("log_fdi ~ host_gdp", data=d).fit()
print(model.params)
```

**You should see:** intercept −3.254, `host_gdp` **0.474**. Both are in logs, so the slope is an
elasticity: a host economy **1% larger** holds about **0.47% more** FDI from a given partner.

### Step 3 · How much did the line explain?

```python
print(f"R-squared = {model.rsquared:.3f}")
```

**You should see:** `R-squared = 0.051`. Host size alone accounts for 5% of the variation: who the
investor is matters at least as much as where it invests.

### Step 4 · Two predictors: what "controlling for" means

```python
model2 = smf.ols("log_fdi ~ host_gdp + distance", data=d).fit()
print(model2.params)
print(f"R-squared = {model2.rsquared:.3f}")
```

**You should see:** `host_gdp` **0.512**, `distance` **−0.455**, R² 0.078. Comparing pairs **at the
same distance**, a 1% larger host goes with 0.51% more FDI; and comparing pairs with hosts of the
same size, a partner 1% farther away holds 0.46% less.

### Step 5 · Ridge

The session 5 code: standardise, then let cross-validation choose λ (`alpha` in scikit-learn).

```python
from sklearn.linear_model import RidgeCV

Xc, yc = d[XCOLS].astype(float), d[YCOL].astype(float)
ridge = make_pipeline(StandardScaler(),
                      RidgeCV(alphas=np.logspace(-3, 3, 60))
                      ).fit(Xc, yc)
print(f"λ = {ridge[-1].alpha_:.2f}")
print(f"ridge kept {np.sum(ridge[-1].coef_ != 0)} of {len(XCOLS)} — it never drops a predictor")
```

**You should see:** `λ = 9.25` and `ridge kept 56 of 56`.

### Step 6 · Lasso

```python
from sklearn.linear_model import LassoCV

lasso = make_pipeline(StandardScaler(),
                      LassoCV(cv=5, random_state=0, max_iter=50_000)
                      ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, lasso[-1].coef_) if b != 0]
print(f"λ = {lasso[-1].alpha_:.4f}")
print(f"lasso kept {len(kept)} of {len(XCOLS)}")
```

**You should see:** `λ = 0.0312` and `lasso kept 34 of 56`. Print `kept` to see which.

### Step 7 · Elastic net

```python
from sklearn.linear_model import ElasticNetCV

enet = make_pipeline(StandardScaler(),
                     ElasticNetCV(l1_ratio=0.5, cv=5, random_state=0, max_iter=50_000)
                     ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, enet[-1].coef_) if b != 0]
print(f"λ = {enet[-1].alpha_:.4f}")
print(f"elastic net kept {len(kept)} of {len(XCOLS)}")
```

**You should see:** `λ = 0.0270` and `elastic net kept 46 of 56` — more than the lasso, because its
ridge part keeps correlated candidates together.

### Step 8 · Which one predicts best?

The session 6 review code: fit each model on 70% of the pairs, score it on the other 30%.

```python
Xtr, Xte, ytr, yte = train_test_split(d[XCOLS], d[YCOL], test_size=0.3, random_state=7)

def test_rmse(model):
    pipe = make_pipeline(StandardScaler(), model).fit(Xtr, ytr)
    kept = int(np.sum(np.abs(pipe[-1].coef_) > 1e-8))
    return kept, mean_squared_error(yte, pipe.predict(Xte)) ** 0.5

results = {...}   # OLS, ridge, lasso, elastic net — as in the script
res = pd.DataFrame(results, index=["predictors kept", "test RMSE"]).T.astype({"predictors kept": int})
print(res.round(3))
```

**You should see:**

| | predictors kept | test RMSE |
|---|---|---|
| OLS, all predictors | 55 | 1.631 |
| ridge | 55 | 1.606 |
| lasso | 43 | 1.596 |
| elastic net | 47 | 1.595 |

## Interpretation

- **OLS:** bigger hosts and closer partners hold more FDI. In logs, the slopes read as elasticities:
  about 0.5% more FDI per 1% more host GDP, about 0.5% less per 1% more distance.
- **The penalties:** ridge keeps every candidate; the lasso keeps 34 of the 56 and the elastic net
  46 — the elastic net lets groups of correlated candidates in together.
- **On new pairs**, the penalised models predict a little better than OLS with all 56 (test error
  1.60 against 1.63). With 765 pairs for 56 candidates, OLS is not badly overfitted, so the gain is
  small — the penalty earns most when the table is nearly square.

## What this does not license

- **No causal claim.** A variable the lasso keeps predicts FDI in this sample. It does not show that
  changing it would attract FDI.
- **No "no effect".** A candidate set to zero was not needed for prediction once the others were in;
  among correlated candidates the lasso keeps one almost arbitrarily.
- **No p-values after selection.** Refitting OLS on the kept variables and reading its p-values reuses
  the data that did the selecting.
- **No claim about all countries.** Requiring all 56 candidates leaves 765 pairs, mostly between
  data-rich OECD countries.

## Pitfalls

- **Positive FDI only.** The log of zero or a negative stock does not exist, so those pairs drop out.
- **"Kept 55 of 56" in step 8.** `both_wto` is the same for every pair (all are WTO members), so it
  carries no information and its coefficient is zero up to rounding, for every model. Step 5 counts
  it as kept because its test is `!= 0`; step 8 uses a tolerance of `1e-8`.
- **λ is `alpha`.** scikit-learn calls the penalty `alpha`; the elastic net's mix is `l1_ratio`.
- **Standardise inside the pipeline**, so the scaler never sees the held-out rows.
