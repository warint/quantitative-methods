# Paper 2 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)

> **Reuses:** binary, ordinal and multinomial logits (session 04) · **Time:** about 30 minutes ·
> **Script:** [`starter/r3_saganowski_2019.py`](../starter/r3_saganowski_2019.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

## How to work through it

Open `r3_saganowski_2019.py` in VS Codium. Each step below is one block of the script, marked
`# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read the output, and
check it against **You should see** before moving on. If a number differs, stop and find out why.

You are **not** following the paper. You take the code of the session-04 slides, **line for line**,
and plug in this paper's data: only the data set and the variable names change.

## The data

Saganowski, S., Bródka, P., Koziarski, M. & Kazienko, P. (2019), *Analysis of group evolution
prediction in complex networks*, PLOS ONE 14(10): e0224194 · data: Harvard Dataverse,
doi:10.7910/DVN/ONOFS7.

- **File:** `04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.1.csv`
  — private messages between UC Irvine students, cut into weekly windows. 498 groups.
- **One row:** one group of students who message each other, in one week.
- **Outcome:** `event_type`, what happened to the group the next week: **dissolving** (35.5%),
  **shrinking** (25.9%), **growing** (25.1%), **continuing** (10.0%), splitting (1.8%), merging (1.6%).
- **Features built in step 2:** `log2_size` (log base 2 of the number of members: +1 means twice as
  big), `avg_degree` (ties per member inside the group), `aging` (how long its members have been
  around).

## The models, and where the code comes from

Every step copies a tab of the session-04 lecture
([`MATH60033A-S04-Lecture.qmd`](../../../04-logistic-ordinal-multinomial/01-lecture/MATH60033A-S04-Lecture.qmd)).
The only other change: `print(...)` around a result, because a script does not display a bare
expression the way a slide does.

| Step | Model | Copies the session-04 tab | There it was |
|---|---|---|---|
| 3–5 | **Binary logit**: does the group dissolve next week? | LR 6 · Log-odds, LR 7 · Odds, LR 8 · Predicted probability | default on a loan, by FICO score |
| 6–8 | **Ordinal logit**: shrinking < continuing < growing | OLR 3 · The code, OLR 4 · Log-odds → odds, OLR 5 · Probabilities | applying to graduate school |
| 9–11 | **Multinomial logit**: dissolving, shrinking, growing or continuing | MLR 3 · The code, MLR 4 · Log-odds → RRR, MLR 5 · Probabilities | high-school programme |

## Steps

### Step 1 · Load the groups, and what happened to each one next week

```python
FILE = ("04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/"
        "12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.1.csv")
raw = pd.read_csv(FILE)
print(raw.shape)
print(raw["event_type"].value_counts(normalize=True).round(3))   # the base rates
```

**You should see:** `(498, 89)`, then the base rates: dissolving 0.355, shrinking 0.259, growing
0.251, continuing 0.100, splitting 0.018, merging 0.016.

### Step 2 · Three features a person can read

```python
groups = pd.DataFrame({
    "event": raw["event_type"],
    "log2_size": np.log2(raw["g1_size"]),            # +1 = the group is twice as big
    "avg_degree": raw["g1_avg_group_degree_total"],  # ties per member, inside the group
    "aging": raw["g1_IlhanAging"]})                  # how long its members have been around
print(groups[["log2_size", "avg_degree", "aging"]].median().round(2))
```

**You should see:** medians `log2_size` 2.32 (about 5 members), `avg_degree` 2.67, `aging` 8.46.
These are the "typical group" values used in steps 8 and 11 (rounded to 2.7 and 8.5).

### Step 3 · Binary logit: log-odds (session 04, LR 6)

```python
groups["dissolve"] = (groups["event"] == "dissolving").astype(int)
# Fit the logistic regression. The coefficients come out as log-odds.
m2 = smf.logit("dissolve ~ log2_size", data=groups).fit(disp=0)
print(m2.params.round(4))
```

**You should see:** `Intercept 0.7784`, `log2_size -0.5716`. A group twice as big has a log-odds of
dissolving 0.57 lower.

### Step 4 · Binary logit: odds (session 04, LR 7)

```python
# Log-odds -> odds ratio: take the exponential of each coefficient
print(np.exp(m2.params["log2_size"]).round(4))
```

**You should see:** `0.5646`. Doubling the size of a group multiplies its odds of dissolving by
0.56 — about **44% lower odds**.

### Step 5 · Binary logit: predicted probability (session 04, LR 8)

```python
# predict() does the same calculation for you: groups of 4, 8 and 16 members
print(m2.predict(pd.DataFrame({"log2_size": [2, 3, 4]})).round(3))
```

**You should see:** `0.410`, `0.282`, `0.181`. A 4-member group dissolves with probability 0.41, a
16-member group with 0.18.

### Step 6 · Ordinal logit: the code (session 04, OLR 3)

```python
# Keep the order: shrinking < continuing < growing
order = ["shrinking", "continuing", "growing"]
dat = groups[groups["event"].isin(order)].copy()
dat["event_c"] = pd.Categorical(dat["event"], categories=order, ordered=True)
om = OrderedModel(dat["event_c"], dat[["log2_size", "avg_degree", "aging"]], distr="logit").fit(method="bfgs", disp=0)
print(om.summary())
```

**You should see:** 304 observations (the groups that shrank, continued or grew). `log2_size`
−1.3384 (p 0.000), `avg_degree` −0.0755 (p 0.734), `aging` −0.0154 (p 0.176); cutpoints
`shrinking/continuing` −4.0540 and `continuing/growing` −0.1979.

### Step 7 · Ordinal logit: log-odds → odds (session 04, OLR 4)

```python
# Log-odds: the slopes as fitted (the cutpoints are left out)
print(om.params[["log2_size", "avg_degree", "aging"]].round(3))
# Proportional-odds ratios
print(np.exp(om.params[["log2_size", "avg_degree", "aging"]]).round(3))
```

**You should see:** log-odds −1.338, −0.075, −0.015; odds ratios **0.262**, 0.927, 0.985.

### Step 8 · Ordinal logit: probabilities (session 04, OLR 5)

```python
# A 4-member group, and an otherwise identical 16-member one.
# Columns: shrinking, continuing, growing.
new = pd.DataFrame({"log2_size": [2, 4], "avg_degree": [2.7, 2.7], "aging": [8.5, 8.5]})
print(pd.DataFrame(np.asarray(om.predict(new)), columns=order, index=["4 members", "16 members"]).round(3))
```

**You should see:**

```
            shrinking  continuing  growing
4 members       0.261       0.184    0.555
16 members      0.837       0.084    0.079
```

### Step 9 · Multinomial logit: the code (session 04, MLR 3)

```python
# Code 0 (dissolving) is the baseline: every coefficient reads "relative to dissolving"
levels = ["dissolving", "shrinking", "growing", "continuing"]
ml = groups[groups["event"].isin(levels)].copy()
ml["event_c"] = pd.Categorical(ml["event"], categories=levels).codes
X = ml[["log2_size", "avg_degree", "aging"]].astype(float)
X = sm.add_constant(X)
# Three sets of coefficients at once, each against the dissolving baseline
mn = sm.MNLogit(ml["event_c"], X).fit(disp=0)
print(mn.summary().tables[1])          # the coefficient table
```

**You should see:** three blocks. `event_c=1` is shrinking vs dissolving (`log2_size` 1.1698,
p 0.000; `avg_degree` 0.8228, p 0.001), `event_c=2` growing vs dissolving (`log2_size` −0.1244,
p 0.562), `event_c=3` continuing vs dissolving (`log2_size` −0.7569, p 0.034).

### Step 10 · Multinomial logit: log-odds → relative risk ratios (session 04, MLR 4)

```python
# Log-odds and RRR, for shrinking, growing and continuing vs dissolving
print(pd.concat({"log-odds": mn.params, "RRR": np.exp(mn.params)}, axis=1)
      .set_axis(["log-odds: shrinking", "log-odds: growing", "log-odds: continuing",
                 "RRR: shrinking", "RRR: growing", "RRR: continuing"], axis=1).round(3))
```

**You should see:** for `log2_size`, RRR **3.221** (shrinking), 0.883 (growing), 0.469
(continuing); for `avg_degree`, 2.277, 1.536, 1.117.

### Step 11 · Multinomial logit: probabilities (session 04, MLR 5)

```python
# Typical groups (median degree and aging), from 4 to 32 members
grid = pd.DataFrame({"const": 1.0, "log2_size": [2, 3, 4, 5],
                     "avg_degree": 2.7, "aging": 8.5})
out = pd.DataFrame(mn.predict(grid).values, columns=levels, index=grid["log2_size"])
print(out.round(3))
```

**You should see:**

```
           dissolving  shrinking  growing  continuing
log2_size
2               0.424      0.135    0.328       0.113
3               0.353      0.362    0.241       0.044
4               0.201      0.665    0.122       0.012
5               0.082      0.872    0.044       0.002
```

## Interpretation

- **Binary:** bigger groups dissolve less. Doubling a group's size multiplies its odds of dissolving
  by 0.56; the probability falls from 0.41 for 4 members to 0.18 for 16.
- **Ordinal:** among groups that survive, bigger ones move **down** the scale. Doubling the size
  multiplies the odds of being in a higher category (continuing rather than shrinking, growing
  rather than the rest) by 0.26. A 4-member group grows with probability 0.56; a 16-member group
  shrinks with probability 0.84. Degree and aging have no detectable effect here.
- **Multinomial:** relative to dissolving, doubling the size multiplies the ratio
  P(shrinking)/P(dissolving) by 3.2. In probabilities: as a group goes from 4 to 32 members, the
  chance it dissolves falls from 0.42 to 0.08 and the chance it shrinks rises from 0.14 to 0.87.
- **Together:** large groups rarely vanish in one week, but they lose members. The three models
  answer three different questions about the same groups.

## What this does not license

- **No causal reading.** Bigger groups dissolve less, but adding members would not by itself keep a
  group alive.
- **No claim about other networks.** One university's messaging groups, one tracking method, weekly
  windows.
- **No reading of the rare events.** Splitting and merging (3.4% together) are left out of the
  multinomial model: too few to estimate a set of coefficients each.

## Pitfalls

- **Folder and file names contain spaces.** In Python, a quoted string is fine. In a terminal, quote
  the path:
  - macOS and Linux: `ls "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state"`
  - Windows PowerShell: `Get-ChildItem "04-logistic-ordinal-multinomial\data\replication\12 IrvineMessages_s7o3_infomap_1state"`
- **The ordinal model has no intercept.** `OrderedModel` uses cutpoints instead; do not pass a
  constant, or the model cannot be estimated.
- **The multinomial baseline is code 0.** Reorder `levels` and every coefficient changes meaning,
  with nothing in the output to warn you.
- **Check the multinomial converged** before reading a ratio: `mn.mle_retvals["converged"]` should be
  `True`. With merging and splitting in, it may not.
