# Replication 5 · Session 06 · Topalova & Khandelwal (2011)

> **Reuses:** panel data (session 06) · **Time:** about 30 minutes ·
> **Script:** [`starter/r5_topalova_khandelwal_2011.py`](../starter/r5_topalova_khandelwal_2011.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r5_topalova_khandelwal_2011.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## Citation

Topalova, Petia, and Amit Khandelwal. 2011. "Trade Liberalization and Firm Productivity: The Case of India." *Review of Economics and Statistics* 93 (3): 995–1009. https://doi.org/10.1162/REST_a_00095. Replication package: Harvard Dataverse, https://doi.org/10.7910/DVN/8WEXYD (`06-advanced-regression/data/replication/`).

## The paper in brief

In 1991 India cut its import tariffs sharply and quickly, because the IMF made that a condition of a bailout, and not because some industries asked for it. The authors follow about 3,000 listed manufacturing firms (Prowess database) and ask whether firms in industries whose tariffs fell more became more productive. They separate two channels: lower tariffs on a firm's *output* (more import competition) and lower tariffs on its *inputs* (cheaper and better imported intermediates). Both raise productivity, and the input channel is the larger of the two.

## The research question

Within the same firm over time, does a fall in output tariffs or in input tariffs raise total factor productivity?

## The published target

- **Table 5, column 3** ("Output and Input Tariffs on Total Factor Productivity"), published version, p. 1003. Firm fixed effects and year fixed effects, standard errors clustered **by firm**, N = 14,648.
  - Lagged output tariff: **−0.032**\* [0.017]
  - Lagged input tariff: **−0.480**\*\*\* [0.098]
- Column 1 of the same table (pooled OLS, year dummies, firm-clustered): output tariff −0.011 [0.022], input tariff 0.060 [0.075].
- Where: the published article, Table 5, p. 1003 — use the DOI above. The text on p. 1004 reads column 3 as: "a 10 percentage point decline in output tariffs leads to a .32% increase in productivity. A similar decline in input tariffs increases productivity by 4.8%."
- Specification in `Tables_restat.do`:
  - line 41: `global cov2 "prgroup govown foreign medium small age age2"`
  - line 281: `keep if yr<1997`
  - line 285: column 1, `reg tfp1000 lagtariff laginputariff $cov2 i.yr, robust cluster(companyname)`
  - line 291: column 3, `areg tfp1000 lagtariff laginputariff $cov2 i.yr, absorb(companyname) cluster(companyname)`
- Note that the do-file and the table note both cluster by **firm** (`companyname`), not by industry.

## Data

- **File:** `06-advanced-regression/data/replication/prod_dataregression.dta`: 32,422 rows, 63 columns, 1989–2002.
- **Unit of observation:** one firm in one year.
- **Key variables:**
  - `tfp1000`: log total factor productivity of the firm (estimated by the authors with Levinsohn–Petrin; the outcome)
  - `lagtariff`: last year's nominal tariff on the firm's industry's output (0.65 = 65%)
  - `laginputariff`: last year's input tariff, a weighted average of the tariffs on the industry's inputs, with input-output weights
  - `prgroup`, `govown`, `foreign`: ownership dummies (private business group, state owned, foreign); private stand-alone is the base
  - `medium`, `small`: size-class dummies; large is the base
  - `age`, `age2`: firm age and its square
  - `id` / `companyname`: firm identifier (one-to-one); `industrycode`: industry (a string); `yr`: year
- **After cleaning** (years before 1997, rows with a missing regressor dropped): **14,648 rows, 3,077 firms, 117 industries, 8 years (1989–1996)**. The panel is unbalanced: 800 firms are observed all 8 years and 293 only once.

## Steps

The whole script takes about 1.5 seconds.

### Step 1 · Load the firm-year panel and look at it

*What and why.* A panel is many entities observed over many periods, so the first thing to check is what one row is and how the entity and time columns are stored.

```python
firms = pd.read_stata("06-advanced-regression/data/replication/prod_dataregression.dta")
print(firms.shape)
print(firms[["companyname", "industrycode", "yr", "tfp1000",
             "lagtariff", "laginputariff"]].head())
print(firms[["id", "industrycode", "yr"]].dtypes)
```

**You should see:** `(32422, 63)`. The first rows belong to "20 Microns Ltd.", industry 2692, in 1997–2001 (for 1997, `tfp1000` 0.1855 and `lagtariff` 0.4667). The dtypes are `id int16`, `industrycode str`, `yr int16`.

### Step 2 · Keep the paper's sample

*What and why.* The paper studies the years before 1997, the period of the externally imposed reform (do-file line 281). Stata drops any row with a missing regressor without saying so. We drop them on purpose, so we know what the sample is.

```python
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age", "age2"]
sample = firms[firms["yr"] < 1997].dropna(subset=cols)
print(sample.shape)
print(sample["id"].nunique(), "firms")
print(sample["yr"].value_counts().sort_index())
```

**You should see:** `(14648, 63)` and `3077 firms`. Observations per year rise from 921 (1989) to 2,907 (1996): 921, 1101, 1389, 1547, 1811, 2277, 2695, 2907. N = 14,648 matches the paper exactly.

### Step 3 · See the reform: average tariffs by year

*What and why.* A panel model can only use the variation that is in the data. The tariffs fell over time, and by different amounts in different industries. With firm and year effects, the industry-by-industry differences in those cuts are what identify the slope.

```python
by_year = sample.groupby("yr")[["lagtariff", "laginputariff"]].mean()
print(by_year.round(3))
by_year.plot(marker="o")
plt.ylabel("average lagged tariff (1 = 100%)")
plt.title("India's tariff cuts, estimation sample")
plt.savefig(OUTPUT / "tariffs_by_year.png", dpi=150, bbox_inches="tight")
```

**You should see:**

| year | 1989 | 1990 | 1991 | 1992 | 1993 | 1994 | 1995 | 1996 |
|---|---|---|---|---|---|---|---|---|
| output tariff | 0.973 | 0.949 | 0.812 | 0.858 | 0.596 | 0.795 | 0.585 | 0.452 |
| input tariff | 0.367 | 0.357 | 0.304 | 0.306 | 0.224 | 0.309 | 0.218 | 0.174 |

The figure is saved as `tariffs_by_year.png`. These are averages over the firms in the sample, so the bump in 1994 partly reflects which firms enter the data that year. They are not the paper's Table 1 industry averages.

### Step 4 · Pooled OLS with year dummies, classical standard errors

*What and why.* This is the baseline that ignores the panel structure: every firm-year is treated as an independent draw, and the firm characteristics are included as dummies. `C(yr)` adds one dummy per year.

```python
formula = ("tfp1000 ~ lagtariff + laginputariff + prgroup + govown + foreign"
           " + medium + small + age + age2 + C(yr)")
pooled = smf.ols(formula, data=sample).fit()
print(pooled.params[["lagtariff", "laginputariff"]].round(4))
print(pooled.bse[["lagtariff", "laginputariff"]].round(4))
```

**You should see:** coefficients −0.0110 (output tariff) and 0.0601 (input tariff), with classical SEs 0.0156 and 0.0392.

### Step 5 · The same pooled OLS, standard errors clustered by firm

*What and why.* Clustered standard errors. A firm appears up to eight times, and its errors are correlated across those years. Clustering leaves the coefficients unchanged and corrects the standard errors. This is the paper's column 1.

```python
pooled_cl = smf.ols(formula, data=sample).fit(
    cov_type="cluster", cov_kwds={"groups": sample["id"]})
print(pooled_cl.params[["lagtariff", "laginputariff"]].round(4))
print(pooled_cl.bse[["lagtariff", "laginputariff"]].round(4))
```

**You should see:** the same −0.0110 and 0.0601, with SEs 0.0223 and 0.0748. The input-tariff SE is almost twice the classical one. This matches the published column 1 exactly (−0.011 [0.022], 0.060 [0.075]).

### Step 6 · Give the data a panel index

*What and why.* `linearmodels` finds the entity and the time period in a two-level index, entity first and time second, as in class (`set_index(["country", "year"])`).

```python
panel = sample.set_index(["id", "yr"])
y = panel["tfp1000"]
X = panel[["lagtariff", "laginputariff", "age", "age2"]]
print(panel.index.names, panel.shape)
```

**You should see:** `['id', 'yr'] (14648, 61)`. Two columns have moved into the index.

### Step 7 · Firm and year fixed effects, clustered by firm (column 3)

*What and why.* Two-way fixed effects. Entity effects remove everything about a firm that never changes, such as its management quality or location, and time effects remove anything common to all firms in a year, such as the 1991 crisis. The ownership and size dummies never change within a firm (checked: one value per firm), so the firm effects absorb them and they are left out of `X`, just as Stata's `areg` drops them.

```python
fe = PanelOLS(y, X, entity_effects=True, time_effects=True).fit(
    cov_type="clustered", cluster_entity=True)
print(fe)
```

**You should see:** 14,648 observations and 3,077 entities. Output tariff **−0.0317 (SE 0.0169, p = 0.061)** and input tariff **−0.4795 (SE 0.0980, p < 0.001)**. Age is 0.0149 (0.0090) and age² is −5.36e-05 (2.70e-05). The F-test for poolability is 14.549 on (3083, 11560) df, p = 0.0000. This is Table 5, column 3.

### Step 8 · Random effects

*What and why.* Random effects keeps the time-invariant firm characteristics, but it assumes the firm effect is uncorrelated with the regressors. `RandomEffects` has no `time_effects` switch, so we use the year dummies already in the file (`yeardum2`–`yeardum8`, with 1989 as the base).

```python
years = ["yeardum2", "yeardum3", "yeardum4", "yeardum5",
         "yeardum6", "yeardum7", "yeardum8"]
X_re = sm.add_constant(panel[cols[1:] + years])
re = RandomEffects(y, X_re).fit(cov_type="clustered", cluster_entity=True)
print(re.params[["lagtariff", "laginputariff"]].round(4))
print(re.std_errors[["lagtariff", "laginputariff"]].round(4))
```

**You should see:** output tariff −0.0344 (SE 0.0145) and input tariff −0.3074 (SE 0.0655).

### Step 9 · Put the four estimates side by side

*What and why.* This step compares the estimators. The coefficient changes when the variation used changes, and the standard error changes when the assumption about the errors changes.

```python
keys = ["lagtariff", "laginputariff"]
table = pd.DataFrame({
    "pooled, classical SE": list(pooled.params[keys]) + list(pooled.bse[keys]),
    "pooled, firm-clustered": list(pooled_cl.params[keys]) + list(pooled_cl.bse[keys]),
    "firm + year FE (col. 3)": list(fe.params[keys]) + list(fe.std_errors[keys]),
    "random effects": list(re.params[keys]) + list(re.std_errors[keys])},
    index=["b output tariff", "b input tariff", "se output tariff", "se input tariff"])
print(table.T.round(3).to_string())
```

**You should see:**

| | b output | b input | se output | se input |
|---|---|---|---|---|
| pooled, classical SE | −0.011 | 0.060 | 0.016 | 0.039 |
| pooled, firm-clustered | −0.011 | 0.060 | 0.022 | 0.075 |
| firm + year FE (col. 3) | −0.032 | −0.480 | 0.017 | 0.098 |
| random effects | −0.034 | −0.307 | 0.014 | 0.066 |

N = 14,648 in all four.

**Which to report, and why:** firm and year fixed effects, clustered by firm. Pooled OLS gives the input tariff the wrong sign (+0.060, not significant). It compares different firms, and the industries that kept high input tariffs differ in many unmeasured ways. Random effects moves most of the way (−0.307), but it still mixes in some of that between-firm variation, so it falls between pooled and FE. The gap between −0.307 and −0.480 is the evidence the Hausman logic from class looks for: the firm effect is correlated with the tariffs, so the random-effects assumption fails. The poolability F-test (14.5, p ≈ 0) also rejects a common intercept. The paper chooses column 3 for the same reason.

## Compare with the paper

| | ours | paper, Table 5 |
|---|---|---|
| col. 1, output tariff | −0.0110 (0.0223) | −0.011 [0.022] |
| col. 1, input tariff | 0.0601 (0.0748) | 0.060 [0.075] |
| col. 3, output tariff | −0.0317 (0.0169) | −0.032* [0.017] |
| col. 3, input tariff | −0.4795 (0.0980) | −0.480*** [0.098] |
| N | 14,648 | 14,648 |

Both columns match to every printed digit, coefficients and standard errors. In the paper's words, a 10-point cut in input tariffs raises TFP by about 4.8%, and the same cut in output tariffs raises it by about 0.3%. The paper's random-effects estimate is not published; our −0.307 is ours alone.

## What this does not license

- **Not a general "trade raises productivity" law.** The design relies on India's 1991 reform being imposed from outside (the IMF programme) and not driven by each industry's own prospects. The paper backs this up in Tables 2–3, and this exercise does not re-test it. Without that exogeneity, firm fixed effects remove fixed differences between firms, but they do not rule out a time-varying reverse channel.
- **Not an aggregate welfare claim.** The estimate is the within-firm change for surviving, listed Prowess firms. It says nothing about firms that entered or exited, informal firms, or consumers. Also, `tfp1000` is itself estimated, so the standard errors understate the true uncertainty.
- **Not evidence that the output-tariff effect is robust.** At p = 0.061 it is significant only at 10%, and it depends on the specification: it is −0.066 in column 2 and −0.020 in column 5 of the paper. The input-tariff result is the solid one.

## Pitfalls

- **Stata types.** `read_stata` returns `industrycode` and `companyname` as strings, and `yr`/`id` as `int16`. That is fine here. If a `.dta` file stores labelled categoricals, `read_stata` returns pandas `Categorical` columns, and these break arithmetic and `groupby` totals. Check `.dtypes` first.
- **Missing values.** Stata drops incomplete rows without telling you. Of the 14,889 pre-1997 rows, 79 lack `lagtariff`, 215 lack `laginputariff` and 2 lack `age`. Run `.dropna(subset=cols)` *before* fitting, so that all four models use the same 14,648 rows. Otherwise pooled OLS, PanelOLS and RE can quietly use different samples.
- **Index for linearmodels.** The index must be `(entity, time)` in that order: `set_index(["id", "yr"])`. The reverse order swaps the meaning of `entity_effects` and `time_effects`. Keep a numeric year so the time dimension is ordered.
- **Absorbed regressors.** If `prgroup`, `govown`, `foreign`, `medium` or `small` goes into `PanelOLS` with `entity_effects=True`, it fails with an absorbed-variable error. With `drop_absorbed=True` it instead drops them with a warning. Either way they are constant within firm and cannot be estimated. Random effects can keep them, and that is its whole appeal.
- **Which cluster.** The paper clusters by firm. Clustering the same FE model by industry (117 clusters, `clusters=` an industry code) gives SEs of 0.029 (output) and 0.253 (input). The input-tariff effect is still significant, and the output-tariff effect is not. Say which cluster you used.
- **Singletons.** 293 firms appear only once. They add nothing to the within estimate but still count in N, as they do in Stata's `areg`.
- **Runtime.** About 1.5 seconds for the whole script. Do not add `C(companyname)` to `smf.ols` to "do fixed effects by hand": that is 3,077 dummy columns and is very slow. `PanelOLS` absorbs them instead.
