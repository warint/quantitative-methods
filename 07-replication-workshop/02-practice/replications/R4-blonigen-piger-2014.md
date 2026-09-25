# Replication 4 · Session 05 · Blonigen & Piger (2014)

> **Reuses:** regularisation (session 05) · **Time:** about 30 minutes ·
> **Script:** [`starter/r4_blonigen_piger_2014.py`](../starter/r4_blonigen_piger_2014.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r4_blonigen_piger_2014.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## Citation

Blonigen, B. A. & Piger, J. (2014). Determinants of foreign direct investment. *Canadian Journal of
Economics*, 47(3), 775–812. https://doi.org/10.1111/caje.12091 · free preprint: NBER working paper
w16704, https://www.nber.org/papers/w16704

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

## The published target

The paper's table 3 gives the inclusion probabilities. The course names the log-levels survivors
(inclusion probability of 85% or more) in the session 05 pre-session deck
(`05-ridge-lasso-elastic-net/00-pre-session/MATH60033A-S05-Pre-Session.qmd`, "What the paper found").
It lists nine by name. They are the target used here:

| Group | Variables |
|---|---|
| Gravity | `parent_gdp`, `host_gdp`, `distance` |
| Cultural distance | `common_language_official`, `colonial_link` |
| Trade agreements | `regional_trade_agreement`, `customs_union` |
| Income and endowments | `parent_gdp_pc`, `host_skill` |

The paper says "about sixteen" survive, and `scripts/build_fdi_determinants.py` repeats that count, but
the course material names only these nine. Check the other survivors against table 3 in the paper
before claiming a full 16-variable comparison. The deck also names what did **not** survive: host
business costs, communications infrastructure, financial depth and institutions. The practice deck
adds that `host_is_tax_haven` had an inclusion probability of 4%.

## Data

- **Source:** `qmib.load("fdi")`, which reads `data/spine/fdi_determinants.parquet`. It was rebuilt by
  `scripts/build_fdi_determinants.py` from OECD bilateral FDI positions (BMD4, outward), the CEPII
  Gravity database, the World Development Indicators and Freedom House. The authors published no
  replication package. The year is **2019**, where the paper used 2000. Data dictionary:
  `data/spine/dictionaries/S05-fdi.md`.
- **Unit of observation:** a directed parent × host country pair (what country A holds in country B).
- **Outcome:** `np.log(fdi_stock_musd)`, the log of the outward FDI position in US$ millions.
- **The 56 candidates, in the paper's groups:** gravity (3) · other GDP terms (8) · geography other
  than distance (4) · relative labour endowments (8) · other relative endowments (7) · cultural
  distance (3) · multilateral openness (4) · bilateral trade openness (3) · host business costs (4,
  substituted) · host tax policy (2) · bilateral agreements (2, substituted: `both_wto`, `both_eu`) ·
  host communications (3) · host financial infrastructure (2) · politics and institutions (3). Six
  variables are substitutes for the paper's own, and the dictionary marks them.
- **Rows after cleaning:** there are 7,051 pairs. 3,427 have a positive position, and **765** of those
  are complete on all 56 candidates. That leaves 36 parents and only **32 hosts**. The 70/30 split
  gives 535 training rows and 230 test rows.

## Steps

The whole script takes about 1.5 seconds.

### Step 1 · Load the data and keep the log-levels sample

**What and why.** Taking the log of the outcome drops every zero position, and requiring all 56
covariates drops most of what is left. Both are sample-selection choices you make before any
penalty is applied, so count the rows at each stage.

```python
fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=cov)   # log drops zeros; listwise deletion on the 56
print("all pairs:", len(fdi), "| positive FDI:", (fdi.fdi_stock_musd > 0).sum(), "| complete sample:", len(d))
print("candidates:", len(cov), "| parents:", d.parent.nunique(), "| hosts:", d.host.nunique())
```

**You should see:** `all pairs: 7051 | positive FDI: 3427 | complete sample: 765` and
`candidates: 56 | parents: 36 | hosts: 32`.

### Step 2 · Outcome and design

**What and why.** The outcome is log FDI, as in the course material. The paper's preferred
specification is in log levels, so the gravity trio (the two GDPs and distance) also goes in logs.
In raw US$ they are so skewed that a handful of giant economies dominate the fit. The step also
checks for a constant column, which carries no information and which the scaler will quietly turn
into zeros.

```python
y = np.log(d.fdi_stock_musd)
X = d[cov].copy()
for v in ["parent_gdp", "host_gdp", "distance"]:
    X[v] = np.log(X[v])
print("log FDI: mean", round(y.mean(), 2), "sd", round(y.std(), 2))
print("constant columns:", [c for c in cov if X[c].nunique() == 1])
```

**You should see:** `log FDI: mean 5.95 sd 3.09` and `constant columns: ['both_wto']`. Every pair in
the complete sample is a WTO pair.

### Step 3 · Write down the published target

**What and why.** Write down the list you are testing against before you fit anything, so the
comparison cannot drift towards whatever the lasso happens to keep.

```python
paper = ["parent_gdp", "host_gdp", "distance",                  # gravity
         "common_language_official", "colonial_link",           # cultural distance
         "regional_trade_agreement", "customs_union",           # trade agreements
         "parent_gdp_pc", "host_skill"]                         # income and endowments
print("paper keeps (as named by the course):", len(paper))
```

**You should see:** `paper keeps (as named by the course): 9`.

### Step 4 · Hold out a test set

**What and why.** The test set is used only to score the models. Cross-validation, which chooses
λ, runs entirely inside the training set. Using the test set to choose λ would make its RMSE an
optimistic estimate rather than an honest one.

```python
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
print("train:", len(Xtr), "| test:", len(Xte))
```

**You should see:** `train: 535 | test: 230`.

### Step 5 · OLS vs ridge vs lasso vs elastic net

**What and why.** This is the session's core comparison. A penalty on β_j depends on the units of
x_j, so every model standardises **inside** the pipeline. The scaler then learns its means and
standard deviations from the training folds only. Ridge shrinks every coefficient, the lasso sets
some exactly to zero, and the elastic net mixes the two penalties. Predicting the training mean is
the floor every model must beat.

```python
models = {
    "OLS":         make_pipeline(StandardScaler(), LinearRegression()),
    "ridge (CV)":  make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 60))),
    "lasso (CV)":  make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0, max_iter=50_000)),
    "elastic net": make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, 1],
                                                                cv=5, random_state=0, max_iter=50_000)),
}
print("predict the mean   test RMSE", round(np.sqrt(mean_squared_error(yte, np.full(len(yte), ytr.mean()))), 3))
for name, m in models.items():
    m.fit(Xtr, ytr)
    print(f"{name:18s} test RMSE", round(np.sqrt(mean_squared_error(yte, m.predict(Xte))), 3))
```

**You should see:** test RMSE of **3.081** for predicting the mean, **1.753** for OLS, **1.749** for
ridge, **1.737** for the lasso and **1.737** for the elastic net. The penalty improves prediction by
only about 1%. With 535 rows and 56 predictors, OLS is not badly overfitted, so the value of the
lasso here is in selection, not in forecasting.

### Step 6 · Choose λ by cross-validation, and the one-standard-error λ

**What and why.** λ_min is the value with the lowest 5-fold CV error. λ_1se is the largest λ whose
CV error is within one standard error of that minimum: the most parsimonious model that is
statistically indistinguishable from the best one. The session teaches both, and for selection
λ_1se is the more honest choice.

```python
print("ridge alpha_:", round(models["ridge (CV)"][-1].alpha_, 3))
print("elastic net alpha_:", round(models["elastic net"][-1].alpha_, 4), "l1_ratio_:", models["elastic net"][-1].l1_ratio_)
lcv = models["lasso (CV)"][-1]
mse = lcv.mse_path_.mean(axis=1)                   # CV error at each lambda, averaged over 5 folds
se = lcv.mse_path_.std(axis=1) / np.sqrt(5)        # its standard error
lam_min = lcv.alpha_
lam_1se = lcv.alphas_[mse <= mse.min() + se[mse.argmin()]].max()   # largest lambda within 1 SE
print("lasso lambda_min:", round(lam_min, 4), "| lambda_1se:", round(lam_1se, 4))
```

**You should see:** `ridge alpha_: 9.249`, `elastic net alpha_: 0.012 l1_ratio_: 1.0` and
`lasso lambda_min: 0.012 | lambda_1se: 0.0738`. The elastic net chose `l1_ratio = 1`, which **is**
the lasso, so the two rows in step 5 are identical.

### Step 7 · What the lasso keeps

**What and why.** This is the lasso's selection property. Count the non-zero coefficients at both
λs, and rank the survivors by the size of their standardised coefficient.

```python
keep_min = [v for v, b in zip(cov, lcv.coef_) if b != 0]
las1 = make_pipeline(StandardScaler(), Lasso(alpha=lam_1se, max_iter=50_000)).fit(Xtr, ytr)
coef = pd.Series(las1[-1].coef_, index=cov)
keep_1se = list(coef[coef != 0].index)
print("kept at lambda_min:", len(keep_min), "of 56 | kept at lambda_1se:", len(keep_1se), "of 56")
print("lambda_1se test RMSE:", round(np.sqrt(mean_squared_error(yte, las1.predict(Xte))), 3))
print(coef[coef != 0].abs().sort_values(ascending=False).round(3).head(12))
```

**You should see:** `kept at lambda_min: 48 of 56 | kept at lambda_1se: 30 of 56`, and a
`lambda_1se test RMSE: 1.817`, which is what parsimony costs. The largest standardised coefficients
are parent_gdp 1.781, host_gdp 1.198, distance 0.783, parent_gdp_pc 0.580, host_is_tax_haven 0.572,
parent_education 0.534, host_openness 0.395, common_language_official 0.393, parent_urban 0.325,
gdp_similarity 0.275, host_urban 0.261 and customs_union 0.206.

### Step 8 · Compare with the paper

**What and why.** This measures the overlap with the published list, checks the signs, and counts
what the lasso keeps beyond it.

```python
overlap = [v for v in paper if v in keep_1se]
print("paper's survivors kept by lasso (1se):", len(overlap), "of", len(paper))
print("paper's survivors dropped:", [v for v in paper if v not in keep_1se])
print("kept by lasso but not on the paper's list:", len(keep_1se) - len(overlap))
print("signs on the paper's list:", coef[paper].round(3).to_dict())
```

**You should see:** `9 of 9`, dropped `[]`, and `21` kept beyond the list. The signs are parent_gdp
+1.781, host_gdp +1.198, distance −0.783, common_language_official +0.393, colonial_link +0.106,
regional_trade_agreement +0.059, customs_union +0.206, parent_gdp_pc +0.580 and host_skill +0.071.
Every sign is the expected one: bigger economies and shared language raise FDI, and distance lowers it.

### Step 9 · Stability: how often does each variable survive?

**What and why.** A single lasso selection is one draw. Refit at λ_1se on 20 random half-samples of
the training set and record how often each coefficient is non-zero. A variable that survives
only some of the time is not a finding. (Half-samples drawn without replacement are used instead of
the bootstrap because duplicated rows make the lasso keep too many variables.)

```python
rng = np.random.default_rng(60033)
hits = pd.Series(0.0, index=cov)
for b in range(20):
    k = rng.choice(len(Xtr), size=len(Xtr) // 2, replace=False)
    m = make_pipeline(StandardScaler(), Lasso(alpha=lam_1se, max_iter=50_000)).fit(Xtr.iloc[k], ytr.iloc[k])
    hits += (m[-1].coef_ != 0)
freq = (hits / 20).sort_values(ascending=False)
print("paper's list, share of resamples kept:", freq[paper].to_dict())
print("variables kept in >= 80% of resamples:", (freq >= 0.8).sum(), "| never kept:", (freq == 0).sum())
print("the >= 80% group:", list(freq[freq >= 0.8].index))
print("never kept:", list(freq[freq == 0].index))
```

**You should see:** the paper's list survives in parent_gdp 1.0, host_gdp 1.0, distance 1.0,
common_language_official 1.0, parent_gdp_pc 1.0, colonial_link 0.85, regional_trade_agreement 0.7,
customs_union 0.7 and host_skill 0.65 of the resamples. **17** variables survive in at least 80%
of them: parent_gdp, gdp_similarity, common_language_official, parent_education, host_is_tax_haven,
parent_urban, both_eu, parent_gdp_pc, distance, host_gdp, host_urban, host_land, host_openness,
colonial_link, host_new_business_density, timezone_diff and parent_openness. **6** are never kept:
host_hitech_exports, both_wto, gdp_sum, host_logistics, host_capital_per_worker and
host_civil_liberties.

### Step 10 · Picture the stability check

**What and why.** A bar for each variable shows its survival share, with the paper's survivors in
the darker colour. It shows at a glance whether the paper's list sits at the top.

```python
top = freq[freq > 0]
colours = ["#1f4e79" if v in paper else "#9db4cc" for v in top.index]
fig, ax = plt.subplots(figsize=(7, 9))
ax.barh(top.index[::-1], top.values[::-1], color=colours[::-1])
ax.axvline(0.8, color="grey", ls=":", lw=1)
ax.set_xlabel("share of 20 half-samples in which the lasso keeps the variable")
ax.set_title("Lasso survival at lambda_1se\n(dark = the paper's survivors)")
plt.tight_layout()
plt.savefig(OUTPUT / "s05_stability.png", dpi=150)
```

**You should see:** `s05_stability.png` with 50 bars. Six of the nine dark bars are at or above the
0.8 line. The two trade-agreement dummies and host_skill sit just below it, between 0.65 and 0.70.

## Compare with the paper

- **What holds.** All nine survivors the course names are kept at λ_1se (9 of 9), each with the
  expected sign. The gravity block, parent income per capita and shared official language are kept
  in every one of the 20 resamples, and colonial links in 85%. Two decades later, the core of
  the paper's list still holds.
- **What weakens.** Regional trade agreement (0.70), customs union (0.70) and host skill (0.65) are
  kept but are not stable. Their coefficients are small (+0.059, +0.206, +0.071 standardised).
- **What the lasso adds.** It keeps 30 variables, not nine, and 17 survive in 80% or more of the
  resamples. Among the stable extras, `host_is_tax_haven` stands out: it is kept every time, with the
  fifth-largest coefficient (+0.572). The paper gave it an inclusion probability of 4%. Pass-through
  investment through offshore centres grew a great deal between 2000 and 2019.
- **What still fails.** Host institutions stay near zero, as in the paper: political rights are kept
  in 5% of resamples and civil liberties never. Logistics and high-tech exports are never kept either.
- **The method is not the paper's.** The lasso picks one good predictive model, while BMA averages
  over all of them. The two need not agree, especially among correlated variables.

## What this does not license

- **No causal claim.** A variable the lasso keeps predicts FDI in this sample. It does not show that
  changing it would attract FDI. Host institutions dropping out does not mean institutions do not
  matter.
- **No claim about all countries.** Only 36 OECD parents and 32 hosts survive listwise deletion. The
  results are conditional on an OECD investor and a data-rich host, not on the world.
- **No inference from the selected coefficients.** Refitting OLS on the lasso's survivors and reading
  its t-statistics reuses the data that did the selecting. Those p-values are too small.

## Pitfalls

- **Scaling outside the pipeline.** If you fit `StandardScaler` on all 765 rows before the split,
  test-set information leaks into training. Keep it inside `make_pipeline`.
- **Only 32 hosts.** Twenty-five of the 56 candidates are host characteristics (`host_*`), and in this sample
  each takes just 32 distinct values. Together they can act like host dummies, which is one reason
  the lasso keeps so many (host_urban, host_land, host_openness...). Selection among them is fragile.
- **Collinearity.** `parent_gdp` and `gdp_sum` correlate at 0.98. The lasso keeps one of the pair
  (parent_gdp) and never keeps the other. That does not show gdp_sum is irrelevant, only that it
  duplicates parent_gdp.
- **`both_wto` is constant** in the complete sample. It can never be selected, so "never kept" tells
  you nothing about it.
- **λ_min vs λ_1se.** At λ_min the lasso keeps 48 of 56, which is hardly any selection. Always say
  which λ your list comes from.
- **Elastic net = lasso here.** `l1_ratio_` came out at 1.0, so there is no separate elastic net
  result to report.
- **The bootstrap overselects.** Resampling with replacement duplicates rows, and when λ is re-chosen by CV on each bootstrap sample it pushes about
  half of the 56 to 90% or more (in 50 bootstrap draws checked while building this exercise). Use half-samples with λ fixed, as done here.
- **Importing `qmib`.** The starter script moves to the repository root itself, so `import qmib`
  works whether you press Run in VS Codium or type `python` in a terminal. If you copy the steps into
  a file of your own elsewhere, copy the four lines at the top that do that as well.
- **The target list is partial.** The course names nine of the paper's "about sixteen" survivors.
  Check table 3 of the paper for the rest before you say "the lasso recovers the paper's list".
