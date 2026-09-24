# Replication 3 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)

> **Reuses:** logistic and multinomial regression (session 04) · **Time:** about 30 minutes ·
> **Script:** [`starter/r3_saganowski_2019.py`](../starter/r3_saganowski_2019.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r3_saganowski_2019.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs,
stop and find out why — that is the exercise, not a detour from it.

## Citation

Saganowski, S., Bródka, P., Koziarski, M. & Kazienko, P. (2019). Analysis of group evolution prediction in complex networks. *PLOS ONE* 14(10): e0224194. https://doi.org/10.1371/journal.pone.0224194. Supporting information (S1 File): https://doi.org/10.1371/journal.pone.0224194.s001. Replication data: Harvard Dataverse, https://doi.org/10.7910/DVN/ONOFS7.

## The paper in brief

The authors cut a social network (who messages whom) into time windows, find the groups (communities) in each window, and record what happened to each group in the next window: it dissolved, shrank, grew, stayed the same, merged or split. They describe each group with about 90 network measures, such as its size, how tightly its members are connected and how central they are, and train 15 machine-learning classifiers to predict the next event. Across fifteen data sets they find that tree-based classifiers (Bagging and Random Forest) do best, and they report the plain average of the per-class F-measures as their score. A feature-selection experiment, whose data are the replication package, ranks which measures the classifiers rely on most.

## The research question

Can a group's current structure predict which of six events will happen to it in the next time window?

## The published target

The paper gives **no accuracy or F-measure for any of the 28 configurations in the replication package**. Both the article and its S1 File were checked. The package holds the data for the feature-ranking experiment (S1 File, Table E). What the paper does publish:

- **This configuration.** S1 Table E, ranking id 4: IrvineMessages, 1-state chains, overlapping windows of 7 days that overlap by 3 days, 47 time windows.
- **The feature ranking for all 1-state chains** (S1 Table F, ids 1–12 merged). The top three features are **IlhanAging** (258 occurrences), **network density** (242) and **network leadership** (216). This is the claim tested here with a likelihood-ratio test.
- **The nearest published overall scores**, from other data sets:
  - Facebook: average F-measure 0.291 (Random Forest, 1 tree) to 0.350 (100 trees), 0.305 to 0.360 for Bagging, and 0.297 to 0.326 for C4.5 (S1 File, "Adjusting classifiers parameters", Fig C).
  - S1 Table K example samples: Digg, average F 0.2406 with accuracy 0.4564; MIT, average F 0.3752 with accuracy 0.4379, and 0.3867 with 0.4020.
- **The paper's measure.** The "plain average F-measure" is the unweighted mean of the six per-event F-measures (S1 File, "Classification performance measure"). The paper prefers it to accuracy because accuracy rewards predicting the dominant classes.

## Data

- **Files:** `04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.1.csv` (used to fit) and `...partition.1.fold.2.csv` (used to test).
  - Each of the 5 partitions is the full data set split into two stratified halves. This is the paper's 5 × 2 design. Every partition contains the same 995 groups.
- **Why this configuration:**
  - IrvineMessages is private messages between UC Irvine students (1,899 people, 6 months; S1 Table B).
  - It has 995 groups, which is large enough for a six-outcome logit but small enough to load in a second.
  - The 1-state version has one set of 89 columns, not 179 or 800. Weekly windows are easy to explain.
  - It is one of the configurations behind Table F.
  - Folders with 30–160 groups are too small for six classes. Loans has 97% dissolving. Slashdot and Digg files run to tens of megabytes.
- **Unit of observation:** one group (an Infomap community) in one weekly window, with the event recorded for the following window.
- **Events (train / test):** dissolving 177 / 177, shrinking 129 / 128, growing 125 / 125, continuing 50 / 50, splitting 9 / 9, merging 8 / 8. Across all 995 groups: 354, 257, 250, 100, 18, 16.
- **Features used (5):**
  - `log2_size`: log base 2 of `g1_size`, the number of members. +1 means twice as big.
  - `avg_degree`: `g1_avg_group_degree_total`, the average number of ties a member has inside the group.
  - `aging`: `g1_IlhanAging`, İlhan et al.'s "aging" feature, ranked #1 in Table F. It ranges from 0 to 44 and is usually fractional. That fits the average number of windows the members have been active, but the S1 File does not define it, so read it as "how long this group's people have been around".
  - `net_density`: `g1_network_density` × 1000, the density of the whole network in that window, per thousand (#2 in Table F).
  - `net_leadership`: `g1_network_leadership` × 100, the centralisation of the whole network in that window, in points (#3 in Table F).
  - The last two describe the window, not the group. They take only 46 distinct values.

## Steps

### Step 1 · Load the two halves of partition 1

The concept is the train/test split (session 04: judge a classifier on data it has not seen). Fold 1 fits the model and fold 2 scores it, as in the paper's 5 × 2 design.

```python
FOLDER = "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/"
FILE = FOLDER + "12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.{}.csv"
train = pd.read_csv(FILE.format(1))
test = pd.read_csv(FILE.format(2))
print("train", train.shape, "| test", test.shape)
print(pd.concat([train["event_type"].value_counts(), test["event_type"].value_counts()],
                axis=1, keys=["train", "test"]))
```

**You should see:** `train (498, 89) | test (497, 89)`, then dissolving 177/177, shrinking 129/128, growing 125/125, continuing 50/50, splitting 9/9, merging 8/8. The folds are stratified, so the event mix is the same in both.

### Step 2 · Five readable features and a 0/1 outcome

Coefficients are per unit, so the units must mean something. A network density of 0.0065 is unreadable, while 6.5 per thousand is readable. Size is logged in base 2 so that one unit means "twice as big".

```python
def features(df):
    return pd.DataFrame({
        "dissolve": (df["event_type"] == "dissolving").astype(int),
        "event": df["event_type"],
        "log2_size": np.log2(df["g1_size"]),
        "avg_degree": df["g1_avg_group_degree_total"],
        "aging": df["g1_IlhanAging"],
        "net_density": df["g1_network_density"] * 1000,
        "net_leadership": df["g1_network_leadership"] * 100})
tr, te = features(train), features(test)
print(tr.groupby("event")[["log2_size", "avg_degree", "aging", "net_density", "net_leadership"]].median().round(2))
```

**You should see:** median `log2_size` 2.00 for dissolving and continuing (4 members), 3.00 for shrinking (8 members) and 3.46 for splitting (about 11 members). Median `aging` is 8.00 for dissolving against 13.08 for continuing. Groups that shrink or split are the big ones.

### Step 3 · Binary logit: does the group dissolve next week?

The concept is the binary logit and odds ratios. A coefficient is a change in log-odds, and `np.exp` turns it into an odds ratio.

```python
full = smf.logit("dissolve ~ log2_size + avg_degree + aging + net_density + net_leadership", data=tr).fit(disp=0)
print(full.summary().tables[1])
print(np.exp(full.params).round(3))
```

**You should see:**

| | coef | p | odds ratio |
|---|---|---|---|
| log2_size | −0.4495 | 0.005 | 0.638 |
| avg_degree | −0.4515 | 0.016 | 0.637 |
| aging | −0.0015 | 0.907 | 0.998 |
| net_density | −0.1633 | 0.006 | 0.849 |
| net_leadership | −0.0297 | 0.293 | 0.971 |

In words:
- Doubling a group's size multiplies its odds of dissolving by 0.64, a 36% cut, holding the rest fixed.
- One more tie per member cuts the odds by about 36% as well.
- Each extra point of network density per thousand cuts the odds by 15%.
- Aging, the paper's top-ranked feature, does nothing here: the odds ratio is 0.998 and p = 0.91.

### Step 4 · Predicted probabilities for a small and a larger group

The concept is predicted probabilities. Odds ratios are multiplicative, while a probability says what they mean for a real group. `get_prediction` adds a confidence interval.

```python
typical = tr.drop(columns=["dissolve", "event"]).median()
cases = pd.DataFrame([typical, typical])
cases["log2_size"] = [2, 4]
pred = full.get_prediction(cases).summary_frame()
pred.index = ["4 members", "16 members"]
print(pred.round(3))
```

**You should see:** a 4-member group dissolves with probability 0.395 (95% CI 0.335–0.460), and a 16-member group with probability 0.210 (0.136–0.310). Other features are held at their medians.

### Step 5 · Likelihood-ratio test for the paper's three top features

The concept is the likelihood-ratio test on a group of variables, plus McFadden's pseudo-R². The small model is nested in the full one, so 2 × (difference in log-likelihood) follows a χ² distribution with 3 degrees of freedom.

```python
small = smf.logit("dissolve ~ log2_size + avg_degree", data=tr).fit(disp=0)
lr = 2 * (full.llf - small.llf)
print(f"LR = {lr:.2f}, df = 3, p = {stats.chi2.sf(lr, df=3):.4f}")
print(f"McFadden pseudo-R2: small {small.prsquared:.4f}   full {full.prsquared:.4f}")
```

**You should see:** `LR = 18.20, df = 3, p = 0.0004`, and McFadden pseudo-R² rising from 0.0395 to 0.0676. Together, Table F's top three features add information, but step 3 shows it all comes from network density.

### Step 6 · Out of sample: accuracy against the base rate

The concept is accuracy versus the base rate. A classifier that always says "does not dissolve" is right 64% of the time, and the logit has to beat that.

```python
p_test = full.predict(te)
acc = ((p_test > 0.5).astype(int) == te["dissolve"]).mean()
base = 1 - te["dissolve"].mean()
print(f"logit accuracy {acc:.3f} | base rate {base:.3f} | groups flagged as dissolving: {(p_test > 0.5).sum()} of {len(te)}")
```

**You should see:** `logit accuracy 0.632 | base rate 0.644 | groups flagged as dissolving: 86 of 497`. The binary logit with a 0.5 cut-off does slightly worse than always guessing "no". The coefficients are significant, but the model does not beat the base rate as a classifier.

### Step 7 · Multinomial logit over all six events

The concept is the multinomial logit with a named baseline. Each coefficient compares one event with dissolving, the baseline, so the baseline must be named.

```python
order = ["dissolving", "shrinking", "growing", "continuing", "merging", "splitting"]
X_cols = ["log2_size", "avg_degree", "aging", "net_density", "net_leadership"]
y_tr = pd.Categorical(tr["event"], categories=order).codes
mn = sm.MNLogit(y_tr, sm.add_constant(tr[X_cols])).fit(disp=0, maxiter=200)
print("converged:", mn.mle_retvals["converged"], "| McFadden pseudo-R2:", round(mn.prsquared, 4))
odds = np.exp(mn.params)
odds.columns = order[1:]
print(odds.round(3))
```

**You should see:** `converged: True | McFadden pseudo-R2: 0.1305`. The odds ratios for `log2_size` are:

| shrinking | growing | continuing | merging | splitting |
|---|---|---|---|---|
| 3.363 | 0.902 | 0.487 | 0.975 | 8.619 |

In words, compared with dissolving:
- Doubling a group's size multiplies the odds of shrinking by 3.4 and of splitting by 8.6.
- It halves the odds of simply continuing (0.487).
- For `aging`, the odds ratio for continuing is 1.031 per window. Long-standing members tilt a group slightly towards continuing rather than dissolving.

### Step 8 · The same LR test in the multinomial

The concept is the LR test again. Degrees of freedom are 3 features × 5 non-baseline equations, which gives 15.

```python
mn_small = sm.MNLogit(y_tr, sm.add_constant(tr[["log2_size", "avg_degree"]])).fit(disp=0, maxiter=200)
lr_mn = 2 * (mn.llf - mn_small.llf)
print(f"LR = {lr_mn:.2f}, df = 15, p = {stats.chi2.sf(lr_mn, df=15):.4f}")
print(f"McFadden pseudo-R2: small {mn_small.prsquared:.4f}   full {mn.prsquared:.4f}")
```

**You should see:** `LR = 40.16, df = 15, p = 0.0004`, and McFadden pseudo-R² rising from 0.1024 to 0.1305.

### Step 9 · Out of sample: accuracy and the paper's average F-measure

The concepts are the confusion table (`pd.crosstab`), accuracy against the base rate, and per-class F-measure. F is computed by hand from precision and recall because only `crosstab` and counting are allowed.

```python
probs = np.asarray(mn.predict(sm.add_constant(te[X_cols])))
guess = pd.Categorical.from_codes(probs.argmax(axis=1), categories=order)
truth = pd.Categorical(te["event"], categories=order)
print(pd.crosstab(pd.Series(truth, name="true"), pd.Series(guess, name="predicted"), dropna=False))
f = {}
for k in order:
    tp = ((guess == k) & (truth == k)).sum()
    prec = tp / (guess == k).sum() if (guess == k).sum() > 0 else 0
    rec = tp / (truth == k).sum()
    f[k] = float(2 * prec * rec / (prec + rec)) if prec + rec > 0 else 0.0
print("F-measure by event:", {k: round(v, 3) for k, v in f.items()})
print(f"accuracy {(guess == truth).mean():.3f} | base rate {(truth == 'dissolving').mean():.3f} | average F {np.mean(list(f.values())):.3f}")
```

**You should see:**
- **Diagonal of the confusion table:** 126 dissolving, 77 shrinking, 30 growing and 0 for each of the other three events. The model never predicts continuing, merging or splitting, and 75 of the 125 growing groups are called dissolving.
- **F-measures:** dissolving 0.556, shrinking 0.556, growing 0.308, continuing 0.0, merging 0.0, splitting 0.0.
- **Overall:** `accuracy 0.469 | base rate 0.356 | average F 0.237`.

### Step 10 · Picture: predicted probabilities across group size

The concept is predicted probabilities plotted against one predictor, with the others held at their medians. Six curves that always sum to one show the multinomial logit more clearly than a table.

```python
grid = pd.DataFrame([typical] * 50)
grid["log2_size"] = np.linspace(np.log2(3), np.log2(64), 50)
curves = np.asarray(mn.predict(sm.add_constant(grid[X_cols], has_constant="add")))
fig, ax = plt.subplots(figsize=(7, 4))
for j, name in enumerate(order):
    ax.plot(2 ** grid["log2_size"], curves[:, j], label=name)
ax.set_xscale("log", base=2)
ax.set_xlabel("group size (members, log scale)"); ax.set_ylabel("predicted probability")
ax.legend(fontsize=8)
plt.savefig(OUTPUT / "s04_event_probabilities.png", dpi=150)
```

**You should see:** the file `s04_event_probabilities.png`.
- At 3–4 members, dissolving (about 0.42) and growing (about 0.35) lead.
- Shrinking overtakes dissolving near 8 members and peaks at about 0.75 near 32 members.
- Splitting climbs to about 0.32 at 64 members.
- Continuing and merging stay near zero past about 16 members.

## Compare with the paper

| | this replication (IrvineMessages s7o3, 1 state, fold 1 → fold 2) | paper |
|---|---|---|
| Multinomial logit, accuracy | 0.469 (base rate 0.356) | none for this network; S1 Table K samples: 0.4020–0.4564 (Digg, MIT) |
| Multinomial logit, plain average F | **0.237** | none for this network; Facebook, tuned trees: 0.291–0.360 (S1 Fig C text); Table K: 0.2406 (Digg), 0.3752 and 0.3867 (MIT) |
| Binary logit (dissolve), accuracy | 0.632 against a base rate of 0.644 | not reported |
| Table F's top-3 features jointly | LR = 18.20 (binary) and 40.16 (multinomial), both p = 0.0004 | ranked 1st, 2nd and 3rd for 1-state chains |

Five linear features score a plain average F of 0.237, well below the 0.29–0.36 the paper's tuned trees reach on Facebook. It is about level with the Digg sample in Table K (0.2406). That is a comparison across data sets, not a replication of a number.

The logit's weakness is the one the paper warns about. It learns the three big classes and never predicts the three small ones, so their F of 0 drags the average down.

On features, the logit supports only part of Table F. Network density matters, but aging, the paper's #1, has no linear effect on dissolving (p = 0.91), and network leadership is not significant (p = 0.29). A tree ranking and a logit coefficient answer different questions.

## What this does not license

- **No claim that the paper's numbers were reproduced.** The paper publishes no accuracy or F-measure for this configuration, so the comparison is only with other networks. The logit also uses 5 features where the paper used 89.
- **No claim of precise standard errors for the network-level features.** `net_density` and `net_leadership` take only 46 distinct values, one per time window. All the groups in a window share them, so the observations are not independent and the p-values for those two features are too small. The event label also comes from the GED tracking algorithm with alpha = beta = 50%, so it is a measured construct, not an observed fact.
- **No causal reading.** "Bigger groups dissolve less" describes weekly message groups at one university. Adding members would not by itself keep a group alive.

## Pitfalls

- **Folder and file names contain spaces**, for example `12 IrvineMessages_s7o3_infomap_1state/12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.1.csv`. In Python, a quoted string is fine. In a terminal, quote the path:
  - macOS and Linux: `ls "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state"`
  - Windows PowerShell: `Get-ChildItem "04-logistic-ordinal-multinomial\data\replication\12 IrvineMessages_s7o3_infomap_1state"`
- **File layout.**
  - The leading number on a folder (12) is the package's numbering. It is not the ranking id in S1 Table E (4).
  - Each partition already contains all 995 groups. Do not stack several partitions or you will duplicate every group.
  - The outcome column is `event_type`, and features carry a `g1_` prefix. In 2- and 3-state folders the prefixes are `g1_`, `g2_` and `g3_`; the package does not say which is the most recent state.
- **Convergence.**
  - Merging and splitting have only 8 and 9 training cases. With more features, or with raw unscaled columns, `MNLogit` can hit the iteration limit or come close to separation.
  - Keep the feature set small, pass `maxiter=200` and check `mn.mle_retvals["converged"]` before reading any odds ratio.
  - Do not feed in `g1_network_density` raw at 0.0065: its coefficient becomes huge and hard to read. Rescale it as in step 2.
- **`sm.add_constant` on a grid of identical rows** (step 10) silently skips the constant because a column looks constant. Pass `has_constant="add"`.
