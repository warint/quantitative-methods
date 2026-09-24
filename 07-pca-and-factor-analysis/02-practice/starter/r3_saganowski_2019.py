"""
Replication 3 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)
*Analysis of group evolution prediction in complex networks*

Step-by-step guide: 07-pca-and-factor-analysis/02-practice/replications/R3-saganowski-2019.md

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-pca-and-factor-analysis/02-practice/starter/r3_saganowski_2019.py

Work one step at a time: select a step's lines and press Shift+Enter to run only
those, read the output, and compare it with "You should see" in the guide.
"""

from pathlib import Path
import os
import sys

# Work from the repository root whichever way the script was started, so the
# data paths below and `import qmib` both resolve.
try:
    ROOT = Path(__file__).resolve().parents[3]
except NameError:            # lines sent one by one with Shift+Enter: the
    ROOT = Path.cwd()        # terminal already starts in the repository root
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
OUTPUT = Path("07-pca-and-factor-analysis/02-practice/output")   # figures land here
OUTPUT.mkdir(exist_ok=True)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

FOLDER = "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/"
FILE = FOLDER + "12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.{}.csv"

# Step 1 · Load the two halves of partition 1: fold 1 to fit, fold 2 to test
train = pd.read_csv(FILE.format(1))
test = pd.read_csv(FILE.format(2))
print("train", train.shape, "| test", test.shape)
print(pd.concat([train["event_type"].value_counts(), test["event_type"].value_counts()],
                axis=1, keys=["train", "test"]))

# Step 2 · Five features in units a person can read, and a 0/1 outcome
def features(df):
    return pd.DataFrame({
        "dissolve": (df["event_type"] == "dissolving").astype(int),
        "event": df["event_type"],
        "log2_size": np.log2(df["g1_size"]),              # +1 = the group is twice as big
        "avg_degree": df["g1_avg_group_degree_total"],    # ties per member, inside the group
        "aging": df["g1_IlhanAging"],                     # how long members have been around (windows)
        "net_density": df["g1_network_density"] * 1000,   # whole-network density, per thousand
        "net_leadership": df["g1_network_leadership"] * 100})  # network centralisation, in points
tr, te = features(train), features(test)
print(tr.groupby("event")[["log2_size", "avg_degree", "aging", "net_density", "net_leadership"]].median().round(2))

# Step 3 · Binary logit: does the group dissolve in the next week?
full = smf.logit("dissolve ~ log2_size + avg_degree + aging + net_density + net_leadership", data=tr).fit(disp=0)
print(full.summary().tables[1])
print("odds ratios:")
print(np.exp(full.params).round(3))

# Step 4 · Predicted probabilities for a 4-member and a 16-member group, other features at the median
typical = tr.drop(columns=["dissolve", "event"]).median()
cases = pd.DataFrame([typical, typical])
cases["log2_size"] = [2, 4]                            # 2**2 = 4 members, 2**4 = 16 members
pred = full.get_prediction(cases).summary_frame()
pred.index = ["4 members", "16 members"]
print(pred.round(3))

# Step 5 · Likelihood-ratio test: do the paper's three top-ranked features (Table F) add anything?
small = smf.logit("dissolve ~ log2_size + avg_degree", data=tr).fit(disp=0)
lr = 2 * (full.llf - small.llf)
print(f"LR = {lr:.2f}, df = 3, p = {stats.chi2.sf(lr, df=3):.4f}")
print(f"McFadden pseudo-R2: small {small.prsquared:.4f}   full {full.prsquared:.4f}")

# Step 6 · Out of sample: accuracy on fold 2 against the base rate
p_test = full.predict(te)
acc = ((p_test > 0.5).astype(int) == te["dissolve"]).mean()
base = 1 - te["dissolve"].mean()                       # always say "does not dissolve"
print(f"logit accuracy {acc:.3f} | base rate {base:.3f} | groups flagged as dissolving: {(p_test > 0.5).sum()} of {len(te)}")

# Step 7 · Multinomial logit over all six events, baseline = dissolving
order = ["dissolving", "shrinking", "growing", "continuing", "merging", "splitting"]
X_cols = ["log2_size", "avg_degree", "aging", "net_density", "net_leadership"]
y_tr = pd.Categorical(tr["event"], categories=order).codes
mn = sm.MNLogit(y_tr, sm.add_constant(tr[X_cols])).fit(disp=0, maxiter=200)
print("converged:", mn.mle_retvals["converged"], "| McFadden pseudo-R2:", round(mn.prsquared, 4))
odds = np.exp(mn.params)
odds.columns = order[1:]
print("odds ratios, each event versus dissolving:")
print(odds.round(3))

# Step 8 · LR test for the same three features, now in the multinomial (3 features x 5 equations)
mn_small = sm.MNLogit(y_tr, sm.add_constant(tr[["log2_size", "avg_degree"]])).fit(disp=0, maxiter=200)
lr_mn = 2 * (mn.llf - mn_small.llf)
print(f"LR = {lr_mn:.2f}, df = 15, p = {stats.chi2.sf(lr_mn, df=15):.4f}")
print(f"McFadden pseudo-R2: small {mn_small.prsquared:.4f}   full {mn.prsquared:.4f}")

# Step 9 · Out of sample: accuracy and the paper's measure, the plain average F-measure
probs = np.asarray(mn.predict(sm.add_constant(te[X_cols])))
guess = pd.Categorical.from_codes(probs.argmax(axis=1), categories=order)
truth = pd.Categorical(te["event"], categories=order)
print(pd.crosstab(pd.Series(truth, name="true"), pd.Series(guess, name="predicted"), dropna=False))
f = {}
for k in order:
    tp = ((guess == k) & (truth == k)).sum()
    prec = tp / (guess == k).sum() if (guess == k).sum() > 0 else 0
    rec = tp / (truth == k).sum()
    f[k] = float(2 * prec * rec / (prec + rec)) if prec + rec > 0 else 0.0
print("F-measure by event:", {k: round(v, 3) for k, v in f.items()})
print(f"accuracy {(guess == truth).mean():.3f} | base rate {(truth == 'dissolving').mean():.3f} | average F {np.mean(list(f.values())):.3f}")

# Step 10 · Picture: predicted probability of each event as the group grows
grid = pd.DataFrame([typical] * 50)
grid["log2_size"] = np.linspace(np.log2(3), np.log2(64), 50)
curves = np.asarray(mn.predict(sm.add_constant(grid[X_cols], has_constant="add")))
fig, ax = plt.subplots(figsize=(7, 4))
for j, name in enumerate(order):
    ax.plot(2 ** grid["log2_size"], curves[:, j], label=name)
ax.set_xscale("log", base=2)
ax.set_xlabel("group size (members, log scale)")
ax.set_ylabel("predicted probability")
ax.set_title("IrvineMessages, weekly windows: what happens next, by group size")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUTPUT / "s04_event_probabilities.png", dpi=150)
print("saved", OUTPUT / "s04_event_probabilities.png")
