# Session replications — the article and data behind each practice

Sessions 02–06 and 08–11 (and 13, after the course) pair one **academic article** with the **data behind it** — a Harvard Dataverse
replication package where the authors deposited one, and otherwise the public database the paper
itself is built on, fetched by `qmib.load()`.
Before class, read and annotate the article, download the package, and identify the table cell,
coefficient, or figure named in the pre-session deck. ISLR is optional background throughout.

During the 90-minute practice, each group:

1. states the article's question, sample, and target result;
2. reproduces one published result from the package;
3. compares it with the session method or a hard benchmark;
4. breaks one assumption or changes one defensible specification; and
5. presents one slide: **article result · our replication · the catch**.

Session 01 is the exception: the pre-session installs the workstation and assigns *Europe 2031*;
the practice is a conversation about evidence, scenario, prediction, and what a local language model
actually does.

## Article–data map

| Session | Academic article | Harvard Dataverse package | Practice target |
|---|---|---|---|
| 02 · Exploratory data analysis | Fraiberger et al. (2021), *Media sentiment and international asset prices* · [article](https://doi.org/10.1016/j.jinteco.2021.103526) | [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF) | Profile the sentiment index — centre, spread, shape, thresholds tested — then fit the paper's simplest return regression and state the slope in units. |
| 03 · Regression diagnostics | Amsili, van Es & Schindelbeck (2024), *Pedotransfer Functions for Field Capacity, Permanent Wilting Point, and Available Water Capacity* · [article](https://doi.org/10.1080/00103624.2024.2336573) | [10.7910/DVN/U5DAEP](https://doi.org/10.7910/DVN/U5DAEP) | Reproduce one predictive regression, then diagnose it: residuals versus fitted, scale–location, leverage and Cook's distance. Which conclusions survive? |
| 04 · Logistic regression | Saganowski et al. (2019), *Analysis of group evolution prediction in complex networks* · [article](https://doi.org/10.1371/journal.pone.0224194) | [10.7910/DVN/ONOFS7](https://doi.org/10.7910/DVN/ONOFS7) | Reproduce one classification result as a logistic model; interpret the odds ratios in words and test one nested comparison. |
| 05 · Regularisation | Blonigen & Piger (2014), *Determinants of foreign direct investment* · [article](https://doi.org/10.1111/caje.12091) · [free preprint](https://www.nber.org/papers/w16704) | No package published — rebuilt by `scripts/build_fdi_determinants.py` from OECD, CEPII, World Bank and Freedom House; load with `qmib.load("fdi")` | The paper runs Bayesian model averaging over 56 candidate determinants of bilateral FDI and finds about sixteen survive. Refit the same 56 for 2019 with lasso, ridge and elastic net, and say which of its conclusions still hold. |
| 06 · Panel data and interactions | Topalova & Khandelwal (2011), *Trade Liberalization and Firm Productivity* · [article](https://doi.org/10.1162/REST_a_00095) | [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) | Reproduce one firm-productivity regression; refit it as a panel with fixed and then random effects, and say which you would report. |
| 07 · Replication workshop | The five articles of sessions 02–06, one replication each | The four packages above, plus `qmib.load("fdi")` | Three hours in autonomy: rebuild one published result from each with only the code seen in class — step-by-step guides in [`07-…/02-practice/replications/`](07-pca-and-factor-analysis/02-practice/replications/). |
| 08 · KNN and bias–variance | Bluwstein, Buckmann, Joseph, Kapadia & Şimşek (2023), *Credit growth, the yield curve and financial crisis prediction* · [article](https://doi.org/10.1016/j.jinteco.2023.103773) · [free working paper](https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2614~6974517ac3.en.pdf) | Jordà–Schularick–Taylor Macrohistory Database, public; load with `qmib.load("jst")` | The paper reports that flexible machine learning beats logistic regression at predicting financial crises. Fit KNN against logistic regression on the same 18-country panel, choose $k$ by cross-validation, and say whether flexibility earned its keep on **your** feature set. |
| 09 · Structural equation modelling | Bennani & Romelli (2024), *Exploring the informativeness and drivers of tone during committee meetings* · [article](https://doi.org/10.1016/j.jimonfin.2024.103161) | [10.7910/DVN/TZEN38](https://doi.org/10.7910/DVN/TZEN38) | The paper builds a measure of an unobservable — tone — from observed indicators. Reproduce one tone result, then specify it as a measurement model and report the fit indices. |
| 10 · Causal inference I | Atkin, Khandelwal & Osman (2017), *Exporting and Firm Performance: Evidence from a Randomized Experiment* · [article](https://doi.org/10.1093/qje/qjx002) | [10.7910/DVN/QOGMVI](https://doi.org/10.7910/DVN/QOGMVI) | Egyptian rug producers were randomly given export orders, so the counterfactual is known. Reproduce the experimental estimate; then throw the randomisation away, re-estimate by propensity-score matching on observables, and report how far matching lands from the truth. |
| 11 · Causal inference II | Cavallo, Gopinath, Neiman & Tang (2021), *Tariff Passthrough at the Border and at the Store: Evidence from US Trade Policy* · [article](https://doi.org/10.1257/aeri.20190536) | [10.7910/DVN/JV7FCH](https://doi.org/10.7910/DVN/JV7FCH) | The 2018–19 US tariffs hit some goods and not others — a difference-in-differences design with a real policy as the treatment. Reproduce one passthrough estimate, show the parallel-trends evidence, and compare conventional with design-aware uncertainty. |
| 13 · One more thing — PCA and factor analysis *(self-study)* | Gygli, Haelg, Potrafke & Sturm (2019), *The KOF Globalisation Index — revisited* · [article](https://doi.org/10.1007/s11558-019-09344-2) | No deposit — the index itself is public; load with `qmib.load("kof")` | The index asserts that globalisation has three dimensions — economic, social, political — built from six sub-dimensions. Run PCA on the sub-indices and ask how many the data actually supports. Defend the number you retain, and interpret the loadings. |

## Downloading a package

Use the DOI link in the pre-session deck and download once, before class. Extract the files to:

```text
Desktop/quantitative-methods/NN-session-name/data/replication/
```

Keep the authors' folder structure and README. Large downloads belong in the git-ignored `data/`
folder, never inside a practice script. The analysis should run locally after the download.

Session 05 is the exception: its authors published no replication package, so the course rebuilt their
design from the sources the paper names. It needs no download — `qmib.load("fdi")` reads a file committed
to the repository. `scripts/build_fdi_determinants.py` documents every source and every substitution.

If command-line download is useful, Dataverse also exposes a dataset endpoint:

```bash
curl -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/8WEXYD" \
  -o data/topalova.zip
unzip data/topalova.zip -d data/topalova/
```

Cite the article and the Dataverse package separately. They are distinct research contributions with
distinct DOIs.
