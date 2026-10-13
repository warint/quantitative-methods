# Paper 3 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)

> **Reuses:** binary, ordinal and multinomial logits (session 04) · **Time:** about 30 minutes ·
> **Script:** [`starter/r3_saganowski_2019.py`](../starter/r3_saganowski_2019.py) ·
> **Log:** one block in your [`replication-log.md`](../replication-log.md)

**How to work through it.** Open `r3_saganowski_2019.py` in VS Codium. Each step below is one block of the
script, marked `# Step N`. Select a step's lines and press **Shift+Enter** to run only those, read
the output, and check it against **You should see** before moving on. If a number differs, stop and
find out why.

You are **not** reproducing the paper's numbers. You take the three logits you typed in session 04,
fit them on the paper's data with three readable features, and say what they show — and how that
differs from what the authors did.

## Citation

Saganowski, S., Bródka, P., Koziarski, M. & Kazienko, P. (2019). Analysis of group evolution
prediction in complex networks. *PLOS ONE* 14(10): e0224194. https://doi.org/10.1371/journal.pone.0224194.
Replication data: Harvard Dataverse, https://doi.org/10.7910/DVN/ONOFS7.

## The paper in brief

The authors cut a social network (who messages whom) into time windows, find the groups in each
window, and record what happened to each group in the next window: it **dissolved, shrank, grew,
continued, merged or split**. They describe each group with about 90 network measures and train 15
machine-learning classifiers to predict the next event. Across fifteen data sets, tree-based
classifiers (Bagging and Random Forest) do best. They score the classifiers by the plain average of
the per-event F-measures, because accuracy rewards predicting the common events.

## The research question

Can a group's current structure predict which of six events will happen to it in the next time
window?

## Data

- **Files:** `04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/`, the
  `.partition.1.fold.1.csv` file (to fit) and `.fold.2.csv` (to test) — two halves of the same 995 groups.
- **Network:** private messages between UC Irvine students, cut into weekly windows.
- **Unit of observation:** one group in one weekly window, with the event recorded for the following window.
- **Events (fit half / test half):** dissolving 177 / 177, shrinking 129 / 128, growing 125 / 125,
  continuing 50 / 50, splitting 9 / 9, merging 8 / 8.
- **Three features** (step 2):
  - `log2_size`: log base 2 of the number of members — +1 means **twice as big**;
  - `avg_degree`: ties per member, inside the group;
  - `aging`: how long the group's members have been active (the paper's top-ranked measure).

## The simple models, and why

| Question | Model (session 04) | Why this one |
|---|---|---|
| Does the group dissolve? | **binary logit**, `smf.logit` | two outcomes: dissolves or not |
| Does it shrink, continue or grow? | **ordinal logit**, `OrderedModel` | three outcomes with a natural order |
| Which of the four common events? | **multinomial logit**, `sm.MNLogit` | four outcomes with no order |

Merging and splitting are left out of the multinomial: 17 groups out of 498, too few to estimate
an equation each.

## Steps

### Step 1 · Load the two halves

Fit on one half, test on the other. The share of each event is the **base rate**: what you would
get right by always predicting that event.

```python
train, test = pd.read_csv(FILE.format(1)), pd.read_csv(FILE.format(2))
print("train", train.shape, "| test", test.shape)
print(train["event_type"].value_counts(normalize=True).round(3))   # the base rates
```

**You should see:** `train (498, 89) | test (497, 89)`. Dissolving 0.355, shrinking 0.259,
growing 0.251, continuing 0.100, splitting 0.018, merging 0.016.

### Step 2 · Three features a person can read

```python
def features(df):
    return pd.DataFrame({
        "event": df["event_type"],
        "log2_size": np.log2(df["g1_size"]),            # +1 = the group is twice as big
        "avg_degree": df["g1_avg_group_degree_total"],  # ties per member, inside the group
        "aging": df["g1_IlhanAging"]})                  # how long its members have been around
tr, te = features(train), features(test)
X = ["log2_size", "avg_degree", "aging"]
print(tr.groupby("event")[X].median().round(2))
```

