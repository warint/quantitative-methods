# Session 07 — teaching plan (3 hours, workshop)

# Five Papers, One Toolkit

> **Instructor page.** The student-facing pages are [`README.md`](README.md) and
> [`../02-practice/README.md`](../02-practice/README.md); the slides are
> [`MATH60033A-S07-Lecture.qmd`](MATH60033A-S07-Lecture.qmd).

workshop 180 min · no lecture · students work alone or in teams
*What do the course's models say on the papers' own data?*

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
| 0:15 – 0:45 | Paper 1 · Fraiberger | Steps 4–7 — a slope of 0.07 points with p ≈ 0, yet R² ≈ 0.001 and P(up day) moving only from 0.50 to 0.54. Ask: *significant, but does it matter?* |
| 0:45 – 1:15 | Paper 2 · Amsili | Steps 5–6 — the one Georgia clay soil. Ask: *would you delete it?* The answer you want is "no — I refit without it, report both, and it changes nothing here". Step 7: a significant squared term that adds 0.0003 to R². |
| 1:15 – 1:45 | Paper 3 · Saganowski | Steps 5–7 — size pushes groups toward **shrinking** (ordinal and multinomial) yet lowers the chance of dissolving (binary). Step 8: 46% accuracy against 37% for always guessing "dissolving" — better, but it almost never predicts growing. Ask: *which model answers which question?* |
| 1:55 – 2:25 | R4 · Blonigen & Piger | Step 9 — the tax-haven dummy. Ask what changed in the world between the paper's data and 2019. |
| 2:25 – 2:50 | Paper 5 · Topalova & Khandelwal | Step 4 — the tariff slopes collapse once year controls are in. Ask: *why is the paper's −0.48 so different?* Because it compares each firm with itself; the pooled model compares different firms. |

At **2:25**, remind split-and-teach teams to stop and teach each other.

## Misconception to pre-empt

> That a simple model's number is "the paper's result", or that the paper is wrong because the
> numbers differ. They answer different questions: a pooled slope compares different firms, the
> paper's compares each firm with itself. Say it once, at 1:45, to the whole room.

## The last ten minutes

The log, committed and pushed. A block that reads one model precisely and says honestly how it
differs from the paper earns full marks; say so again, because students will otherwise pad.

## Midterm

The midterm on 28 October covers sessions 1 to 6. This workshop is its revision: every block of the
log names the session idea it reused.
