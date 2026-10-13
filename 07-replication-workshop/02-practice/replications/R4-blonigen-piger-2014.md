# Paper 4 · Session 05 · Blonigen & Piger (2014)

> **Reuses:** ridge, lasso and elastic net (session 05) · **Time:** about 30 minutes ·
> **Script:** [`starter/r4_blonigen_piger_2014.py`](../starter/r4_blonigen_piger_2014.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r4_blonigen_piger_2014.py` in VS Codium. Each step below is one
block of the script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only
those, read the output, and check it against **You should see** before moving on. The code is the
code you typed in session 05; only the data are new.

## Citation

Blonigen, B. A., & Piger, J. (2014). Determinants of foreign direct investment. *Canadian Journal of
Economics*, 47(3), 775–812. https://doi.org/10.1111/caje.12091. Free preprint: NBER working paper
16704, https://www.nber.org/papers/w16704.

## The paper in brief

Empirical FDI studies disagree about which variables belong in the regression, and each study picks
its own short list. Blonigen and Piger collect 56 candidate determinants of bilateral FDI for 2000 and
use Bayesian model averaging, which weights every combination of them, to give each variable an
inclusion probability. About sixteen variables come out with high inclusion probability: gravity,
cultural distance, parent income, some trade agreements and host skill. Many variables that earlier
papers leaned on (host business costs, infrastructure, financial depth, institutions) turn out not to
be robust.

## The research question

Of 56 candidate determinants of bilateral FDI, which few actually carry the signal?

## Data

- **Source:** `qmib.load("fdi")` — no download. The course rebuilt the paper's design from OECD
  bilateral FDI positions, the CEPII Gravity database, the World Development Indicators and Freedom
  House; the authors published no package. The year is **2019**, where the paper used **2000**.
  Data dictionary: `data/spine/dictionaries/S05-fdi.md`.
- **Unit of observation:** a directed parent × host country pair (what country A holds in country B).
- **Outcome:** the log of the FDI stock, in US$ millions. Pairs with no positive position drop out,
  because the log of zero does not exist.
- **Rows:** 7,051 pairs; 765 have a positive position and are complete on all 56 candidates —
  36 parents and only 32 hosts. The 70/30 split gives 535 training rows and 230 test rows.

## The simple models, and why

The paper's question — many candidates, which matter? — is session 05's question. So you run
session 05's four models on the 56 candidates, each standardised **inside** a pipeline:

| Model | What it does | What to read |
|---|---|---|
| **OLS** | uses all 56, no penalty | the benchmark test error |
| **Ridge** | shrinks every coefficient, keeps all | test error, the λ chosen |
| **Lasso** | shrinks and sets the weak ones to exactly zero | how many kept, which dropped |
| **Elastic net** | half lasso, half ridge (`l1_ratio = 0.5`) | how many kept, which dropped |

In scikit-learn, λ is called `alpha`; cross-validation (5 folds) chooses it. Nothing here
replicates the paper's Bayesian model averaging — it asks the same question with the course's tools.

## Steps

### Step 1 · Load the data: log FDI, 56 candidates, complete cases only

Keep the pairs with a positive FDI stock and no missing candidate, take the log of FDI, and put the
three gravity variables (the two GDPs and distance) in logs as the paper does.

```python
fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=cov)
y = np.log(d.fdi_stock_musd)
X = d[cov].copy()
for v in ["parent_gdp", "host_gdp", "distance"]:
    X[v] = np.log(X[v])
```

**You should see:** `country pairs: 765 | candidate predictors: 56 | rows per predictor: 13.7`.
Thirteen rows per candidate is not many: exactly the setting where a penalty can help.

### Step 2 · Hold out 30% of the pairs

The test set is touched only to score the four models. `rmse(m)` is the test error of a fitted
model, in log points of FDI.

**You should see:** `train: 535 | test: 230`.

### Step 3 · Benchmark: OLS with all 56 candidates

**You should see:** `OLS: predictors kept 56 | test RMSE 1.753`. As a yardstick, predicting the
mean for every pair gives about 3.08: the 56 candidates explain a great deal.

### Step 4 · Ridge

`RidgeCV` tries 60 values of λ and keeps the one with the lowest cross-validated error.

**You should see:** `ridge: lambda 9.25 | kept 56 | test RMSE 1.749`. Ridge never drops a
variable; it buys a slightly lower error by shrinking all 56.

### Step 5 · Lasso

**You should see:** `lasso: lambda 0.012 | kept 48 of 56 | test RMSE 1.737`, and the eight dropped:
`host_gdp_pc, gdp_sum, timezone_diff, parent_capital_per_worker, both_wto, host_domestic_credit,
host_political_rights, host_civil_liberties`.

### Step 6 · Elastic net

Fixed at half lasso, half ridge (`l1_ratio = 0.5`), so that it differs from the lasso. (Left free to
choose the mix by cross-validation, it picks 1.0 — the lasso itself.)

**You should see:** `elastic net: lambda 0.0182 | kept 51 of 56 | test RMSE 1.739`, dropping
`host_gdp_pc, gdp_sum, both_wto, host_political_rights, host_civil_liberties`. Its ridge part keeps
three that the lasso dropped.

### Step 7 · The four models side by side

**You should see:**

```
             predictors kept  test RMSE
