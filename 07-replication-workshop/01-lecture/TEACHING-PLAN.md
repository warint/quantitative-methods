# Session 07 — teaching plan (3 hours, workshop)

# Four Papers, One Toolkit

> **Instructor page.** The student-facing pages are [`README.md`](README.md) and
> [`../02-practice/README.md`](../02-practice/README.md); the slides are
> [`MATH60033A-S07-Lecture.qmd`](MATH60033A-S07-Lecture.qmd).

workshop 180 min · no lecture · students work alone or in teams
*What do the course's models say on the papers' data?*

---

## Before the day

- Run every script once on your own machine, from the repository root:
  `python 07-replication-workshop/02-practice/starter/r1_fraiberger_2021.py`, then `r3`, `r4` and `r5`.
  Each takes two seconds. If a Dataverse package has been updated since 24 September 2026 and a
  number moves, correct the guide and the slide to match the script.
- Remind the class two days ahead that the four packages must be downloaded **before** they
  arrive (the pre-session page). The Saganowski package is 160 MB; a room
  of forty laptops downloading them at 15:30 is the one way this afternoon fails.

## The first fifteen minutes — the only time you talk

Five slides, no more: *No new method*, *The three hours*, *Alone or as a team*, *Part 0*, *One step
at a time*. Then everyone runs `check_setup.py`. Walk the room: a `MISSING` line is the only thing
worth your attention in the first half hour.

## While they work

| Clock | Where most of the room should be | Watch for |
|---|---|---|
| 0:15 – 0:55 | Paper 1 · Fraiberger | Steps 2–8 — a slope of 0.07 points with R² ≈ 0.001, and P(up day) moving only from 0.50 to 0.54. Ask: *significant, but does it matter?* |
| 0:55 – 1:35 | Paper 2 · Saganowski | Steps 3–11 — size lowers the chance of dissolving (binary) yet pushes groups toward **shrinking** (ordinal, multinomial). Ask: *which model answers which question?* |
| 1:45 – 2:15 | Paper 3 · Blonigen & Piger | Step 8 — 765 pairs for 56 candidates: the penalised models edge OLS on held-out pairs, and the lasso keeps 43. Ask: *is a dropped variable "no effect"?* |
| 2:15 – 2:50 | Paper 4 · Topalova & Khandelwal | Step 10 — with ~10,000 rows for 16 candidates, the penalties keep everything and tie OLS. Ask: *when does a penalty help, and when not?* |

At **2:15**, remind split-and-teach teams to stop and teach each other.

## Misconception to pre-empt

> That a model run on a paper's data reproduces "the paper's result". It does not: it is the
> course's model on their data, answering a simpler question. Say it once, at 1:45, to the whole
> room.

## The last ten minutes

The log, committed and pushed. A block that reads each model precisely, in a sentence with units,
earns full marks; say so again, because students will otherwise pad.

## Midterm

The midterm on 28 October covers sessions 1 to 6. This workshop is its revision: every block of the
log names the session idea it reused.
