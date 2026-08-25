# MATH60033A course PowerPoints

The course contains **35 PowerPoint decks and 351 slides**. The files have stable, descriptive names
and use the same visual system throughout. Source credits and reading links are stored in the speaker
notes under `[Sources]`.

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

## Deck and demo index

| Session | Pre-session | Lecture | 90-minute practice | Python demo |
|---|---|---|---|---|
| 01 | [Pre-session](../01-foundations-scenarios-and-tools/00-pre-session/MATH60033A-S01-Pre-Session.pptx) | [Lecture](../01-foundations-scenarios-and-tools/01-lecture/MATH60033A-S01-Lecture.pptx) | [In-class practice](../01-foundations-scenarios-and-tools/02-practice/MATH60033A-S01-In-Class-Practice.pptx) | [`session01_foundations_demo.py`](../01-foundations-scenarios-and-tools/demo/session01_foundations_demo.py) |
| 02 | [Pre-session](../02-exploratory-data-analysis/00-pre-session/MATH60033A-S02-Pre-Session.pptx) | [Lecture](../02-exploratory-data-analysis/01-lecture/MATH60033A-S02-Lecture.pptx) | [In-class practice](../02-exploratory-data-analysis/02-practice/MATH60033A-S02-In-Class-Practice.pptx) | [`session02_ols_geometry_demo.py`](../02-exploratory-data-analysis/demo/session02_ols_geometry_demo.py) |
| 03 | [Pre-session](../03-inference-diagnostics-interpretation/00-pre-session/MATH60033A-S03-Pre-Session.pptx) | [Lecture](../03-inference-diagnostics-interpretation/01-lecture/MATH60033A-S03-Lecture.pptx) | [In-class practice](../03-inference-diagnostics-interpretation/02-practice/MATH60033A-S03-In-Class-Practice.pptx) | [`session03_inference_demo.py`](../03-inference-diagnostics-interpretation/demo/session03_inference_demo.py) |
| 04 | [Pre-session](../04-bias-variance-and-cross-validation/00-pre-session/MATH60033A-S04-Pre-Session.pptx) | [Lecture](../04-bias-variance-and-cross-validation/01-lecture/MATH60033A-S04-Lecture.pptx) | [In-class practice](../04-bias-variance-and-cross-validation/02-practice/MATH60033A-S04-In-Class-Practice.pptx) | [`session04_cross_validation_demo.py`](../04-bias-variance-and-cross-validation/demo/session04_cross_validation_demo.py) |
| 05 | [Pre-session](../05-ridge-lasso-elastic-net/00-pre-session/MATH60033A-S05-Pre-Session.pptx) | [Lecture](../05-ridge-lasso-elastic-net/01-lecture/MATH60033A-S05-Lecture.pptx) | [In-class practice](../05-ridge-lasso-elastic-net/02-practice/MATH60033A-S05-In-Class-Practice.pptx) | [`session05_regularisation_demo.py`](../05-ridge-lasso-elastic-net/demo/session05_regularisation_demo.py) |
| 06 | [Pre-session](../06-classification-logistic-and-penalised/00-pre-session/MATH60033A-S06-Pre-Session.pptx) | [Lecture](../06-classification-logistic-and-penalised/01-lecture/MATH60033A-S06-Lecture.pptx) | [In-class practice](../06-classification-logistic-and-penalised/02-practice/MATH60033A-S06-In-Class-Practice.pptx) | [`session06_classification_demo.py`](../06-classification-logistic-and-penalised/demo/session06_classification_demo.py) |
| 07 | [Pre-session](../07-trees-forests-boosting/00-pre-session/MATH60033A-S07-Pre-Session.pptx) | [Lecture](../07-trees-forests-boosting/01-lecture/MATH60033A-S07-Lecture.pptx) | [In-class practice](../07-trees-forests-boosting/02-practice/MATH60033A-S07-In-Class-Practice.pptx) | [`session07_ensembles_demo.py`](../07-trees-forests-boosting/demo/session07_ensembles_demo.py) |
| 08 | [Pre-session](../08-pca-and-factor-models/00-pre-session/MATH60033A-S08-Pre-Session.pptx) | [Lecture](../08-pca-and-factor-models/01-lecture/MATH60033A-S08-Lecture.pptx) | [In-class practice](../08-pca-and-factor-models/02-practice/MATH60033A-S08-In-Class-Practice.pptx) | [`session08_pca_demo.py`](../08-pca-and-factor-models/demo/session08_pca_demo.py) |
| 09 | [Pre-session](../09-clustering-and-text-as-data/00-pre-session/MATH60033A-S09-Pre-Session.pptx) | [Lecture](../09-clustering-and-text-as-data/01-lecture/MATH60033A-S09-Lecture.pptx) | [In-class practice](../09-clustering-and-text-as-data/02-practice/MATH60033A-S09-In-Class-Practice.pptx) | [`session09_clustering_text_demo.py`](../09-clustering-and-text-as-data/demo/session09_clustering_text_demo.py) |
| 10 | [Pre-session](../10-causal-machine-learning/00-pre-session/MATH60033A-S10-Pre-Session.pptx) | [Lecture](../10-causal-machine-learning/01-lecture/MATH60033A-S10-Lecture.pptx) | [In-class practice](../10-causal-machine-learning/02-practice/MATH60033A-S10-In-Class-Practice.pptx) | [`session10_dml_demo.py`](../10-causal-machine-learning/demo/session10_dml_demo.py) |
| 11 | [Pre-session](../11-forecasting-drift-and-governance/00-pre-session/MATH60033A-S11-Pre-Session.pptx) | [Lecture](../11-forecasting-drift-and-governance/01-lecture/MATH60033A-S11-Lecture.pptx) | [In-class practice](../11-forecasting-drift-and-governance/02-practice/MATH60033A-S11-In-Class-Practice.pptx) | [`session11_governance_demo.py`](../11-forecasting-drift-and-governance/demo/session11_governance_demo.py) |
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
