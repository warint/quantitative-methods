"""
Paper 5 · Session 06 · Topalova & Khandelwal (2011)
*Trade liberalization and firm productivity: the case of India*

Step-by-step guide: 07-replication-workshop/02-practice/replications/R5-topalova-khandelwal-2011.md

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

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


# Step 1 · Load the firms, keep the paper's years, and see the reform
firms = pd.read_stata("06-advanced-regression/data/replication/prod_dataregression.dta")
cols = ["tfp1000", "lagtariff", "laginputariff", "prgroup", "govown",
        "foreign", "medium", "small", "age"]
d = firms[firms["yr"] < 1997].dropna(subset=cols)       # 1989-1996, no gaps
print(d.shape[0], "firm-years,", d["id"].nunique(), "firms")
by_year = d.groupby("yr")[["lagtariff", "laginputariff"]].mean()
print(by_year.round(2))                                  # 1 = a 100% tariff
by_year.plot(marker="o", ylabel="average lagged tariff (1 = 100%)")
plt.savefig(OUTPUT / "tariffs_by_year.png", dpi=150, bbox_inches="tight")
plt.show()

# Step 2 · The simplest regression: productivity on the output tariff
# tfp1000 is log productivity, so 100 x slope = % change per unit of tariff.
m1 = smf.ols("tfp1000 ~ lagtariff", data=d).fit()
b = m1.params["lagtariff"]
print(f"slope = {b:.4f}   p = {m1.pvalues['lagtariff']:.3f}   R2 = {m1.rsquared:.4f}")
print(f"a 10-point tariff cut goes with {-b * 0.10 * 100:.2f}% higher productivity")

# Step 3 · Add the input tariff: each slope now holds the other tariff fixed
m2 = smf.ols("tfp1000 ~ lagtariff + laginputariff", data=d).fit()
print(m2.params.round(4))
print(m2.pvalues.round(3))

# Step 4 · Add ownership, size, age and year dummies
# C(yr) gives each year its own intercept: what all firms shared in a year
# (the reform itself, the 1991 crisis) no longer counts as a tariff effect.
f4 = ("tfp1000 ~ lagtariff + laginputariff + prgroup + govown + foreign"
      " + medium + small + age + C(yr)")
m4 = smf.ols(f4, data=d).fit()
keys = ["lagtariff", "laginputariff"]
print(pd.DataFrame({"coef": m4.params[keys], "p": m4.pvalues[keys]}).round(3))

# Step 5 · Is the effect of age a curve? Add age squared
m5 = smf.ols(f4 + " + I(age**2)", data=d).fit()
a, a2 = m5.params["age"], m5.params["I(age ** 2)"]
for age in (5, 16, 40):                                  # inside the data: 0 to 171
    print(f"one more year at age {age:>2}: {100 * (a + 2 * a2 * age):+.2f}% productivity")
print(f"adjusted R2: {m4.rsquared_adj:.4f} without the square, {m5.rsquared_adj:.4f} with it")

# Step 6 · Side by side with the paper's own estimate
# The paper compares each firm with itself before and after its tariffs fell.
table = pd.DataFrame({
    "step 2": [m1.params["lagtariff"], None],
    "step 3": m2.params[keys].values,
    "step 5 (paper's col. 1)": m5.params[keys].values,
    "paper col. 3, same firm over time": [-0.032, -0.480]}, index=keys)
print(table.T.round(3).to_string())
