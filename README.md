# MATH60033A — Quantitative Methods in International Business

A twelve-session course in which every method is **derived** before it is **used**, and every result
is produced on the student's own machine with open tools.

---

## How every session works

**Sessions 1–11** have the same three-part shape.

```
Before class                First half (~90 min)          Second half (~90 min)
─────────────────────────   ───────────────────────────   ────────────────────────────
00-pre-session/             01-lecture/                   02-lab/
  · reading                   · the mathematics             · group work in VS Codium
  · concepts to review        · derivations                 · implement it yourself
  · download the data         · what the method assumes     · then break it deliberately
  · written self-check        · what it cannot do           · a written deliverable
```

The lecture assumes the pre-session work is done. The lab assumes the data are already downloaded.
Nothing in a lab requires an internet connection.

**Session 12** is different: group presentations fill both halves. No lecture, no lab.

### The second half is collective research

Every session has a **big theme** — one question the whole class attacks. Ten groups of three answer
it from **five fixed angles** (two groups each, at different units of analysis), then report for two
minutes each. Five different lights on the same question, every week.

| Angle | Owns | Interrogates |
|---|---|---|
| **A** Compute & energy | electricity prices, generation mix, industrial demand | Is power really the binding constraint? |
| **B** Work & skills | employment by occupation, earnings, task exposure | Does exposure predict what happened to jobs? |
| **C** AI adoption | enterprise AI use, barriers, R&D, productivity | Is diffusion happening, and where does it stall? |
| **D** Trade & dependence | bilateral flows in semiconductors, equipment, robots | How concentrated is Europe's input dependence? |
| **E** Policy language | ECB, EUR-Lex, national strategies | Does policy text lead, lag, or track the economy? |

Angles are fixed for the semester so expertise accumulates; themes rotate so each method is used to
answer something real. Data are **cleaned and cached before class** — lab time goes to analysis, not
wrangling.

**Full brief: [`RESEARCH-MANDATES.md`](RESEARCH-MANDATES.md)** — research questions, goals, group
allocation, data sources with dataset codes, and what each angle does in each session.

---

## The twelve sessions

| # | Session | The method | The question it answers |
|---|---|---|---|
| [01](01-foundations-scenarios-and-tools/README.md) | Foundations: Scenarios, Tools, and the Supervised Learning Problem | Loss, risk, $\mathbb{E}[Y\mid X]$ | Before we model the future, what are we claiming to know? |
| [02](02-geometry-of-least-squares/README.md) | Data, Vectors, and the Geometry of Least Squares | OLS, projection, FWL, QR | Why is the most-used estimator in economics a right-angle triangle? |
| [03](03-inference-diagnostics-interpretation/README.md) | Linear Regression: Inference, Diagnostics, Interpretation | Gauss–Markov, robust SEs, OVB | Your coefficient has a standard error. When does it mean anything? |
| [04](04-bias-variance-and-cross-validation/README.md) | Bias–Variance, Overfitting, Cross-Validation | CV, optimism, effective df | Your model fits the past perfectly. Why is that bad news? |
| [05](05-ridge-lasso-elastic-net/README.md) | Regularisation: Ridge, Lasso, Elastic Net | Soft-thresholding, coordinate descent | When is a deliberately biased estimator the better one? |
| [06](06-classification-logistic-and-penalised/README.md) | Classification: Logistic Regression, Regularisation, Thresholds | MLE, IRLS, elastic-net GLM, ROC, cost thresholds | Your classifier is 97% accurate. Should anyone be impressed? |
| [07](07-trees-forests-boosting/README.md) | Trees, Forests, and Gradient Boosting | CART, bagging, functional gradient descent | If we abandon linearity, is interpretability recoverable? |
| [08](08-pca-and-factor-models/README.md) | Unsupervised I: PCA, SVD, and Factor Models | Eckart–Young, Bai–Ng, diffusion indexes | Two hundred macro series move together. How many things are happening? |
| [09](09-clustering-and-text-as-data/README.md) | Unsupervised II: Clustering, Embeddings, Text as Data | Lloyd's algorithm, TF–IDF, validity | How do you measure something that only exists as words? |
| [10](10-causal-machine-learning/README.md) | Causal Machine Learning: Double/Debiased ML | Neyman orthogonality, cross-fitting | You have a superb predictive model. Why can't you choose a policy with it? |
| [11](11-forecasting-drift-and-governance/README.md) | Forecasting, Distribution Shift, and Model Governance | Rolling-origin backtests, Diebold–Mariano, model cards | What are you responsible for when someone acts on your model? |
| [12](12-group-presentations/README.md) | **Final Group Presentations** | — | Can you make a decision-maker act on this — and say what would change your mind? |

