"""
Replication 4 · Session 05 · Blonigen & Piger (2014)
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import qmib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Step 1 · Load the data and keep the log-levels sample
fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d = fdi[fdi.fdi_stock_musd > 0].dropna(subset=cov)   # log drops zeros; listwise deletion on the 56
print("all pairs:", len(fdi), "| positive FDI:", (fdi.fdi_stock_musd > 0).sum(), "| complete sample:", len(d))
print("candidates:", len(cov), "| parents:", d.parent.nunique(), "| hosts:", d.host.nunique())

# Step 2 · Outcome and design: log FDI, and the gravity trio in logs as in the paper
y = np.log(d.fdi_stock_musd)
X = d[cov].copy()
for v in ["parent_gdp", "host_gdp", "distance"]:
    X[v] = np.log(X[v])
print("log FDI: mean", round(y.mean(), 2), "sd", round(y.std(), 2))
print("constant columns:", [c for c in cov if X[c].nunique() == 1])

# Step 3 · The paper's retained determinants (pre-session deck, table 3, inclusion prob. >= 85%)
paper = ["parent_gdp", "host_gdp", "distance",                  # gravity
         "common_language_official", "colonial_link",           # cultural distance
         "regional_trade_agreement", "customs_union",           # trade agreements
         "parent_gdp_pc", "host_skill"]                         # income and endowments
print("paper keeps (as named by the course):", len(paper))

# Step 4 · Hold out 30% of the pairs; nothing below touches the test set until scoring
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
print("train:", len(Xtr), "| test:", len(Xte))

# Step 5 · OLS vs ridge vs lasso vs elastic net, all standardised INSIDE a pipeline
models = {
    "OLS":         make_pipeline(StandardScaler(), LinearRegression()),
    "ridge (CV)":  make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 60))),
    "lasso (CV)":  make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0, max_iter=50_000)),
    "elastic net": make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, 1],
                                                                cv=5, random_state=0, max_iter=50_000)),
}
print("predict the mean   test RMSE", round(np.sqrt(mean_squared_error(yte, np.full(len(yte), ytr.mean()))), 3))
for name, m in models.items():
    m.fit(Xtr, ytr)
    print(f"{name:18s} test RMSE", round(np.sqrt(mean_squared_error(yte, m.predict(Xte))), 3))

# Step 6 · The lambdas cross-validation chose, and the one-standard-error lambda
print("ridge alpha_:", round(models["ridge (CV)"][-1].alpha_, 3))
print("elastic net alpha_:", round(models["elastic net"][-1].alpha_, 4), "l1_ratio_:", models["elastic net"][-1].l1_ratio_)
lcv = models["lasso (CV)"][-1]
mse = lcv.mse_path_.mean(axis=1)                   # CV error at each lambda, averaged over 5 folds
se = lcv.mse_path_.std(axis=1) / np.sqrt(5)        # its standard error
lam_min = lcv.alpha_
lam_1se = lcv.alphas_[mse <= mse.min() + se[mse.argmin()]].max()   # largest lambda within 1 SE
print("lasso lambda_min:", round(lam_min, 4), "| lambda_1se:", round(lam_1se, 4))

# Step 7 · What the lasso keeps, at lambda_min and at lambda_1se
keep_min = [v for v, b in zip(cov, lcv.coef_) if b != 0]
las1 = make_pipeline(StandardScaler(), Lasso(alpha=lam_1se, max_iter=50_000)).fit(Xtr, ytr)
coef = pd.Series(las1[-1].coef_, index=cov)
keep_1se = list(coef[coef != 0].index)
print("kept at lambda_min:", len(keep_min), "of 56 | kept at lambda_1se:", len(keep_1se), "of 56")
print("lambda_1se test RMSE:", round(np.sqrt(mean_squared_error(yte, las1.predict(Xte))), 3))
print(coef[coef != 0].abs().sort_values(ascending=False).round(3).head(12))

# Step 8 · Compare with the paper: overlap, and what the lasso adds
overlap = [v for v in paper if v in keep_1se]
print("paper's survivors kept by lasso (1se):", len(overlap), "of", len(paper))
print("paper's survivors dropped:", [v for v in paper if v not in keep_1se])
print("kept by lasso but not on the paper's list:", len(keep_1se) - len(overlap))
print("signs on the paper's list:", coef[paper].round(3).to_dict())

# Step 9 · Stability: refit at lambda_1se on 20 random half-samples; how often does each survive?
rng = np.random.default_rng(60033)
hits = pd.Series(0.0, index=cov)
for b in range(20):
    k = rng.choice(len(Xtr), size=len(Xtr) // 2, replace=False)
    m = make_pipeline(StandardScaler(), Lasso(alpha=lam_1se, max_iter=50_000)).fit(Xtr.iloc[k], ytr.iloc[k])
    hits += (m[-1].coef_ != 0)
freq = (hits / 20).sort_values(ascending=False)
print("paper's list, share of resamples kept:", freq[paper].to_dict())
print("variables kept in >= 80% of resamples:", (freq >= 0.8).sum(), "| never kept:", (freq == 0).sum())
print("the >= 80% group:", list(freq[freq >= 0.8].index))
print("never kept:", list(freq[freq == 0].index))

# Step 10 · Picture the stability check: paper's survivors in a darker colour
top = freq[freq > 0]
colours = ["#1f4e79" if v in paper else "#9db4cc" for v in top.index]
fig, ax = plt.subplots(figsize=(7, 9))
ax.barh(top.index[::-1], top.values[::-1], color=colours[::-1])
ax.axvline(0.8, color="grey", ls=":", lw=1)
ax.set_xlabel("share of 20 half-samples in which the lasso keeps the variable")
ax.set_title("Lasso survival at lambda_1se\n(dark = the paper's survivors)")
plt.tight_layout()
plt.savefig(OUTPUT / "s05_stability.png", dpi=150)
print("saved", OUTPUT / "s05_stability.png")
