# Paper 2 · Session 03 · Amsili, van Es & Schindelbeck (2024)

> **Reuses:** the regression and its checks (session 03), a squared term (session 06) · **Time:**
> about 30 minutes · **Script:** [`starter/r2_amsili_2024.py`](../starter/r2_amsili_2024.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r2_amsili_2024.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. The goal is not to land on the
paper's number. It is to fit the simple model you know, read it in units, check it, and then say in
words how it differs from what the authors did.

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
random forest, and a multiple linear regression on sand, clay and soil organic matter with their
pairwise products. The full random forest predicts best (86% of variance explained), but the linear
regression (adjusted R² 0.79) does about as well as the reduced random forest.

## The research question

Can cheap, routinely measured soil properties predict a soil's water-holding capacity well enough
to replace direct measurement, and does a random forest do better than a linear regression?

## Data

- **File**: `03-regression-adequacy-and-validity/data/replication/2015-2019_CompleteAWC_w.1and15bar_dataset_toshare.xlsx`,
  **sheet 2**. Sheet 1, `metadata`, is empty.
- **Unit of observation**: one topsoil sample (0–15 cm) sent to the Cornell Soil Health Laboratory
  between 2015 and 2019, from across the continental US. 7,232 rows, no missing values, organic
  matter already capped at 10%.
- **The four variables we use**: `FC_10kPa`, field capacity — the water a soil holds after
  draining, in **g of water per g of soil**; `sand` and `clay`, texture in **%**; `SOM`, soil
  organic matter in **%**.

## The simple model, and why

The session-03 regression, with nothing added:

$$\text{FC} = \beta_0 + \beta_1\,\text{sand} + \beta_2\,\text{clay} + \beta_3\,\text{SOM} + \varepsilon$$

We keep the predictors in **per cent**, as the lab records them, so every slope reads "g of water
per g of soil, per percentage point". We leave out the paper's three product terms on purpose: the
question is how far the simplest model goes. Then we check it the way session 03 taught — residuals,
then Cook's distance — and try one session-06 transformation, a squared term for organic matter.

## Steps

### Step 1 · Load the data, and describe the four variables

Read the second sheet (`sheet_name=1`: Python counts from 0) and look at centre and spread before
fitting anything.

```python
d = pd.read_excel(DATA, sheet_name=1)
print(d.shape)
print(d[["FC_10kPa", "sand", "clay", "SOM"]].describe().loc[["mean", "50%", "std", "min", "max"]].round(3))
```

**You should see:** `(7232, 17)`. Field capacity averages 0.336 g/g (median 0.350, sd 0.095, from
0.02 to 0.68). Sand averages 33.3% (median 28.5%) and clay 18.6% (median 18.0%, but up to 95.6%);
SOM averages 3.36% (from 0.08 to 9.97). Sand's mean sits well above its median: a right tail of very
sandy soils.

### Step 2 · The simple regression

```python
fit = smf.ols("FC_10kPa ~ sand + clay + SOM", data=d).fit()
print(fit.params.round(5))
```

**You should see:**

| term | coefficient |
|---|---|
| Intercept | 0.32720 |
| sand | −0.00251 |
| clay | 0.00062 |
| SOM | 0.02421 |

### Step 3 · How much does it explain?

```python
print(f"R2 = {fit.rsquared:.3f}   adj. R2 = {fit.rsquared_adj:.3f}   n = {int(fit.nobs)}")
```

**You should see:** `R2 = 0.786   adj. R2 = 0.786   n = 7232`. With three predictors and 7,232
rows, the adjustment changes nothing at three decimals.

### Step 4 · Residuals versus fitted

The first session-03 plot: if a straight line is the right shape, the residuals scatter around zero
with no pattern.

```python
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.scatter(fit.fittedvalues, fit.resid, s=4, alpha=0.3)
ax.axhline(0, color="red", ls="--")
ax.set_xlabel("Fitted field capacity (g/g)"); ax.set_ylabel("Residual (g/g)")
plt.savefig(OUTPUT / "s03_resid_vs_fitted.png", dpi=110, bbox_inches="tight")
plt.show()
```

**You should see:** a cloud centred on zero with no clear curve. The diagonal stripes come from the
outcome itself: most field-capacity values are recorded to 0.01 g/g. A handful of points sit far
below the line — soils that hold much less water than their texture predicts.

### Step 5 · Cook's distance: which soil moves the answer most?

```python
cooks_d = fit.get_influence().cooks_distance[0]
i = cooks_d.argmax()
print(f"largest Cook's D = {cooks_d[i]:.3f} (row {i}); next largest = {np.sort(cooks_d)[-2]:.3f}")
print(d.iloc[i][["State", "soil_texture_class", "sand", "clay", "SOM", "FC_10kPa"]])
print(f"fitted {fit.fittedvalues.iloc[i]:.3f}, observed {d.FC_10kPa.iloc[i]:.3f}")
```

**You should see:** the largest Cook's distance is **0.105, row 5986**, four times the next (0.025).
It is a Georgia soil classed **Clay**: 78% clay, 16% sand, 0.8% organic matter, with a field
capacity of **0.09** — where the model predicts **0.355**. A clay soil that holds almost no water is
either a very unusual soil or a lab error; only someone who checks the sample can say which.

### Step 6 · Refit without that one soil

A sensitivity check, not a deletion: fit again without row 5986 and compare.

```python
fit_drop = smf.ols("FC_10kPa ~ sand + clay + SOM", data=d.drop(index=d.index[i])).fit()
print(pd.DataFrame({"all soils": fit.params, "without that soil": fit_drop.params}).round(5))
```

**You should see:** almost nothing moves — sand −0.00251 → −0.00250, clay 0.00062 → 0.00066, SOM
0.02421 → 0.02410. In the simple model no single soil decides the answer. (In the paper's model with
product terms, the same soil flips the clay×SOM term: more terms, more ways for one row to matter.)

### Step 7 · A squared term for organic matter

Session 06: if the effect of organic matter weakens as there is more of it, a squared term will pick
that up.

```python
fit_sq = smf.ols("FC_10kPa ~ sand + clay + SOM + I(SOM**2)", data=d).fit()
print(fit_sq.params.round(5))
print(f"adj. R2 {fit.rsquared_adj:.4f} -> {fit_sq.rsquared_adj:.4f};  AIC {fit.aic:.0f} -> {fit_sq.aic:.0f}")
print(f"p-value of SOM squared: {fit_sq.pvalues['I(SOM ** 2)']:.4f}")
```

**You should see:** SOM 0.02890 and SOM² **−0.00057**; adjusted R² **0.7857 → 0.7860**; AIC
**−24603 → −24612**; p-value of the squared term **0.0014**. The curvature is real (negative: each
extra point of organic matter adds a little less) but tiny: the effect of one more point of SOM falls
from about 0.027 g/g at 2% to about 0.020 g/g at 8%, and the fit barely improves.

### Step 8 · Our simple models next to the paper's

```python
compare = pd.DataFrame({"explains (adj. R2 or % variance)": [fit.rsquared_adj, fit_sq.rsquared_adj, 0.79, 0.86]},
                       index=["ours: sand + clay + SOM", "ours: + SOM squared",
                              "paper: + three pairwise products", "paper: full random forest"])
print(compare.round(3))
```

**You should see:** 0.786, 0.786, 0.790 and 0.860. Three plain slopes get within 0.004 of the paper's
seven-term regression. Only the random forest, using many more lab measurements, does clearly better.

## Interpretation

- **Organic matter:** comparing two soils with the same sand and clay, one percentage point more
  organic matter goes with **0.024 g of water per g of soil** more field capacity — about a quarter of
  a standard deviation.
- **Sand:** ten percentage points more sand, holding clay and organic matter fixed, goes with
  **0.025 g/g less** field capacity: sandy soils drain.
- **Clay:** once sand and organic matter are held fixed, clay adds little — **0.006 g/g** per ten
  points. Sand and clay move together (more of one is less of the other and of silt), so "holding
  sand fixed" changes what the clay slope means.
- **Fit:** the three predictors account for **79%** of the variation in field capacity. That is a
  statement about prediction across these soils, not about what causes water retention.

## How it differs from the paper

- **The model.** The paper adds the three pairwise products (sand×clay, sand×SOM, clay×SOM) and
  writes the predictors in g per g, not per cent; we keep the three main effects only. The products
  buy very little: 0.786 against 0.79.
- **The method the paper prefers** is a random forest, which the course does not teach. It explains
  86% of the variance, and it uses many more lab measurements than our three.
- **The scoring.** The paper's random-forest figures are *out-of-bag* (scored on samples each tree
  did not see); our R² is in-sample. The paper's headline comparison — the random forest's error
  16.3% lower — uses a separate validation dataset that is not in the package.

