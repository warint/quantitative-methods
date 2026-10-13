# Paper 5 · Session 06 · Topalova & Khandelwal (2011)

> **Reuses:** OLS, controls and dummies (session 03), a squared term (session 06) ·
> **Time:** about 30 minutes ·
> **Script:** [`starter/r5_topalova_khandelwal_2011.py`](../starter/r5_topalova_khandelwal_2011.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r5_topalova_khandelwal_2011.py` in VS Codium. Each step below is
one block of the script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run
only those, read the output, and check it against **You should see** before moving on. If a number
differs, stop and find out why.

You are **not** reproducing the paper's headline. You take the regressions you typed in sessions 03
and 06, fit them on the authors' data, and read them. The last step puts your numbers next to the
paper's, and the interesting part is why they differ.

## Citation

Topalova, Petia, and Amit Khandelwal. 2011. "Trade Liberalization and Firm Productivity: The Case of
India." *Review of Economics and Statistics* 93 (3): 995–1009. https://doi.org/10.1162/REST_a_00095.
Replication package: Harvard Dataverse, https://doi.org/10.7910/DVN/8WEXYD
(`06-advanced-regression/data/replication/`).

## The paper in brief

In 1991 India cut its import tariffs sharply and quickly, because the IMF made that a condition of
a bailout, not because some industries asked for it. The authors follow about 3,000 listed
manufacturing firms and ask whether firms in industries whose tariffs fell more became more
productive. They separate two channels: lower tariffs on a firm's **output** (more import
competition) and lower tariffs on its **inputs** (cheaper, better imported intermediate goods). Both
raise productivity, and the input channel is the larger.

## The research question

Do lower output tariffs and lower input tariffs go with higher firm productivity?

## Data

- **File:** `06-advanced-regression/data/replication/prod_dataregression.dta` (1989–2002).
- **One row:** one firm in one year.
- **Variables used:**
  - `tfp1000` — log total factor productivity (the outcome). Because it is a log, 100 × a slope is a
    percentage change.
  - `lagtariff`, `laginputariff` — last year's tariff on the industry's output and on its inputs,
    as a share: 0.65 means 65%.
  - `prgroup`, `govown`, `foreign` — ownership dummies (business group, state-owned, foreign); a
    private stand-alone firm is the reference.
  - `medium`, `small` — size dummies; large is the reference.
  - `age` — firm age in years; `yr` — the year.
- **Sample:** years before 1997 with no missing value: **14,648 firm-years, 3,077 firms**.

## The simple models, and why

| Step | Model | From session |
|---|---|---|
| 2 | productivity on the output tariff alone | 03 · the slope in units |
| 3 | + the input tariff | 03 · "controlling for" |
| 4 | + ownership, size, age and year dummies `C(yr)` | 03 · controls and dummies |
| 5 | + age squared | 06 · a squared term |

Every model is a plain OLS on all firm-years together. No panel estimator is used.

## Steps

### Step 1 · Load the firms, keep the paper's years, and see the reform

Keep 1989–1996 and drop rows with a missing variable, so that every model below uses the same rows.
Then average the two tariffs by year.

```python
firms = pd.read_stata("06-advanced-regression/data/replication/prod_dataregression.dta")
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age"]
d = firms[firms["yr"] < 1997].dropna(subset=cols)       # 1989-1996, no gaps
print(d.shape[0], "firm-years,", d["id"].nunique(), "firms")
by_year = d.groupby("yr")[["lagtariff", "laginputariff"]].mean()
print(by_year.round(2))                                  # 1 = a 100% tariff
by_year.plot(marker="o", ylabel="average lagged tariff (1 = 100%)")
plt.savefig(OUTPUT / "tariffs_by_year.png", dpi=150, bbox_inches="tight")
plt.show()
```

**You should see:** `14648 firm-years, 3077 firms`. The average output tariff falls from **0.97**
(1989) to **0.45** (1996), the input tariff from **0.37** to **0.17**. The fall is not smooth: 1992
and 1994 tick up, because the average is over the firms present that year.

### Step 2 · The simplest regression: productivity on the output tariff

```python
m1 = smf.ols("tfp1000 ~ lagtariff", data=d).fit()
b = m1.params["lagtariff"]
print(f"slope = {b:.4f}   p = {m1.pvalues['lagtariff']:.3f}   R2 = {m1.rsquared:.4f}")
print(f"a 10-point tariff cut goes with {-b * 0.10 * 100:.2f}% higher productivity")
```

**You should see:** `slope = -0.0832   p = 0.000   R2 = 0.0043`, and *a 10-point tariff cut goes
with 0.83% higher productivity*. The sign is the paper's; the $R^2$ says the tariff explains less
than half a percent of the differences in productivity between firm-years.

### Step 3 · Add the input tariff

```python
m2 = smf.ols("tfp1000 ~ lagtariff + laginputariff", data=d).fit()
print(m2.params.round(4))
print(m2.pvalues.round(3))
```

**You should see:** output tariff **−0.0657** ($p$ = 0.000), input tariff **−0.0753**
($p$ = 0.029). Both negative: lower tariffs of either kind go with higher productivity. The output
slope falls from −0.083 to −0.066 because the two tariffs moved together — part of what step 2
credited to the output tariff belongs to the input tariff.

### Step 4 · Add ownership, size, age and year dummies

`C(yr)` gives every year its own intercept. Whatever all firms shared in a year — the reform as a
whole, the 1991 crisis, the business cycle — is then no longer counted as a tariff effect.

```python
f4 = ("tfp1000 ~ lagtariff + laginputariff + prgroup + govown + foreign"
      " + medium + small + age + C(yr)")
m4 = smf.ols(f4, data=d).fit()
keys = ["lagtariff", "laginputariff"]
print(pd.DataFrame({"coef": m4.params[keys], "p": m4.pvalues[keys]}).round(3))
```

**You should see:** output tariff **−0.006** ($p$ = 0.708), input tariff **+0.048** ($p$ = 0.219).
Both slopes collapse, and the input tariff even changes sign. Most of steps 2–3 was the common fall
over time: tariffs fell everywhere *and* productivity rose everywhere, year after year. Once each
year has its own intercept, what is left compares industries with high and low tariffs in the same
year — and in that comparison the tariffs say almost nothing.

### Step 5 · Is the effect of age a curve?

```python
m5 = smf.ols(f4 + " + I(age**2)", data=d).fit()
a, a2 = m5.params["age"], m5.params["I(age ** 2)"]
for age in (5, 16, 40):                                  # inside the data: 0 to 171
    print(f"one more year at age {age:>2}: {100 * (a + 2 * a2 * age):+.2f}% productivity")
print(f"adjusted R2: {m4.rsquared_adj:.4f} without the square, {m5.rsquared_adj:.4f} with it")
```

**You should see:** one more year goes with **−0.23%** productivity at age 5, **−0.19%** at 16 (the
median firm) and **−0.10%** at 40. Older firms are less productive, but the gap per year narrows with
age. Adjusted $R^2$ rises from 0.0313 to 0.0332, so the square earns its place. The tariff slopes are
now −0.011 and +0.060.

### Step 6 · Side by side with the paper's own estimate

```python
table = pd.DataFrame({
    "step 2": [m1.params["lagtariff"], None],
    "step 3": m2.params[keys].values,
    "step 5 (paper's col. 1)": m5.params[keys].values,
    "paper col. 3, same firm over time": [-0.032, -0.480]}, index=keys)
print(table.T.round(3).to_string())
```

**You should see:**

| | output tariff | input tariff |
|---|---|---|
| step 2 | −0.083 | — |
| step 3 | −0.066 | −0.075 |
| step 5 | −0.011 | +0.060 |
| paper, Table 5 col. 3 | −0.032 | −0.480 |

Step 5 is exactly the paper's own column 1 (−0.011, 0.060): the authors start where you finished.

## Interpretation

- **Step 2:** "Across Indian firm-years 1989–1996, a 10-percentage-point lower output tariff is
  associated with 0.8% higher productivity."
- **Step 4:** "Comparing firms in the same year, with the same ownership, size class and age,
  industries with lower tariffs are not detectably more productive."
- **Step 5:** "Each extra year of age goes with about 0.2% lower productivity for a young firm, and
  about half that at 40."

## How it differs from the paper

Your regressions compare **different firms**: a firm in a low-tariff industry with a firm in a
high-tariff industry. But firms differ in a thousand ways the data do not record — technology,
management, location — and those differences can be related to their industry's tariffs. The paper
instead compares **each firm with itself**, before and after its tariffs fell, so everything constant
about the firm drops out of the comparison. That different comparison is why its input-tariff effect
is −0.480 — a 10-point cut raises productivity by 4.8% — where yours is close to zero. Same data,
different question: "are low-tariff firms more productive than others?" against "does a firm become
more productive when its tariffs fall?"

## What this does not license

- **No causal claim from steps 2–3.** They mix the effect of tariffs with everything else that
  changed over 1989–1996.
- **No "tariffs do not matter" from step 4.** A slope near zero in a comparison across firms says
  that comparison cannot see the effect; the paper's within-firm comparison does.
- **No claim beyond surviving, listed manufacturing firms**, and productivity is itself estimated by
  the authors.

## Pitfalls

- **Stata types.** `read_stata` returns `companyname` and `industrycode` as text. Check `.dtypes`
  before doing arithmetic on a column.
- **The same rows everywhere.** Drop missing values once, before fitting, so every model uses the
  same 14,648 rows; otherwise each `smf.ols` drops its own.
- **A log outcome.** `tfp1000` is a log: multiply a slope by 100 for a percentage, and by the size of
  the change (0.10 for ten points) before you say it.
- **Age squared.** Never read the `age` coefficient on its own once the square is in: the effect of one
  more year is (coefficient on age) + 2 × (coefficient on age²) × age, and it depends on the age you
  evaluate it at.
- **Runtime.** About two seconds for the whole script.