**The arc.** Sessions 2–3 build the classical estimator and its inference. Session 4 is the hinge:
in-sample fit stops being evidence. Sessions 5–7 buy flexibility and pay for it in interpretability.
Sessions 8–9 turn to structure we did not label. Session 10 shows why none of the previous nine
sessions licences a policy claim. Session 11 asks what you owe the person who acts on your work —
and returns to the scenario the course opened with. Session 12 is where you defend it.

**Session 6 is deliberately dense.** It composes the Session 5 penalty with the logistic likelihood,
which is why the second half can be short: by then you have derived both halves yourself. Its lab is
split into a compulsory Track A (German Credit) and an extension Track B (bankruptcy data).

---

## Getting started

```bash
git clone <this-repo> MATH60033A
cd MATH60033A

python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py
```

Full instructions, including VS Codium and the local LLM:
**[Setup guide](01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md)**

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
| **Participation** | pass/fail | individual, continuous |
| **Midterm** | **20%** | individual, in class, calculator, no documents — after Session 06 |
| **Group project** | **30%** | groups of three, presented Session 12 |
| **Final paper** | **40%** | teams of three, English, written for [SDAfrique](https://sdafrique.org) |

Group project (30) breaks down as governance file 10 · reproducible analysis 10 · revised Session 1
memo 5 · presentation and defence 5. Session labs themselves are **formative** — commented on, not
marked.

- Example midterm with full solutions: [`assessments/midterm/`](assessments/midterm/EXAM.md)
- Final paper brief: [`assessments/final-paper/`](assessments/final-paper/README.md)
- Session 12 rubric: [`12-group-presentations/`](12-group-presentations/README.md)

Groups confirm their project dataset by Session 10 and draft three of the four components in the
[Session 11 lab](11-forecasting-drift-and-governance/02-lab/README.md).

### Individual accountability inside groups

Four mechanisms, three of which cost nothing during the term. Full policy:
**[`GROUP-ASSESSMENT.md`](GROUP-ASSESSMENT.md)**.

| Mechanism | When | Effect |
|---|---|---|
| **Random presenter draw** | every lab | the 2-minute report is delivered by a member drawn live — so all three must understand everything |
| **Git contribution report** | automatic | commits, share, and weeks active per member; flags the extremes |
| **Rotating role log** | every lab | Driver / Analyst / Reporter must rotate; one row per session |
| **Confidential peer ratings** | once, at term end | four dimensions, 1–5, computing an individual multiplier |

**The default multiplier is 1.00, and a mark is reduced only when the peer ratings and the git
history independently agree.** One signal opens a conversation; it does not move a mark. That gate
is what defeats both rating inflation and retaliation.

### Participation

Pass/fail, separate from the group mark. Attendance is assumed, so participation means contributing
to the room. After each lab you tick the students who did — aim for about a fifth of the class,
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
provenance and a checksum. Every lab must run offline.

**On reproducibility.** One virtual environment, one committed `requirements.txt`, every seed set
explicitly. If your result does not reproduce from a clean clone, it does not reproduce.

**On the local LLM.** Use it freely — as a sparring partner, never as an oracle. Ask it to argue
against you. Verify every factual claim, especially about library APIs and statistical results.
**Every lab deliverable must document at least one instance where you caught the model being wrong,
unverifiable, or misleading.** You are never penalised for using it; you are penalised for using it
uncritically.

**On claims.** When you report a number, be able to say in one sentence where it came from and what
would falsify it.

---

## Repository layout

```
MATH60033A/
├── README.md                          this file
├── RESEARCH-MANDATES.md               the five angles, ten groups, session themes
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
│   ├── 02-lab/
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
  template](11-forecasting-drift-and-governance/02-lab/governance-file-template.md), which is the
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

The course opens and closes with an independent scenario narrative published on 11 June 2026. It is
**not** an official European Union forecast, and its figures are internal parameters of a story
rather than measured predictions. It is used here as a **stress test** — a device for exposing
assumptions — because that is also what a statistical model is.

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
