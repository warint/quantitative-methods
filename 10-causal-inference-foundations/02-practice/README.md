# Session 10 — Group practice (second half, ~90 min)

# Causal Inference I: Counterfactuals, Randomisation, Matching

---

## The theme of this session

> # Can your project support a causal claim at all?

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
mkdir -p 10-causal-inference-foundations/02-practice/submissions/group-XX
```

---

## 1 · Reproduce one result from the paper — 20 min

Take the result the pre-session reading rests on, and reproduce it — or establish that you cannot,
and say precisely where it breaks. A failed reproduction that is diagnosed earns full marks; one
that is not attempted earns none.

```python
import qmib
data = qmib.load("core")
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
git add 10-causal-inference-foundations/02-practice/submissions/group-XX
git commit -m "Session 10 practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

- Reporting a matched estimate with no overlap diagnostic
- Matching on a variable affected by the treatment
- Calling an association causal because you controlled for something
- Omitting the balance table

---

[<- The lecture](../01-lecture/README.md) · [Session 10 overview](../README.md)
