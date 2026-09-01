# Session 02 — Group practice (second half, ~90 min)

# Profiling a variable you will have to defend

> **[Open the practice slides](https://warint.github.io/quantitative-methods/session-02-practice.html)** ·
> source: [`MATH60033A-S02-Practice.qmd`](MATH60033A-S02-Practice.qmd)

---

## The theme of this session

> # Which summary of your project's key variable would you defend in print?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

---

## What you are doing, in one paragraph

Every group has a research question and a data angle
([`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md)). Today you profile the three variables that
question depends on most — centre, spread and shape — and decide which summary you would put in a
paper. The deliverable is not a table of numbers. It is a defensible **choice**, with the reason
written down.

---

## Before you start

Everyone in the group pushes at least once this session. Replace `XX` with your group number
everywhere below — group 07 uses `group-07`.

```bash
git checkout -b group-XX
mkdir -p groups/A2026/group-XX/session-02
```

---

## 0 · Reproduce one result from the paper — 20 min

Fraiberger et al. build a sentiment index and relate it to returns. Take the descriptive result the
paper opens with — the distribution of the sentiment measure — and reproduce it from the
replication package you downloaded:

```text
02-exploratory-data-analysis/data/replication/
```

A failed reproduction that you **diagnose** earns full marks; one you do not attempt earns none.
"It did not work" is not a diagnosis — where did it stop, and what did you check?

---

## 1 · Load your angle and pick three variables — 15 min

```python
import numpy as np
import pandas as pd
import qmib
from scipy import stats

core = qmib.load("core")                  # shared by every group
mine = qmib.load("angle_c_country")       # your angle — see your dictionary
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

Choose **three** numeric variables: the outcome your research question is about, and the two you
most expect to explain it. Write one sentence each on why you chose it, before you compute
anything.

> Read your [data dictionary](../../data/spine/dictionaries/) first. Some columns carry flags,
> breaks in series, or structural missingness. A variable that is only observed from 2021 will
> produce a perfectly clean profile of a period that is not the one you meant to describe.

---

## 2 · Centre — 15 min

For each variable, report the mean, the 5% trimmed mean and the median.

```python
def centre(x):
    x = pd.Series(x).dropna()
    return pd.Series({
        "n":       len(x),
        "mean":    x.mean(),
        "trim_5%": stats.trim_mean(x, 0.05),
        "median":  x.median(),
    })
```

**The question to answer:** do the three agree? If they do not, in which direction, and by how
much relative to the spread? A gap between mean and median that is a tenth of a standard deviation
is a curiosity; one that is a third of a standard deviation is a finding.

---

## 3 · Spread — 15 min

Report the standard deviation and the IQR for each variable, and test the empirical rule directly:

```python
def empirical_rule(x):
    """What fraction actually falls within 1, 2 and 3 standard deviations?"""
    x = pd.Series(x).dropna()
    m, s = x.mean(), x.std(ddof=1)
    return {f"±{k}s": float(((x - m).abs() <= k * s).mean()) for k in (1, 2, 3)}
```

Compare what you get against 68% / 95% / 99.7%. **Where it fails, say by how much and in which
tail.** That failure is the bridge to the next section.

---

## 4 · Shape — 20 min

Compute skewness and excess kurtosis from the definitions in
[the notes](../01-lecture/README.md#23-measuring-the-shape), and test each against its threshold.

```python
def shape(x):
    x = pd.Series(x).dropna().to_numpy(float)
    n = len(x)
    xbar, s = x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / s ** 3
    g2 = ((x - xbar) ** 4).mean() / s ** 4 - 3
    return {"n": n, "g1": g1, "g2": g2,
            "skewed": abs(g1) > 2 * np.sqrt(6 / n),
            "kurtic": abs(g2) > 4 * np.sqrt(6 / n)}
```

Then plot each variable — a histogram and a boxplot side by side — and check that the picture
agrees with the two numbers. **If they disagree, trust the picture and work out why.** Usually it
is a second mode, which neither $g_1$ nor $g_2$ can see.

---

## 5 · Decide, and write it down — 20 min

For the variable at the centre of your research question, write the 250-word note:

- Which summary would you put in a paper, and why that one
- What the shape implies for the methods available to you later — a badly skewed outcome constrains
  what Session 03 can do with it
- One thing you would need to check before trusting the profile

> **What earns marks.** A group that reports a variable is skewed, says which direction, tests it
> against the threshold, and then says what that costs them later has done the work. A group that
> prints `df.describe()` and moves on has not.

---

## 6 · Two-minute report — 20 min

One slide, one variable, three numbers and one sentence of judgement. The presenter is chosen at
random when you start, so everyone prepares.

---

## Submitting

```bash
git add groups/A2026/group-XX/session-02
git commit -m "Session 02 practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

- `df.describe()` pasted with no interpretation
- Reporting a skewness without its threshold — $0.4$ is substantial at $n=437$ and negligible at $n=40$
- Calling a variable "normal" because it is symmetric
- Applying the empirical rule to a variable you have just shown to be skewed
- Dropping outliers before you have said what they are

---

[<- The lecture](../01-lecture/README.md) · [Session 02 overview](../README.md)
