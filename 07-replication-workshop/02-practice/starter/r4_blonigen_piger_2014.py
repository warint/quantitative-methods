"""
Paper 3 · Session 05 · Blonigen & Piger (2014)
*Determinants of foreign direct investment*

Step-by-step guide: 07-replication-workshop/02-practice/replications/R4-blonigen-piger-2014.md

The data of the paper, the code of sessions 3 and 5: OLS, then ridge, the lasso
and the elastic net, line for line as in class, with this data's variable names.

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-replication-workshop/02-practice/starter/r4_blonigen_piger_2014.py

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

import warnings
warnings.filterwarnings("ignore")       # convergence notes are not part of the answer
import numpy as np
import pandas as pd
import qmib
import statsmodels.formula.api as smf
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Step 1 · Load the data: one row per country pair, log FDI, 56 candidates
fdi = qmib.load("fdi")
YCOL = "log_fdi"
XCOLS = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=XCOLS).copy()   # positive FDI, complete rows
d["log_fdi"] = np.log(d["fdi_stock_musd"])
for v in ["parent_gdp", "host_gdp", "distance"]:                # gravity variables in logs
    d[v] = np.log(d[v])
print(f"country pairs: {len(d)}   candidate predictors: {len(XCOLS)}")

# Step 2 · OLS: three lines of Python (session 3)
# The formula reads "log_fdi explained by host_gdp" (both in logs).
model = smf.ols("log_fdi ~ host_gdp", data=d).fit()

# .params holds the two coefficients. The slope is an elasticity: % more FDI
# per 1% more host GDP — always say the units.
print(model.params)

# Step 3 · How much did the line explain?
# R-squared is the share of variance the line accounts for — and nothing about
# whether the line is the right shape.
print(f"R-squared = {model.rsquared:.3f}")

# Step 4 · Two predictors: what "controlling for" means
# Adding distance changes what the host-GDP coefficient means: it is now the
# association holding distance fixed, not the raw association.
model2 = smf.ols("log_fdi ~ host_gdp + distance", data=d).fit()
print(model2.params)
print(f"R-squared = {model2.rsquared:.3f}")

# Step 5 · Ridge (session 5)
from sklearn.linear_model import RidgeCV

Xc, yc = d[XCOLS].astype(float), d[YCOL].astype(float)
ridge = make_pipeline(StandardScaler(),                        # same scale for all
                      RidgeCV(alphas=np.logspace(-3, 3, 60))   # try 60 values of λ
                      ).fit(Xc, yc)
print(f"λ = {ridge[-1].alpha_:.2f}")
print(f"ridge kept {np.sum(ridge[-1].coef_ != 0)} of {len(XCOLS)} — it never drops a predictor")

# Step 6 · Lasso
from sklearn.linear_model import LassoCV

lasso = make_pipeline(StandardScaler(),
                      LassoCV(cv=5, random_state=0, max_iter=50_000)   # λ by 5-fold CV
                      ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, lasso[-1].coef_) if b != 0]
print(f"λ = {lasso[-1].alpha_:.4f}")
print(f"lasso kept {len(kept)} of {len(XCOLS)}")

# Step 7 · Elastic net
from sklearn.linear_model import ElasticNetCV

enet = make_pipeline(StandardScaler(),
                     ElasticNetCV(l1_ratio=0.5,            # half lasso, half ridge
                                  cv=5, random_state=0, max_iter=50_000)
                     ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, enet[-1].coef_) if b != 0]
print(f"λ = {enet[-1].alpha_:.4f}")
print(f"elastic net kept {len(kept)} of {len(XCOLS)}")

# Step 8 · Which one predicts best? Fit on 70% of the pairs, score on 30%
Xtr, Xte, ytr, yte = train_test_split(d[XCOLS], d[YCOL], test_size=0.3, random_state=7)

def test_rmse(model):                  # fit on 70% of rows, score on the other 30%
    pipe = make_pipeline(StandardScaler(), model).fit(Xtr, ytr)   # standardise first
    kept = int(np.sum(np.abs(pipe[-1].coef_) > 1e-8))             # non-zero coefficients
    return kept, mean_squared_error(yte, pipe.predict(Xte)) ** 0.5

results = {
    "OLS, all predictors": test_rmse(LinearRegression()),
    "ridge":       test_rmse(RidgeCV(alphas=np.logspace(-3, 3, 60))),   # λ by CV
    "lasso":       test_rmse(LassoCV(cv=5, random_state=0, max_iter=50_000)),
    "elastic net": test_rmse(ElasticNetCV(l1_ratio=0.5, cv=5, random_state=0, max_iter=50_000)),
}
res = pd.DataFrame(results, index=["predictors kept", "test RMSE"]).T.astype({"predictors kept": int})
print(res.round(3))
