<!-- authored: do not regenerate -->

# Session 11 — Group practice (second half, ~90 min)

# Causal Inference II: Difference-in-Differences

> **[Open the practice slides](https://warint.github.io/quantitative-methods/session-11-practice.html)** ·
> source: [`MATH60033A-S11-Practice.qmd`](MATH60033A-S11-Practice.qmd)

---

## The theme of this session

> # What is your counterfactual, and would anyone believe it?

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

---

## What you are doing

The lecture taught a difference-in-differences study in steps. The workshop runs those steps three
times: **in the paper** you read, **on known ground** (the course data, where the true effect is
known), then **on your own project** ([`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md)). Every
step has one objective, and the slides give the code, what each instruction does to meet it, and how
to read the output.

| Minutes | Step | Objective |
|---|---|---|
| 00–20 | 1 · Reproduce | find the DiD inside the paper: treated, controls, dates, estimate, parallel-trends evidence; reproduce one number |
| 20–40 | 2 · Known ground | on `qmib.load("angle_c_country")`: the adoption table, TWFE beside Callaway–Sant'Anna, the event study and a breakdown value |
| 40–55 | 3 · Your project | map your data onto four columns (unit, time, outcome, adoption year) and rerun step 2, or say precisely why the design cannot apply |
| 55–70 | 4 · Break one assumption | the dates, the controls, the scale or the trends; put both estimates in one table |
| 70–90 | 5 · Write, and report | 250 words, then two minutes to the room |

The deliverable is not a printout. It is a **decision**, with the reason written down.

---

## Before you start

Everyone in the group pushes at least once this session. Replace `XX` with your group number —
group 07 uses `group-07`.

```bash
git checkout -b group-XX
mkdir -p groups/A2026/group-XX/session-11
```

---

## 1 · Reproduce — 20 min

**Objective:** recognise the design when someone else builds it. Answer from the paper: what is
treated and what is the control group; what are the dates, and is adoption staggered; which
coefficient is the estimate, in what units; what evidence is shown for parallel trends; what could
have changed at the same time. Then reproduce one number. A failed reproduction that is diagnosed
earns full marks; one that is not attempted earns none.

The paper is **Cavallo, Gopinath, Neiman & Tang (2021), *Tariff Passthrough at the Border and at the Store: Evidence from US Trade Policy*, American Economic Review: Insights 3(1)**. Its replication package ([10.7910/DVN/JV7FCH](https://doi.org/10.7910/DVN/JV7FCH)) should already be unzipped at `11-causal-inference-did/data/replication/`.

---

## 2 · Known ground — 20 min

**Objective:** get the study working where the answer is known (+2.4 points) before trusting it where
it is not. Three cells, on the slides: the panel and the adoption table (2a), the cohorts plotted and
TWFE beside Callaway–Sant'Anna (2b), the event study and Rambachan–Roth (2c). The first cell writes
`ai_panel.csv`; the others read it.

---

## 3 · Your project — 15 min

**Objective:** decide whether your data can support the design. You need a unit, a time, an outcome
and an adoption year (0 if never treated). Stop and write it down if no unit is ever treated, none stays
untreated, or no cohort has a year before its treatment.

---

## 4 · Break one assumption — 15 min

**Objective:** find which choice the estimate leans on hardest. Change **one** on purpose — the
adoption dates, the control group (`control_group="not_yet_treated"`), the scale (logs) or the size of
the allowed violation (`M`) — and put the two estimates side by side in one table. **This is the part
that carries the marks.**

---

## 5 · Write it down — 20 min

A 250-word note in your submissions folder, in this order:

1. The design: treated, controls, dates, and the adoption table in one line
2. What you found, in units, with its interval, and TWFE beside it
3. The parallel-trends evidence: the pre-period, and the breakdown value
4. Which assumption you broke, and what it did to the number
5. What this result does **not** license you to claim

---

## Submitting

```bash
git add groups/A2026/group-XX/session-11
git commit -m "Session 11 practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

- A DiD with no evidence on parallel trends
- Reading the post-treatment dummy as the effect
- Two-way fixed effects alone under staggered adoption
- Claiming a causal effect the design cannot deliver

---

## After class, if you want it

The **[QMIB Lab for this session](https://warin.ca/qmib-labs/qmib-lab-11.html)** has a knowledge check on what you have just done. It is
optional, never a prerequisite for the next lecture, and never marked for correctness — a completed
report counts because attempting it is the engagement being measured.

---

[<- The lecture](../01-lecture/README.md) · [Session 11 overview](../README.md)
