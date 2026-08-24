# Session replications — the article and data behind each practice

Sessions 02–11 pair one **academic article** with its **Harvard Dataverse replication package**.
Before class, read and annotate the article, download the package, and identify the table cell,
coefficient, or figure named in the pre-session PowerPoint. ISLR is optional background throughout.

During the 90-minute practice, each group:

1. states the article's question, sample, and target result;
2. reproduces one published result from the package;
3. compares it with the session method or a hard benchmark;
4. breaks one assumption or changes one defensible specification; and
5. presents one slide: **article result · our replication · the catch**.

Session 01 is the exception: the pre-session installs the workstation and assigns *Europe 2031*;
the practice is a conversation about evidence, scenario, prediction, and what a local language model
actually does.

## Article–Dataverse map

| Session | Academic article | Harvard Dataverse package | Practice target |
|---|---|---|---|
| 02 · OLS geometry | Topalova & Khandelwal (2011), *Trade Liberalization and Firm Productivity* · [article](https://doi.org/10.1162/REST_a_00095) | [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) | Reproduce one firm-productivity regression; rebuild the OLS geometry and collinearity stress test in Python. |
| 03 · Inference | Ferman & Pinto (2019), *Inference in Differences-in-Differences with Few Treated Groups and Heteroskedasticity* · [article](https://doi.org/10.1162/rest_a_00759) | [10.7910/DVN/PIAZWN](https://doi.org/10.7910/DVN/PIAZWN) | Reproduce one inference result; compare conventional, robust, and design-aware uncertainty. |
| 04 · Cross-validation | Amsili, van Es & Schindelbeck (2024), *Pedotransfer Functions for Field Capacity, Permanent Wilting Point, and Available Water Capacity* · [article](https://doi.org/10.1080/00103624.2024.2336573) | [10.7910/DVN/U5DAEP](https://doi.org/10.7910/DVN/U5DAEP) | Reproduce one reported predictive comparison; rebuild the validation and stress spatial leakage. |
| 05 · Regularisation | Frandi et al. (2016), *Fast and Scalable Lasso via Stochastic Frank-Wolfe Methods with a Convergence Guarantee* · [article](https://doi.org/10.1007/s10994-016-5578-4) | [10.7910/DVN/QJEUKR](https://doi.org/10.7910/DVN/QJEUKR) | Reproduce one sparse-model comparison on selected train/test files; compare lasso, ridge, and elastic net. |
| 06 · Classification | Saganowski et al. (2019), *Analysis of group evolution prediction in complex networks* · [article](https://doi.org/10.1371/journal.pone.0224194) | [10.7910/DVN/ONOFS7](https://doi.org/10.7910/DVN/ONOFS7) | Reproduce one classification result; then set a decision threshold from error costs. |
| 07 · Ensembles | Amsili, van Es & Schindelbeck (2025), *Pedotransfer Functions for Soil Protein Based on Random Forest Modeling* · [article](https://doi.org/10.1080/00103624.2025.2454015) | [10.7910/DVN/HGBPCW](https://doi.org/10.7910/DVN/HGBPCW) | Reproduce the full-versus-reduced random-forest comparison; add boosting and audit importance. |
| 08 · PCA and factors | Koopman & Mesters (2017), *Empirical Bayes Methods for Dynamic Factor Models* · [article](https://doi.org/10.1162/REST_a_00614) | [10.7910/DVN/NKWMQM](https://doi.org/10.7910/DVN/NKWMQM) | Reproduce one factor or forecast figure; rebuild the first components and compare predictive value. |
| 09 · Text and clustering | Bennani & Romelli (2024), *Exploring the informativeness and drivers of tone during committee meetings* · [article](https://doi.org/10.1016/j.jimonfin.2024.103161) | [10.7910/DVN/TZEN38](https://doi.org/10.7910/DVN/TZEN38) | Reproduce one tone result; rebuild a text index and test cluster stability. |
| 10 · Causal ML | Bodory, Huber & Lafférs (2022), *Evaluating (weighted) dynamic treatment effects by double machine learning* · [article](https://doi.org/10.1093/ectj/utac018) | [10.7910/DVN/FS0KBA](https://doi.org/10.7910/DVN/FS0KBA) | Reproduce one treatment-effect estimate; vary nuisance learners and document what remains stable. |
| 11 · Forecasting and governance | Fraiberger et al. (2021), *Media sentiment and international asset prices* · [article](https://doi.org/10.1016/j.jinteco.2021.103526) | [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF) | Reproduce one sentiment-return result; backtest by forecast origin and write a drift response. |

## Downloading a package

Use the DOI link in the pre-session PowerPoint and download once, before class. Extract the files to:

```text
Desktop/quantitative-methods/NN-session-name/data/replication/
```

Keep the authors' folder structure and README. Large downloads belong in the git-ignored `data/`
folder, never inside a practice script. The analysis should run locally after the download.

The Session 05 package is especially large. Download only the selected train/test files named in the
pre-session instructions (about 48 MB), not the entire deposit.

If command-line download is useful, Dataverse also exposes a dataset endpoint:

```bash
curl -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/8WEXYD" \
  -o data/topalova.zip
unzip data/topalova.zip -d data/topalova/
```

Cite the article and the Dataverse package separately. They are distinct research contributions with
distinct DOIs.
