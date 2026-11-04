r"""
Session 08 · File 1 of 2 — train a KNN classifier, choosing K by cross-validation

THE QUESTION
    Can the stock market's returns of the last two days tell us whether it will
    go up or down today? We let a K-nearest-neighbours classifier try, we choose
    its K honestly by cross-validation, we judge it once on a year it has never
    seen, and we save it so that File 2 can use it on a brand-new date.

HOW TO RUN IT
    1. Put this file in a folder of your own (for example "session-08") and open
       that folder in VS Codium (File > Open Folder).
    2. You need four packages. If you have not installed them yet, type this
       once in the VS Codium terminal:
           pip install pandas numpy matplotlib scikit-learn
    3. Press the Run button (the triangle, top right), or type in the terminal:
           python session08_1_train.py
       It takes a few seconds. When it finishes, a file called
       knn_smarket.joblib has appeared in your folder: that is the trained model.
    4. Then run File 2, session08_2_predict.py, from the same folder.

    The data is read from the internet, so you need a connection — nothing else.
    On macOS with Python from python.org, if reading the data fails with
    CERTIFICATE_VERIFY_FAILED, run this once in the terminal, then try again:
           open /Applications/Python\ 3*/Install\ Certificates.command

    To go one step at a time: select the lines of one step and press
    Shift+Enter. Run the steps in order: each step uses what the earlier
    steps created.

THE STEPS
    Step 1  Load the data and look at it
    Step 2  Put the newest day aside: it plays "tomorrow" for File 2
    Step 3  Split the rest by time: learn from 2001-2004, test on 2005
    Step 4  Cut the training years into cross-validation folds, in time order
    Step 5  Cross-validation by hand, for one value of K
    Step 6  Cross-validation for every K at once, and the curve it draws
    Step 7  Open the test year — once — and judge the chosen model
    Step 8  Refit on all the history we have, and save the model for File 2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib                      # installed together with scikit-learn: saves a model to a file
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix


# =============================================================================
# Step 1 · Load the data and look at it
# =============================================================================
# Smarket: the S&P 500 index, every trading day from 2001 to 2005 (1,250 days).
# It comes from the textbook "An Introduction to Statistical Learning" (ISLR).
#   Lag1   the market's % return the day before
#   Lag2   the market's % return two days before
#   Lag3 ... Lag5, Volume   older returns, and the number of shares traded
#   Today      the market's % return that day
#   Direction  "Up" or "Down": did the market rise that day?   <- what we predict
# Careful: Direction is just the sign of Today. Today is the answer in disguise,
# so it must NEVER be used as a predictor.
URL = "https://raw.githubusercontent.com/intro-stat-learning/ISLP/main/ISLP/data/Smarket.csv"
smarket = pd.read_csv(URL)

print(smarket.shape)                          # (1250, 9): 1,250 days, 9 columns
print(smarket.head())
print(smarket["Direction"].value_counts())    # roughly as many Up days as Down days

# The two predictors we give KNN: the returns of the last two days.
predictors = ["Lag1", "Lag2"]


# =============================================================================
# Step 2 · Put the newest day aside
# =============================================================================
# The very last row is the last trading day of 2005 (30 December 2005).
# We hide it now and never show it to the model in this file. File 2 will
# treat it as a new date and predict it: a genuine out-of-sample prediction.
new_day = smarket.tail(1)
history = smarket.iloc[:-1]                   # every day except the last one

print("The day kept aside for File 2:")
print(new_day[["Year", "Lag1", "Lag2", "Direction"]])
print(f"History left for this file: {len(history)} days")


# =============================================================================
# Step 3 · Split by time: learn from 2001-2004, test on 2005
# =============================================================================
# Never shuffle a time series. A random split would put days of 2005 in the
# training set and days of 2001 in the test set: the model would learn from the
# future to "predict" the past, and its score would be too good to be true.
train = history[history["Year"] < 2005]
test = history[history["Year"] == 2005]

X_train, y_train = train[predictors], train["Direction"]
X_test, y_test = test[predictors], test["Direction"]

print(f"training set: {len(train)} days (2001-2004)  <- used to learn and to choose K")
print(f"test set:     {len(test)} days (2005)       <- locked away until Step 7")


# =============================================================================
# Step 4 · Cut the training years into cross-validation folds, in time order
# =============================================================================
# We need to choose K without touching the test year. Cross-validation does it
# by pretending part of the training data is new: hide it, fit on the rest,
# count the mistakes on what was hidden, and repeat.
#
# With a time series the hidden part must always come AFTER the part we fit on.
# TimeSeriesSplit cuts the 998 training days into 6 blocks in time order:
#   round 1: fit on block 1,            validate on block 2
#   round 2: fit on blocks 1-2,         validate on block 3
#   ...
#   round 5: fit on blocks 1-5,         validate on block 6
folds = TimeSeriesSplit(n_splits=5)

for r, (fit_rows, check_rows) in enumerate(folds.split(X_train), start=1):
    print(f"round {r}: fit on days 1 to {fit_rows[-1] + 1}, "
          f"validate on days {check_rows[0] + 1} to {check_rows[-1] + 1}")


# =============================================================================
# Step 5 · Cross-validation by hand, for one value of K
# =============================================================================
# KNN measures distances, so both predictors must be on the same scale.
# StandardScaler turns each column into (x - mean) / standard deviation.
# make_pipeline glues the scaler and KNN together into ONE model: every time
# the model is fitted, the scaler is fitted too, on the fitting rows only.
# So the scaler never peeks at the rows it will be judged on.
model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=25))

errors = []
for r, (fit_rows, check_rows) in enumerate(folds.split(X_train), start=1):
    # .iloc picks rows by position: the fitting rows, then the hidden rows
    model.fit(X_train.iloc[fit_rows], y_train.iloc[fit_rows])
    accuracy = model.score(X_train.iloc[check_rows], y_train.iloc[check_rows])
    errors.append(1 - accuracy)
    print(f"round {r}: error on the hidden block = {1 - accuracy:.3f}")

print(f"K = 25: cross-validated error = {np.mean(errors):.3f}  "
      f"(the five rounds differ by up to {max(errors) - min(errors):.3f})")
# This average is our estimate of how K = 25 would do on days it has not seen.


# =============================================================================
# Step 6 · Cross-validation for every K at once
# =============================================================================
# GridSearchCV is exactly the loop of Step 5, run for every K in a list.
# It then picks the K with the best cross-validated accuracy, and refits the
# model with that K on all 998 training days.
#
# K = 1, 3, 5, ..., 151: odd numbers, so a two-class vote can never tie.
# "kneighborsclassifier__n_neighbors" means: inside the pipeline, the step
# called "kneighborsclassifier", its setting "n_neighbors" (two underscores).
k_values = list(range(1, 152, 2))
search = GridSearchCV(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                      {"kneighborsclassifier__n_neighbors": k_values},
                      cv=folds)
search.fit(X_train, y_train)

best_k = search.best_params_["kneighborsclassifier__n_neighbors"]
majority = y_train.value_counts(normalize=True).max()   # share of the commonest class
print(f"best K = {best_k}")
print(f"cross-validated accuracy at that K = {search.best_score_:.3f}")
print(f"always predicting the commonest direction = {majority:.3f}   <- the bar to beat")

# The whole curve: one cross-validated accuracy per K.
# Small K (left): flexible, follows single days, noisy.  Large K (right): rigid, smooth.
plt.figure(figsize=(8, 3.5))
plt.plot(k_values, search.cv_results_["mean_test_score"], "o-", markersize=3,
         label="KNN, cross-validated accuracy")
plt.axhline(majority, color="red", linestyle="--", label="always predict the commonest direction")
plt.axvline(best_k, color="grey", linestyle=":", label=f"chosen K = {best_k}")
plt.xlabel("K (number of neighbours)")
plt.ylabel("accuracy on the hidden blocks")
plt.legend()
plt.tight_layout()
plt.show()          # close the plot window to let the script continue


# =============================================================================
# Step 7 · Open the test year — once — and judge the chosen model
# =============================================================================
# K is chosen. Only now do we look at 2005. We do it once: if we went back and
# changed K after seeing this score, 2005 would become training data and the
# score would no longer be honest.
y_pred = search.predict(X_test)

table = pd.DataFrame(confusion_matrix(y_test, y_pred, labels=["Down", "Up"]),
                     index=["actual Down", "actual Up"],
                     columns=["predicted Down", "predicted Up"])
print(table)       # rows = what really happened, columns = what the model said

accuracy = (y_pred == y_test).mean()
baseline = y_test.value_counts(normalize=True).max()
print(f"KNN accuracy on 2005:                   {accuracy:.3f}")
print(f"always predicting the commonest direction: {baseline:.3f}")
# Read this honestly. If KNN does not beat the simple rule, the two lags carry
# (almost) no usable signal about today's direction. That is a finding, not a
# failure: markets that were easy to predict from yesterday would not stay so.


# =============================================================================
# Step 8 · Refit on all the history we have, and save the model
# =============================================================================
# The test year has done its job: it gave us an honest score. Before using the
# model for real, we let it learn from everything we know — 2001 to 2005, all
# but the day kept aside — with the K that cross-validation chose.
final_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k))
final_model.fit(history[predictors], history["Direction"])

# Save it to a file in this folder. File 2 loads it from there.
joblib.dump(final_model, "knn_smarket.joblib")
print(f"Saved: knn_smarket.joblib  (KNN with K = {best_k}, "
      f"learned from {len(history)} days). Now run session08_2_predict.py.")
