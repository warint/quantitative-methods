# Session 07 — Group practice (second half, ~90 min)

# Principal Component and Factor Analyses

> **[Open the practice slides](https://warint.github.io/quantitative-methods/session-07-practice.html)** ·
> source: [`MATH60033A-S07-Practice.qmd`](MATH60033A-S07-Practice.qmd)

---

## The theme of this session

> # How many distinct dimensions does your angle really have?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

---

## What you are doing

The lecture showed the method on the session's dataset. You now apply it to **your own angle**, and
to the question your group is actually trying to answer
([`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md)).

The deliverable is not a printout. It is a **decision**, with the reason written down.

---

## Before you start

Everyone in the group pushes at least once this session. Replace `XX` with your group number —
group 07 uses `group-07`.

```bash
git checkout -b group-XX
mkdir -p groups/A2026/group-XX/session-07
```

---

## 1 · Reproduce one result from the paper — 20 min

Take the result the pre-session reading rests on, and reproduce it — or establish that you cannot,
and say precisely where it breaks. A failed reproduction that is diagnosed earns full marks; one
that is not attempted earns none.

The paper is **Koopman & Mesters (2017), *Empirical Bayes Methods for Dynamic Factor Models***, and its replication package
([10.7910/DVN/NKWMQM](https://doi.org/10.7910/DVN/NKWMQM)) should already be unzipped at:

```text
07-pca-and-factor-analysis/data/replication/
```

The session's own dataset, for comparison:

```python
import qmib
data = qmib.load("movies")
```

---

## 2 · Apply the method to your own angle — 35 min

```python
core = qmib.load("core")
mine = qmib.load("angle_c_country")     # your angle — see your dictionary
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

Fit the session's method on your own data. Report what the lecture said to report, in the units of
your own variables.

---

## 3 · Break one assumption — 15 min

Every method in this course rests on something. Find the assumption this one rests on hardest, break
it deliberately, and record what happened to your answer. **This is the part that carries the
marks.**

---

## 4 · Write it down — 20 min

A 250-word note in your submissions folder:

- What you found, in units
- Which assumption you broke, and what it did
- What this result does **not** license you to claim

---

## Submitting

```bash
git add groups/A2026/group-XX/session-07
git commit -m "Session 07 practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

- Running PCA on unstandardised columns
- Retaining components by a rule you did not state
- Naming a component ("this is competitiveness") with no rotation caveat
- Reporting variance explained as though it measured correctness

---

[<- The lecture](../01-lecture/README.md) · [Session 07 overview](../README.md)
