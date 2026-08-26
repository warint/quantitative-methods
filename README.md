# Quantitative Methods in International Business

### Econometrics and machine learning, taught the way the work is now done — in an IDE, with an LLM beside you, on your own machine.

A twelve-session graduate course in which every method is **derived** before it is **used**, every
result is produced on the student's own laptop, and the AI assistant is treated as what it is: a
fast, confident, unaccountable collaborator whose output you are answerable for.

**The premise.** You can no longer learn quantitative methods as if the tooling were neutral. A
student in 2026 will reach for a language model on the first line of code. The question is not
whether they use one, but whether they can tell when it is wrong — and that is a skill you have to
teach on purpose.

So this course does four unusual things:

| | |
|---|---|
| **The model runs on your machine** | Ollama + Qwen 2.5 Coder. No API key, no per-token bill, no data leaving the room. You also learn what is achievable *without* a frontier system, which is the realistic institutional constraint. |
| **You work in a real IDE, from the terminal** | VS Codium, git, and an agent (`aider`) that reads and edits your files while you steer it in prose. Not notebooks; the workflow you will actually be hired into. |
| **Catching the model is graded** | Every practice session deliverable must document one instance where you caught the LLM being wrong, unverifiable, or misleading. You are never penalised for using it — only for using it uncritically. |
| **Everything is open, and it is research** | Open-source tools end to end — Python, git, VS Codium, Ollama. Open licences (CC BY 4.0 / MIT). Published articles with their replication data, cited by DOI. The practice sessions are not exercises with known answers; they are ten groups producing five perspectives on one question, assembled each week. |

Underneath, the mathematics is uncompromising: projection and FWL, Gauss–Markov, the bias–variance
decomposition, soft-thresholding, Neyman orthogonality. Nothing is cited that is not first derived.
The tooling is modern; the standards are not new.

**Research-oriented, not exercise-oriented.** Sessions 02–11 are each built on an academic article
and its Harvard Dataverse replication package — see [`REPLICATIONS.md`](REPLICATIONS.md). The term
ends in a research paper written for a real reader, and an
oral defence of it. Nothing here is a toy problem with a number at the back of the book.

**Open by construction.** No proprietary software, no API keys, no cloud accounts, no per-token
bills — and no dependency that stops the course working in a room with no internet. The whole
repository is licensed for reuse, including commercially: take it, translate it, teach it.

**Who it is for.** Graduate students in economics and international business who will be expected to
produce a defensible number, on real European data, and say out loud what it does not license.

---

## Lecture slides, in your browser

