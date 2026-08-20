# Research mandates

**Your group's project comes from Africa. Your job is to turn it into research.**

---

## Contents

1. [How this works](#1-how-this-works)
2. [What you receive](#2-what-you-receive)
3. [The three moves](#3-the-three-moves)
4. [Allocation](#4-allocation)
5. [The session themes](#5-the-session-themes)
6. [Finding your data](#6-finding-your-data)
7. [The data spine — your practice ground](#7-the-data-spine--your-practice-ground)
8. [The two-minute report](#8-the-two-minute-report)
9. [Rules that always apply](#9-rules-that-always-apply)

---

## 1. How this works

### The partnership

[**Science des Données au Féminin en Afrique**](https://sdafrique.org) (SDAfrique) trains one
hundred young women from francophone Africa each year in data science. Its pedagogy is
problem-first: **each team identifies a societal problem in their own community** and builds a
project addressing one dimension of it. Past cohorts have worked on speech recognition,
disinformation detection and health service delivery.

Those projects are the input to this course.

```
        SDAfrique team (Africa)              HEC group of three (Montréal)
        ───────────────────────              ────────────────────────────
        identifies a problem      ───────►   formulates a research question
        in their own community               finds the data
        and a project around it              answers it with a method from class
                                                        │
                                                        ▼
                                             a paper the SDAfrique team can use
```

### Why this shape

A problem someone else chose, in a context you do not live in, is harder than a problem you invent
— and that is the point.

- You cannot quietly redefine the question to suit the data you found.
- You cannot assume the institutional background; you have to learn it.
- Every assumption you absorbed without noticing becomes visible the moment the setting changes.

It is also the same commission as your [final paper](assessments/final-paper/README.md). The term is
not eleven exercises followed by an unrelated assignment: **it is one project, approached with a new
method every week.**

### The shape of a session

Every session has a **big theme** — one methodological question the whole class attacks. In the
second half, each group attacks it **on its own project**. The last twenty minutes are ten
two-minute reports.

```
                    SESSION THEME (changes every week)
                             │
       ┌──────────┬──────────┼──────────┬──────────┐
    group 01   group 02   group 03    ...       group 10
   project A  project B  project C            project J
       │          │          │          │          │
       └──────────┴──────────┼──────────┴──────────┘
                             │
                   COLLECTIVE DISCUSSION
              (instructor synthesis, 5 min)
```

Ten different problems, one method per week. The synthesis is about **the method's behaviour across
very different data** — which is where its assumptions become visible.

---

## 2. What you receive

From your SDAfrique counterparts, in Session 02:

| | |
|---|---|
| **The problem** | A societal problem in a specific place, in their words |
| **What they are building** | The project dimension they chose to address |
| **Context** | Why it matters locally, and what is already being done |

**What you do *not* receive:** a research question, a dataset, a specification, or a method. Those
are the whole of your work.

> **This is not a simulated client.** These are real teams with real projects. Papers judged strong
> are offered back to the SDAfrique programme. Write accordingly — and remember that your reader
> works in R, on a modest machine, with limited bandwidth.

---

## 3. The three moves

### Move 1 — Formulate a research question

A problem is not a question. *"Youth unemployment in Cotonou"* is a problem. A question is
answerable, and it names its own estimand:

- ❌ *"How can we reduce youth unemployment?"* — not answerable by any dataset
- ❌ *"Is unemployment related to education?"* — no estimand, no unit, no period
- ✅ *"Among Beninese labour-force respondents aged 18–30, how much of the gap in employment
  probability between secondary and tertiary completers survives conditioning on region, sector and
  household composition?"*

The third one tells you what to estimate, on whom, and what would falsify it.

> **Write the question before you look for data.** Then, when the data force you to change it —
> and they will — the change is a decision you made rather than a drift you did not notice.

### Move 2 — Find the data

Nobody hands you a dataset. See [§6](#6-finding-your-data) for where to look and what is required.

- If the ideal data do not exist, say what you used instead and what that costs you.
- If nothing usable exists, that is a finding — **document the search** and reformulate.

### Move 3 — Answer it with a method from class

Each week you apply that week's method to your project. Sometimes it will fit. Sometimes it will
not.

> **When a method cannot answer the theme with your data, saying so clearly — and showing why — is a
> full-credit answer.** That judgement is the skill this course exists to build. What is not
> acceptable is running the method anyway and reporting the number as if it meant something.

---

## 4. Allocation

**Projects are assigned in class, in Session 02.** They are not listed here, because they do not
exist until the SDAfrique teams define them.

- Ten HEC groups of three
- One SDAfrique project each
- Fixed for the semester — expertise accumulates, and so does your understanding of the context

Groups are formed in Session 02 and registered with the instructor. Once fixed, your project is
your project: eleven weeks of accumulated work, not eleven disconnected exercises.

---

## 5. The session themes

The theme is the same for everyone; the execution is yours, on your project.

| # | Method taught | **Theme of the session** |
|---|---|---|
| 02 | OLS geometry, FWL | **How much of the measured gap is real, and how much is composition?** |
| 03 | Inference, robust SEs, OVB | **Which of these differences would survive a referee?** |
| 04 | Bias–variance, cross-validation | **Are we predicting, or only describing the past?** |
| 05 | Ridge, lasso, elastic net | **Of many candidate indicators, which few actually carry the signal?** |
| 06 | Logistic and penalised logistic | **Can we flag the outcome ahead of time — and what does a false alarm cost?** |
| 07 | Trees, forests, boosting | **Is the relationship non-linear — and can you still explain it to a minister?** |
| 08 | PCA and factor models | **How many independent things are we actually measuring?** |
| 09 | Clustering and text as data | **Do the units fall into types — and does the available text track them?** |
| 10 | Double machine learning | **Did the intervention do anything, or did we measure who was already ahead?** |
| 11 | Forecasting, drift, governance | **If this became a monitoring tool for your SDAfrique team, would you sign it?** |

Session 01 has no project work — it is the syllabus and the *Europe 2031* conversation. Session 12
is the presentation of accumulated work.

### Where the method may not fit

Some weeks the honest answer is *"not with these data"*. Expect this in particular where:

- **Session 08–09** need many series or a real corpus. If your project has neither, say so and
  demonstrate the method on the spine instead, then explain what it would take to apply it for real.
- **Session 10** needs a treatment and defensible overlap. Most observational projects do not have
  one. Identifying *why* your project cannot support a causal claim is worth more than a
  manufactured one.

---

## 6. Finding your data

### Where to look

| Source | Good for |
|---|---|
| **National statistical offices** | Censuses, labour-force and household surveys |
| [**IPUMS International**](https://international.ipums.org) | Harmonised census microdata, many African countries |
| **DHS Program** | Demographic and health surveys, geo-referenced |
| **Afrobarometer** | Attitudes, governance, service delivery |
| **World Bank / WDI, Microdata Library** | Country aggregates; survey microdata |
| **UN Comtrade, FAOSTAT, ILOSTAT** | Trade, agriculture, labour |
| [**Harvard Dataverse**](https://dataverse.harvard.edu) | Replication packages — see [`REPLICATIONS.md`](REPLICATIONS.md) |
| **OpenStreetMap, WorldPop, nighttime lights** | Geospatial covariates where surveys are thin |

### What is required of you

1. **Provenance.** Institution, dataset name, version or wave, access date, licence. In a table.
2. **A cached local copy.** Download once, save as parquet, read from the cache. No lab may require
   an internet connection.
3. **Coverage, stated honestly.** Which years, which regions, which population — and who is missing.
4. **Missingness confronted.** Not dropped silently. Say who disappears when you drop rows, and in
   which direction that biases you.
5. **Licence respected.** Some microdata may not be redistributed. **Never commit data you are not
   licensed to share** — cache it locally and commit the script that fetches it.

> Bandwidth and hardware are real constraints for your reader. A method needing a GPU, or data
> needing 40 GB, is not usable by the team that gave you the problem.

---

## 7. The data spine — your practice ground

The repository ships a **synthetic European panel** in `data/spine/`. It is not your project data
and it is not observed data. It exists so that you can see a method work on **known ground** before
turning it on data whose truth you do not know.

| | |
|---|---|
| **What it is** | 30 European countries, 2010–2024, generated from a known latent structure |
| **Why it exists** | Every session's pathology is deliberately built in — collinearity, heteroskedasticity, temporal dependence, a rare event, three latent factors, four country types, a known treatment effect, a post-2021 shift |
| **How to use it** | Get the method working here first. Then apply it to your project. |

- Lecture examples use the spine, so everyone is looking at the same numbers.
- **Your reported result must come from your own project**, not the spine.
- Where a method cannot be applied to your project at all, demonstrating it on the spine and
  explaining the gap is the acceptable substitute.

> **⚠️ These are teaching fixtures, not observed data.** Do not cite any number from them as a fact
> about Europe. See [`data/spine/PROVENANCE.md`](data/spine/PROVENANCE.md).

---

## 8. The two-minute report

At the end of every lab, one member — **drawn at random** — gives the report.

**One slide. Three sentences.**

1. **What I did.** *"We estimated X on Y for our project's unit, partialling out Z."*
2. **The number.** One figure or estimate, with its uncertainty or its benchmark.
3. **The catch.** What surprised you, what you cannot claim, or where your data failed you.

No method exposition — everyone learned it ninety minutes ago. No code on the slide.

> **Sentence 3 earns the slot.** A result plus what would undermine it is worth more than a result
> alone. And because the presenter is drawn live, all three of you must be able to give it.

---

## 9. Rules that always apply

**On data.** Never commit data you are not licensed to redistribute. Download once, cache as
parquet, read from the cache, record provenance and a checksum. Every lab must run offline.

**On reproducibility.** One virtual environment, one committed `requirements.txt`, every seed set
explicitly. If your result does not reproduce from a clean clone, it does not reproduce.

**On the local LLM.** A sparring partner, never an oracle — and especially not about a context it
has seen little of. Ask it to argue against you. Verify every factual claim about the country you
are writing about. Every deliverable documents at least one instance where you caught it being wrong
or unverifiable.

**On claims.** When you report a number, be able to say in one sentence where it came from and what
would falsify it.

**On the people who gave you the problem.** Their project is not a case study you are extracting
from. Write something they can use, credit them, and do not overstate what your analysis settles.

---

[Syllabus](SYLLABUS.md) · [Group assessment](GROUP-ASSESSMENT.md) · [Final exam brief](assessments/final-paper/README.md)
