# Session 11 — teaching plan (first half, 90 min)

# Forecasting, Distribution Shift, and Model Governance

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · lab follows on
*If this were a monitoring dashboard for a European agency, would you sign it?*

---

## Opening

Put a model card on the screen with the Limitations section blank. Ask: *"would you sign this?"* Then: *"your name goes on it, and someone allocates fifty million euros on the strength of it."*

---

## Board plan

| Minutes | |
|---|---|
| **0–06** | The hook. |
| **06–32** | Backtesting. The three valid designs. Purge and embargo, and why $h-1$ is the minimum gap. **Point-in-time data** — macro series are revised, so today's vintage gives your model information no forecaster had. Then the rule: every preprocessing step inside the loop, *including factor extraction from Session 08*. |
| **32–52** | Diebold–Mariano. Loss differential, HAC variance, lag truncation $\ge h-1$. The cautions: invalid for nested models (use Clark–West), HLN correction in small samples. A lower RMSE without this is an anecdote. |
| **52–72** | The shift taxonomy. Then the classifier diagnostic — pool the two periods, label by period, try to predict the label. **If a classifier can tell your periods apart, so can your model's errors.** |
| **72–80** | Goodhart, stated precisely: when a measure becomes a target, the relationship the model learned is exactly the one agents are paid to break. A causal problem, not a monitoring problem. |
| **80–90** | The governance file, seven headings. Then the arc table — the whole course on one board. |

---

## Worked example — do this live

Diebold–Mariano on a toy series. Ten loss differentials with mean $0.42$ and HAC standard error $0.18$ give $\mathrm{DM} = 2.33$, $p \approx 0.02$. Then halve the sample and watch significance vanish — the point being how little power these tests have at realistic horizons.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Which of your own preprocessing steps is inside the cross-validation loop, and which is not?"* Go around the room by group. The ones who hesitate have found their bug.

---

## Misconception to pre-empt

> That retraining fixes concept drift. Retraining is necessary but not sufficient — if $P(Y|X)$ changed because the world changed, the model *form* may now be wrong. And under feedback, retraining chases a target you are moving.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

The arc table. Leave it up for the whole second half — it is what they present next week.

---

## If you are running short

Compress the shift taxonomy to the table plus the classifier diagnostic. The arc table is the emotional close of the course; do not cut it.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 11`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 11](../README.md) · [Lab](../02-lab/README.md)
