# Session 11 — teaching plan (first half, 90 min)

# Causal Inference II: Difference-in-Differences

> **Instructor page.** The student-facing companion is [`README.md`](README.md); the deck is
> [`MATH60033A-S11-Lecture.qmd`](MATH60033A-S11-Lecture.qmd).

lecture 90 min · practice follows on
*What would have happened otherwise?*

---

## Opening

Put the session question on the board and let them attempt an answer before any method appears:

> **What would have happened otherwise?**

Then the pre-session paper: ask what they underlined, and why. Two minutes, three students. It
establishes that the reading is load-bearing rather than decorative.

---

## Board plan

| Minutes | |
|---|---|
| **0–8** | The question, and the paper they read. Part 1: why time can replace measurement; the two differences, and why one is not enough. |
| **8–15** | Card and Krueger: ask for the sign before showing it; the +2.76 comes from Pennsylvania falling. The interaction regression cell by cell (`Treated × Post` is 1 in one cell only), the words, parallel trends stated exactly. |
| **15–25** | Example 1, housing: after-only −25, before-after +20, DiD −10.5. Ask the room what each naive comparison mixes in. No code on screen. |
| **25–33** | Example 2: six years, two cities; the event study catches B. Ask them to read the pre-years *before* showing the estimate. |
| **33–45** | Example 3, AI strategies: the adoption table first; the forbidden comparison (+3 becomes −1) and when it matters; TWFE 2.81 against Callaway–Sant'Anna 2.20 and the other repairs in one table; then the sensitivity plot, reading $M$ aloud. |
| **45–52** | Matching or DiD; what DiD cannot fix; the seven steps. |
| **52–56** | A third solution: differencing removes what is constant about a unit, measured or not. |
| **56–82** | Solution 3 in Python, a DiD from start to finish: panel and adoption table, the plot, one clean 2×2, the event study, all cohorts, the Bacon decomposition (the −1.60 comparison), sensitivity. Read each **objective** aloud before running the cell. |
| **82–90** | Your turn: tasks 2 (a pre-trend) and 3 (the forbidden comparison) in the room; the rest at home. Hand off to the practice. |

---

## Run the code live

The examples are taught from pictures and tables; the code waits until minute 56, and it does not
replay them. The students carry out a difference-in-differences on new data: a staggered rollout of
export desks. Open the VS Codium terminal, activate `.venv`, and run the first cell in front of them (it
writes the data file the later cells read) before they run the rest themselves. Before each cell,
ask what the step is **for**. Type the mistakes as well as the fixes: an already-treated cohort used
as the control group, a 2×2 read without its pre-period.

---

## Put this to the room

*"What would have to be true of your own data for this method to apply — and is it?"*

Do not accept "it probably is". Push until someone names the specific column and the specific
assumption.

---

## Misconception to pre-empt

A DiD with no evidence on parallel trends. Say it explicitly, early, and once more at the end. Misconceptions that go
unnamed in the lecture reappear in the deliverable.

---

## Leave on the board for the practice

The method's core expression, and the one diagnostic that tells you it has failed.

---

[Student companion](README.md) · [Practice brief](../02-practice/README.md)