OLS                       56      1.753
ridge                     56      1.749
lasso                     48      1.737
elastic net               51      1.739
```

and the figure `output/s05_test_rmse.png`.

### Step 8 · Compare with the paper's robust determinants

The paper's nine survivors that the course names (inclusion probability of 85% or more): parent and
host GDP, distance, common official language, colonial link, regional trade agreement, customs
union, parent GDP per head, host skill.

**You should see:** `paper's nine kept by the lasso: 9 | by the elastic net: 9`, with the expected
signs — parent GDP 2.15, host GDP 1.56, distance −1.07, the others small and positive — and the six
largest lasso coefficients `parent_gdp, host_gdp, distance, host_is_tax_haven, parent_gdp_pc,
host_openness`.

## Interpretation

- **The penalty barely changes the test error.** From 1.753 (OLS) to 1.737 (lasso): about 1%. With
  535 training rows for 56 candidates, OLS is not badly overfitted; regularisation earns its keep
  when there are fewer rows per predictor.
- **The lasso selects only a little.** It keeps 48 of 56 at the λ cross-validation prefers. A
  "short list" needs a larger λ — the course's λ_1se — and the list then depends on that choice.
- **The gravity core agrees with the paper.** All nine of the paper's named survivors are kept, by
  both the lasso and the elastic net, with the expected signs: bigger economies and closer pairs hold
  more FDI.
- **The institutions variables drop out** (political rights, civil liberties), as in the paper.
- **A tax-haven dummy is among the largest coefficients** — a variable the paper did not find robust.
  Pass-through FDI via offshore centres grew a great deal between 2000 and 2019.

## How it differs from the paper

- **Method:** the paper averages over very many models (Bayesian model averaging) and reports an
  inclusion probability for each variable; here one penalised model is fitted at one λ and keeps or
  drops each variable.
- **Score:** the paper asks which variables are robust; the course's models are judged on their
  error on pairs they never saw.
- **Data:** 2019, not 2000, rebuilt from public sources, with six substituted variables and only
  32 host countries after listwise deletion.

## What this does not license

- **No causal claim.** A variable the lasso keeps predicts FDI in this sample. It does not show that
  changing it would attract FDI.
- **No "institutions do not matter".** A dropped variable is not a zero effect: it may be correlated
  with one that was kept.
- **No claim about all countries.** Only 36 OECD parents and 32 hosts survive listwise deletion. The
  results hold for an OECD investor and a data-rich host, not for the world.
- **No inference from the selected coefficients.** Refitting OLS on the lasso's survivors and reading
  its p-values reuses the data that did the selecting.

## Pitfalls

- **Scaling outside the pipeline.** If you fit `StandardScaler` on all 765 rows before the split,
  test-set information leaks into training. Keep it inside `make_pipeline`.
- **Only 32 hosts.** Many candidates are host characteristics (`host_*`), and here each takes just 32
  distinct values. Together they act almost like host dummies, which is one reason the lasso keeps so
  many. Selection among them is fragile.
- **Collinearity.** `parent_gdp` and `gdp_sum` correlate at 0.98. The lasso and the elastic net keep
  parent_gdp and drop gdp_sum: that shows gdp_sum duplicates parent_gdp, not that it is irrelevant.
- **`both_wto` is constant** in the complete sample, so it can never be kept. "Dropped" tells you
  nothing about it.
- **Say which λ.** At the λ with the lowest CV error the lasso keeps 48; at a larger λ it would keep
  fewer. A list of survivors without its λ is not a result.
- **The target list is partial.** The course names nine of the paper's "about sixteen" survivors.
  Check table 3 of the paper before you say the lasso recovers the paper's list.
