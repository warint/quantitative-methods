"""
Replication 2 · Session 03 · Amsili, van Es & Schindelbeck (2024)
*Pedotransfer functions for field capacity, wilting point and available water*

Step-by-step guide: 07-pca-and-factor-analysis/02-practice/replications/R2-amsili-2024.md

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-pca-and-factor-analysis/02-practice/starter/r2_amsili_2024.py

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
OUTPUT = Path("07-pca-and-factor-analysis/02-practice/output")   # figures land here
OUTPUT.mkdir(parents=True, exist_ok=True)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

DATA = "03-regression-adequacy-and-validity/data/replication/2015-2019_CompleteAWC_w.1and15bar_dataset_toshare.xlsx"

# Step 1 · Load the data (the first sheet is metadata; the data are on the second)
sheets = pd.ExcelFile(DATA).sheet_names
print(sheets)
d = pd.read_excel(DATA, sheet_name=sheets[1])
print(d.shape)
print(d[["sand", "clay", "SOM", "FC_10kPa"]].describe().round(3))
print("missing values:", d.isna().sum().sum(), "| samples with SOM > 10%:", (d["SOM"] > 10).sum())

# Step 2 · Put the predictors on the paper's scale: g per g, not per cent
for c in ["sand", "clay", "SOM"]:
    d[c + "_g"] = d[c] / 100
print(d[["sand_g", "clay_g", "SOM_g", "FC_10kPa"]].head(3).round(3))

# Step 3 · Fit the paper's MLR: sand, clay, SOM and their three pairwise products
formula = "FC_10kPa ~ sand_g + clay_g + SOM_g + sand_g:clay_g + sand_g:SOM_g + clay_g:SOM_g"
fit = smf.ols(formula, data=d).fit()
paper = pd.Series({"Intercept": 0.3477, "sand_g": -0.313, "clay_g": 0.040, "SOM_g": 1.855,
                   "sand_g:clay_g": 0.222, "sand_g:SOM_g": 1.405, "clay_g:SOM_g": -0.202})
print(pd.DataFrame({"ours": fit.params.round(4), "paper Eq. 6": paper}))

# Step 4 · Fit statistics the paper reports: adjusted R-squared and RMSE
rmse = np.sqrt(np.mean(fit.resid ** 2))
print(f"adj. R2 = {fit.rsquared_adj:.3f}  (paper: 0.79)")
print(f"RMSE    = {rmse:.4f} g/g  (paper MLR: 0.043; paper Full RF: 0.036)")
print(f"n = {int(fit.nobs)}, parameters p = {int(fit.df_model) + 1}")

# Step 5 · Residuals versus fitted: is the line the right shape?
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(fit.fittedvalues, fit.resid, s=4, alpha=0.3)
ax.axhline(0, color="red", ls="--")
ax.set_xlabel("Fitted field capacity (g/g)"); ax.set_ylabel("Residual (g/g)")
plt.savefig(OUTPUT / "s03_resid_vs_fitted.png", dpi=110, bbox_inches="tight")
# Mean and spread of the residuals in five bands of fitted value (1 = lowest fifth)
band = np.digitize(fit.fittedvalues, fit.fittedvalues.quantile([0.2, 0.4, 0.6, 0.8])) + 1
print(fit.resid.groupby(band).agg(["mean", "std"]).round(4))

# Step 6 · Scale-location: is the spread constant, and do robust (HC1) errors change a verdict?
infl = fit.get_influence()
std_resid = infl.resid_studentized_internal
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(fit.fittedvalues, np.sqrt(np.abs(std_resid)), s=4, alpha=0.3)
ax.set_xlabel("Fitted field capacity (g/g)"); ax.set_ylabel("sqrt(|standardised residual|)")
plt.savefig(OUTPUT / "s03_scale_location.png", dpi=110, bbox_inches="tight")
print("corr(fitted, sqrt|std resid|) =", round(np.corrcoef(fit.fittedvalues, np.sqrt(np.abs(std_resid)))[0, 1], 3))
robust = smf.ols(formula, data=d).fit(cov_type="HC1")
print(pd.DataFrame({"coef": fit.params, "SE classical": fit.bse, "SE HC1": robust.bse,
                    "p classical": fit.pvalues, "p HC1": robust.pvalues}).round(4))

# Step 7 · Leverage: which soils sit far from the others in (sand, clay, SOM) space?
h = infl.hat_matrix_diag
p, n = int(fit.df_model) + 1, int(fit.nobs)
print(f"sum of h = {h.sum():.2f} (= p = {p}); 2p/n = {2*p/n:.5f}; above it: {(h > 2*p/n).sum()}")
print(d.loc[h > 2*p/n, "soil_texture_class"].value_counts().head(5))
print(d.iloc[np.argsort(h)[-3:]][["soil_texture_class", "sand", "clay", "SOM", "FC_10kPa"]].round(2))

# Step 8 · Cook's distance: which rows move the answer?
cooks_d = infl.cooks_distance[0]
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.stem(cooks_d, markerfmt=",")
ax.axhline(4 / n, color="red", ls="--")
ax.set_xlabel("Observation"); ax.set_ylabel("Cook's distance")
plt.savefig(OUTPUT / "s03_cooks_distance.png", dpi=110, bbox_inches="tight")
print(f"largest Cook's D {cooks_d.max():.4f}; above 4/n ({4/n:.5f}): {(cooks_d > 4/n).sum()} rows")

# Step 9 · Look at the tallest spike, then refit without it (a sensitivity check, not a deletion)
i = cooks_d.argmax()
print(d.iloc[i][["State", "soil_texture_class", "sand", "clay", "SOM", "FC_10kPa", "PWP_1500kPa"]])
print(f"fitted {fit.fittedvalues.iloc[i]:.3f}, residual {fit.resid.iloc[i]:.3f}, std. residual {std_resid[i]:.2f}, leverage {h[i]:.4f}")
fit_drop1 = smf.ols(formula, data=d[cooks_d < cooks_d[i]]).fit()
print(pd.DataFrame({"all rows": fit.params, "without that one row": fit_drop1.params}).round(3))
print(f"p-value of clay_g:SOM_g: {fit.pvalues['clay_g:SOM_g']:.3f} -> {fit_drop1.pvalues['clay_g:SOM_g']:.3f}")

# Step 10 · AIC and BIC: are the three interaction terms worth their rent? (same rows, same y)
main = smf.ols("FC_10kPa ~ sand_g + clay_g + SOM_g", data=d).fit()
ic = pd.DataFrame({"k": [int(m.df_model) + 1 for m in (main, fit)],
                   "adj R2": [m.rsquared_adj for m in (main, fit)],
                   "RMSE": [np.sqrt(np.mean(m.resid ** 2)) for m in (main, fit)],
                   "AIC": [m.aic for m in (main, fit)], "BIC": [m.bic for m in (main, fit)]},
                  index=["main effects", "+ interactions (Eq. 6)"])
ic["dAIC"], ic["dBIC"] = ic.AIC - ic.AIC.min(), ic.BIC - ic.BIC.min()
print(ic.round(4).to_string())
