r"""
Session 08 · File 2 of 2 — predict one new date with the model File 1 trained

THE IDEA
    File 1 did all the work: it chose K by cross-validation, judged the model
    on 2005, and saved it as knn_smarket.joblib. This file does what a model is
    for — it predicts ONE date the model has never seen. No data to download,
    no training: load the model, describe the new day, ask.

HOW TO RUN IT
    1. Run session08_1_train.py first, from the same folder. It creates
       knn_smarket.joblib next to it.
    2. Press the Run button (the triangle, top right), or type in the terminal:
           python session08_2_predict.py
    3. Then change the two numbers in Step 2 and run it again: that is your
       own "tomorrow".
"""

import pandas as pd
import joblib                      # installed together with scikit-learn


# =============================================================================
# Step 1 · Load the trained model
# =============================================================================
# The file holds the whole pipeline: the scaler (with the means and standard
# deviations it learned in File 1), the chosen K, and the 1,249 days KNN will
# look for neighbours among.
try:
    model = joblib.load("knn_smarket.joblib")
except FileNotFoundError:
    raise SystemExit("knn_smarket.joblib was not found. Run session08_1_train.py first, "
                     "from this same folder, then run this file again.")

k = model.named_steps["kneighborsclassifier"].n_neighbors
print(f"Loaded a KNN classifier with K = {k}.")


# =============================================================================
# Step 2 · The new date
# =============================================================================
# 30 December 2005, the last trading day in the data. File 1 kept it aside, so
# the model has never seen it. All we know that morning is the market's
# return on the two days before:
#   Lag1 = -0.298   on 29 December the market fell 0.298%
#   Lag2 =  0.130   on 28 December it rose 0.130%
# The column names must be the ones the model was trained with: Lag1, Lag2.
new_day = pd.DataFrame({"Lag1": [-0.298], "Lag2": [0.130]})


# =============================================================================
# Step 3 · Predict it
# =============================================================================
# KNN finds the K past days whose (Lag1, Lag2) are closest to the new day's,
# and lets them vote. The probabilities are the shares of the vote.
prediction = model.predict(new_day)[0]
probabilities = model.predict_proba(new_day)[0]

print(f"Prediction for 30 December 2005: {prediction}")
for label, prob in zip(model.classes_, probabilities):
    print(f"   Pr({label}) = {prob:.3f}   "
          f"-> about {round(prob * k)} of the {k} nearest past days went {label}")


# =============================================================================
# Step 4 · What actually happened
# =============================================================================
# On 30 December 2005 the S&P 500 fell 0.489%: the true answer is "Down".
actual = "Down"
print(f"What happened: {actual}.  The model was {'right' if prediction == actual else 'wrong'}.")
# One date proves nothing either way: File 1's test year is the honest score.
# A single prediction is how the model is USED, not how it is judged.

# Your turn: change the two numbers in Step 2 (in %, e.g. Lag1 = 1.5, Lag2 = -0.8)
# and run this file again. Does a big rise yesterday change the vote?
