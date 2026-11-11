# Session 10 — teaching plan (first half, 90 min)

# Causal Inference I: Counterfactuals, Randomisation, Matching

> **Instructor page.** The student-facing companion is [`README.md`](README.md); the deck is
> [`MATH60033A-S10-Lecture.qmd`](MATH60033A-S10-Lecture.qmd).

lecture 90 min · practice follows on
*Did the policy do anything, or were the groups different to begin with?*

---

## Opening

Put the session question on the board and let them attempt an answer before any method appears:

> **Did the policy do anything, or were the groups different to begin with?**

Then the pre-session paper: ask what they underlined, and why. Two minutes, three students. It
establishes that the reading is load-bearing rather than decorative.

---

## Board plan

| Minutes | |
|---|---|
| **0–10** | The question, and the paper they read. Part 1: two outcomes per firm, one observed; the words. |
| **10–20** | Naive = effect + selection bias, on the board, then the back-door picture. |
| **20–30** | Example 1, the firms: a coin recovers +2, self-selection says 5.3, the boxplot shows why. No code on screen. |
| **30–50** | Example 2, LaLonde: −\$8,498 → balance → score → overlap → love plot → +\$2,001 against +\$1,794. |
| **50–60** | Example 3, the HR course: matching works (5.3), then fails with perfect balance (9.0). Ask the room what is missing *before* showing the motivation plot. |
| **60–65** | Matching or regression; what matching does not fix. |
| **65–70** | One problem, two solutions: a trial removes selection by design, matching by assumption. |
| **70–80** | Solution 1 in Python, a trial from start to finish: baseline file, power, the draw, balance, the estimate, firms that refuse. |
| **80–90** | Solution 2 in Python, a match from start to finish: score, overlap, caliper, balance, ATT with a bootstrap interval, robustness. The real-data *Your turn* (LaLonde as a trial, then with the PSID) goes home or into the practice. Hand off. |

---

## Run the code live

The examples are taught from pictures and tables; the code waits until minute 65, and it does not
replay them. The students carry out each solution on new data: a trial they design and analyse, then
a match they build and check. Open the VS Codium terminal, activate `.venv`, and run the first cell
of each solution in front of them (it writes the data file the later cells read) before they run the
rest themselves. Before each cell, ask what the step is **for**. Type the mistakes as well as the
fixes: a draw replaced by a choice, `exports_after` in the score, a score changed after looking at
the ATT. Watching an error appear and be read is worth more than a slide saying errors happen.

---

## Put this to the room

*"What would have to be true of your own data for this method to apply — and is it?"*

Do not accept "it probably is". Push until someone names the specific column and the specific
assumption.

---

## Misconception to pre-empt

Reporting a matched estimate with no overlap diagnostic. Say it explicitly, early, and once more at the end. Misconceptions that go
unnamed in the lecture reappear in the deliverable.

---

## Leave on the board for the practice

Naive = ATT + selection bias, and the love plot: every standardised difference inside ±0.1,
checked **before** the outcome is looked at.

---

[Student companion](README.md) · [Practice brief](../02-practice/README.md)
