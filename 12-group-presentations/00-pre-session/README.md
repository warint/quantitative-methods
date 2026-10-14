# Session 12 — Preparation

> There is no reading and no new material. This is production week.

---

## Checklist

Work through this in order. The team work is the SDAfrique methods paper
([brief](../../assessments/team-work/README.md)): today you present and defend it (**4** of the 20);
the finished paper and its repository are due **Sunday 13 December, 23:59** (**16** of the 20).
The governance content, backtest and shift diagnostic were drafted in the
[Session 11 practice](../../11-causal-inference-did/02-practice/README.md).

### 1. The paper, as a draft you can defend

- [ ] Question, literature argument, data, derived method and main result in place
- [ ] Section 6 carries the governance content — all seven headings of
      [`governance-file-template.md`](../../11-causal-inference-did/02-practice/governance-file-template.md)
- [ ] Limitations specific and numerical — no "may not generalise"
- [ ] Monitoring names a threshold, not just a quantity

### 2. The repository

- [ ] Runs end-to-end from `git clone` + `pip install -r requirements.txt`
- [ ] Every random seed set explicitly
- [ ] Data read from a local cache, never downloaded at runtime
- [ ] Every preprocessing step inside the CV loop
- [ ] Backtest results and Diebold–Mariano statistic reported
- [ ] Shift diagnostic (train-vs-deploy classifier AUC) reported

### 3. The deck  *(the presentation and defence: 4 of the 20)*

- [ ] Eight slides maximum
- [ ] Slide 1: the decision. Slide 2: your recommendation
- [ ] One slide titled **"What would change our mind"**
- [ ] No code anywhere
- [ ] Every figure captioned with what it *shows*
- [ ] Every number carries an interval or a benchmark
- [ ] Rehearsed to **8 minutes**. Not 9

### 4. The defence

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
