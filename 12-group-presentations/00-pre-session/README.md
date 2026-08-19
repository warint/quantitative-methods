# Session 12 — Preparation

> There is no reading and no new material. This is production week.

---

## Checklist

Work through this in order. Items 1–3 were drafted in the
[Session 11 lab](../../11-forecasting-drift-and-governance/02-lab/README.md); here you finish them.

### 1. Model governance file  *(7 of the team work's 20)*

- [ ] All seven sections of [`governance-file-template.md`](../../11-forecasting-drift-and-governance/02-lab/governance-file-template.md) completed
- [ ] Section 5 (Limitations) is specific and numerical — no "may not generalise"
- [ ] Section 6 (Monitoring) names a threshold, not just a quantity
- [ ] Reproducibility statement tested from a clean clone
- [ ] LLM-use paragraph written

### 2. Reproducible analysis  *(10 of 30)*

- [ ] Runs end-to-end from `git clone` + `pip install -r requirements.txt`
- [ ] Every random seed set explicitly
- [ ] Data read from a local cache, never downloaded at runtime
- [ ] Every preprocessing step inside the CV loop (or justified in §3 of the governance file)
- [ ] Backtest results and Diebold–Mariano statistic reported
- [ ] Shift diagnostic (train-vs-deploy classifier AUC) reported

### 3. Revised Session 1 memo + change log  *(5 of 30)*

- [ ] Original memo included, unedited
- [ ] Revised memo
- [ ] One-page change log: what changed, and **which session changed it**

### 4. The deck and defence  *(5 of 30)*

- [ ] Eight slides maximum
- [ ] Slide 1: the decision. Slide 2: your recommendation
- [ ] One slide titled **"What would change our mind"**
- [ ] No code anywhere
- [ ] Every figure captioned with what it *shows*
- [ ] Every number carries an interval or a benchmark
- [ ] Rehearsed to **8 minutes**. Not 9

### 5. The defence

- [ ] A two-sentence answer to *"why should I believe this?"*
- [ ] An answer to each question in the [session README](../README.md#questions-you-will-be-asked)
- [ ] Someone in the group can explain every line of code

---

## Rehearsal advice

Present to another group before class. If they cannot restate your recommendation after slide 2,
the deck is not finished — the problem is almost never the analysis.

The commonest failure is spending seven minutes on method and one on the recommendation. Invert it.
A decision-maker needs to know *what to do* and *how much to trust it*; the method is what you
defend under questioning, not what you lead with.

---

[Back to session 12](../README.md)
