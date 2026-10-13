"""
Paper 1 · Session 02 · Fraiberger, Lee, Puy & Ranciere (2021)
*Media sentiment and international asset prices*

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
from scipy import stats
import statsmodels.formula.api as smf

# Step 1 · Load the few columns the simple models need
path = "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
cols = ["iso", "DATE", "F0_index", "sent1_best", "L1_sent1_best", "L1_returns", "L1_vix"]
d = pd.read_stata(path, columns=cols)
print("rows:", len(d), "| countries:", d["iso"].nunique(),
      "| dates:", d["DATE"].min().date(), "to", d["DATE"].max().date())

# Step 2 · One row is a country-day, weekends included: keep days with a return
d["weekend"] = d["DATE"].dt.dayofweek >= 5
print(pd.crosstab(d["weekend"], d["F0_index"].notna(), rownames=["weekend"], colnames=["has return"]))
m = d.dropna(subset=["F0_index", "L1_sent1_best", "L1_returns", "L1_vix"]).copy()
m["up"] = (m["F0_index"] > 0).astype(int)            # 1 on a day the market rose
print("rows for the models:", len(m))

# Step 3 · Describe the outcome and the predictor before modelling (session 02)
r = m["F0_index"]
print(f"return  : mean {r.mean():.3f}  median {r.median():.3f}  sd {r.std():.2f}  "
      f"skew {stats.skew(r):.2f}  excess kurtosis {stats.kurtosis(r):.0f}")
s = m["L1_sent1_best"]
print(f"sentiment (yesterday): mean {s.mean():.2f}  sd {s.std():.2f}  median {s.median():.2f}")
print(f"share of up days: {m['up'].mean():.3f}")

# Step 4 · OLS: today's return on yesterday's sentiment (session 03)
ols1 = smf.ols("F0_index ~ L1_sent1_best", data=m).fit()
print(ols1.params.round(4))
print(f"p-value on sentiment: {ols1.pvalues['L1_sent1_best']:.1e}   R2 = {ols1.rsquared:.4f}")

# Step 5 · OLS with two controls: yesterday's return and yesterday's VIX
ols2 = smf.ols("F0_index ~ L1_sent1_best + L1_returns + L1_vix", data=m).fit()
print(ols2.params.round(4))
print(f"p-value on sentiment: {ols2.pvalues['L1_sent1_best']:.1e}   R2 = {ols2.rsquared:.4f}")

# Step 6 · Binary logit: does the market go up today? (session 04)
logit = smf.logit("up ~ L1_sent1_best + L1_returns + L1_vix", data=m).fit(disp=0)
print(pd.DataFrame({"log-odds": logit.params, "odds ratio": np.exp(logit.params)}).round(4))
print(f"p-value on sentiment: {logit.pvalues['L1_sent1_best']:.1e}")

# Step 7 · Predicted probability of an up day, at three levels of yesterday's sentiment
grid = pd.DataFrame({"L1_sent1_best": [-1.0, 0.0, 1.0],
                     "L1_returns": m["L1_returns"].mean(), "L1_vix": m["L1_vix"].mean()})
grid["P(up day)"] = logit.predict(grid)
print(grid[["L1_sent1_best", "P(up day)"]].round(4).to_string(index=False))

# Step 8 · Our simple slopes next to the paper's, in words not in a match
print(pd.Series({"Step 4 · sentiment only": ols1.params["L1_sent1_best"],
                 "Step 5 · + yesterday's return and VIX": ols2.params["L1_sent1_best"],
                 "Paper · 8 lags of everything, country effects, extreme days": 0.049}).round(3))
