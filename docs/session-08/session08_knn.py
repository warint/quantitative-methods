"""
Session 08 · K-nearest neighbours — every line of code from the lecture, in order

HOW TO RUN IT
    1. Put this file in a folder of your own (for example "session-08") and open
       that folder in VS Codium (File > Open Folder).
    2. You need four packages. If you have not installed them yet, type this
       once in the VS Codium terminal:
           pip install pandas numpy matplotlib scikit-learn
    3. Press the Run button (the triangle, top right), or type in the terminal:
           python session08_knn.py

    The data is read from the internet, so you need a connection — nothing else.
    On macOS with Python from python.org, if reading the data fails with
    CERTIFICATE_VERIFY_FAILED, run this once in the terminal, then try again:
           open /Applications/Python\ 3*/Install\ Certificates.command

    To go one step at a time: select the lines of one step and press
    Shift+Enter. Run the steps in order: each step uses what the earlier
    steps created (smarket, train, test, ...).

WHAT IT DOES
    Step 1  KNN by hand: six observations, one test point, Euclidean distances
    Step 2  Load the stock-market data (S&P 500, 2001-2005)
    Step 3  Split by time: train on 2001-2004, test on 2005
    Step 4  Choose K by cross-validation, and plot the result
    Step 5  Which inputs matter? (permutation importance)
    Step 6  Score the model on the test year, once
    Step 7  Predict one day of your own choosing
    Step 8  Beyond one classifier: iris, house prices, a random forest
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.inspection import permutation_importance


# =============================================================================
# Step 1 · KNN by hand: which of six observations is closest to (0, 0, 0)?
# =============================================================================
# Six training observations, three predictors (X1, X2, X3) and a colour.
by_hand = pd.DataFrame({
    "X1": [0, 2, 0, 0, -1, 1],
    "X2": [3, 0, 1, 1, 0, 1],
    "X3": [0, 0, 3, 2, 1, 1],
    "Y":  ["Red", "Red", "Red", "Green", "Green", "Red"],
}, index=[1, 2, 3, 4, 5, 6])

# The test point is X1 = X2 = X3 = 0. Euclidean distance to it:
#   d = square root of (X1 - 0)^2 + (X2 - 0)^2 + (X3 - 0)^2
by_hand["distance"] = np.sqrt(by_hand["X1"]**2 + by_hand["X2"]**2 + by_hand["X3"]**2)

# Sort from nearest to farthest, and read off the answer for K = 1 and K = 3.
by_hand = by_hand.sort_values("distance")
print(by_hand.round(3))
print("K = 1 predicts:", by_hand["Y"].iloc[:1].mode()[0])   # the single nearest
print("K = 3 predicts:", by_hand["Y"].iloc[:3].mode()[0])   # majority of the 3 nearest


# =============================================================================
# Step 2 · Load the stock-market data
# =============================================================================
# Smarket: 1,250 trading days of the S&P 500, 2001-2005 (from the ISLR textbook).
#   Lag1 ... Lag5  the market's % return 1 to 5 days earlier
#   Direction      "Up" or "Down": did the market rise that day?   <- what we predict
URL = "https://raw.githubusercontent.com/intro-stat-learning/ISLP/main/ISLP/data/Smarket.csv"
smarket = pd.read_csv(URL)

print(smarket.shape)                          # (1250, 9): rows, columns
print(smarket.head())
print(smarket["Direction"].value_counts())    # how many Up days, how many Down


# =============================================================================
# Step 3 · Split by time: train on 2001-2004, test on 2005
# =============================================================================
# Never shuffle a time series: a random split would let tomorrow's market help
# "predict" yesterday's (leakage), and the score would be too good to be true.
train = smarket[smarket["Year"] < 2005]
test = smarket[smarket["Year"] == 2005]

predictors = ["Lag1", "Lag2"]                 # yesterday's and the day before's return
X_train, y_train = train[predictors], train["Direction"]
X_test, y_test = test[predictors], test["Direction"]

print(f"training set: {len(train)} days (2001-2004)")
print(f"test set:     {len(test)} days (2005)")


# =============================================================================
# Step 4 · Choose K by cross-validation
# =============================================================================
# KNN measures distances, so every predictor must be on the same scale:
# StandardScaler turns each column into (x - mean) / standard deviation.
# Putting the scaler INSIDE the pipeline means it is refitted on each
# cross-validation fold, so it never peeks at the fold it is scored on.
pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier())

# Try K = 1, 3, 5, ..., 101 (odd values cannot tie in a two-class vote),
# scoring each by 5-fold cross-validation on the TRAINING set only.
# The pipeline names its KNN step "kneighborsclassifier"; the double underscore
# "__" reaches inside that step to its n_neighbors setting.
k_values = list(range(1, 102, 2))
search = GridSearchCV(pipeline, {"kneighborsclassifier__n_neighbors": k_values}, cv=5)
search.fit(X_train, y_train)

best_k = search.best_params_["kneighborsclassifier__n_neighbors"]
majority = y_train.value_counts(normalize=True).max()   # share of the commonest class
print(f"best K = {best_k}")
print(f"cross-validated accuracy at that K = {search.best_score_:.3f}")
print(f"always predicting the commonest class = {majority:.3f}   <- the bar to beat")

# The whole curve: accuracy for every K that was tried.
plt.figure(figsize=(8, 3.5))
plt.plot(k_values, search.cv_results_["mean_test_score"], "o-", label="KNN, 5-fold CV")
plt.axhline(majority, color="red", linestyle="--", label="always predict the commonest class")
plt.xlabel("K (number of neighbours)")
plt.ylabel("cross-validated accuracy")
plt.legend()
plt.tight_layout()
plt.show()          # close the plot window to let the script continue


# =============================================================================
# Step 5 · Which inputs matter? Permutation importance
# =============================================================================
# KNN has no coefficients. Instead: shuffle one column, and see how much the
# test accuracy drops. A big drop = the model relied on that column.
# A value near zero (or negative) = the column carried no usable signal.
importance = permutation_importance(search, X_test, y_test, n_repeats=10, random_state=0)
for name, mean, sd in zip(predictors, importance.importances_mean, importance.importances_std):
    print(f"{name}: accuracy drop {mean:+.4f}  (sd {sd:.4f})")


# =============================================================================
# Step 6 · Score the model on the test year — once
# =============================================================================
# search.predict uses the best K, refitted on all of 2001-2004.
y_pred = search.predict(X_test)

# Prediction next to the truth, first five days of 2005
print(test.assign(predicted=y_pred)[["Year", "Lag1", "Lag2", "Direction", "predicted"]].head())

# Confusion matrix: rows = what really happened, columns = what we predicted
labels = ["Down", "Up"]
table = pd.DataFrame(confusion_matrix(y_test, y_pred, labels=labels),
                     index=["actual Down", "actual Up"],
                     columns=["predicted Down", "predicted Up"])
print(table)
print(classification_report(y_test, y_pred))

accuracy = (y_pred == y_test).mean()
baseline = y_test.value_counts(normalize=True).max()
print(f"KNN test accuracy:                   {accuracy:.3f}")
print(f"always predicting the commonest day: {baseline:.3f}")


# =============================================================================
# Step 7 · Predict one day of your own
# =============================================================================
# Change these two numbers: yesterday's return and the day before's, in %.
my_day = pd.DataFrame({"Lag1": [1.5], "Lag2": [-0.8]})
print("prediction:", search.predict(my_day)[0])
for label, prob in zip(search.classes_, search.predict_proba(my_day)[0]):
    print(f"Pr({label}) = {prob:.3f}")


# =============================================================================
# Step 8 · Beyond one classifier
# =============================================================================
# 8a · Classification on data with a real signal: iris (ships with scikit-learn)
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
iris_search = GridSearchCV(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                           {"kneighborsclassifier__n_neighbors": range(1, 16)}, cv=10)
iris_search.fit(iris.data, iris.target)
print(f"iris: best K = {iris_search.best_params_['kneighborsclassifier__n_neighbors']}, "
      f"CV accuracy = {iris_search.best_score_:.3f}")

# 8b · KNN for a number, not a class: house prices, against a linear regression
from sklearn.linear_model import LinearRegression

HOUSES = "https://www.warin.ca/datalake/courses_data/qmibr/session5/Real_Estate_Sample.csv"
houses = pd.read_csv(HOUSES, index_col=0).dropna()
X_h = houses[["Living.area", "bedrooms", "bathrooms", "year", "garage"]]
y_h = houses["Price"]

models = {
    "KNN, K = 5": make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5)),
    "KNN, K = 25": make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=25)),
    "linear regression": LinearRegression(),
}
for name, model in models.items():
    # cross_val_score returns NEGATIVE errors (scikit-learn always maximises),
    # so the minus sign turns them back into an ordinary RMSE.
    rmse = -cross_val_score(model, X_h, y_h, cv=5, scoring="neg_root_mean_squared_error").mean()
    print(f"{name:18}  RMSE = {rmse:10,.0f}")
print(f"price standard deviation = {y_h.std():,.0f}   <- what predicting the average would cost")

# 8c · A random forest on the stock market, for comparison with KNN
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=0)
forest_accuracy = cross_val_score(forest, X_train, y_train, cv=5).mean()
print(f"random forest CV accuracy = {forest_accuracy:.3f}")
print(f"KNN CV accuracy           = {search.best_score_:.3f}")
print(f"commonest class           = {majority:.3f}")
