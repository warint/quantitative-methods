# MATH60033A deck and demo index

Every deck in the course is **Quarto**, rendered to revealjs and published to the course site. The
one exception is session 12, whose pre-session and presentation brief are still PowerPoint.

`slides/reference.pptx` is not a deck — it is the reference document Quarto uses when a `.qmd` is
rendered to `pptx`, which a few are as a fallback.

## The session rhythm

1. **Before class:** open the pre-session PowerPoint, read and annotate the required academic article,
   download its Dataverse package, and answer the self-check. ISLR is optional.
2. **Lecture:** use the equations, visual derivations, graphs, and article connection to build the
   method from intuition to interpretation.
3. **Practice:** work in groups for 90 minutes to reproduce one article result, compare it with the
   session method or a benchmark, and break one assumption.
4. **Present:** finish one slide and give a two-minute presentation. The presenter is selected at
   random. Class ends after the presentations.
5. **Optional lab:** use the QMIB Lab App for an at-home knowledge check. A completed app report
   counts toward participation and is not required preparation for the next lecture.

Session 01 is the exception: its pre-session installs VS Codium, Python, Ollama, Qwen 2.5 Coder,
and Aider; its lecture introduces the syllabus and semester; and its practice is the *Europe 2031*
conversation.

All commands assume that this repository is placed directly at:

```text
Desktop/quantitative-methods
```

Open that folder in VS Codium. Each runnable Python demo is self-contained, uses a fixed seed, works
offline, and saves its figure locally.

> **Everything here is Quarto.** Lecture provenance — which imported source each deck came from —
> is in [`COURSE-QUARTO-SESSIONS.md`](COURSE-QUARTO-SESSIONS.md). Render a single deck with
> `quarto render <file>.qmd --to revealjs`, or the whole site with `scripts/build_docs.py`.

## Deck and demo index

