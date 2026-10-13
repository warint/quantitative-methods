"""
Paper 4 · Session 06 · Topalova & Khandelwal (2011)
*Trade liberalization and firm productivity: the case of India*

Step-by-step guide: 07-replication-workshop/02-practice/replications/R5-topalova-khandelwal-2011.md

The authors' data, and the course's models: the OLS cells of session 3 and the
ridge, lasso and elastic-net cells of session 5, line for line — only the data
and the variable names change.

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-replication-workshop/02-practice/starter/r5_topalova_khandelwal_2011.py

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
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Step 1 · Load the firms: one row is one firm in one year, 1989-1996
firms = pd.read_stata("06-advanced-regression/data/replication/prod_dataregression.dta")
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age"]
d = firms[firms["yr"] < 1997].dropna(subset=cols)       # no gaps in what we use
print(f"{len(d):,} firm-years, {d['companyname'].nunique():,} firms")
print(d[["tfp1000", "lagtariff", "laginputariff"]].describe().round(3))

# Step 2 · Three lines of Python (session 3): productivity on the output tariff
# The formula reads "tfp1000 explained by lagtariff". statsmodels adds the
# intercept for you. The slope is in log points of productivity per one unit
# of tariff (1.0 = 100 percentage points) — always say the units.
model = smf.ols("tfp1000 ~ lagtariff", data=d).fit()
print(model.params)

# Step 3 · How much did the line explain? (session 3)
# R-squared is the share of variance the line accounts for — and nothing about
# whether the line is the right shape.
print(f"R-squared = {model.rsquared:.3f}")

# Step 4 · Two predictors: what "controlling for" means (session 3)
# Adding a second predictor changes what the first coefficient means: it is now
# the association holding the input tariff fixed, not the raw association.
model2 = smf.ols("tfp1000 ~ lagtariff + laginputariff", data=d).fit()
print(model2.params)
print(f"R-squared = {model2.rsquared:.3f}")

# Step 5 · Residuals vs fitted (session 3): structure the straight line missed?
fit = model2
plt.scatter(fit.fittedvalues, fit.resid, s=12, alpha=0.6)
plt.axhline(0, color="black", lw=1)
plt.xlabel("Fitted values"); plt.ylabel("Residuals")
plt.savefig(OUTPUT / "s06_resid_vs_fitted.png", dpi=110, bbox_inches="tight")
plt.show()

# Step 6 · The candidates for ridge, lasso and elastic net (session 5)
d = d.copy()
d["age2"] = d["age"] ** 2
years = pd.get_dummies(d["yr"], prefix="yr", drop_first=True).astype(float)   # 1989 is the base
d = pd.concat([d, years], axis=1)
YCOL = "tfp1000"
XCOLS = cols[1:] + ["age2"] + list(years.columns)
Xc, yc = d[XCOLS].astype(float), d[YCOL].astype(float)
print(f"{len(XCOLS)} candidates:", XCOLS)

# Step 7 · Ridge (session 5)
from sklearn.linear_model import RidgeCV

ridge = make_pipeline(StandardScaler(),                        # same scale for all
                      RidgeCV(alphas=np.logspace(-3, 3, 60))   # try 60 values of λ
                      ).fit(Xc, yc)
print(f"λ = {ridge[-1].alpha_:.2f}")
print(f"ridge kept {np.sum(ridge[-1].coef_ != 0)} of {len(XCOLS)} — it never drops a predictor")

# Step 8 · Lasso (session 5)
from sklearn.linear_model import LassoCV

lasso = make_pipeline(StandardScaler(),
                      LassoCV(cv=5, random_state=0, max_iter=50_000)   # λ by 5-fold CV
                      ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, lasso[-1].coef_) if b != 0]
print(f"λ = {lasso[-1].alpha_:.4f}")
print(f"lasso kept {len(kept)} of {len(XCOLS)}:", kept)

# Step 9 · Elastic net (session 5)
from sklearn.linear_model import ElasticNetCV

enet = make_pipeline(StandardScaler(),
                     ElasticNetCV(l1_ratio=0.5,            # half lasso, half ridge
                                  cv=5, random_state=0, max_iter=50_000)
                     ).fit(Xc, yc)
kept = [c for c, b in zip(XCOLS, enet[-1].coef_) if b != 0]
print(f"λ = {enet[-1].alpha_:.4f}")
print(f"elastic net kept {len(kept)} of {len(XCOLS)}:", kept)

# Step 10 · The four, on rows they never saw (session 5, as reviewed in session 6)
Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=7)

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
