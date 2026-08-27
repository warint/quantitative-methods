# Session 11 — Pre-session preparation

> **What would have happened otherwise?**

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-11-pre-session.html)** ·
> source: [`MATH60033A-S11-Pre-Session.qmd`](MATH60033A-S11-Pre-Session.qmd)

Two things to do before class, and they are the two halves of the practice.
Budget **60–90 minutes**.

| | Before class | Used in the practice for |
|---|---|---|
| **1** | Read the paper | reproducing one of its results |
| **2** | Get both datasets | that, and applying the method to your own angle |

---

## 1. The reading — 45–60 min

**Ferman & Pinto (2019), *Inference in Differences-in-Differences with Few Treated Groups and Heteroskedasticity***
[Read the article](https://doi.org/10.1162/rest_a_00759)

Read for the **argument**, not for coverage:

| | What to look for |
|---|---|
| **1** | The research question, in one sentence |
| **2** | The method or design, and why they chose it |
| **3** | The strongest single piece of evidence |
| **4** | One limitation you would raise as a referee |

**Annotate as you go.** You will be asked what you underlined and why.

---

## 2. The data — 10 min

You need **two** datasets in the practice, and both should be on your machine before you arrive.

### a) The paper's replication package

This is what you reproduce in the first twenty minutes of the practice.

**Harvard Dataverse: [10.7910/DVN/PIAZWN](https://doi.org/10.7910/DVN/PIAZWN)**

Download it once, and unzip it here — the folder is git-ignored, so nothing large is committed:

```text
11-causal-inference-did/data/replication/
```

Keep the authors' own folder structure and README.

### b) The course data, for your own angle

This is what you apply the method to in the second half.

```python
import qmib

data = qmib.load("core")      # what the lecture uses
core = qmib.load("core")                 # shared by every group
mine = qmib.load("angle_c_country")      # YOUR angle — see your dictionary

print(data.shape, core.shape, mine.shape)
```

The spine's post-2021 structural break, treated as a policy change.

> Run this **before** class. It downloads once and caches as parquet, so the practice works
> whatever the room's wifi is doing. `qmib.catalog()` lists everything available.

Your group's file, columns, units and traps are in your
[data dictionary](../../data/spine/dictionaries/).

---

## 3. Self-check — 15 min

Answer on paper. If you cannot, that is what the lecture is for.

1. In one sentence: what does this session's method let you claim that the previous one did not?
2. What must be true of your data for it to apply?
3. Which claim in the paper rests on this method — and how hard does it lean on it?

---

## Arrive with

- [ ] The paper read and annotated
- [ ] The replication package downloaded and unzipped
- [ ] `qmib.load()` run at least once, so the cache exists
- [ ] Your self-check answers, on paper

---

[Session 11 overview](../README.md) · [The lecture](../01-lecture/README.md) ·
[The practice](../02-practice/README.md)