| Session | Pre-session | Lecture | 90-minute practice | Python demo |
|---|---|---|---|---|
| 01 | [Pre-session (Quarto)](../01-foundations-scenarios-and-tools/00-pre-session/MATH60033A-S01-Pre-Session.qmd) | [Lecture (Quarto)](../01-foundations-scenarios-and-tools/01-lecture/MATH60033A-S01-Lecture.qmd) | [Practice (Quarto)](../01-foundations-scenarios-and-tools/02-practice/MATH60033A-S01-Practice.qmd) | [`session01_foundations_demo.py`](../01-foundations-scenarios-and-tools/demo/session01_foundations_demo.py) |
| 02 | [Pre-session (Quarto)](../02-exploratory-data-analysis/00-pre-session/MATH60033A-S02-Pre-Session.qmd) | [Lecture (Quarto)](../02-exploratory-data-analysis/01-lecture/MATH60033A-S02-Lecture.qmd) | [Practice (Quarto)](../02-exploratory-data-analysis/02-practice/MATH60033A-S02-Practice.qmd) | [`session02_eda_demo.py`](../02-exploratory-data-analysis/demo/session02_eda_demo.py) |
| 03 | [Pre-session (Quarto)](../03-regression-adequacy-and-validity/00-pre-session/MATH60033A-S03-Pre-Session.qmd) | [Lecture (Quarto)](../03-regression-adequacy-and-validity/01-lecture/MATH60033A-S03-Lecture.qmd) | [Practice (Quarto)](../03-regression-adequacy-and-validity/02-practice/MATH60033A-S03-Practice.qmd) | [`session03_inference_demo.py`](../03-regression-adequacy-and-validity/demo/session03_inference_demo.py) |
| 04 | [Pre-session (Quarto)](../04-logistic-ordinal-multinomial/00-pre-session/MATH60033A-S04-Pre-Session.qmd) | [Lecture (Quarto)](../04-logistic-ordinal-multinomial/01-lecture/MATH60033A-S04-Lecture.qmd) | [Practice (Quarto)](../04-logistic-ordinal-multinomial/02-practice/MATH60033A-S04-Practice.qmd) | [`session04_cross_validation_demo.py`](../04-logistic-ordinal-multinomial/demo/session04_cross_validation_demo.py) |
| 05 | [Pre-session (Quarto)](../05-ridge-lasso-elastic-net/00-pre-session/MATH60033A-S05-Pre-Session.qmd) | [Lecture (Quarto)](../05-ridge-lasso-elastic-net/01-lecture/MATH60033A-S05-Lecture.qmd) | [Practice (Quarto)](../05-ridge-lasso-elastic-net/02-practice/MATH60033A-S05-Practice.qmd) | [`session05_regularisation_demo.py`](../05-ridge-lasso-elastic-net/demo/session05_regularisation_demo.py) |
| 06 | [Pre-session (Quarto)](../06-advanced-regression/00-pre-session/MATH60033A-S06-Pre-Session.qmd) | [Lecture (Quarto)](../06-advanced-regression/01-lecture/MATH60033A-S06-Lecture.qmd) | [Practice (Quarto)](../06-advanced-regression/02-practice/MATH60033A-S06-Practice.qmd) | [`session06_classification_demo.py`](../06-advanced-regression/demo/session06_classification_demo.py) |
| 07 | [Pre-session (Quarto)](../07-pca-and-factor-analysis/00-pre-session/MATH60033A-S07-Pre-Session.qmd) | [Lecture (Quarto)](../07-pca-and-factor-analysis/01-lecture/MATH60033A-S07-Lecture.qmd) | [Practice (Quarto)](../07-pca-and-factor-analysis/02-practice/MATH60033A-S07-Practice.qmd) | [`session07_ensembles_demo.py`](../07-pca-and-factor-analysis/demo/session07_ensembles_demo.py) |
| 08 | [Pre-session (Quarto)](../08-knn-and-bias-variance/00-pre-session/MATH60033A-S08-Pre-Session.qmd) | [Lecture (Quarto)](../08-knn-and-bias-variance/01-lecture/MATH60033A-S08-Lecture.qmd) | [Practice (Quarto)](../08-knn-and-bias-variance/02-practice/MATH60033A-S08-Practice.qmd) | [`session08_pca_demo.py`](../08-knn-and-bias-variance/demo/session08_pca_demo.py) |
| 09 | [Pre-session (Quarto)](../09-structural-equation-modelling/00-pre-session/MATH60033A-S09-Pre-Session.qmd) | [Lecture (Quarto)](../09-structural-equation-modelling/01-lecture/MATH60033A-S09-Lecture.qmd) | [Practice (Quarto)](../09-structural-equation-modelling/02-practice/MATH60033A-S09-Practice.qmd) | [`session09_clustering_text_demo.py`](../09-structural-equation-modelling/demo/session09_clustering_text_demo.py) |
| 10 | [Pre-session (Quarto)](../10-causal-inference-foundations/00-pre-session/MATH60033A-S10-Pre-Session.qmd) | [Lecture (Quarto)](../10-causal-inference-foundations/01-lecture/MATH60033A-S10-Lecture.qmd) | [Practice (Quarto)](../10-causal-inference-foundations/02-practice/MATH60033A-S10-Practice.qmd) | [`session10_dml_demo.py`](../10-causal-inference-foundations/demo/session10_dml_demo.py) |
| 11 | [Pre-session (Quarto)](../11-causal-inference-did/00-pre-session/MATH60033A-S11-Pre-Session.qmd) | [Lecture (Quarto)](../11-causal-inference-did/01-lecture/MATH60033A-S11-Lecture.qmd) | [Practice (Quarto)](../11-causal-inference-did/02-practice/MATH60033A-S11-Practice.qmd) | [`session11_governance_demo.py`](../11-causal-inference-did/demo/session11_governance_demo.py) |
| 12 | [Pre-session](../12-group-presentations/00-pre-session/MATH60033A-S12-Pre-Session.pptx) | [Group presentations](../12-group-presentations/01-lecture/MATH60033A-S12-Group-Presentations.pptx) | — | — |

## Run a demo

From the VS Codium terminal, for example:

```bash
cd ~/Desktop/quantitative-methods/05-ridge-lasso-elastic-net/demo
python session05_regularisation_demo.py
```

On Windows PowerShell:

```powershell
Set-Location "$HOME\Desktop\quantitative-methods\05-ridge-lasso-elastic-net\demo"
python session05_regularisation_demo.py
```

## QMIB Lab App

Each practice deck closes by distinguishing the optional at-home knowledge check from the next
session's required article and Dataverse preparation.
