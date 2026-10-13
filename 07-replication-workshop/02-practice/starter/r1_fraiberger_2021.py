"""
Paper 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)
*Media sentiment and international asset prices* — the data, with the course's code

Step-by-step guide: 07-replication-workshop/02-practice/replications/R1-fraiberger-2021.md

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-replication-workshop/02-practice/starter/r1_fraiberger_2021.py

Work one step at a time: select a step's lines and press Shift+Enter to run only
those, read the output, and compare it with "You should see" in the guide.
"""

from pathlib import Path
import os
import sys

# Work from the repository root — the folder that holds qmib.py — wherever this
# file is saved and however it is run (Run button, terminal, or Shift+Enter).
starts = [Path.cwd()] + ([Path(__file__).resolve().parent] if "__file__" in globals() else [])
ROOT = next((p for s in starts for p in [s, *s.parents] if (p / "qmib.py").exists()), None)
if ROOT is None:
    sys.exit("Open the quantitative-methods folder in VS Codium (File > Open Folder) and run again.")
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
OUTPUT = Path("07-replication-workshop/02-practice/output")   # figures land here
OUTPUT.mkdir(parents=True, exist_ok=True)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Step 1 · Load the data: one row is a country-day
path = "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
d = pd.read_stata(path, columns=["iso", "DATE", "F0_index", "L1_sent1_best", "L1_vix"])
d = d.dropna(subset=["F0_index", "L1_sent1_best", "L1_vix"])
d["up"] = (d["F0_index"] > 0).astype(int)            # 1 if the market rose that day
print(f"{len(d):,} country-days, {d['iso'].nunique()} countries, share of up days {d['up'].mean():.3f}")

# Step 2 · Three lines of Python (session 03): today's return on yesterday's news
# The formula reads "F0_index explained by L1_sent1_best". statsmodels
# adds the intercept for you; write ~ 0 + x if you ever want it suppressed,
# and know that R-squared stops being interpretable when you do.
model = smf.ols("F0_index ~ L1_sent1_best", data=d).fit()

# .params holds the two coefficients. The slope is in percentage points of
# return per one standard deviation of sentiment — always say the units.
print(model.params)

# Step 3 · How much did the line explain? (session 03)
# R-squared is the share of variance the line accounts for — and nothing about
# whether the line is the right shape. The rest of this hour is that difference.
print(f"R-squared = {model.rsquared:.3f}")

# Step 4 · Two predictors: what "controlling for" means (session 03)
# Adding a second predictor changes what the first coefficient means: it is now
# the association holding global risk (yesterday's VIX) fixed, not the raw
# association. The two answer different questions, and the number will move.
model2 = smf.ols("F0_index ~ L1_sent1_best + L1_vix", data=d).fit()
print(model2.params)

# Step 5 · The residual plot is the instrument (session 03)
# Residuals vs Fitted: is there structure the straight line missed?
plt.scatter(model2.fittedvalues, model2.resid, s=12, alpha=0.6)
plt.axhline(0, color="black", lw=1)
plt.xlabel("Fitted values"); plt.ylabel("Residuals")
plt.show()

# Step 6 · Log-odds (session 04): does the market go up today?
# Fit the logistic regression. The coefficients come out as log-odds.
m2 = smf.logit("up ~ L1_sent1_best", data=d).fit(disp=0)
print(m2.params.round(4))

# Step 7 · Odds (session 04)
# Log-odds -> odds ratio: take the exponential of each coefficient
print(np.exp(m2.params["L1_sent1_best"]).round(4))

# Step 8 · Predicted probability (session 04)
# predict() does the same calculation for you: a bad, an ordinary and a good news day
print(m2.predict(pd.DataFrame({"L1_sent1_best": [-1, 0, 1]})).round(3))
