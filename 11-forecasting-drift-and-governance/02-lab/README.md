# Session 11 — Group lab (second half, ~90 min)

# Final-project workshop: backtest, shift diagnostic, governance file

---

## The theme of this session

> # If this were a monitoring dashboard for a European agency, would you sign it?

All ten groups attack this question. Each answers it with **its own angle** and its own slice of the
data spine, and the last twenty minutes assemble the five answers into one.

Backtest properly (purge and embargo where features are windowed), run Diebold-Mariano against a hard benchmark, run the train-versus-deploy shift diagnostic, and complete the governance file.

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

Groups of 3-4, working on **your own final project**. This is a working session, not
a new exercise: you leave with three of the four Session 12 deliverables substantially complete. The
instructor circulates; use the time to get the hard questions answered while help is available.

Bring your draft analysis. Groups without one will spend the session writing it and will be behind.

---

## Tasks

1. **Backtest design.** Write down your CV scheme and justify, in two sentences, why it mirrors deployment. Add a purge and embargo if your features are windowed. Have another group try to find a leak in it.
2. Implement the backtest. Report performance against a named, hard benchmark.
3. Run the **Diebold-Mariano** test on your loss differential with a HAC variance and lag truncation $\ge h-1$. Report the statistic and what it licenses you to claim.
4. **Shift diagnostic.** Train a classifier to separate your training period from your evaluation period. Report its AUC and interpret it. If the AUC is high, say what you will do about it.
5. Complete the **model governance file** using the template and the seven headings in section 11.4. This is a graded deliverable in its own right.
6. Re-read your Session 1 memo. Draft the one-page change log: what you would now write differently, and which session changed it.
7. Sketch slide 1 (the decision) and slide 2 (your recommendation). Show them to another group. If they cannot restate your recommendation, rewrite it.

---

## Deliverable

By the end of this session, `02-lab/submissions/group-XX/` should contain a
draft **governance file**, your **backtest results with the DM test**, and the **shift diagnostic**.
These carry forward directly into the Session 12 submission — nothing here is thrown away.

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

- "Design a monitoring plan for a model that forecasts regional unemployment quarterly. What do I track, and what triggers a review?"
- "Review my backtest for look-ahead bias. Be specific about which line leaks: <paste>"
- "Explain when the Diebold-Mariano test is invalid, and what to use instead."
- "Read my governance file's Limitations section and tell me what a regulator would say is missing."

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

Fill in this session's row of your group's role log
(`assessment/role-logs/gXX.md`): who was **Driver** (wrote the code), **Analyst** (decided the
specification and owns the interpretation), **Reporter** (wrote the three sentences). Roles rotate
every week.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis on your angle |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + instructor synthesis |

---

[Back to session 11](../README.md) · [<- Lecture notes](../01-lecture/README.md)
