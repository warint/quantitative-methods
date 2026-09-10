# Session 03 — teaching plan (first half, 90 min)

# Regression: Adequacy, Validity, and Robustness

> **Instructor page.** The student-facing companion is [`README.md`](README.md); the deck is
> [`MATH60033A-S03-Lecture.qmd`](MATH60033A-S03-Lecture.qmd).

lecture 90 min · practice follows on
*You have fitted a regression. Can it be trusted?*

---

## Opening

Put the session question on the board and let them attempt an answer before any method appears:

> **You have fitted a regression. Can it be trusted?**

Then the pre-session paper: ask what they underlined, and why. Two minutes, three students. It
establishes that the reading is load-bearing rather than decorative.

---

## Board plan

| Minutes | |
|---|---|
| **0–08** | The question, and the paper they read. Establish what is at stake. |
| **08–25** | **From data to models.** Scatter first, then least squares as the mean done conditionally. Fit it live and make someone say the slope **in units** — euros per index point. Show the intercept at $-86{,}118$ and refuse to interpret it. |
| **25–33** | **Why evaluate at all.** The regression table on screen: every number an estimate, every star a claim. Put the four questions on the board and leave them there for the rest of the hour. |
| **33–48** | **Adequacy.** RSE and $R^2$ from RSS and TSS, then adjusted $R^2$. Quote the RSE in euros, not the $R^2$ — it is the number a non-specialist can act on. |
| **48–68** | **Validity.** Residuals-versus-fitted **first**, as the instrument; then linearity, normality and constant variance read off it. Draw the funnel and the curve by hand before showing either. |
| **68–80** | **Robustness.** Leverage, then Cook's distance. Find the country-year at the top of the spike plot and look it up in front of them — the point is to investigate a row, not to delete it. |
| **80–90** | **Parsimony.** AIC and BIC as comparisons between models you already wrote down. Say why choosing the model is session 05's problem, and hand off to the practice. |

---

## Run the code live

Open the VS Codium terminal, activate `.venv`, and run the deck's examples in front of them. Type
the mistakes as well as the fixes: a forgotten `dropna` that silently drops a third of the panel,
and an intercept read out loud at a productivity index nobody in the data has. Watching an
error appear and be read is worth more than a slide saying errors happen.

---

## Put this to the room

*"What would have to be true of your own data for this method to apply — and is it?"*

Do not accept "it probably is". Push until someone names the specific column and the specific
assumption.

---

## Misconception to pre-empt

Reporting $R^2$ without a single diagnostic plot. Say it explicitly, early, and once more at the end. Misconceptions that go
unnamed in the lecture reappear in the deliverable.

---

## Leave on the board for the practice

$e_i = y_i - \hat y_i$, and the residuals-versus-fitted plot beside it. Every diagnostic in the
practice is that one picture asked a different question.

---

[Student companion](README.md) · [Practice brief](../02-practice/README.md)
