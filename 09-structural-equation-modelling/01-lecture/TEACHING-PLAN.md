# Session 09 — teaching plan (first half, 90 min)

# Structural Equation Modelling

> **Instructor page.** The student-facing companion is [`README.md`](README.md); the deck is
> [`MATH60033A-S09-Lecture.qmd`](MATH60033A-S09-Lecture.qmd).

lecture 90 min · practice follows on
*Can you measure something you cannot observe?*

---

## Opening

Put the session question on the board and let them attempt an answer before any method appears:

> **Can you measure something you cannot observe?**

Then the pre-session paper: ask what they underlined, and why. Two minutes, three students. It
establishes that the reading is load-bearing rather than decorative.

---

## Board plan

| Minutes | |
|---|---|
| **0–10** | The question, and the paper they read. Establish what is at stake. |
| **10–20** | Part 1: the language — one construct and its indicators, the five symbols, the five words, the two halves, corr = λᵢλⱼ. |
| **20–35** | Example 1, Holzinger–Swineford: look, draw, read the loadings, judge the fit, find the miss, compare three drawings. No code on screen. |
| **35–50** | Example 2, Political Democracy: paths, R², direct and indirect effects, the same-question covariances, the reversed arrow. |
| **50–60** | Example 3, the exporting survey: a known truth; SEM finds it, averaged items shrink it. Ask the room *why* before showing the attenuation. |
| **60–65** | What a good fit does not prove. |
| **65–90** | In class: the code behind the three examples. Students run each cell, check they get the lecture's numbers, then do the *Your turn* task. Circulate; hand off to the practice. |

---

## Run the code live

The examples are taught from pictures and tables; the code waits until minute 65. Then open the
VS Codium terminal, activate `.venv`, and run the first cell of each example in front of them before
they run the rest themselves. Type the mistakes as well as the fixes: a `=~` written as `~`, a
variable name misspelled in the description. Watching an error appear and be read is worth more
than a slide saying errors happen.

---

## Put this to the room

*"What would have to be true of your own data for this method to apply — and is it?"*

Do not accept "it probably is". Push until someone names the specific column and the specific
assumption.

---

## Misconception to pre-empt

Reporting fit indices without saying which threshold you applied. Say it explicitly, early, and once more at the end. Misconceptions that go
unnamed in the lecture reappear in the deliverable.

---

## Leave on the board for the practice

The method's core expression, and the one diagnostic that tells you it has failed.

---

[Student companion](README.md) · [Practice brief](../02-practice/README.md)
