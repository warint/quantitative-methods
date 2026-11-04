# Session 08 — Group practice (second half, ~90 min)

# K-Nearest Neighbours and the Bias–Variance Trade-off

> **[Open the practice slides](https://warint.github.io/quantitative-methods/session-08-practice.html)** ·
> source: [`MATH60033A-S08-Practice.qmd`](MATH60033A-S08-Practice.qmd)

---

## The theme of this session

> # Does flexibility buy you anything on your own data?

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
mkdir -p groups/A2026/group-XX/session-08
```

---

## The starter script

Work in a folder of your own, with `pandas numpy matplotlib scikit-learn` installed. Download
[`session08_practice.py`](https://warint.github.io/quantitative-methods/session-08/session08_practice.py)
(source: [`starter/session08_practice.py`](starter/session08_practice.py)), set
`MY_ANGLE` to your group's angle, and run it one part at a time. It reads both datasets from the
course site.

---

## 1 · Reproduce one result from the paper — 20 min

Take the result the pre-session reading rests on, and reproduce it — or establish that you cannot,
and say precisely where it breaks. A failed reproduction that is diagnosed earns full marks; one
that is not attempted earns none.

The paper is **Bluwstein, Buckmann, Joseph, Kapadia & Şimşek (2023), *Credit growth, the yield curve and financial crisis prediction: evidence from a machine learning approach*, Journal of International Economics 145**. Part 1 of the script fits a logit, KNN and a random forest to predict a crisis within two years (train 1870–1979, test 1980–2020), scores them by AUC, and ranks the predictors.

---

## 2 · Apply the method to your own angle — 35 min

Part 2 of the script merges `core.csv` with your angle (averaged to one row per country-year),
predicts `falling_behind_next`, and compares the logit with KNN on the last two years. Replace the
default predictor list with the ones your question needs, and report in the units of your own variables.

---

## 3 · Break one assumption — 15 min

Every method in this course rests on something. Find the assumption this one rests on hardest, break
it deliberately, and record what happened to your answer. **This is the part that carries the
marks.** Part 3 of the script has three ready to run: no standardising, fewer predictors, a random split.

---

## 4 · Write it down — 20 min

A 250-word note in your submissions folder:

- What you found, in units
- Which assumption you broke, and what it did
- What this result does **not** license you to claim

---

## Submitting

```bash
git add groups/A2026/group-XX/session-08
git commit -m "Session 08 practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

- Running KNN on unstandardised predictors
- Choosing $k$ on the test set
- Reporting accuracy with no benchmark
- Treating a low training error as evidence of anything

---

## After class, if you want it

The **[QMIB Lab for this session](https://warin.ca/qmib-labs/qmib-lab-08.html)** has a knowledge check on what you have just done. It is
optional, never a prerequisite for the next lecture, and never marked for correctness — a completed
report counts because attempting it is the engagement being measured.

---

[<- The lecture](../01-lecture/README.md) · [Session 08 overview](../README.md)
