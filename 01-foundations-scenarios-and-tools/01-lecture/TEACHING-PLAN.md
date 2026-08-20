# Session 01 — teaching plan (first half, 90 min)

# Foundations: Scenarios, Tools, and the Supervised Learning Problem

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · practice follows on
the research mandates

---

## Opening

Put the two numbers on the board: **255.1 GW** and **20.9 GW**. Ask the room what they are. Someone will say 'US and EU compute in 2031'. Then ask: *is that a measurement, a forecast, or something else — and how would you know?* Let it run for three minutes. Nobody has the vocabulary yet. That is the point of the course.

---

## Board plan

| Minutes | |
|---|---|
| **0–05** | The hook. Do not resolve it. |
| **05–20** | Scenario vs forecast. Draw the timeline: fact-based prologue (Jan 2025–Jun 2026) | speculative path (Aug 2026–Mar 2031) | epilogue (Jun 2034). Mark **the seam**. Everything to the right is a parameter of a story. |
| **20–40** | The supervised learning problem. $Y = f(X) + \varepsilon$. Define each term slowly; students conflate $f$ and $\hat f$ all semester if you rush. |
| **40–65** | **Derive** that $\mathbb{E}[Y\mid X]$ minimises squared-error risk. Do the add-and-subtract trick on the board and show the cross term vanishing by the tower property. Land on $R(g) = \sigma^2 + \mathbb{E}[(\mathbb{E}[Y|X]-g)^2]$. |
| **65–80** | Prediction vs inference. Build the four-row table WITH the room — ask for the economic examples rather than supplying them. |
| **80–90** | Narrative claim → indicator → direction → trigger → falsifier. This is the practice brief, so do it once on the board with an example they did not choose. |

---

## Worked example — do this live

No arithmetic today. The live derivation IS the worked example: the vanishing cross term. Write $\mathbb{E}[(Y-\mathbb{E}[Y|X])h(X)] = 0$ and make them tell you which property of conditional expectation you just used.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"Give me an economic question that needs inference and one that needs prediction, and tell me what changes about how you would evaluate the model."* Take three answers. If all three are prediction questions, that is diagnostic — say so.

---

## Misconception to pre-empt

> That irreducible error $\sigma^2$ means the model is bad. It means your predictors do not observe everything. Being at the floor is success, not failure — and knowing when you are there is a large part of applied judgement.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the practice

The prediction/inference table, and the five-part indicator template. Both are used immediately in the practice session.

---

## If you are running short

Cut the timeline discussion to five minutes. Do NOT cut the risk derivation — Session 04 assumes it.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 1`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- **every member has pushed** before they leave the room

---

[Student notes](README.md) · [Session 01](../README.md) · [Practice](../02-practice/README.md)