## What this does not license

- **No causal claim.** "One more point of organic matter goes with 0.024 g/g more water" describes a
  pattern across one lab's soils. It does not say what adding organic matter to a given field would
  do — the paper itself finds that water capacity barely responds to management in trials shorter
  than about 15–30 years.
- **No out-of-sample claim.** Every number here is in-sample, on the data the model was fitted to.
- **No claim beyond the sampled soils.** These are topsoils sent to one US lab, with organic matter
  capped at 10%. A pedotransfer function is trusted only inside the range of soils it was fitted on.
- **Row 5986 is not to be deleted.** It is to be checked. Report the fit with and without it.

## Pitfalls

- **Two sheets.** `pd.read_excel(file)` with no `sheet_name` reads the first sheet, `metadata`, which
  is empty: you get an empty DataFrame and no error. Use `sheet_name=1`.
- **Units.** Texture and SOM are in %, field capacity in g/g. A slope is therefore "g/g per
  percentage point" — small numbers, so read them per ten points when that is clearer.
- **Column names**: `FC_10kPa`, with the units in the name, not `FC`.
- **The squared term needs `I()`**: `SOM**2` without it is read by the formula language as an
  interaction of SOM with itself, which is just SOM.
- **Rounded response.** Most field-capacity values sit on a 0.01 grid, which is why the residual plot
  shows diagonal stripes. It is not a modelling problem.
- **Figures** are saved in `07-replication-workshop/02-practice/output/`, which git ignores.