**You should see:** groups that shrink are the largest (median `log2_size` 3.00, about 8 members);
groups that dissolve or continue are small (2.00, 4 members). Continuing groups have the oldest
members (median aging 13.1, against 8.0 for dissolving).

### Step 3 · Binary logit: does the group dissolve next week?

```python
tr["dissolve"] = (tr["event"] == "dissolving").astype(int)
bi = smf.logit("dissolve ~ log2_size + avg_degree + aging", data=tr).fit(disp=0)
print(pd.DataFrame({"log-odds": bi.params, "odds ratio": np.exp(bi.params),
                    "p-value": bi.pvalues}).round(3))
```

**You should see:**

| | log-odds | odds ratio | p-value |
|---|---|---|---|
| log2_size | −0.428 | 0.652 | 0.006 |
| avg_degree | −0.433 | 0.648 | 0.018 |
| aging | −0.027 | 0.974 | 0.009 |

All three signs are negative: bigger, more connected and older groups are **less** likely to dissolve.

### Step 4 · From odds to probabilities

```python
typical = tr[X].median()
cases = pd.DataFrame([typical, typical], index=["4 members", "16 members"])
cases["log2_size"] = [2, 4]                         # 2**2 = 4, 2**4 = 16
print("P(dissolve):", bi.predict(cases).round(3).to_dict())
```

**You should see:** `P(dissolve): {'4 members': 0.407, '16 members': 0.226}` — the other two
features held at their medians (2.67 ties per member, aging 8.5).

### Step 5 · Ordinal logit: shrinks < continues < grows

Only the groups that shrink, continue or grow (304 of 498). One slope per feature, shared by both
cuts; positive pushes the group **up** the scale, towards growing.

```python
levels = ["shrinking", "continuing", "growing"]
sub = tr[tr["event"].isin(levels)].copy()
sub["size_change"] = pd.Categorical(sub["event"], categories=levels, ordered=True)
om = OrderedModel(sub["size_change"], sub[X], distr="logit").fit(method="bfgs", disp=0)
print(pd.DataFrame({"log-odds": om.params[X], "odds ratio": np.exp(om.params[X]),
                    "p-value": om.pvalues[X]}).round(3))
print("P(shrink, continue, grow):")
print(pd.DataFrame(np.asarray(om.predict(cases[X])), index=cases.index, columns=levels).round(3))
```

**You should see:** `log2_size` −1.338, odds ratio **0.262**, p < 0.001; `avg_degree` (0.927,
p = 0.73) and `aging` (0.985, p = 0.18) are not detectable. Probabilities:

| | shrinking | continuing | growing |
|---|---|---|---|
| 4 members | 0.260 | 0.184 | 0.556 |
| 16 members | 0.836 | 0.084 | 0.079 |

### Step 6 · Multinomial logit: four events, baseline = dissolving

```python
four = ["dissolving", "shrinking", "growing", "continuing"]   # merging and splitting: 17 groups
m4 = tr[tr["event"].isin(four)]
mn = sm.MNLogit(pd.Categorical(m4["event"], categories=four).codes,
                sm.add_constant(m4[X])).fit(disp=0, maxiter=200)
rrr = np.exp(mn.params)
rrr.columns = four[1:]                              # each column: that event against dissolving
print("relative risk ratios, against dissolving:")
print(rrr.round(3))
```

**You should see:**

| | shrinking | growing | continuing |
|---|---|---|---|
| log2_size | 3.221 | 0.883 | 0.469 |
| avg_degree | 2.277 | 1.536 | 1.117 |
| aging | 1.035 | 1.012 | 1.036 |

### Step 7 · Predicted probabilities across group size

```python
grid = pd.DataFrame({"log2_size": np.linspace(1.6, 6, 40), "avg_degree": typical["avg_degree"],
                     "aging": typical["aging"]})
probs = pd.DataFrame(np.asarray(mn.predict(sm.add_constant(grid, has_constant="add"))), columns=four)
for e in four:
    plt.plot(2 ** grid["log2_size"], probs[e], label=e)
plt.xscale("log"); plt.xlabel("group size (members)"); plt.ylabel("predicted probability")
plt.legend(); plt.savefig(OUTPUT / "s04_event_probabilities.png", dpi=150, bbox_inches="tight"); plt.show()
```

