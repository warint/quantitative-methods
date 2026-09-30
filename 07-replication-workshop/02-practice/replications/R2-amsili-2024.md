# Replication 2 · Session 03 · Amsili, van Es & Schindelbeck (2024)

> **Reuses:** regression diagnostics (session 03) · **Time:** about 30 minutes ·
> **Script:** [`starter/r2_amsili_2024.py`](../starter/r2_amsili_2024.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r2_amsili_2024.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## Citation

Amsili, J. P., van Es, H. M., & Schindelbeck, R. R. (2024). Pedotransfer functions for field
capacity, permanent wilting point, and available water capacity based on random forest models for
routine soil health analysis. *Communications in Soil Science and Plant Analysis*.
https://doi.org/10.1080/00103624.2024.2336573. Replication package: Harvard Dataverse,
doi:10.7910/DVN/U5DAEP.

## The paper in brief

Measuring how much water a soil can hold is slow and expensive, so soil labs would rather predict
it from cheap measurements they already take. The authors use 7,232 soil samples from the Cornell
Soil Health Laboratory to build three predictive models ("pedotransfer functions") for field
capacity, permanent wilting point and available water capacity: a full random forest, a reduced
random forest, and a multiple linear regression (MLR) on sand, clay and soil organic matter. The
full random forest predicts best. But the linear regression does about as well as the reduced
random forest, which uses the same inputs.

## The research question

Can cheap, routinely measured soil properties predict a soil's water-holding capacity well enough
to replace direct measurement, and does a random forest do better than a linear regression?

## The published target

Field capacity (θFC, water held at −10 kPa, in g of water per g of soil), linear model, training
dataset:

- **Equation 6 (p. 8)**: θFC = 0.3477 − 0.313 sand + 0.040 clay + 1.855 SOM + 0.222 (sand×clay) +
  1.405 (sand×SOM) − 0.202 (clay×SOM), with every variable in g g⁻¹ (p. 7). The model is described
  on pp. 5–6: sand, clay, SOM and their three pairwise products, fitted with `lm` in R.
- **Fit (p. 8, Figure 2c)**: MLR adjusted R² = **0.79**, RMSE = **0.043**.
- **The benchmarks on the same page**: the full random forest explains 86.0% of variance with RMSE
  0.036, and the reduced random forest explains 80.9% with RMSE 0.042. (The random-forest figures
  are out-of-bag, so they are not computed the same way as the MLR's in-sample R².)
- The abstract's "16.3% lower RMSE than MLR" (p. 1, p. 8) is measured on the separate NAPESHM
  validation dataset, which is **not** in the replication package, so we do not try to match it.

## Data

- **File**: `03-regression-adequacy-and-validity/data/replication/2015-2019_CompleteAWC_w.1and15bar_dataset_toshare.xlsx`,
  sheet 2 (`2015-2019_CompleteAWC_w.1and15b`). Sheet 1, `metadata`, is empty.
- **Unit of observation**: one composite topsoil sample (0–15 cm) sent to the Cornell Soil Health
  Laboratory between 2015 and 2019, from across the continental US.
- **Key variables**: `FC_10kPa` is field capacity (g water per g soil). `sand`, `silt` and `clay`
  are texture in % (they sum to 100). `SOM` is soil organic matter in %. `PWP_1500kPa` is the
  wilting point (g/g), `AWC` is available water capacity (g/g), and `soil_texture_class` and
  `State` are labels. The file also has other lab measurements (WAS, Resp, POXC, K, Mg, Fe, Mn)
  that the linear model does not use.
- **Rows after cleaning**: 7,232. There are no missing values, and the paper's SOM ≤ 10% filter
  has already been applied, so no rows are dropped.

## Steps

### Step 1 · Load the data

Open the workbook, check its sheets and read the one that holds the data. Then confirm the sample
the paper describes: 7,232 rows, no gaps, and no soil above 10% SOM.

```python
sheets = pd.ExcelFile(DATA).sheet_names
print(sheets)
d = pd.read_excel(DATA, sheet_name=sheets[1])
print(d.shape)
print(d[["sand", "clay", "SOM", "FC_10kPa"]].describe().round(3))
print("missing values:", d.isna().sum().sum(), "| samples with SOM > 10%:", (d["SOM"] > 10).sum())
```

**You should see:** `['metadata', '2015-2019_CompleteAWC_w.1and15b']` and `(7232, 17)`. Mean sand
is 33.317 (%), clay 18.631, SOM 3.359 and FC_10kPa 0.336. Clay reaches 95.553 and SOM reaches
9.972. The last line reads `missing values: 0 | samples with SOM > 10%: 0`.

### Step 2 · Put the predictors in the paper's units

Equation 6 is written in g per g, but the file stores sand, clay and SOM in per cent. You only
get the paper's coefficients if you divide by 100. This is the session-03 habit of stating a slope
**in units**: the same model gives a coefficient 100 times smaller if you leave the predictors in %.

```python
for c in ["sand", "clay", "SOM"]:
    d[c + "_g"] = d[c] / 100
print(d[["sand_g", "clay_g", "SOM_g", "FC_10kPa"]].head(3).round(3))
```

**You should see:** the first row is `0.164  0.354  0.050  0.42`.

### Step 3 · Fit the paper's regression

This is an OLS fit with `smf.ols`, the multiple regression from session 03. The formula names each
product term explicitly with `:`, so the model has exactly the seven terms of Equation 6.

```python
formula = "FC_10kPa ~ sand_g + clay_g + SOM_g + sand_g:clay_g + sand_g:SOM_g + clay_g:SOM_g"
fit = smf.ols(formula, data=d).fit()
paper = pd.Series({"Intercept": 0.3477, "sand_g": -0.313, "clay_g": 0.040, "SOM_g": 1.855,
                   "sand_g:clay_g": 0.222, "sand_g:SOM_g": 1.405, "clay_g:SOM_g": -0.202})
print(pd.DataFrame({"ours": fit.params.round(4), "paper Eq. 6": paper}))
```

**You should see:** every coefficient matches Equation 6 to three decimals.

| term | ours | paper |
|---|---|---|
| Intercept | 0.3477 | 0.3477 |
| sand_g | −0.3127 | −0.313 |
| clay_g | 0.0403 | 0.040 |
| SOM_g | 1.8548 | 1.855 |
| sand_g:clay_g | 0.2221 | 0.222 |
| sand_g:SOM_g | 1.4045 | 1.405 |
| clay_g:SOM_g | −0.2023 | −0.202 |

### Step 4 · The fit statistics the paper reports

Compute adjusted R² and RMSE, where RMSE is the square root of the mean squared residual (the
paper's Equation 3, dividing by n). Here R² answers "how much of the variation does the model
account for", not "is the model right".

```python
rmse = np.sqrt(np.mean(fit.resid ** 2))
print(f"adj. R2 = {fit.rsquared_adj:.3f}  (paper: 0.79)")
print(f"RMSE    = {rmse:.4f} g/g  (paper MLR: 0.043; paper Full RF: 0.036)")
print(f"n = {int(fit.nobs)}, parameters p = {int(fit.df_model) + 1}")
```

**You should see:** `adj. R2 = 0.794`, `RMSE = 0.0433 g/g`, `n = 7232, parameters p = 7`.

### Step 5 · Residuals versus fitted

This is the first session-03 plot, and it asks whether a straight-line model (with products) has
the right shape. As a check, the step also prints the mean residual in each fifth of the fitted
values. If the model were missing a curve, these means would drift away from zero in a pattern.
The figure is saved as `s03_resid_vs_fitted.png`.

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(fit.fittedvalues, fit.resid, s=4, alpha=0.3)
ax.axhline(0, color="red", ls="--")
ax.set_xlabel("Fitted field capacity (g/g)"); ax.set_ylabel("Residual (g/g)")
plt.savefig(OUTPUT / "s03_resid_vs_fitted.png", dpi=110, bbox_inches="tight")
# Mean and spread of the residuals in five bands of fitted value (1 = lowest fifth)
band = np.digitize(fit.fittedvalues, fit.fittedvalues.quantile([0.2, 0.4, 0.6, 0.8])) + 1
print(fit.resid.groupby(band).agg(["mean", "std"]).round(4))
```

**You should see:** the band means are all within ±0.003 of zero (0.0018, 0.0005, −0.0025,
0.0013, −0.0011), so there is no systematic curve. The plot shows one cloud centred on zero, with
two stray points at about +0.35 and −0.28. The standard deviation climbs from 0.0402 in the lowest
band to 0.0480 in the highest.

### Step 6 · Scale–location, and whether robust errors change a verdict

The second session-03 plot asks whether the spread of the residuals is constant. The step then
re-estimates the standard errors with `cov_type="HC1"`, the remedy for non-constant spread, and
checks whether any coefficient's significance changes. The figure is saved as
`s03_scale_location.png`.

```python
infl = fit.get_influence()
std_resid = infl.resid_studentized_internal
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(fit.fittedvalues, np.sqrt(np.abs(std_resid)), s=4, alpha=0.3)
ax.set_xlabel("Fitted field capacity (g/g)"); ax.set_ylabel("sqrt(|standardised residual|)")
plt.savefig(OUTPUT / "s03_scale_location.png", dpi=110, bbox_inches="tight")
print("corr(fitted, sqrt|std resid|) =", round(np.corrcoef(fit.fittedvalues, np.sqrt(np.abs(std_resid)))[0, 1], 3))
robust = smf.ols(formula, data=d).fit(cov_type="HC1")
print(pd.DataFrame({"coef": fit.params, "SE classical": fit.bse, "SE HC1": robust.bse,
                    "p classical": fit.pvalues, "p HC1": robust.pvalues}).round(4))
```

**You should see:** `corr(fitted, sqrt|std resid|) = 0.08`, a weak upward drift in the spread. The
HC1 standard errors are roughly 1.3 to 2 times the classical ones. For example, SOM_g goes from
0.1615 to 0.2602, clay_g from 0.0269 to 0.0552, and clay_g:SOM_g from 0.5680 to 1.0891. The
verdicts do not change. Sand, SOM, sand×clay and sand×SOM stay at p < 0.0001. Clay (p 0.135 → 0.466)
and clay×SOM (p 0.722 → 0.853) were not significant before and are not significant now. The
diagonal cross-hatching in the plot comes from FC being recorded to two decimals (see Pitfalls).
It is not a finding.

### Step 7 · Leverage

Leverage (the hat values) depends only on the predictors. It measures how unusual a soil's
combination of sand, clay and SOM is. The step checks that the hat values sum to p, counts the
rows above the 2p/n convention, and lists the three most extreme.

```python
h = infl.hat_matrix_diag
p, n = int(fit.df_model) + 1, int(fit.nobs)
print(f"sum of h = {h.sum():.2f} (= p = {p}); 2p/n = {2*p/n:.5f}; above it: {(h > 2*p/n).sum()}")
print(d.loc[h > 2*p/n, "soil_texture_class"].value_counts().head(5))
print(d.iloc[np.argsort(h)[-3:]][["soil_texture_class", "sand", "clay", "SOM", "FC_10kPa"]].round(2))
```

**You should see:** `sum of h = 7.00 (= p = 7); 2p/n = 0.00194; above it: 743`. The high-leverage
rows are mostly at the edges of the texture triangle: Sand 152, Silty Clay 147, Sandy Loam 136,
Silt Loam 113, Sandy Clay Loam 45. The three highest-leverage soils are all "Clay", with 95.55%,
78.35% and 69.60% clay. The paper's own Table S1 (p. 20) lists only 36 clay soils in 7,232.

### Step 8 · Cook's distance

Cook's distance combines a residual with leverage: it measures how far the fitted values would move
if one row were deleted. Read the stem plot for its **shape**, and treat 4/n as a screen, not a
test. The figure is saved as `s03_cooks_distance.png`.

```python
cooks_d = infl.cooks_distance[0]
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.stem(cooks_d, markerfmt=",")
ax.axhline(4 / n, color="red", ls="--")
ax.set_xlabel("Observation"); ax.set_ylabel("Cook's distance")
plt.savefig(OUTPUT / "s03_cooks_distance.png", dpi=110, bbox_inches="tight")
print(f"largest Cook's D {cooks_d.max():.4f}; above 4/n ({4/n:.5f}): {(cooks_d > 4/n).sum()} rows")
```

**You should see:** `largest Cook's D 0.5619; above 4/n (0.00055): 394 rows`. In the plot, one
spike (near observation 6,000) is more than 20 times taller than any other. With n = 7,232, 4/n
flags hundreds of harmless rows, which is why the shape matters more than the count.

### Step 9 · Look at the tallest spike, then refit without it

The session-03 rule is to find out which row it is and go and look at it. Refitting without the
row is a **sensitivity check**. It tells you which conclusions depend on one soil sample. It is
not a licence to delete the row.

```python
i = cooks_d.argmax()
print(d.iloc[i][["State", "soil_texture_class", "sand", "clay", "SOM", "FC_10kPa", "PWP_1500kPa"]])
print(f"fitted {fit.fittedvalues.iloc[i]:.3f}, residual {fit.resid.iloc[i]:.3f}, std. residual {std_resid[i]:.2f}, leverage {h[i]:.4f}")
fit_drop1 = smf.ols(formula, data=d[cooks_d < cooks_d[i]]).fit()
print(pd.DataFrame({"all rows": fit.params, "without that one row": fit_drop1.params}).round(3))
print(f"p-value of clay_g:SOM_g: {fit.pvalues['clay_g:SOM_g']:.3f} -> {fit_drop1.pvalues['clay_g:SOM_g']:.3f}")
```

**You should see:** row 5986, a **Clay** soil from GA with 78.35% clay and 0.77% SOM, and a
measured FC of only **0.09**, with PWP 0.02. The model predicts 0.372, so the residual is −0.282,
the standardised residual −6.79 and the leverage 0.0786 (about 80 times the average p/n). This one
row is both badly predicted and far out, and the product of the two is what makes it influential.
Without it:

| term | all rows | without row 5986 |
|---|---|---|
| clay_g | 0.040 | 0.093 |
| SOM_g | 1.855 | 2.059 |
| sand_g:clay_g | 0.222 | 0.194 |
| sand_g:SOM_g | 1.405 | 1.265 |
| clay_g:SOM_g | −0.202 | **−1.203** |

`p-value of clay_g:SOM_g: 0.722 -> 0.040`. **One soil out of 7,232 turns the clay×SOM term from
"nothing" into "significant at 5%"**, and multiplies it by six. The sand, SOM and sand×SOM effects
keep their signs and roughly their size.

### Step 10 · AIC and BIC: are the three product terms worth it?

Compare the paper's model with a main-effects-only model, on the same rows and the same y, as
session 03 requires. Read the differences, not the levels. BIC charges ln(n) per parameter and AIC
charges 2.

```python
main = smf.ols("FC_10kPa ~ sand_g + clay_g + SOM_g", data=d).fit()
ic = pd.DataFrame({"k": [int(m.df_model) + 1 for m in (main, fit)],
                   "adj R2": [m.rsquared_adj for m in (main, fit)],
                   "RMSE": [np.sqrt(np.mean(m.resid ** 2)) for m in (main, fit)],
                   "AIC": [m.aic for m in (main, fit)], "BIC": [m.bic for m in (main, fit)]},
                  index=["main effects", "+ interactions (Eq. 6)"])
ic["dAIC"], ic["dBIC"] = ic.AIC - ic.AIC.min(), ic.BIC - ic.BIC.min()
print(ic.round(4).to_string())
```

**You should see:**

| model | k | adj R2 | RMSE | AIC | BIC | dAIC | dBIC |
|---|---|---|---|---|---|---|---|
| main effects | 4 | 0.7857 | 0.0441 | −24603.50 | −24575.95 | 267.58 | 246.92 |
| + interactions (Eq. 6) | 7 | 0.7936 | 0.0433 | −24871.08 | −24822.88 | 0 | 0 |

Both criteria prefer the paper's model by far more than 10 points, which is decisive. The two
Δs differ by 20.66, which is exactly 3 × (ln 7232 − 2), BIC's extra charge for three more
parameters. In accuracy terms, though, the product terms cut RMSE only from 0.0441 to 0.0433.

## Compare with the paper

- **The regression replicates exactly.** All seven coefficients of Equation 6 match to three
  decimals, and adjusted R² (0.794 vs 0.79) and RMSE (0.0433 vs 0.043) match what the paper reports
  on p. 8.
- **The linear model's RMSE sits between the paper's two random forests.** It is 0.0433, against
  0.042 for the reduced random forest (same inputs) and 0.036 for the full random forest (eleven
  inputs). This supports the paper's claim that, with only texture and SOM, "simple modeling
  approaches like MLR can be adequate" (p. 9). Most of the random forest's gain comes from the
  extra lab variables, not from the algorithm.
- **What the diagnostics add, which the paper does not report**: 
  - The residuals show no curvature, and the spread drifts up only slightly. HC1 errors are wider
    but change no verdict.
  - One implausible sample, a 78%-clay soil with FC = 0.09 (row 5986), carries the clay×SOM
    coefficient. With the row in, the term is −0.202 and insignificant (which is what the paper
    reports). Without it, the term is −1.203 with p = 0.040.
  - Sand, SOM and sand×SOM are the conclusions that survive every check.

## What this does not license

- **Not a causal statement.** "More SOM raises field capacity by 1.855 per g/g" describes a
  pattern across soils in a lab's customer base. It does not say what adding organic matter to a
  given field would do. The paper itself finds that AWC barely responds to management in trials
  shorter than about 15–30 years (pp. 14–15).
- **Not out-of-sample accuracy.** Every number here is in-sample, on the training data. The
  paper's comparison on the independent NAPESHM dataset, where RMSE rises and random forests beat
  MLR by 16.3%, cannot be checked with this package.
- **Not a reason to delete row 5986.** It may be a lab error, or a genuinely unusual soil. It is
  not a finding either way until someone checks the sample. The honest write-up reports both fits.

## Pitfalls

- **Two sheets.** `pd.read_excel(file)` with no `sheet_name` reads the first sheet, `metadata`,
  which is empty. You get an empty DataFrame and no error. Use `sheet_name=1` (or the sheet's name).
  The sheet name is truncated to `2015-2019_CompleteAWC_w.1and15b` (31-character Excel limit), so
  don't type it from the file name.
- **Units.** Texture and SOM are in %, and FC, PWP and AWC are in g/g. If you skip the ÷100, you
  get coefficients 100× (and products 10,000×) smaller than Equation 6, with identical R². The
  intercept alone will seem to match.
- **Column names**: it is `FC_10kPa` and `PWP_1500kPa` (with units in the name), not `FC`/`PWP`.
  The formula needs `:` for a product term alone. `sand_g*clay_g` means main effects plus the
  product, which gives the same model here but is easy to misread.
- **Rounded response.** 87.6% of the FC values sit exactly on a 0.01 grid (checked with
  `(d.FC_10kPa*100 - (d.FC_10kPa*100).round()).abs().lt(1e-9).mean()`). That is why the
  scale–location plot shows diagonal stripes.
- **AWC is not always exactly FC − PWP** in this file: `(d.AWC - (d.FC_10kPa - d.PWP_1500kPa)).abs().max()`
  returns 0.191. If you switch the exercise to AWC, model the `AWC` column as given, and don't
  rebuild it from the other two.
- **Figures** are saved in `07-replication-workshop/02-practice/output/`, which git ignores.
