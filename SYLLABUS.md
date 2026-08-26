# Quantitative Methods in International Business

**HEC Montréal · Professor Thierry Warin, PhD**
`thierry.warin@hec.ca`

---

## Contents

1. [What this course is](#1-what-this-course-is)
2. [Learning outcomes](#2-learning-outcomes)
3. [How a session works](#3-how-a-session-works)
4. [The twelve sessions](#4-the-twelve-sessions)
5. [Assessment](#5-assessment)
6. [The four evaluations, and why each exists](#6-the-four-evaluations-and-why-each-exists)
7. [Tools](#7-tools)
8. [Working with a language model](#8-working-with-a-language-model)
9. [Policies](#9-policies)
10. [Materials](#10-materials)
11. [Document map](#11-document-map)

---

## 1. What this course is

A course in the mathematics of machine learning, taught to economists, in which **every method is
derived before it is used** and **every result is produced by the student on their own machine with
open tools**.

It is not a course in calling library functions. Any language model can call a library function.
What it cannot do — what remains scarce, and what this course exists to build — is the judgement to
know *which* function, on *what* data, under *which* assumptions, and to recognise when the answer
that comes back is wrong.

The course opens with a scenario about Europe's technological position in 2031 and closes by asking
you to carry what you have learned to a problem in francophone Africa. Between those two points you
will derive, implement, break, and defend eleven methods.

> ### Why the course is built this way
>
> Three commitments explain nearly every decision below.
>
> **Derive before you use.** You will not remember a formula you were shown. You will remember one
> you derived, and — more importantly — you will recognise the situations where its assumptions
> fail. A method you cannot derive is a method you cannot audit.
>
> **Break what you build.** Every practice session includes a task that deliberately damages your own analysis:
> introduce collinearity, leak the test set, induce perfect separation. Knowing how a method fails
> is a different and more useful knowledge than knowing how it succeeds. Most professional errors
> are failures you did not know were possible.
>
> **Write for a reader who is not you.** Every deliverable has an audience: a credit committee, a
> European agency, a data science student in Cotonou. Analysis that cannot be handed to someone
> else is not finished.

---

## 2. Learning outcomes

By the end of the course you will be able to:

1. **Derive** the estimators of linear regression, penalised regression, logistic regression,
   panel models, principal components, and causal inference — from first principles, on
   paper.
2. **State the assumptions** each method requires, identify when they fail, and quantify the
   consequence.
3. **Implement** each method from scratch and reconcile it, to numerical precision, with a
   production library.
4. **Design an honest evaluation** — one whose cross-validation scheme matches deployment and whose
   preprocessing sits inside the loop.
5. **Distinguish prediction from identification**, and refuse to present the first as the second.
6. **Convert a decision problem into a threshold**, from an explicit statement of costs.
7. **Document a model** so that a competent stranger can run it, trust it appropriately, and know
   when to retire it.
8. **Communicate quantitative findings** to a decision-maker who will not read your code, including
   what would change your mind.

---

## 3. How a session works

Sessions 1–11 have the same three-part shape. Session 12 is presentations.

```
Before class                First half (~90 min)          Second half (~90 min)
─────────────────────────   ───────────────────────────   ────────────────────────────
00-pre-session/             01-lecture/                   02-practice/
  · reading                   · the mathematics             · your group's research angle
  · concepts to review        · derivations                 · implement, then break it
  · data already cached       · what the method assumes     · 2-minute report
  · written self-check        · what it cannot do           · everyone pushes before leaving
```

The second half is **real research**. Each group of three is paired with a project defined by
students in [Science des Données au Féminin en Afrique](https://sdafrique.org), whose teams identify
a societal problem in their own community. The group's job is to turn that problem into an
answerable research question, find the data, and answer it with the method taught that week.

Every session poses one big methodological question; each group attacks it on its own project. The
last twenty minutes are ten two-minute reports and a synthesis — ten different problems, one method,
which is where the method's assumptions become visible. **Projects are assigned in class, in Session
04**; sessions 02 and 03 build least squares and its inference on the practice data first.

Full brief: **[`RESEARCH-MANDATES.md`](RESEARCH-MANDATES.md)**.

> ### Why you keep the same angle all semester
>
> Because expertise is cumulative and shallow acquaintance with eleven datasets is worth less than
> deep acquaintance with one. By Session 8 you will know that your series is revised, that it breaks
> in 2021, that two of its columns measure nearly the same thing. That knowledge is what lets you
> spot an implausible result — including one produced confidently by a language model.
>
> ### Why the theme changes every week
>
> Because a method rehearsed on a toy dataset is a method you will not transfer. Each week you use
> what you just derived to answer something real, with data that resists you.
>
> ### Why your data are cleaned before class
>
> So that ninety minutes go to analysis rather than to encoding errors. Data wrangling is a real
> skill; it is not the skill this course is testing, and it will consume the entire session if
> permitted to.

---

## 4. The twelve sessions

| # | Session | Method | Theme of the second half |
|---|---|---|---|
| 01 | Foundations: Scenarios, Tools, and the Syllabus | the syllabus, the toolchain, and a conversation | *(no practice; discussion)* |
| 02 | Exploratory Data Analysis, and the First Model | mean/median/trimmed, variance, IQR, skewness, kurtosis, simple and multiple regression | Which summary of your key variable would you defend in print? |
| 03 | Regression: Adequacy, Validity, and Robustness | residual diagnostics, leverage, Cook's distance, information criteria | Which model would survive a referee? |
| 04 | Logistic Regression: Binary, Ordinal, and Multinomial | maximum likelihood, odds ratios, pseudo-$R^2$, likelihood-ratio tests | Can we predict a discrete outcome honestly? |
| 05 | Regularisation: Ridge, Lasso, and the Elastic Net | soft-thresholding, coordinate descent, the grouping effect | Of many indicators, which few actually carry the signal? |
| 06 | Regression: Advanced Considerations | panel data, fixed and random effects, non-linearity, interactions | Does your finding survive the structure of your data? |
| — | **MIDTERM** *(in class, covering Sessions 1–6)* | | |
| 07 | Principal Component and Factor Analyses | eigenvalues, loadings, scree plots, rotation, FAMD | How many distinct dimensions does your angle really have? |
| 08 | K-Nearest Neighbours and the Bias–Variance Trade-off | the Bayes classifier, distance, choosing $k$ by cross-validation | Does flexibility buy you anything on your own data? |
| 09 | Structural Equation Modelling | measurement and structural models, latent variables, fit indices | What is the construct behind your indicators? |
| 10 | Causal Inference I: Counterfactuals, Randomisation, Matching | potential outcomes, randomisation, propensity scores, matching | Can your project support a causal claim at all? |
| 11 | Causal Inference II: Difference-in-Differences | parallel trends, the interaction as the estimate, instrumental variables | What is your counterfactual, and would anyone believe it? |
| 12 | Final Group Presentations | — | — |

**The arc.** Session 2 describes one variable, then relates two — the smallest possible model.
Session 3 asks whether that model can be trusted, which is where diagnostics live. Session 4 carries
regression to discrete outcomes, and Session 5 to problems with more predictors than you can
estimate. Session 6 takes the panel structure of international data seriously. Sessions 7 to 9 turn
to structure nobody labelled: dimensions, neighbours, and quantities you cannot observe directly.
Sessions 10 and 11 confront the question the first nine sessions cannot answer — whether anything
*caused* anything — and Session 12 is where you defend your own attempt.

---

## 5. Assessment

| Component | Weight | Form | When |
|---|---|---|---|
| **Participation** | **10%** | individual, continuous | every session |
| **Midterm exam** | **30%** | individual, on paper, pen and calculator only — no computer, no internet | after Session 06 |
| **Team work** | **20%** | groups of three (practice groups) | Session 12 |
| **Final exam** | **40%** | **individual** research paper (25) + individual oral, 15 min (15) | end of term |

**Team work, 20%**, broken down:

| | |
|---|---|
| Model governance file | 7 |
| Reproducible analysis | 7 |
| Revised Session 1 memo + change log | 3 |
| Presentation and defence | 3 |

**Individual accountability.** An individual multiplier derived from confidential peer ratings,
gated on the git contribution history, applies to the **team work 20% only** — never to the
midterm, and never to the final exam. Default is
×1.00; a mark is reduced only when two independent records agree. Full policy:
[`GROUP-ASSESSMENT.md`](GROUP-ASSESSMENT.md).

---

## 6. The four evaluations, and why each exists

You are entitled to know why you are asked to do everything you are asked to do. Here is the
reasoning, in full.

### Participation — 10%

Attendance is assumed at HEC Montréal, so participation cannot mean turning up. It means
contributing to the room: a question that changed how another group saw their result, a connection
between two angles, a correction that landed. After each practice session the instructor records who did that.

> **Why it is graded at all.** The second half of this course is a joint enterprise. Ten groups
> produce five perspectives on one question, and the value of the session comes from the collision
> between them. A room where nobody challenges anybody produces ten monologues and learns a
> fraction of what it could. Participation is graded because the collision is the point.

**How the 10% is earned.** Against an **absolute, published bar** — never against each other:

| | |
|---|---|
| Bar met | **10 / 10** |
| Within one contribution of the bar | 7 / 10 |
| Roughly half the bar | 5 / 10 |
| Little or no recorded contribution | 0–3 / 10 |

The bar is a recorded contribution in at least **N of the ten practice sessions**, and no more than one
failure to deliver the two-minute report when drawn.

> **Why an absolute bar rather than a ranking.** Because a participation score that ranks students
> against one another measures confidence and extraversion as much as engagement, and it makes
> helping another group personally costly — the exact opposite of what the course design requires.
> Everyone who clears the bar gets the full 10. There is no curve and no quota.

If you contribute mainly in writing or within your group, say so — being quiet is not being absent,
and the record should reflect what you actually did. A student who delivered every time they were
drawn and worked steadily is flagged for **review, never auto-zeroed**: the instructor's attention
is the measuring instrument, and it is imperfect.

### Midterm exam — 30%, individual, on paper, closed book

Covers Sessions 1–6: the supervised learning problem, least squares and its geometry, inference and
diagnostics, bias–variance and cross-validation, ridge/lasso/elastic net, logistic regression and
decision thresholds.

Four parts: **definitions** (state it precisely), **calculations** (derive and compute),
**diagnostics** (read an output and find the fault), **interpretation** (say what may and may not
be claimed).

> **Why an exam, when the real work is the project.** Because a group project cannot tell me what
> *you* know. Three people and a language model produce a good notebook without any one of them
> being able to derive the estimator inside it. The midterm is the only instrument in this course
> that isolates your individual understanding of the mathematics.
>
> **Why no documents.** Not to test memory for its own sake. The formulas that matter — the normal
> equations, the bias–variance decomposition, the soft-thresholding operator, $\tau^\star =
> c_{FP}/(c_{FP}+c_{FN})$ — are few, and having them *in your head* is what lets you notice, in the
> middle of a meeting, that a proposed analysis cannot be right. Expertise you must look up is
> expertise you will not deploy under pressure.
>
> **Why a calculator.** Because the point is not arithmetic. You will compute a ridge estimate, a
> soft-threshold, a marginal effect, a cost-optimal threshold. Doing these by hand once makes the
> formulas concrete in a way that reading them never will.

Example paper with full solutions: [`assessments/midterm/`](assessments/midterm/).

### Team work — 20%, Session 12

Eleven weeks of work with a **real client**: a student in the
[Science des Données au Féminin en Afrique](https://sdafrique.org) programme who has identified a
problem in her own community and will use what you produce.

**The work is the relationship as much as the analysis.** You are in contact with her from Session
04 onward: you agree what the question is, you send a draft rather than only a final version, and
you hand back something she can act on without you in the room.

Three parts: a **model governance file** that she could act on — what the model is for, what it
must not be used for, how it was validated, and where it is weakest — a **reproducible analysis**
that runs from a clean clone on modest hardware, and a **presentation** to a decision-maker who
will not read your code.

> **Why the governance file carries the most weight.** Because it is where every other skill in the
> course has to be written down for someone else — someone in another country, working in another
> language, on another machine. Its Limitations section is the hardest paragraph you will write this
> semester.
>
> **Why a real client rather than a simulated one.** Because a client who will actually use the
> result asks different questions from a marker, and cannot be satisfied with a number that is
> technically correct and practically useless. She is your client, **not your co-author** — see
> [`RESEARCH-MANDATES.md`](RESEARCH-MANDATES.md).
>
> **Why reproducibility is graded, not assumed.** A result that does not reproduce from a clean
> clone is not a result. This is not pedantry: it is the difference between a finding and an
> anecdote, and it is the standard every serious journal now applies.
>
> **Why you defend it out loud.** Because a question you did not anticipate is the fastest test of
> whether you understood your own analysis. The instructor chooses who answers.

Details and rubric: [Session 12](12-group-presentations/README.md).

### Final exam — 40%: research paper (25) + individual oral (15)

An academic paper, **written alone**, that takes the method your group mastered on European data
and **transfers it to a problem in francophone Africa**, written for a specific reader: a student
in the [Science des Données au Féminin en Afrique](https://sdafrique.org) programme who works in R.

> **Why this one is individual.** Everything else in the second half of the course is collective:
> the practice sessions, the project, the presentation. This is the piece where you answer for your
> own judgement, with nobody to divide the work with. It is the closest thing in the course to what
> you will be asked to do in a job.

> **Why transfer rather than extension.** Re-running your method on more of the same data proves
> you can run code. Carrying it to a new context — new data, new constraints, new reader — is the
> only evidence that you understood the method rather than the pipeline. Every assumption you
> absorbed without noticing becomes visible the moment the setting changes.
>
> **Why a real reader.** SDAfrique trains one hundred francophone African women a year in data
> science, in teams, on problems they identify in their own communities. They will read what you
> write. Constraints follow immediately and they are not hypothetical: bandwidth is limited, so your
> data must be small enough to download; hardware is modest, so your method must run without a GPU;
> the working language of the programme is R, so you must separate *method* from *implementation*
> clearly enough that an R user can follow. Writing under real constraints for a real audience is a
> different intellectual act from writing for a marker.
>
> **Why 40%.** Because it is the piece that asks the most: a literature review, a defensible design,
> an honest evaluation, and prose that survives contact with a reader who did not take this course.

**The oral, 15 minutes per student, examined individually.** No slides, no documents. Roughly half
on the methods used in your own paper — derive the estimator, state the assumptions, say what would
break the result — and half on the course, Sessions 02 to 11.

> **Why an oral on top of a paper.** A paper can be written slowly, with help, over weeks. Fifteen
> minutes without documents establishes what you can reconstruct and defend in real time — which is
> a different thing, and the thing an employer or a referee will actually test. The two together
> measure preparation and command; either alone measures half of it.
>
> This is also why the individual multiplier does not apply to the final: both components already
> measure you individually, so there is nothing to correct.

Full brief: [`assessments/final-paper/`](assessments/final-paper/README.md).

---

## 7. Tools

| Tool | Why this one |
|---|---|
| **VS Codium** | VS Code with telemetry removed. Your work involves confidential and licensed data; the editor should not exfiltrate it. |
| **Ollama + a local model** | Inference runs on your machine. Nothing leaves it. You also learn what is achievable without a frontier system — the realistic institutional constraint. |
| **Python + git** | Reproducibility is graded. A commit history is auditable; a notebook's execution state is not. |

Setup, with troubleshooting:
[Session 01 setup guide](01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).
Budget 60–90 minutes **before** Session 1; installation time is not part of class.

Git, GitHub and the group repository are set up separately, before Session 2:
[Session 02 setup guide](02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md).
Budget 45 minutes.

> **Why local rather than hosted.** Partly governance — data sovereignty is a real constraint in
> institutions and you should experience working inside it. Partly honesty — a frontier model
> masks how much of your competence is yours. And partly because the final paper is written for
> readers whose access to compute is not what yours is.

---

## 8. Working with a language model

You are expected to use one. It is a required tool, not a tolerated one.

**The standing rule: every deliverable must document at least one instance where you identified an
LLM output as wrong, unverifiable, or misleading, and explain how you established that.**

You are never penalised for using the model. You are penalised for using it uncritically.

> ### Why this rule, and why it is the point of the whole course
>
> Language models have made information abundant. What they have not made abundant is the ability
> to **ask the right question** and to **recognise a wrong answer**. Both are functions of expertise,
> and expertise is what this course is trying to build in you.
>
> A concrete illustration you will meet in Session 5. Ask a model to select variables for you and it
> will run a lasso and hand you a list. The list will look authoritative. Only if you know that the
> lasso is unstable under correlated predictors — that it picks one member of a correlated group
> more or less arbitrarily, and picks a different one on a resampled dataset — will you think to ask
> the follow-up question that matters: *"how often is each of these selected across bootstrap
> replicates?"* That question turns a misleading answer into a useful one. The model would not have
> volunteered it. **You have to know enough to ask.**
>
> This is precisely why the final paper requires a literature review, and why the review is not a
> formality. Fifteen papers on your topic give you priors: the standard controls, the usual data
> problems, the range in which a coefficient is plausible. Armed with those, you can ask your
> assistant *"why is my estimate three times what the literature reports?"* — and that question is
> the one that finds the bug. Without the review you would not have known the estimate was strange.
>
> The literature review is not a hoop. It is what converts you from someone who receives answers
> into someone who can interrogate them.

**Practical guidance.** Ask it to argue against you; its most useful output is an objection you had
not considered. Verify every factual claim, especially about library APIs, statistical results and
citations — it will state plausible falsehoods with complete confidence. Record what you checked.

---

### The rule, stated as a publisher would state it

This course applies the same standard that **Elsevier** and **Emerald** apply to submitted
manuscripts. It is not stricter, and it is not vaguer.

**1. Generative AI is a research assistant. It is not an author and it does not do the work.**

An assistant may improve how you say something. It may not decide what you say.

| Permitted — assistance | Not permitted — substitution |
|---|---|
| Improving readability, grammar, phrasing, translation | Writing sections you then submit as your reasoning |
| Explaining a method or a library you are learning | Choosing your specification, or your estimand |
| Debugging code you wrote and can explain | Producing analysis you cannot derive or defend |
| Suggesting search terms; summarising a paper **you have read** | Generating a literature review from papers you have not read |
| Drafting boilerplate you then verify line by line | Interpreting your results, or drawing your conclusions |
| Reformatting references you have checked | Inventing, extrapolating or "cleaning" data |

**2. AI cannot be an author or a co-author.** Authorship carries responsibility and accountability
for the work, and a model can hold neither. It is credited in a statement, never in a byline. Nor
may it be cited as a source: if you learned something from it, find and cite the actual source.

**3. Every use must be disclosed.** Each deliverable carries an LLM statement naming the tool, the
version, and what it was used for. *"We used AI for assistance"* is not a disclosure. For the final
paper the requirement is set out in
[`assessments/final-paper/`](assessments/final-paper/README.md#llm-use-statement).

**4. You are fully responsible for every word and every number you submit** — including the ones the
assistant produced. "The model wrote it" is not a defence, in this course or after it. If you cannot
derive it, do not submit it.

**5. Undisclosed substitution is academic misconduct**, handled under HEC Montréal's regulations —
not as a course-level matter. The distinction is between an assistant that helped you do your work
and an assistant that did it instead of you.

> **Why the framing is generous rather than restrictive.** The oral examination in the final exam
> exists partly for this reason. Fifteen minutes of questions on your own methods will establish
> what you understand far more reliably than any policing of drafts. A student who let a model do
> the thinking will discover it there, and the honest use of a research assistant costs nothing.

---

## 9. Policies

**Attendance.** Assumed. Absence does not itself reduce a grade, but the participation record is
built from what happens in the room, and you cannot contribute from elsewhere.

**Late work.** Team work and the final paper: 10% per day, to a maximum of three days, after which
the component is not accepted. Extensions for documented circumstances, requested before the
deadline.

**The two-minute report.** The presenter is drawn at random when your group is called. Any of the
three of you may have to give it, so all three must understand the analysis, the number, and what
would undermine it. Failing to deliver when drawn is the clearest participation failure there is.

**Academic integrity.** HEC Montréal's *Règlement sur les fraudes et plagiat* applies in full.
Two clarifications specific to this course:

- **Language model use is permitted and expected**, subject to the documentation rule in §8.
  Presenting model output as your own reasoning, without the verification the rule requires, is
  misrepresentation.
- **Code from any source may be used with attribution.** Copy a Stack Overflow answer, cite it in a
  comment. Adapt a package's internals, say so. Unattributed borrowing is plagiarism; attributed
  borrowing is normal practice.

**Data.** All data used in this course are public. Respect each source's licence and terms of use,
and record provenance. Nothing in `data/spine/` may be redistributed outside the class without
checking its licence first.

**Accommodation.** Students registered with HEC Montréal's support services should contact the
instructor in the first two weeks so that arrangements — including for the in-class midterm — are
made in good time.

---

## 10. Materials

All free and open:

- James, Witten, Hastie & Tibshirani, *An Introduction to Statistical Learning* — <https://www.statlearning.com/>
- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* — <https://hastie.su.domains/ElemStatLearn/>
- Molnar, *Interpretable Machine Learning* — <https://christophm.github.io/interpretable-ml-book/>

Per-session readings, including the journal articles, are listed in each session's
`00-pre-session/README.md`. There is no textbook to purchase.

---

## 11. Document map

| Document | What it is for |
|---|---|
| [`README.md`](README.md) | Course overview and repository layout |
| **`SYLLABUS.md`** | This document |
| [`RESEARCH-MANDATES.md`](RESEARCH-MANDATES.md) | The ten projects, ten groups, session themes, data sources |
| [`GROUP-ASSESSMENT.md`](GROUP-ASSESSMENT.md) | Participation, presenter draw, contribution report, peer ratings |
| [`assessments/midterm/`](assessments/midterm/) | Example paper and full solutions |
| [`assessments/final-paper/`](assessments/final-paper/README.md) | The SDAfrique brief and rubric |
| `NN-session-slug/` | Per-session pre-session, lecture, and practice |

---

*Last revised for the 2026 offering.*
