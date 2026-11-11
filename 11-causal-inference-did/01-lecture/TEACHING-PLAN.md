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
| **0–8** | The question, and the paper they read. Part 1: why time can replace measurement; the two differences. |
| **8–15** | The interaction regression, the words, parallel trends stated exactly. |
| **15–25** | Example 1, housing: after-only −25, before-after +20, DiD −10.5. Ask the room what each naive comparison mixes in. No code on screen. |
| **25–33** | Example 2: six years, two cities; the event study catches B. Ask them to read the pre-years *before* showing the estimate. |
| **33–45** | Example 3, AI strategies: the adoption table first, then TWFE 2.81 against Callaway–Sant'Anna 2.20, then the sensitivity plot. |
| **45–57** | Example 4, exporters: why neither design applies; the three conditions; the ratio 4.6; then version B at 12.1 with the same F. Ask which condition failed *before* showing the diagram. |
| **57–62** | Matching, DiD or an instrument; what DiD cannot fix. |
| **62–66** | Two more solutions: differencing removes what is constant, an instrument uses only what an outside push caused. |
| **66–80** | Solution 3 in Python, a DiD from start to finish: panel and adoption table, the plot, one clean 2×2, the event study, all cohorts, sensitivity. |
| **80–90** | Solution 4 in Python, an instrument from start to finish: naive, balance and first stage, reduced form and ratio, two-stage least squares, whom it describes. Hand off to the practice. |

---

## Run the code live

The examples are taught from pictures and tables; the code waits until minute 62, and it does not
replay them. The students carry out each design on new data: a staggered rollout they analyse as a
difference-in-differences, then a randomly drawn voucher they use as an instrument. Open the
VS Codium terminal, activate `.venv`, and run the first cell of each design in front of them (it
writes the data file the later cells read) before they run the rest themselves. Before each cell,
ask what the step is **for**. Type the mistakes as well as the fixes: an already-treated cohort used
as the control group, a second stage run by hand with `smf.ols`.

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
