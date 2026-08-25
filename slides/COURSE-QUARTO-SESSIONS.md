# Imported Quarto lecture sequence

The lecture sequence below uses the supplied `en.zip` archive and the published
course presentations as the authoritative content sources. Labs were deliberately
left unchanged.

| Course session | Source | Lecture topic | Runnable QMD |
|---|---|---|---|
| S02 | Original S02 | Exploratory data analysis | `02-exploratory-data-analysis/01-lecture/MATH60033A-S02-Lecture.qmd` |
| S03 | Original S04 | Adequacy, validity, and robustness of regression models | `03-inference-diagnostics-interpretation/01-lecture/MATH60033A-S03-Lecture.qmd` |
| S04 | Original S05 | Logistic, ordinal, and multinomial regression | `04-bias-variance-and-cross-validation/01-lecture/MATH60033A-S04-Lecture.qmd` |
| S05 | Repository-native | Ridge, lasso, and elastic net regularisation | `05-ridge-lasso-elastic-net/01-lecture/MATH60033A-S05-Lecture.qmd` |
| S06 | Original S06 | Advanced regression considerations | `06-classification-logistic-and-penalised/01-lecture/MATH60033A-S06-Lecture.qmd` |
| S07 | Original S07 | Principal components and factor analysis | `07-trees-forests-boosting/01-lecture/MATH60033A-S07-Lecture.qmd` |
| S08 | Original S08 | K-nearest neighbours and the bias–variance trade-off | `08-pca-and-factor-models/01-lecture/MATH60033A-S08-Lecture.qmd` |
| S09 | Original S09 | Structural equation modelling | `09-clustering-and-text-as-data/01-lecture/MATH60033A-S09-Lecture.qmd` |
| S10 | Original S10 | Causal inference: logic and tools | `10-causal-machine-learning/01-lecture/MATH60033A-S10-Lecture.qmd` |
| S11 | Original S11 | Causal inference: difference-in-differences | `11-forecasting-drift-and-governance/01-lecture/MATH60033A-S11-Lecture.qmd` |

This places regularisation immediately after the logistic, ordinal, and
multinomial-regression session. The `source-url`, `source-session`, and
`course-session` metadata in remapped decks preserve provenance.

## Rendering

Render all imported lecture decks from the repository root:

```bash
scripts/render_session_lectures.sh
```

Render one session, for example S05:

```bash
scripts/render_session_lectures.sh 05
```

The static imported decks render without R or Python. S05 executes its Python
examples and uses `.venv/bin/python` when that environment is available.

## Course-owned replacement graphics

Third-party teaching images were replaced by original, course-owned graphics in
each lecture's `economist-assets/` directory. They use a restrained
economic-journalism visual language: warm paper, charcoal typography, direct
labels, a red accent, and minimal decoration. Rebuild the chart and diagram
assets with:

```bash
Rscript scripts/build_economist_assets.R
```

The affordable-housing illustration in S11 is an original generated editorial
illustration and is stored locally with the deck.
