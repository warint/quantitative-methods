# Session 07 — teaching plan (3 hours, workshop)

# Four Papers, One Toolkit

> **Instructor page.** The student-facing pages are [`README.md`](README.md) and
> [`../02-practice/README.md`](../02-practice/README.md); the slides are
> [`MATH60033A-S07-Lecture.qmd`](MATH60033A-S07-Lecture.qmd).

workshop 180 min · no lecture · students work alone or in teams
*What do the course's models say on the papers' data?*

---

## Before the day

- Do Part 0 yourself, as a student would: an empty folder outside the repository, a fresh
  `.venv`, `pip install pandas statsmodels scikit-learn matplotlib`, the scripts' zip from the site,
  then `python check_setup.py` and `python r1_fraiberger_2021.py`, `r2`, `r3`, `r4`. Each takes a
  few seconds. If a package update moves a number, correct the guide and the slide to match the
  script.
- After editing a script or the data: `python scripts/build_session07_data.py` (the CSVs), then
  `python scripts/build_docs.py` and push — the students' scripts read the site, not the repo.
- Remind the class two days ahead to set up the folder **before** they arrive (the pre-session
  page). Forty laptops installing pandas and statsmodels at 15:30 is the one way this afternoon
  fails. On the day they need the internet: the data is read from the site.

## The first fifteen minutes — the only time you talk

Five slides, no more: *No new method*, *The three hours*, *Alone or as a team*, *Part 0*, *One step
at a time*. Then everyone runs `check_setup.py`. Walk the room: a `MISSING` line is the only thing
worth your attention in the first half hour.

## While they work

| Clock | Where most of the room should be | Watch for |
|---|---|---|
| 0:15 – 0:55 | Paper 1 · Fraiberger | Steps 2–8 — a slope of 0.07 points with R² ≈ 0.001, and P(up day) moving only from 0.50 to 0.54. Ask: *significant, but does it matter?* Steps 12–14 — the VIX makes **both** down and up days more likely: ask *what can the multinomial see that the ordinal cannot?* |
| 0:55 – 1:35 | Paper 2 · Saganowski | Steps 3–11 — size lowers the chance of dissolving (binary) yet pushes groups toward **shrinking** (ordinal, multinomial). Ask: *which model answers which question?* |
| 1:45 – 2:15 | Paper 3 · Blonigen & Piger | Step 8 — 765 pairs for 56 candidates: the penalised models edge OLS on held-out pairs, and the lasso keeps 43. Ask: *is a dropped variable "no effect"?* |
| 2:15 – 2:50 | Paper 4 · Topalova & Khandelwal | Steps 6–14 — the same tariff read three ways: odds of being above the median, the productivity thirds, and (multinomial) who owns the firm. Step 19 — with ~10,000 rows for 16 candidates, the penalties keep everything and tie OLS. Ask: *when does a penalty help, and when not?* |

At **2:15**, remind split-and-teach teams to stop and teach each other.

## Misconception to pre-empt

> That a model run on a paper's data reproduces "the paper's result". It does not: it is the
> course's model on their data, answering a simpler question. Say it once, at 1:45, to the whole
> room.

## The last ten minutes

Paper 4 runs to the end; there is nothing to hand in. Close on *What loses marks on the midterm*:
a model read precisely, in a sentence with units, earns full marks — say so again, because students
will otherwise pad.

## Midterm

The midterm on 28 October covers sessions 1 to 6. This workshop is its revision: every model of
sessions 3 to 5 comes back once, on real data.
