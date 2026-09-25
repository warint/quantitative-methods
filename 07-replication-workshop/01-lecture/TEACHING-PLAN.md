# Session 07 — teaching plan (3 hours, workshop)

# Replication Workshop: Five Papers, One Toolkit

> **Instructor page.** The student-facing pages are [`README.md`](README.md) and
> [`../02-practice/README.md`](../02-practice/README.md); the slides are
> [`MATH60033A-S07-Lecture.qmd`](MATH60033A-S07-Lecture.qmd).

workshop 180 min · no lecture · students work alone or in teams
*Can you reproduce what the papers claim, with only what you have learned?*

---

## Before the day

- Run every script once on your own machine, from the repository root:
  `python 07-replication-workshop/02-practice/starter/r1_fraiberger_2021.py`, and so on to `r5`.
  Each takes two seconds. If a Dataverse package has been updated since 24 September 2026 and a
  number moves, correct the guide and the slide to match the script.
- Remind the class two days ahead that the four packages must be downloaded **before** they
  arrive (the pre-session page). The Amsili and Saganowski packages are 220 MB and 160 MB; a room
  of forty laptops downloading them at 15:30 is the one way this afternoon fails.

## The first fifteen minutes — the only time you talk

Five slides, no more: *No new method*, *The three hours*, *Alone or as a team*, *Part 0*, *One step
at a time*. Then everyone runs `check_setup.py`. Walk the room: a `MISSING` line is the only thing
worth your attention in the first half hour.

## While they work

| Clock | Where most of the room should be | Watch for |
|---|---|---|
| 0:15 – 0:45 | R1 · Fraiberger | Step 2 — calendar days versus trading days. Ask: *why are there returns on Saturdays?* (Korean Saturday sessions.) |
| 0:45 – 1:15 | R2 · Amsili | Step 9 — the one soil. Ask: *would you delete row 5986?* The answer you want is "no — I would report both fits and go and look at it". |
| 1:15 – 1:45 | R3 · Saganowski | Step 6 — accuracy below the base rate with significant coefficients. The most useful confusion of the afternoon; let them sit in it. |
| 1:55 – 2:25 | R4 · Blonigen & Piger | Step 9 — the tax-haven dummy. Ask what changed in the world between the paper's data and 2019. |
| 2:25 – 2:50 | R5 · Topalova & Khandelwal | Step 9 — the sign flip between pooled OLS and fixed effects. Ask which estimate they would defend to a referee, and why random effects sits where it does. |

At **2:25**, remind split-and-teach teams to stop and teach each other.

## Misconception to pre-empt

> That a replication which lands on the published number has *confirmed* the paper. It has
> confirmed the arithmetic. R1 lands on 0.049 partly by luck; R2 lands exactly and still hides a
> single-observation interaction. Say it once, at 1:45, to the whole room.

## The last ten minutes

The log, committed and pushed. A block that says precisely where a replication breaks earns full
marks; say so again, because students will otherwise pad.

## Midterm

The midterm on 28 October covers sessions 1 to 6. This workshop is its revision: every block of the
log names the session idea it reused.