**[https://warint.github.io/quantitative-methods/](https://warint.github.io/quantitative-methods/)**

Every lecture deck renders as a slideshow you can open directly — no download, no PowerPoint.
Press **F** for full screen, **S** for speaker notes, **Esc** for the slide overview.

The sources are the `MATH60033A-S*-Lecture.qmd` files in each session's `01-lecture/` folder;
rebuild the site with `scripts/render_session_lectures.sh` and `scripts/build_docs.py`.

---

## How every session works

**Sessions 1–11** have the same four-step rhythm, with a different first-session focus.

```
Before class             In class                  In class: 90 minutes       After class
──────────────────────   ───────────────────────   ─────────────────────────  ───────────────────────
00-pre-session/          01-lecture/               02-practice/               QMIB Lab App
  · required article       · basic equations         · article replication      · optional knowledge check
  · Dataverse package      · visual derivations      · compare / break / explain · app-generated report
  · guided annotation      · graphs explained        · one-slide result         · participation credit
  · written self-check     · assumptions and limits  · two-minute presentation  · never required next prep
```

For Sessions 02–11, the pre-session PowerPoint is the complete preparation brief: students read and
annotate the required academic article, download its Dataverse package, identify the target result,
and answer the self-check before class. ISLR is optional background. The lecture assumes that work
is done. The practice reproduces one published result in groups and ends with a
one-slide, two-minute presentation by a randomly selected member. **Class ends with those
presentations; no practice task carries over as required homework.**

**Session 01** begins with workstation installation (VS Codium, Python, Ollama, Qwen 2.5 Coder, and
Aider), introduces the syllabus and semester, and uses *Europe 2031* for a 90-minute conversation
about evidence, scenario, prediction, and AI.

Students who want to check their knowledge may complete the corresponding activity in the **QMIB
Lab App** after class. A completed app report counts toward participation. The lab is optional and
is never a prerequisite for the next lecture.

**Session 12** is different: the pre-session prepares the final presentation and the class meeting is
a presentation workshop and defence. There is no separate practice deck.

**Complete PowerPoint and Python demo index: [`slides/COURSE-POWERPOINTS.md`](slides/COURSE-POWERPOINTS.md).**

### The second half is real research, from Africa

Each group of three is paired with a project defined by students in
[**Science des Données au Féminin en Afrique**](https://sdafrique.org) — a programme training one
hundred young women from francophone Africa each year, whose teams each identify a societal problem
in their own community.

```
   SDAfrique team (Africa)                HEC group of three (Montréal)
   ───────────────────────                ────────────────────────────
   identifies a problem     ─────────►    formulates a research question
   in their own community                 finds the data
   and a project around it                answers it with a method from class
```

Every session has a **big theme** — one methodological question the whole class attacks. Each group
attacks it **on its own project**, then reports for two minutes. Ten different problems, one method
per week; the synthesis is about how the method behaves across very different data, which is where
its assumptions become visible.

This is the same commission as the final paper. The term is not eleven exercises followed by an
unrelated assignment — **it is one project, approached with a new method every week.**

**Full brief: [`RESEARCH-MANDATES.md`](RESEARCH-MANDATES.md)** — how to turn a problem into an
answerable question, where to find data, and what each session asks of you.

> **Projects are assigned in class**, in Session 04 — sessions 02 and 03 build the estimator on the
> practice data first. They do not exist until the SDAfrique teams
> define them.

---

## The twelve sessions

| # | Session | The method | The question it answers |
|---|---|---|---|
| [01](01-foundations-scenarios-and-tools/README.md) | Foundations: Scenarios, Tools, and the Syllabus | the syllabus, the toolchain, and a conversation | Before we model the future, what are we claiming to know? |
| [02](02-exploratory-data-analysis/README.md) | Exploratory Data Analysis, and the First Model | mean/median/trimmed, variance, IQR, skewness, kurtosis, simple and multiple regression | Which summary of your key variable would you defend in print? |
| [03](03-regression-adequacy-and-validity/README.md) | Regression: Adequacy, Validity, and Robustness | residual diagnostics, leverage, Cook's distance, information criteria | Which model would survive a referee? |
| [04](04-logistic-ordinal-multinomial/README.md) | Logistic Regression: Binary, Ordinal, and Multinomial | maximum likelihood, odds ratios, pseudo-$R^2$, likelihood-ratio tests | Can we predict a discrete outcome honestly? |
| [05](05-ridge-lasso-elastic-net/README.md) | Regularisation: Ridge, Lasso, and the Elastic Net | soft-thresholding, coordinate descent, the grouping effect | Of many indicators, which few actually carry the signal? |
| [06](06-advanced-regression/README.md) | Regression: Advanced Considerations | panel data, fixed and random effects, non-linearity, interactions | Does your finding survive the structure of your data? |
| [07](07-pca-and-factor-analysis/README.md) | Principal Component and Factor Analyses | eigenvalues, loadings, scree plots, rotation, FAMD | How many distinct dimensions does your angle really have? |
| [08](08-knn-and-bias-variance/README.md) | K-Nearest Neighbours and the Bias–Variance Trade-off | the Bayes classifier, distance, choosing $k$ by cross-validation | Does flexibility buy you anything on your own data? |
| [09](09-structural-equation-modelling/README.md) | Structural Equation Modelling | measurement and structural models, latent variables, fit indices | What is the construct behind your indicators? |
| [10](10-causal-inference-foundations/README.md) | Causal Inference I: Counterfactuals, Randomisation, Matching | potential outcomes, randomisation, propensity scores, matching | Can your project support a causal claim at all? |
| [11](11-causal-inference-did/README.md) | Causal Inference II: Difference-in-Differences | parallel trends, the interaction as the estimate, instrumental variables | What is your counterfactual, and would anyone believe it? |
| [12](12-group-presentations/README.md) | Final Group Presentations | — | Can you make a decision-maker act on this — and say what would change your mind? |

**The arc.** Sessions 2–3 build the classical estimator and its inference. Session 4 is the hinge:
in-sample fit stops being evidence. Sessions 5–7 buy flexibility and pay for it in interpretability.
Sessions 8–9 turn to structure we did not label. Session 10 shows why none of the previous nine
sessions licences a policy claim. Session 11 asks what you owe the person who acts on your work —
and returns to the scenario the course opened with. Session 12 is where you defend it.

**Session 6 is deliberately dense.** It composes the Session 5 penalty with the logistic likelihood,
which is why the second half can be short: by then you have derived both halves yourself. Its practice is
split into a compulsory Track A (German Credit) and an extension Track B (bankruptcy data).

---

## Getting started

Put the repository **directly on your Desktop** and keep the folder name
`quantitative-methods`. All course commands and PowerPoint instructions assume that location.

macOS / Linux:

```bash
cd ~/Desktop
git clone https://github.com/warint/quantitative-methods.git quantitative-methods
cd quantitative-methods

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py
```

Windows PowerShell:

```powershell
Set-Location "$HOME\Desktop"
git clone https://github.com/warint/quantitative-methods.git quantitative-methods
Set-Location quantitative-methods

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py
```

Full instructions, including VS Codium and the local LLM:
**[Session 01 setup guide](01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md)**

---

## How students submit work

**One repository, one branch per group.** There are no separate student repositories.

```
github.com/warint/quantitative-methods
│
├── main            ← instructor only; protected, nobody else pushes to it
├── group-01
├── group-02
└── group-XX        ← each group commits and pushes here all term
```

In-class practice work and the one-slide group result go in the session folder, on the group's own
branch. They must be finished before the group presents:

```
NN-session-name/02-practice/submissions/group-XX/
```

**Why one repository.** `python scripts/assess.py contributions` reads the git history *of this
repository* to produce the per-member contribution table. Work pushed anywhere else is invisible to
it, and invisible work cannot be credited.

| Who | What they do once, before Session 02 |
|---|---|
| **Student** | Create a GitHub account, send the username to the instructor, clone the repo, check out `group-XX` |
| **Instructor** | Add every student as a collaborator with **Write**; protect `main` so only they can push to it |

Students never need to create, own or configure a repository. Full walkthrough, including the
instructor's steps: **[Session 02 setup guide](02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md)**

Git, GitHub and group working, needed from Session 02:
**[Session 02 setup guide](02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md)**

---

## Tooling, and why

| Tool | Why this one |
|---|---|
| **VS Codium** | VS Code without telemetry. Confidential and licensed data stay put. |
| **Ollama + a local model** | Inference runs on your machine. Nothing leaves it. You also learn what is achievable without a frontier system — the realistic institutional constraint. |
| **Python + git** | Reproducibility is graded. A commit history is auditable; a notebook's execution state is not. |

Tooling is a governance decision. You should be able to defend yours — Session 12 asks you to.

---

## Assessment

Full detail, and the reasoning behind each component: **[`SYLLABUS.md`](SYLLABUS.md)**.

| Component | Weight | Form |
|---|---|---|
| **Participation** | **10%** | individual, continuous; optional QMIB Lab App reports may be submitted for credit |
| **Midterm exam** | **30%** | individual, on paper — pen and calculator only, no computer, no internet — after Session 06 |
| **Team work** | **20%** | groups of three, presented Session 12 |
| **Final exam** | **40%** | **individual** research paper (25) + individual oral, 15 min (15) |

Team work (20) breaks down as governance file 7 · reproducible analysis 7 · revised Session 1
memo 3 · presentation and defence 3. The 90-minute group practices are **formative** — commented on,
not marked. Optional post-class lab reports contribute to participation.

- Example midterm with full solutions: [`assessments/midterm/`](assessments/midterm/EXAM.md)
- Final exam brief (paper + oral): [`assessments/final-paper/`](assessments/final-paper/README.md)
- Session 12 rubric: [`12-group-presentations/`](12-group-presentations/README.md)

Groups confirm their project dataset by Session 10 and draft three of the four components in the
[Session 11 practice](11-causal-inference-did/02-practice/README.md).

### Individual accountability inside groups

Four mechanisms, three of which cost nothing during the term. Full policy:
**[`GROUP-ASSESSMENT.md`](GROUP-ASSESSMENT.md)**.

| Mechanism | When | Effect |
|---|---|---|
| **Random presenter draw** | every practice session | the 2-minute report is delivered by a member drawn live — so all three must understand everything |
| **Git contribution report** | automatic | commits, share, and weeks active per member; flags the extremes |
| **Everyone pushes** | every practice session | all three members commit from their own machine; a per-week grid makes gaps visible |
| **Confidential peer ratings** | once, at term end | four dimensions, 1–5, computing an individual multiplier |

**The default multiplier is 1.00, and a mark is reduced only when the peer ratings and the git
history independently agree.** One signal opens a conversation; it does not move a mark. That gate
is what defeats both rating inflation and retaliation.

### Participation

**10% of the grade**, separate from the group mark. Attendance is assumed, so participation means contributing
to the room. After each practice session you tick the students who did — aim for about a fifth of the class,
because a sparser record cannot support a decision. The bar is **absolute and published**; the class
distribution is used to *calibrate* it, never to rank students against each other.

A student is never auto-failed for going unnoticed: if they delivered every time they were drawn and
worked steadily, they are flagged `REVIEW`, not `FAIL`.

```bash
python scripts/assess.py draw --session 5            # 30s, project it
python scripts/assess.py participation --session 5   # 60s after class
python scripts/assess.py status                      # week 6 and week 11
python scripts/assess.py participation --report      # once, at the end
python scripts/assess.py multipliers                 # once, at the end
```

---

## Standing rules

**On data.** Never committed. Download once, cache as parquet, read from the cache. Record
provenance and a checksum. Every practice session must run offline.

**On reproducibility.** One virtual environment, one committed `requirements.txt`, every seed set
explicitly. If your result does not reproduce from a clean clone, it does not reproduce.

**On the local LLM.** Use it freely — as a sparring partner, never as an oracle. Ask it to argue
against you. Verify every factual claim, especially about library APIs and statistical results.
**Every practice session deliverable must document at least one instance where you caught the model being wrong,
unverifiable, or misleading.** You are never penalised for using it; you are penalised for using it
uncritically.

**On claims.** When you report a number, be able to say in one sentence where it came from and what
would falsify it.

---

## Repository layout

```
qmib/
├── README.md                          this file
├── RESEARCH-MANDATES.md               the ten projects, ten groups, session themes
├── requirements.txt
├── .gitignore
├── data/spine/                        the shared panel — cleaned, cached, committed
├── scripts/
│   ├── verify_sources.py              checks every public endpoint still resolves
│   └── build_spine/                   instructor-run collection scripts
├── NN-session-slug/                   sessions 01–11
│   ├── README.md                      session brief, objectives, timing
│   ├── 00-pre-session/
│   │   └── README.md                  reading, concepts, data, self-check
│   ├── 01-lecture/
│   │   └── README.md                  the mathematics (first half)
│   ├── 02-practice/
│   │   ├── README.md                  the group brief (second half)
│   │   ├── starter/                   scaffolded code
│   │   └── submissions/               group-XX/ — your work goes here
│   └── data/                          git-ignored; see its README to populate
└── 12-group-presentations/
    ├── README.md                      schedule, deck rules, rubric, peer review
    ├── 00-pre-session/README.md       the production checklist
    └── submissions/                   group-XX/ — deck, governance file, analysis
```

Two files sit outside that pattern:

- Session 01 additionally contains the [Europe 2031 reading
  brief](01-foundations-scenarios-and-tools/00-pre-session/reading-europe-2031.md), the setup guide,
  and `verify_environment.py`.
- Session 11 contains the [model governance file
  template](11-causal-inference-did/02-practice/governance-file-template.md), which is the
  largest single component of the final mark.

---

## Core references

- James, Witten, Hastie & Tibshirani, *An Introduction to Statistical Learning* — free at <https://www.statlearning.com/>
- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* — free at <https://hastie.su.domains/ElemStatLearn/>
- Molnar, *Interpretable Machine Learning* — free at <https://christophm.github.io/interpretable-ml-book/>
- Gentzkow, Kelly & Taddy (2019), "Text as Data", *JEL* 57(3)
- Chernozhukov et al. (2018), "Double/Debiased Machine Learning", *Econometrics Journal* 21(1)

Per-session readings are listed in each `00-pre-session/README.md`.

---

## Rendering the mathematics

The lecture notes use LaTeX. GitHub renders `$...$` and `$$...$$` natively. In VS Codium, install
**Markdown Preview Enhanced** and open the preview with `Ctrl/Cmd+K V`.

---

## A note on *Europe 2031*

The course opens and closes with [**Europe 2031**](https://europe2031.ai), an independent scenario
narrative published on 11 June 2026 by the ARQ Foundation. Read it free at
**<https://europe2031.ai>** — online, as a [PDF](https://europe2031.ai/europe-2031.pdf), in
[French](https://europe2031.ai/fr), or as audio.

It is **not** an official European Union forecast, and its figures are internal parameters of a
story rather than measured predictions. It is used here as a **stress test** — a device for
exposing assumptions — because that is also what a statistical model is.

---

## Licence and citation

| | |
|---|---|
| Teaching materials (`*.md`, rubrics, the synthetic data spine) | **CC BY 4.0** — [`LICENSE`](LICENSE) |
| Code (`scripts/`, `**/starter/`, `*.py`) | **MIT** — [`LICENSE-CODE`](LICENSE-CODE) |

Use it, adapt it, translate it, teach it — including commercially — provided you credit the author,
link the licence and indicate what you changed. Attribution is not endorsement. Scope, exceptions
(quoted readings, live source data, student submissions) and the citation formats are set out in
[`LICENSING.md`](LICENSING.md); GitHub's *Cite this repository* button reads
[`CITATION.cff`](CITATION.cff).

Copyright © 2026 Thierry Warin.
