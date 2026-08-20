# Confidential peer assessment

**Complete once, at the end of the semester. Five minutes.**

Your responses go to the instructor only. Your teammates never see who said what.

---

## What this is for

Group marks reward the group. This form is how the course checks that the group mark reflects
what each member actually did.

**Read this before you rate anyone:**

- **The default is that everybody gets the group mark.** A rating below the group's own average
  changes nothing on its own. It only has any effect if the git contribution history *independently*
  shows the same pattern. Two signals must agree.
- **You are not deciding anyone's mark.** You are giving the instructor one of two inputs.
- **Rate the work, not the person.** Someone you found difficult who did their share should be
  rated on their share.
- **Inflation defeats the purpose.** If you rate everyone 5 regardless, you are choosing to let a
  free-rider take your mark. That is your choice to make, but make it knowingly.

---

## Who you rate

You rate your **two teammates**. You do not rate yourself.

---

## The four dimensions

Rate each teammate 1–5 on each. Use the whole scale.

| | 1 | 3 | 5 |
|---|---|---|---|
| **Preparation** | Arrived without the reading or the self-check done, repeatedly | Usually prepared | Consistently arrived ready to start immediately |
| **Contribution to the analysis** | Waited to be told what to do | Did their share of what was decided | Shaped *what* was done — proposed specifications, spotted problems |
| **Reliability** | Missed agreed work, late, absent without warning | Generally delivered | Always delivered what they said, when they said |
| **Understanding** | Could not explain what the group produced | Could explain their own part | Could explain and defend the whole group's work |

**Understanding is the one that matters most.** It is the dimension the random presenter draw and
the Session 12 defence are designed to test independently.

---

## Your form

Copy this block once **per teammate** and send it to the instructor
(`thierry.warin@hec.ca`) by the Session 12 deadline.

```
Your student ID:        ________
Teammate's student ID:  ________
Teammate's name:        ________________________

Preparation                  (1–5): ___
Contribution to the analysis (1–5): ___
Reliability                  (1–5): ___
Understanding                (1–5): ___

One thing this person did that made the work better:
________________________________________________________________
(If there is genuinely nothing to record, write "nothing".)

(Optional) One thing that would have helped:
________________________________________________________________
```

The first free-text box is **required**, and `nothing` is a permitted answer. Where there is a
contribution, naming it takes thirty seconds and makes the whole exercise fairer, because it forces
a specific memory rather than a general impression.

Where there is not, say so plainly. Do not invent a sentence you do not mean in order to fill the
box: a student who contributed nothing has nothing to record here, and the record should say that.
Their mark does not depend on this form in any case — a student who did none of the work fails the
individual participation bar and the Session 12 defence on their own evidence, which is a matter of
what they did, not of how generously a teammate wrote about them.

---

## What happens next

1. The instructor enters the responses into `ratings.csv`.
2. `python scripts/assess.py multipliers` computes a relative score for each student —
   their mean rating divided by their group's mean rating — and proposes a multiplier.
3. **Any multiplier below 1.00 requires the git contribution report to flag the same student.**
   If the peer ratings and the commit history disagree, no automatic change is made; the
   instructor reviews the case.
4. Students whose multiplier is not 1.00 are told the basis and may appeal.

### The bands

| Relative score | Multiplier |
|---|---|
| ≥ 0.90 | **1.00 — no change** (the overwhelming majority) |
| 0.75 – 0.90 | 0.90 |
| 0.60 – 0.75 | 0.80 |
| < 0.60 | 0.70 (floor) |
| ≥ 4.5/5 while a teammate falls below 1.00 | 1.05 |

The multiplier applies to the group mark. Nobody can lose more than 30%, and the 1.05 exists so
that carrying a group is recognised rather than merely endured.

---

## Appeals

If your multiplier is not 1.00 you will be told why, and you may ask for a review within seven
days. The review looks at all three records together: the peer ratings, the git history, and the
push grid. Bring anything else you think is relevant — the point is to get it right, not to defend
the arithmetic.

---

*See [`GROUP-ASSESSMENT.md`](../../GROUP-ASSESSMENT.md) for the full policy.*
