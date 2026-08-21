# Session 03 — Group lab (second half, ~90 min)

# A Mincer equation, and an honest account of what it shows

---

## The theme of this session

> # Which of these differences would survive a referee?

All ten groups attack this question. Each answers it with **its own angle** and its own slice of the
data spine, and the last twenty minutes assemble the five answers into one.

Same specification as Session 02, now with robust and clustered standard errors, a variance-inflation check, and a signed omitted-variable argument. Name the level at which you cluster and defend it.

Your angle, your unit of analysis and your data are fixed for the semester:
**[RESEARCH-MANDATES.md](../../RESEARCH-MANDATES.md)**.

> **If your angle cannot answer the theme this week, say so and show why.** That is a contribution,
> not a failure — and it is graded as one.

---

## Method exercise

The tasks below build the machinery. Do them on the teaching dataset if you need to see the method
work on known ground first, then turn it on your own angle. The reported result must be from **your
angle**.

## Brief

Groups of 3-4. You will estimate a wage equation, compute three different standard
errors for the same coefficient, and write a paragraph that a careful referee would accept.

---

## Tasks

1. Estimate `log(wage) ~ education + experience + experience**2 + female`. Report coefficients with classical standard errors.
2. Re-estimate with HC1 robust standard errors and with standard errors clustered by industry (or region). Present all three in one table. Which changes most, and why?
3. Plot residuals against fitted values and against experience. Diagnose: is the heteroskedasticity you find consistent with the robust SEs being larger or smaller?
4. Compute the variance inflation factor for each regressor by hand (regress each on the others). Reconcile with `statsmodels`.
5. **OVB exercise.** Drop `female` from the model. By how much does the education coefficient move? Use the OVB formula to *predict* the movement before you run it, then check.
6. Write the interpretation paragraph. It must state what the coefficient identifies, name at least two threats to a causal reading, and avoid the word 'effect' unless you can defend it.

---

## Deliverable

`02-lab/submissions/group-XX/mincer.md` with the three-column results table,
two diagnostic plots, your predicted-vs-actual OVB calculation, and the interpretation paragraph.
The paragraph is worth as much as the code.

Create your group's folder as `submissions/group-XX/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this lab requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "My robust standard errors are SMALLER than my classical ones. Is that possible? Under what conditions?"
- "Critique this sentence as a hostile referee: '<paste your interpretation paragraph>'"
- "Explain the difference between clustering at the individual level and at the industry level for panel wage data."

**Required in every deliverable:** at least one instance where you identified an LLM output as
wrong, unverifiable, or misleading — with an explanation of how you established that.

---

## The two-minute report

> **The presenter is drawn at random when your group is called.** Any of the three of you may have
> to give this report, so all three must understand the analysis, the number, and what would
> undermine it. See [`GROUP-ASSESSMENT.md`](../../GROUP-ASSESSMENT.md).

**One slide. Three sentences.**

1. **What I did.** *"We regressed X on Y for [our unit], partialling out [Z]."*
2. **The number.** One figure or estimate, with its uncertainty or its benchmark.
3. **The catch.** What surprised you, what you cannot claim, or where your data failed you.

No method exposition — everyone learned it ninety minutes ago. No code on the slide. **Sentence 3
earns the slot:** a result plus what would undermine it is worth more than a result alone.

## Before you leave the room

**Every member commits and pushes from their own machine.** There are no assigned roles — work on
it together — but all three of you appear in the history, every week:

```bash
git add -A && git commit -m "..." && git push
```

`python scripts/assess.py contributions` prints a per-member, per-week grid. A week where you
pushed nothing is visible, and it is the kind of thing worth fixing in week four rather than week
eleven.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis on your angle |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + instructor synthesis |

---

[Back to session 03](../README.md) · [<- Lecture notes](../01-lecture/README.md)
