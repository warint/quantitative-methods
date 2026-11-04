r"""
Session 08 · Practice — does flexibility buy you anything on your own data?

HOW TO RUN IT
    1. Put this file in a folder of your own (for example "session-08") and open
       that folder in VS Codium (File > Open Folder).
    2. You need four packages. If you have not installed them yet, type this
       once in the VS Codium terminal:
           pip install pandas numpy matplotlib scikit-learn
    3. Press the Run button (the triangle, top right), or type in the terminal:
           python session08_practice.py

    The data is read from the course site, so you need a connection — nothing else.
    On macOS with Python from python.org, if reading the data fails with
    CERTIFICATE_VERIFY_FAILED, run this once in the terminal, then try again:
           open /Applications/Python\ 3*/Install\ Certificates.command

    To go one step at a time: select the lines of one step and press
    Shift+Enter. Run the steps in order: each step uses what the earlier
    steps created.

WHAT IT DOES
    Part 1 · Reproduce   (20 min)  the paper's question on the paper's data:
                                   can credit growth and the yield curve predict
                                   a financial crisis, and does KNN beat a logit?
    Part 2 · Apply       (35 min)  the same comparison on YOUR angle
    Part 3 · Break       (15 min)  one assumption, deliberately: what happens?
    Part 4 · Write       (20 min)  250 words — that part is yours, not the script's

THE ONE LINE YOU MUST CHANGE: MY_ANGLE, in Part 2.
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.inspection import permutation_importance

SITE = "https://warint.github.io/quantitative-methods/data/"

def folds_for(y):
    """Cross-validation folds that keep the share of positives the same in every
    fold — with ~10% positives, a plain split could leave a fold with none.
    Five folds, or fewer if there are fewer than five positives."""
    return StratifiedKFold(n_splits=min(5, int(y.sum())), shuffle=True, random_state=0)


def k_values_for(X, folds):
    """K = 1, 3, 5, ..., 51 — but never more neighbours than a training fold has rows."""
    rows_per_fold = len(X) * (folds.n_splits - 1) // folds.n_splits
    return [k for k in range(1, 52, 2) if k < rows_per_fold]


def knn_by_cv(X, y, standardise=True):
    """KNN with K chosen by cross-validation on AUC. Returns the fitted search;
    its .predict_proba uses the best K, refitted on all of X."""
    folds = folds_for(y)
    steps = [StandardScaler(), KNeighborsClassifier()] if standardise else [KNeighborsClassifier()]
    search = GridSearchCV(make_pipeline(*steps),
                          {"kneighborsclassifier__n_neighbors": k_values_for(X, folds)},
                          cv=folds, scoring="roc_auc")
    return search.fit(X, y)


def logit():
    """The simple alternative: a standardised logistic regression."""
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))


def test_auc(model, X_test, y_test):
    """AUC on the test set: 0.5 = a coin toss, 1.0 = perfect ranking."""
    return roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])


# =============================================================================
# Part 1 · Reproduce — Bluwstein et al. (2023) on the Jorda-Schularick-Taylor data
# =============================================================================
# One row per country-year: 18 advanced economies, 1870-2020.
#   crisis_next2   1 if a systemic banking crisis starts in the next two years  <- outcome
#   the predictors, as the paper builds them (two-year changes unless noted):
#   credit_growth  change in bank credit / GDP     yield_slope   long minus short rate
#   money_growth   change in broad money / GDP     cpi_growth    % change in prices
#   pubdebt_change change in public debt / GDP     ca_gdp        current account / GDP
#   investment_change  change in investment / GDP
# Data: Jorda, Schularick & Taylor (2017), Macrohistory Database, CC BY-NC-SA 4.0.
jst = pd.read_csv(SITE + "session-08/jst_crises.csv")
print(jst.shape)
print(jst.head())

predictors = ["credit_growth", "yield_slope", "money_growth", "cpi_growth",
              "pubdebt_change", "ca_gdp", "investment_change"]

# The paper's filters: drop the two world wars, and the years a crisis is
# already under way (we want to predict a crisis before it starts).
wars = jst["year"].between(1914, 1918) | jst["year"].between(1939, 1945)
jst = jst[~wars & (jst["crisisjst"] != 1)]
jst = jst.dropna(subset=predictors)        # KNN cannot measure a distance to a gap
print(f"{len(jst)} country-years, {int(jst['crisis_next2'].sum())} with a crisis ahead")

# A time split, as in the lecture: learn from history, test on the recent past.
train = jst[jst["year"] < 1980]
test = jst[jst["year"] >= 1980]
X_train, y_train = train[predictors], train["crisis_next2"]
X_test, y_test = test[predictors], test["crisis_next2"]
print(f"train 1870-1979: {len(train)} rows · test 1980-2020: {len(test)} rows")

# Three models, each scored by AUC on 1980-2020. Accuracy would mislead here:
# with ~8% positives, "never a crisis" is 92% accurate and useless.
knn = knn_by_cv(X_train, y_train)
lr = logit().fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=500, min_samples_leaf=5,
                                random_state=0, n_jobs=-1).fit(X_train, y_train)

print("chosen K:", knn.best_params_["kneighborsclassifier__n_neighbors"])
print(f"test AUC   logit {test_auc(lr, X_test, y_test):.3f}   "
      f"KNN {test_auc(knn, X_test, y_test):.3f}   "
      f"random forest {test_auc(forest, X_test, y_test):.3f}")

# The paper's headline: credit growth and the yield slope do most of the work.
# Shuffle one predictor at a time and see how much the forest's test AUC falls.
imp = permutation_importance(forest, X_test, y_test, scoring="roc_auc",
                             n_repeats=20, random_state=0)
print(pd.Series(imp.importances_mean, index=predictors)
      .sort_values(ascending=False).round(3).to_string())
# -> Does your ranking match the paper's? If not, where could the difference come
#    from (sample, horizon, the model, the split)? That is the diagnosis to write.


# =============================================================================
# Part 2 · Apply — the same comparison on YOUR angle
# =============================================================================
# CHANGE THIS to your group's angle (RESEARCH-MANDATES.md, section 4):
#   angle_a_country  angle_a_sector  angle_b_occupation  angle_b_sector
#   angle_c_country  angle_c_sector_size  angle_d_partner  angle_d_product
# (angle_e_* are text corpora: see your data dictionary before you try KNN on them.)
MY_ANGLE = "angle_c_country"

core = pd.read_csv(SITE + "core.csv")        # shared by every group: 30 countries, 2010-2024
mine = pd.read_csv(SITE + MY_ANGLE + ".csv")

# Some angles have more than one row per country-year (one per sector, partner,
# product or occupation). Average them to one row per country-year first.
# ("hs" is a product code, not a measurement, so it is not averaged.)
mine = mine.drop(columns=["hs"], errors="ignore")
mine = mine.groupby(["geo", "time"]).mean(numeric_only=True).reset_index()
# A column in both files (employment_ths, say) keeps the angle's version as "<name>_angle".
mine = mine.rename(columns={c: c + "_angle" for c in mine.columns
                            if c in core.columns and c not in ("geo", "time")})
df = core.merge(mine, on=["geo", "time"], how="inner")

# The outcome, from core: 1 if the country falls behind next year (session 06).
outcome = "falling_behind_next"
# The predictors: every numeric column your angle brings, except those missing
# in more than 20% of rows (some survey questions were asked only in some years).
# Replace this list with the ones your question needs — see your data dictionary.
numeric = [c for c in mine.columns if c not in ("geo", "time")]
share_missing = df[numeric].isna().mean()
my_predictors = [c for c in numeric if share_missing[c] <= 0.20]
print("left out (mostly missing):", [c for c in numeric if c not in my_predictors])
df = df.dropna(subset=my_predictors + [outcome])
print(f"{len(df)} country-years, {df['time'].min()}-{df['time'].max()}, "
      f"{len(my_predictors)} predictors, {df[outcome].mean():.0%} positive")

# Time split: the last two years are the test set.
last = df["time"].max()
train2, test2 = df[df["time"] <= last - 2], df[df["time"] > last - 2]
print(f"train: {len(train2)} rows · test: {len(test2)} rows")
Xa, ya = train2[my_predictors], train2[outcome]
Xb, yb = test2[my_predictors], test2[outcome]

knn2 = knn_by_cv(Xa, ya)
lr2 = logit().fit(Xa, ya)
print("chosen K:", knn2.best_params_["kneighborsclassifier__n_neighbors"])
print(f"test AUC   logit {test_auc(lr2, Xb, yb):.3f}   KNN {test_auc(knn2, Xb, yb):.3f}")
# -> Did the flexible model earn its keep against the logit? Say it in a sentence.


# =============================================================================
# Part 3 · Break one assumption — pick ONE, run it, record what changed
# =============================================================================
# (a) KNN needs standardised predictors. Drop the scaler:
raw = knn_by_cv(Xa, ya, standardise=False)
print(f"(a) without standardising: test AUC {test_auc(raw, Xb, yb):.3f}")

# (b) KNN suffers as predictors multiply. Keep only the first three:
few = my_predictors[:3]
knn_few = knn_by_cv(Xa[few], ya)
print(f"(b) with only {few}: test AUC {test_auc(knn_few, Xb[few], yb):.3f}")

# (c) Never let the future leak into the past. Use a RANDOM split instead of a time split:
from sklearn.model_selection import train_test_split

Xr_a, Xr_b, yr_a, yr_b = train_test_split(df[my_predictors], df[outcome], test_size=0.2,
                                          random_state=0, stratify=df[outcome])
knn_rand = knn_by_cv(Xr_a, yr_a)
print(f"(c) random split: test AUC {test_auc(knn_rand, Xr_b, yr_b):.3f}  "
      f"(time split gave {test_auc(knn2, Xb, yb):.3f})")
# -> Which one moved your answer most, and why? That goes in your 250 words.