**You should see:** a figure saved as `output/s04_event_probabilities.png`. From 3 to 64 members,
the probability of **shrinking** climbs steeply while dissolving, growing and continuing all fall.

### Step 8 · Out of sample: accuracy against the base rate

```python
t4 = te[te["event"].isin(four)]
guess = np.asarray(mn.predict(sm.add_constant(t4[X]))).argmax(axis=1)
truth = pd.Categorical(t4["event"], categories=four).codes
print(f"multinomial accuracy {(guess == truth).mean():.3f} | always 'dissolving' "
      f"{(t4['event'] == 'dissolving').mean():.3f}")
print(pd.crosstab(pd.Series(np.array(four)[truth], name="true"),
                  pd.Series(np.array(four)[guess], name="predicted")))
```

**You should see:** `multinomial accuracy 0.460 | always 'dissolving' 0.369`. The table shows the
model predicts almost only **dissolving** and **shrinking**: of 50 continuing groups it gets 2 right,
of 125 growing groups 7.

## Interpretation

- **Binary.** Doubling a group's size multiplies its odds of dissolving by **0.65** (35% lower
  odds), holding connectedness and aging fixed. In probabilities: a typical 4-member group dissolves
  next week with probability about 0.41, a 16-member group about 0.23.
- **Ordinal.** Among groups that do not dissolve, size is the only clear signal: doubling the size
  multiplies the odds of being higher on the scale (continuing or growing rather than shrinking) by
  **0.26**. A 4-member group most likely grows (0.56); a 16-member group most likely shrinks (0.84).
  Big groups have room to lose members; small ones have room to gain them.
- **Multinomial.** Every ratio reads "against dissolving". Doubling the size multiplies the
  shrinking-to-dissolving ratio by **3.2** but the continuing-to-dissolving ratio by 0.47. More
  ties per member raise the shrinking (2.3) and growing (1.5) ratios.
- **Out of sample.** 0.46 against 0.37 for always guessing "dissolving": better than the base rate,
  but the three features cannot tell a group that continues or grows from one that dissolves.

## How it differs from the paper

| | The paper | This script |
|---|---|---|
| Models | 15 machine-learning classifiers; tree-based ones do best | three logits from session 04 |
| Features | about 90 network measures | three readable ones |
| Events | all six | binary, three ordered, four unordered |
| Score | plain average of per-event F-measures | accuracy against the base rate |
| Purpose | predict as well as possible | read each feature's effect in words |

The logits give up predictive power for **readable coefficients**: an odds ratio you can say in a
sentence. The paper's classifiers predict better but do not hand you that sentence.

## What this does not license

- **No causal reading.** "Bigger groups dissolve less" describes weekly message groups at one
  university. Adding members would not by itself keep a group alive.
- **No claim about the rare events.** Merging and splitting were left out: 17 groups cannot carry an
  equation each.
- **No claim that the labels are facts.** The events come from a tracking algorithm — a measured
  construct, not something observed directly.
- **No claim beyond this network.** One university, one season, weekly windows.

## Pitfalls

- **Folder and file names contain spaces.** In Python, a quoted string is fine. In a terminal, quote
  the path:
  - macOS and Linux: `ls "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state"`
  - Windows PowerShell: `Get-ChildItem "04-logistic-ordinal-multinomial\data\replication\12 IrvineMessages_s7o3_infomap_1state"`
- **Each half already contains its share of all 995 groups.** Do not stack partitions or you will
  duplicate every group.
- **The ordinal model has no intercept.** `OrderedModel` uses cutpoints instead; do not pass a
  constant, or the model cannot be estimated.
- **`sm.add_constant` on a grid where every row looks alike** (step 7) silently skips the constant.
  Pass `has_constant="add"`.
- **Check the multinomial converged** before reading a ratio: `mn.mle_retvals["converged"]` should be
  `True`. With merging and splitting in, it may not.
