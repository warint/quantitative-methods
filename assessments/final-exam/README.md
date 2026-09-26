# Final exam — an individual research paper, and its oral

**40% of the final grade** · **written alone**, English, academic format · paper due **Sunday 13
December 2026, 23:59** · **oral the next day, Monday 14 December** (to be confirmed), 15 minutes
per student

> The first piece of research you would be glad to show a thesis supervisor — on a question of your
> own, with one method you now command, and your name alone on it.

| Component | Weight | Form | When |
|---|---|---|---|
| **Research paper** | 25 | Individual, 6,000–8,000 words | Sunday 13 December 2026, 23:59 |
| **Oral examination** | 15 | Individual, 15 minutes, no documents | Monday 14 December 2026 (to be confirmed) |

> **This is not the team work.** The team work (20%) is the SDAfrique methods paper your practice
> group writes together and defends in Session 12: see [`../team-work/`](../team-work/README.md).
> Both papers are due on the same day. The individual multiplier never applies here: both
> components already measure you alone.

---

## Contents

1. [What this paper is for](#1-what-this-paper-is-for)
2. [Choosing your question](#2-choosing-your-question)
3. [One method, from the semester](#3-one-method-from-the-semester)
4. [Data](#4-data)
5. [Structure of the paper](#5-structure-of-the-paper)
6. [Authorship and LLM statement](#6-authorship-and-llm-statement)
7. [Rubric — the paper](#7-rubric--the-paper)
8. [The oral examination](#8-the-oral-examination)
9. [Timeline and submission](#9-timeline-and-submission)

---

## 1. What this paper is for

Most of this course is collective: the practice sessions, the replications, the team paper. This is
the piece where you answer for your own judgement.

It is also the piece you keep. Write the paper you would want to attach to an application, show a
prospective supervisor, or grow into your **supervised project or thesis** during your MSc. Choose
the question with that in mind: a paper on a topic you will still care about next year is worth
more to you than a tidy exercise on a topic you will never touch again.

> **Why a research paper, and not a problem set.** A problem set tells you whether you can apply a
> method when someone has already chosen the question, the data and the method for you. Research
> starts one step earlier, with a question nobody has handed you. That step — turning a curiosity
> into something answerable with data you can get — is the one a thesis will ask of you, and the one
> this course has not yet asked you to take alone.

---

## 2. Choosing your question

The question is yours. It must pass **five tests**:

1. **International.** This is a course in quantitative methods for **international business**. The
   question must cross a border: trade, investment, migration, firms or policy compared across
   countries, the international exposure of a sector, the diffusion of a practice. A purely domestic
   question that happens to use one country's data does not qualify.
2. **Yours, and worth something on a CV.** A question in the field you want to work or study in,
   that you could describe in an interview in two sentences and that a supervisor would recognise as
   a possible thesis chapter. Say in the introduction why it matters, and to whom.
3. **Answerable with one method from the semester** — see §3. Do not bend the question to fit a
   method you like; if the honest answer is that the method is the wrong tool, choose another
   question.
4. **Public data.** Someone else must be able to obtain your data and re-run your analysis. No
   confidential firm data, no paid subscription the reader cannot get.
5. **Modest.** It must run on a laptop in under an hour.

> **A good question is narrower than you think.** "What drives FDI?" is a literature. "Did the
> 2019 African Continental Free Trade Area agreement change the sectoral composition of
> intra-African FDI?" is a paper. The narrower question is not less ambitious; it is the only kind
> that can be answered in 8,000 words.

**It may not be your team's question.** It may build on your practice angle or your team paper's
method, but the question, the data and every sentence of the analysis must be your own. Say in the
introduction how it differs from your team's work.

---

## 3. One method, from the semester

Choose **one** technique the course taught, and make it the paper's engine:

| Session | Methods you may build the paper on |
|---|---|
| 02–03 | Linear regression, with its diagnostics — residuals, leverage, influence, robust inference |
| 04 | Logistic, ordinal or multinomial regression |
| 05 | Ridge, lasso or elastic net, with honest selection of $\lambda$ |
| 06 | Panel data — fixed and random effects, interactions, non-linearity |
| 08 | K-nearest neighbours, and the bias–variance trade-off |
| 09 | Structural equation modelling — a measurement model and a structural model |
| 10 | Causal inference — randomisation, matching, propensity scores |
| 11 | Difference-in-differences |
| 13 | Principal component or factor analysis *(self-study; allowed if you have worked through it)* |

Other methods may appear as benchmarks or robustness checks, but **one** method must carry the
argument, and you must be able to **derive it** — on paper, in the oral, without notes.

> **Why one.** A paper that runs six methods and reports whichever looks best has answered no
> question; it has searched for a result. One method, understood completely — its assumptions, its
> failure modes, the obvious alternative and why you did not use it — is a stronger paper and a far
> easier oral.

---

## 4. Data

The same standard as the course spine and the team paper:

- **Provenance for every series**: source, identifier, download date, licence.
- **Confront the missingness.** State the pattern, how you handled it, and inside which part of the
  pipeline. "We dropped incomplete rows" is acceptable only if you also say which countries or
  firms that removed and what it does to your claim.
- **Respect the survey design** if you use survey data: weights, strata and clustering.
- **Cache it.** Your repository must run from a local copy, not a live download.

Good starting points: World Bank WDI, OECD, IMF, UN Comtrade, CEPII (BACI, gravity), UNCTAD, ILOSTAT,
Eurostat, Our World in Data, the Harvard Dataverse replication packages of published papers — and
the course's own spine, `qmib.catalog()`, if your question fits it.

---

## 5. Structure of the paper

**Between 6,000 and 8,000 words, including references and appendices.** Standard academic format,
single-authored.

| § | Section | Guidance |
|---|---|---|
| — | **Title, author, abstract** | Abstract 150–200 words: question, data, method, finding, limitation. Write it last. |
| 1 | **Introduction** | The question, why it matters and to whom, what you contribute, and — in the last paragraph — what you found. |
| 2 | **Literature** | **10 academic articles**, organised by argument, not by author. It must end with the gap your paper addresses. |
| 3 | **Data** | Sources, construction, provenance table, missingness, limitations, and the descriptive table a referee will ask for. |
| 4 | **Method** | **Derive it.** The model or objective function, its assumptions, how its tuning or identification is chosen, and why it and not the obvious alternative. |
| 5 | **Results** | The main result with its uncertainty and against a named benchmark. Figures with captions that say what they *show*. |
| 6 | **Robustness and limitations** | What you tested, what moved, what did not — and the paragraph naming what would change your conclusion. |
| 7 | **Conclusion** | What the result licenses, what it does not, and the next question — the one your thesis could take up. |
| — | **References** | Consistent style, APA or Chicago. Every reference verified. |
| — | **Statements** | Authorship and LLM use — see §6. |

**Accompanying repository**, submitted with the paper: code, cached data, a `README.md` with a
one-command reproduction, seeds set, and the provenance file.

---

## 6. Authorship and LLM statement

**Single-authored.** You are responsible for every sentence. Acknowledge anyone who helped —
classmates who discussed the method, a supervisor you consulted, a practitioner who suggested the
question — without making them authors.

**LLM use statement: required, two paragraphs.** First, what you used and for what — drafting,
debugging, literature search, translation — specifically. Second, and graded: **at least one
documented instance where the model was wrong, unverifiable or misleading, and how you established
that.** The most likely candidate is a fabricated citation: verify every reference against the
publisher's record.

> A paper submitted with no LLM statement is returned ungraded.

---

## 7. Rubric — the paper

Out of 100, for the 25 points the paper carries.

| Component | Weight | What earns full marks |
|---|---|---|
| **Question and contribution** | 15 | A specific, answerable, international question; why it matters and to whom; the contribution stated plainly |
| **Literature review** | 15 | 10 read articles organised by argument; priors on magnitudes and known data problems; ends with a genuine gap |
| **Data and provenance** | 10 | Full provenance; missingness confronted rather than concealed; the descriptive table |
| **Method** | 25 | One method, derived rather than cited; assumptions stated; the choice defended against the obvious alternative |
| **Results and honest evaluation** | 20 | Uncertainty reported; a named benchmark; an evaluation design that matches the data's dependence; no leakage |
| **Writing, references, repository, statements** | 15 | Clear prose; verified references; the repository reproduces; the LLM statement is specific |

### What earns credit that students do not expect

- **A null or negative result, investigated precisely.** Full marks are available for it.
- **A limitation you found yourself** before a referee could.
- **A refusal to make a causal claim** where the design cannot support one.
- **A conclusion that names the next paper** — the thesis question this one opens.

### What loses marks reliably

- Citing a method without deriving it.
- A literature review that is a list of summaries rather than an argument.
- Preprocessing outside the cross-validation loop.
- A result with no benchmark, or no uncertainty.
- A question that is not international.
- An unverified citation.

---

## 8. The oral examination

**15 minutes, one student at a time, no documents — Monday 14 December 2026, the day after the
paper is due** (to be confirmed).

It is not a presentation and there are no slides: you sit down and answer questions. The examiner
has your paper.

### What is examined

Two things, roughly half the time each:

1. **Your paper.** Why that method and not the obvious alternative; its assumptions; what would
   break your result; where your uncertainty comes from and what it covers.
2. **The course.** Anything from Sessions 02 to 11. Derive something on paper if asked.

> **Why an oral on top of a paper.** A paper can be written slowly, with help, over weeks. Fifteen
> minutes without documents establishes what you can reconstruct and defend in real time — the thing
> a thesis committee, a referee or an employer will actually test. The two together measure
> preparation and command; either alone measures half of it.

### Questions you should expect

- *Derive the estimator you used. You may use the board.*
- *Your paper reports X. What would have to be true about the data for that to be wrong?*
- *You chose method A over method B. Defend that against someone who prefers B.*
- *Where in your paper is a claim your design cannot support? There is usually one.*
- *Explain [a result from Session 0N], and why it mattered for your paper — or why it did not.*

### How it is marked

Out of 15, in three equal parts:

| | Points | What earns full marks |
|---|---|---|
| **Command of your own method** | 5 | Derives it, states the assumptions, knows what breaks it |
| **Command of the course** | 5 | Connects your paper to the methods you did not use, and says why |
| **Honesty under pressure** | 5 | Concedes precisely what cannot be claimed, and says how you would find out |

> **Saying "I do not know" costs you very little.** Defending an indefensible claim costs you a
> great deal.

### Practical

- Slots are circulated in advance. Bring nothing: your paper is in front of the examiner.
- In English or French, your choice — state it when you book your slot.

---

## 9. Timeline and submission

| When | What |
|---|---|
| **By Session 9 — Wed 11 November** | **One-page proposal**: the question, why it is international, why it matters to you and to whom, the data with links, the one method. Approved before you proceed. |
| **By Session 11 — Wed 25 November** | Literature review draft: the ten sources and the argument. Formative feedback returned. |
| **Sunday 13 December 2026, 23:59** | **Final submission**: the paper as PDF, and the repository — the same deadline as the team paper. |
| **Monday 14 December 2026** (to be confirmed) | **The oral**, 15 minutes. |

**Submit** to `groups/A2026/group-XX/final-paper-<your-name>/`: the PDF and the repository, which
must run from a clean clone. If it does not run, the results component cannot be marked.

Late: 10% per day to a maximum of three days.

---

*Related: [syllabus](../../SYLLABUS.md) · [the team work](../team-work/README.md) ·
[research mandates](../../RESEARCH-MANDATES.md)*
