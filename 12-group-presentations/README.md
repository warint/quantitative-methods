# Session 12 — Final Group Presentations

> **Can you make a decision-maker act on this — and tell them honestly what would change your mind?**

**Wednesday 2 December 2026** · 15:30–18:30 · Décelles — Victoriaville

Quantitative Methods in International Business · duration 3h00

---

**Presentations fill most of the session.** There is no practice.

Ten groups × **13 minutes** each: **8 minutes** of presentation, **5 minutes** of questions from
the other groups and the instructor. The schedule is tight and will be kept to; a group that
overruns loses its question time, not the next group's.

The **closing address** opens the second half — what the twelve weeks were for, why it matters in
private and public organisations, and a return to *Europe 2031* with the tools you did not have in
August. It sits there rather than at the end for two reasons: it is the last teaching of the
course, and the argument it makes deserves a room that has just come back from a break rather than
one that has been listening to presentations for three hours.

> **[Open the closing address](https://warint.github.io/quantitative-methods/session-12-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S12-Lecture.qmd`](01-lecture/MATH60033A-S12-Lecture.qmd).

---

## Learning objectives

- Present quantitative work to a decision-maker who will not read your code.
- State a recommendation, its confidence, and its falsifier in under twelve minutes.
- Defend an identification or validation choice under questioning.
- Assess another group's work against the standards of the course.

---

## Schedule

| Time | | |
|---|---|---|
| 0:00–0:05 | Opening and running order | |
| 0:05–1:10 | Presentations 1–5 | *first half* |
| 1:10–1:25 | Break | |
| 1:25–1:45 | **Closing address** — *What the twelve weeks were for* | *second half opens* |
| 1:45–2:50 | Presentations 6–10 | |
| 2:50–3:00 | Results, next steps, and the final paper | |

Ten presentations at 13 minutes is 2h10; with the opening, the break, the address and the close
that is exactly three hours, and there is no slack in it. A group that runs long is taking the time
out of the address or out of another group.

---

## Deck rules

- **Eight slides maximum.** Slide 1 is the decision. Slide 2 is your recommendation. Everything after that is support.
- **No code on slides.** Not a snippet, not a screenshot of a terminal.
- **Every figure has a sentence-long caption stating what it shows** — not what it is.
- **One slide must be titled 'What would change our mind.'** It is not optional and it is graded.
- **Numbers carry uncertainty.** A point estimate without an interval, or a metric without a benchmark, will be questioned.

---

## Deliverables and weighting

Team work is **20% of the course grade**. Within it:

| Component | Weight | What is assessed |
|---|---|---|
| **Model governance file** | 7 / 20 | The seven headings from Session 11.4. Sections 5 (Limitations) and 6 (Monitoring) carry the most weight. |
| **Reproducible analysis** | 7 / 20 | Runs end-to-end from a clean clone plus `pip install -r requirements.txt`. Seeds set. Data cached, not downloaded at runtime. |
| **Revised Session 1 memo + change log** | 3 / 20 | Original and revision submitted together, with a one-page account of what changed and which session changed it. |
| **Presentation and defence** | 3 / 20 | Clarity of the recommendation; quality of answers under questioning. |

The [individual multiplier](../GROUP-ASSESSMENT.md) applies to these 20 points only — never to the
midterm or the final exam, which are assessed separately. The **final exam (40%)** — a research
an individual paper plus a 15-minute individual oral — is a distinct deliverable with its own
brief:
[`assessments/final-paper/`](../assessments/final-paper/README.md).

Submit everything to `groups/A2026/group-XX/session-12/` — the deck, the governance file, the analysis, and the revised memo. Preparation checklist:
[`00-pre-session/README.md`](00-pre-session/README.md).

The governance file, backtest and shift diagnostic were drafted in the
[Session 11 practice](../11-causal-inference-did/02-practice/README.md) — this session assesses
the finished versions.

---

## Questions you will be asked

Prepare for these. They are not a surprise.

- Why should I believe this? *(Have a two-sentence answer ready.)*
- What is your benchmark, and by how much do you beat it? Is that difference significant?
- Which of your preprocessing steps is inside the cross-validation loop, and which is not?
- Is this a prediction or a causal claim? If causal, what identifies it?
- What would this model do if the world shifted in the way *Europe 2031* describes?
- Where did your local LLM mislead you, and how did you catch it?

> **Questions are directed at a named member, not at the group.** The instructor chooses who
> answers. This is the same principle as the weekly presenter draw: a group mark should reflect
> what all three of you can do. See [`GROUP-ASSESSMENT.md`](../GROUP-ASSESSMENT.md).
>
> Your individual multiplier is computed after the session from confidential peer ratings, gated on
> the git contribution history. The default is 1.00 and most students will be unaffected — but you
> should read the policy before the session, not after.

---

## Peer review

Each group submits **one peer review** of another group's presentation, assigned
on the day, due 48 hours later. Half a page, structured as:

1. The strongest claim they made, restated in your own words.
2. The weakest link in the chain from data to recommendation.
3. One question you would have asked with more time.

Peer reviews are read but not separately graded. They exist because assessing someone else's work
against the standards of this course is the fastest way to see whether you have internalised them.

---

**A closing word, from Session 1.**

The course opened with a scenario that was not a forecast, whose numbers were parameters of a story
rather than measurements. You were asked to convert a narrative assumption into an indicator, a
trigger point and a falsifier — and most of you found it harder than expected.

Eleven sessions later, the discipline is the same: state what you assumed, state what you estimated,
state what would change your mind. The mathematics was in service of that, not the other way round.

Go and be careful with other people's decisions.

---

[<- Session 11: Forecasting, Distribution Shift, and Model Governance](../11-causal-inference-did/README.md)
