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
| **0–10** | The question, and the paper they read. Establish what is at stake. |
| **10–35** | Causal Inference: Logic and Tools — build it from intuition before notation. |
| **35–60** | Counterfactual Framework — derive it, then run it in Python on the session dataset. |
| **60–80** | The Rubin Causal Model — read the output in units, out loud. |
| **80–90** | What the method does **not** license. Hand off to the practice. |

---

## Run the code live

Open the VS Codium terminal, activate `.venv`, and run the deck's examples in front of them. Type
the mistakes as well as the fixes: a forgotten `dropna`, an unstandardised predictor. Watching an
error appear and be read is worth more than a slide saying errors happen.

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

The method's core expression, and the one diagnostic that tells you it has failed.

---

[Student companion](README.md) · [Practice brief](../02-practice/README.md)
