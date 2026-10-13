"""
Paper 3 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)
*Analysis of group evolution prediction in complex networks*

Step-by-step guide: 07-replication-workshop/02-practice/replications/R3-saganowski-2019.md

The session-04 code on the paper's data: a binary, an ordinal and a multinomial
logit, each on three readable features. Not the paper's 15 classifiers — the
three models you typed in class.

Run it in VS Codium with the Run button (the triangle, top right), or from the
repository root in the terminal:

    python 07-replication-workshop/02-practice/starter/r3_saganowski_2019.py

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
warnings.filterwarnings("ignore")            # convergence notes are not part of the answer

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel

FOLDER = "04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/"
FILE = FOLDER + "12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.{}.csv"

# Step 1 · Load the two halves: fit on one, test on the other
train, test = pd.read_csv(FILE.format(1)), pd.read_csv(FILE.format(2))
print("train", train.shape, "| test", test.shape)
print(train["event_type"].value_counts(normalize=True).round(3))   # the base rates

# Step 2 · Three features a person can read
def features(df):
    return pd.DataFrame({
        "event": df["event_type"],
        "log2_size": np.log2(df["g1_size"]),            # +1 = the group is twice as big
        "avg_degree": df["g1_avg_group_degree_total"],  # ties per member, inside the group
        "aging": df["g1_IlhanAging"]})                  # how long its members have been around
tr, te = features(train), features(test)
X = ["log2_size", "avg_degree", "aging"]
print(tr.groupby("event")[X].median().round(2))

# Step 3 · Binary logit: does the group dissolve next week?
tr["dissolve"] = (tr["event"] == "dissolving").astype(int)
bi = smf.logit("dissolve ~ log2_size + avg_degree + aging", data=tr).fit(disp=0)
print(pd.DataFrame({"log-odds": bi.params, "odds ratio": np.exp(bi.params),
                    "p-value": bi.pvalues}).round(3))

# Step 4 · From odds to probabilities: a 4-member and a 16-member group
typical = tr[X].median()
cases = pd.DataFrame([typical, typical], index=["4 members", "16 members"])
cases["log2_size"] = [2, 4]                         # 2**2 = 4, 2**4 = 16
print("P(dissolve):", bi.predict(cases).round(3).to_dict())

# Step 5 · Ordinal logit: shrinks < continues < grows
levels = ["shrinking", "continuing", "growing"]
sub = tr[tr["event"].isin(levels)].copy()
sub["size_change"] = pd.Categorical(sub["event"], categories=levels, ordered=True)
om = OrderedModel(sub["size_change"], sub[X], distr="logit").fit(method="bfgs", disp=0)
print(pd.DataFrame({"log-odds": om.params[X], "odds ratio": np.exp(om.params[X]),
                    "p-value": om.pvalues[X]}).round(3))
print("P(shrink, continue, grow):")
print(pd.DataFrame(np.asarray(om.predict(cases[X])), index=cases.index, columns=levels).round(3))

# Step 6 · Multinomial logit: four events, baseline = dissolving
four = ["dissolving", "shrinking", "growing", "continuing"]   # merging and splitting: 17 groups
m4 = tr[tr["event"].isin(four)]
mn = sm.MNLogit(pd.Categorical(m4["event"], categories=four).codes,
                sm.add_constant(m4[X])).fit(disp=0, maxiter=200)
rrr = np.exp(mn.params)
rrr.columns = four[1:]                              # each column: that event against dissolving
print("relative risk ratios, against dissolving:")
print(rrr.round(3))

# Step 7 · Predicted probabilities across group size, other features at the median
grid = pd.DataFrame({"log2_size": np.linspace(1.6, 6, 40), "avg_degree": typical["avg_degree"],
                     "aging": typical["aging"]})
probs = pd.DataFrame(np.asarray(mn.predict(sm.add_constant(grid, has_constant="add"))), columns=four)
for e in four:
    plt.plot(2 ** grid["log2_size"], probs[e], label=e)
plt.xscale("log"); plt.xlabel("group size (members)"); plt.ylabel("predicted probability")
plt.legend(); plt.savefig(OUTPUT / "s04_event_probabilities.png", dpi=150, bbox_inches="tight"); plt.show()

# Step 8 · Out of sample: accuracy on the test half against the base rate
t4 = te[te["event"].isin(four)]
guess = np.asarray(mn.predict(sm.add_constant(t4[X]))).argmax(axis=1)
truth = pd.Categorical(t4["event"], categories=four).codes
print(f"multinomial accuracy {(guess == truth).mean():.3f} | always 'dissolving' "
      f"{(t4['event'] == 'dissolving').mean():.3f}")
print(pd.crosstab(pd.Series(np.array(four)[truth], name="true"),
                  pd.Series(np.array(four)[guess], name="predicted")))
