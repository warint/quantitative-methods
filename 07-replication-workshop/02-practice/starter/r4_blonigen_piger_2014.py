"""
Paper 4 · Session 05 · Blonigen & Piger (2014)
*Determinants of foreign direct investment*

Step-by-step guide: 07-replication-workshop/02-practice/replications/R4-blonigen-piger-2014.md

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
import matplotlib.pyplot as plt
import qmib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Step 1 · Load the data: log FDI, 56 candidates, complete cases only
fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=cov)        # log drops zeros; complete cases
y = np.log(d.fdi_stock_musd)                                # the outcome: log FDI stock
X = d[cov].copy()
for v in ["parent_gdp", "host_gdp", "distance"]:            # gravity variables in logs
    X[v] = np.log(X[v])
print("country pairs:", len(d), "| candidate predictors:", len(cov), "| rows per predictor:", round(len(d) / len(cov), 1))

# Step 2 · Hold out 30% of the pairs: the test set is touched only to score
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
rmse = lambda m: round(np.sqrt(mean_squared_error(yte, m.predict(Xte))), 3)
print("train:", len(Xtr), "| test:", len(Xte))

# Step 3 · Benchmark: OLS with all 56 candidates
ols = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
print("OLS: predictors kept 56 | test RMSE", rmse(ols))

# Step 4 · Ridge: shrink every coefficient, lambda (alpha) chosen by cross-validation
ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 60))).fit(Xtr, ytr)
print("ridge: lambda", round(ridge[-1].alpha_, 2), "| kept", int((ridge[-1].coef_ != 0).sum()),
      "| test RMSE", rmse(ridge))

# Step 5 · Lasso: shrink, and set the weak coefficients to exactly zero
lasso = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0, max_iter=50_000)).fit(Xtr, ytr)
kept_lasso = [v for v, b in zip(cov, lasso[-1].coef_) if b != 0]
print("lasso: lambda", round(lasso[-1].alpha_, 4), "| kept", len(kept_lasso), "of 56 | test RMSE", rmse(lasso))
print("dropped:", ", ".join(v for v in cov if v not in kept_lasso))

# Step 6 · Elastic net: half lasso, half ridge (l1_ratio = 0.5)
enet = make_pipeline(StandardScaler(),
                     ElasticNetCV(l1_ratio=0.5, cv=5, random_state=0, max_iter=50_000)).fit(Xtr, ytr)
kept_enet = [v for v, b in zip(cov, enet[-1].coef_) if b != 0]
print("elastic net: lambda", round(enet[-1].alpha_, 4), "| kept", len(kept_enet), "of 56 | test RMSE", rmse(enet))
print("dropped:", ", ".join(v for v in cov if v not in kept_enet))

# Step 7 · The four models side by side, and a picture of their test error
table = pd.DataFrame({"predictors kept": [56, 56, len(kept_lasso), len(kept_enet)],
                      "test RMSE": [rmse(ols), rmse(ridge), rmse(lasso), rmse(enet)]},
                     index=["OLS", "ridge", "lasso", "elastic net"])
print(table)
fig, ax = plt.subplots(figsize=(6, 2.4))
ax.barh(table.index[::-1], table["test RMSE"][::-1], color="#1f4e79")
ax.set_xlabel("test RMSE, log FDI (lower is better)")
plt.tight_layout(); plt.savefig(OUTPUT / "s05_test_rmse.png", dpi=150); plt.show()

# Step 8 · Compare with the paper's robust determinants (inclusion probability >= 85%)
paper = ["parent_gdp", "host_gdp", "distance", "common_language_official", "colonial_link",
         "regional_trade_agreement", "customs_union", "parent_gdp_pc", "host_skill"]
coef = pd.Series(lasso[-1].coef_, index=cov)
print("paper's nine kept by the lasso:", sum(v in kept_lasso for v in paper), "| by the elastic net:",
      sum(v in kept_enet for v in paper))
print(coef[paper].round(2).to_string())
print("largest lasso coefficients:", coef.abs().sort_values(ascending=False).head(6).index.tolist())
