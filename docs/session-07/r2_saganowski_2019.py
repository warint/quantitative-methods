"""
Paper 2 · Session 04 · Saganowski, Bródka, Koziarski & Kazienko (2019)
*Analysis of group evolution prediction in complex networks*

Step-by-step guide: https://github.com/warint/quantitative-methods/blob/main/07-replication-workshop/02-practice/replications/R2-saganowski-2019.md

The session-04 code, line for line, on this paper's data: a binary, an ordinal
and a multinomial logit. Only the data and the variable names change.

Run it in your own session-07 folder, opened in VS Codium (File > Open Folder),
with its environment active and pandas, statsmodels, scikit-learn and
matplotlib installed (the guide's Part 0). Then press the Run button (the
triangle, top right), or type in the terminal:

    python r2_saganowski_2019.py

The data comes from the course site, so you need the internet, and nothing else.

Work one step at a time: select a step's lines and press Shift+Enter to run only
those, read the output, and compare it with "You should see" in the guide.
"""

import warnings
warnings.filterwarnings("ignore")            # convergence notes are not part of the answer

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel

pd.set_option("display.width", 130)       # as in the session-04 slides, a little wider
pd.set_option("display.max_columns", 10)

# The data: one CSV per paper on the course site, read over the internet
DATA = "https://warint.github.io/quantitative-methods/data/session-07/"


# Step 1 · Load the groups, and what happened to each one next week
FILE = DATA + "paper2_saganowski_2019.csv"     # the authors' file, unchanged
raw = pd.read_csv(FILE)
print(raw.shape)
print(raw["event_type"].value_counts(normalize=True).round(3))   # the base rates

# Step 2 · Three features a person can read
groups = pd.DataFrame({
    "event": raw["event_type"],
    "log2_size": np.log2(raw["g1_size"]),            # +1 = the group is twice as big
    "avg_degree": raw["g1_avg_group_degree_total"],  # ties per member, inside the group
    "aging": raw["g1_IlhanAging"]})                  # how long its members have been around
print(groups[["log2_size", "avg_degree", "aging"]].median().round(2))

# Step 3 · Binary logit: log-odds (session 04, LR 6)
groups["dissolve"] = (groups["event"] == "dissolving").astype(int)
# Fit the logistic regression. The coefficients come out as log-odds.
m2 = smf.logit("dissolve ~ log2_size", data=groups).fit(disp=0)
print(m2.params.round(4))

# Step 4 · Binary logit: odds (session 04, LR 7)
# Log-odds -> odds ratio: take the exponential of each coefficient
print(np.exp(m2.params["log2_size"]).round(4))

# Step 5 · Binary logit: predicted probability (session 04, LR 8)
# predict() does the same calculation for you: groups of 4, 8 and 16 members
print(m2.predict(pd.DataFrame({"log2_size": [2, 3, 4]})).round(3))

# Step 6 · Ordinal logit: the code (session 04, OLR 3)
# Keep the order: shrinking < continuing < growing
order = ["shrinking", "continuing", "growing"]
dat = groups[groups["event"].isin(order)].copy()
dat["event_c"] = pd.Categorical(dat["event"], categories=order, ordered=True)
om = OrderedModel(dat["event_c"], dat[["log2_size", "avg_degree", "aging"]], distr="logit").fit(method="bfgs", disp=0)
print(om.summary())

# Step 7 · Ordinal logit: log-odds -> odds (session 04, OLR 4)
# Log-odds: the slopes as fitted (the cutpoints are left out)
print(om.params[["log2_size", "avg_degree", "aging"]].round(3))
# Proportional-odds ratios
print(np.exp(om.params[["log2_size", "avg_degree", "aging"]]).round(3))

# Step 8 · Ordinal logit: probabilities (session 04, OLR 5)
# A 4-member group, and an otherwise identical 16-member one.
# Columns: shrinking, continuing, growing.
new = pd.DataFrame({"log2_size": [2, 4], "avg_degree": [2.7, 2.7], "aging": [8.5, 8.5]})
print(pd.DataFrame(np.asarray(om.predict(new)), columns=order, index=["4 members", "16 members"]).round(3))

# Step 9 · Multinomial logit: the code (session 04, MLR 3)
# Code 0 (dissolving) is the baseline: every coefficient reads "relative to dissolving"
levels = ["dissolving", "shrinking", "growing", "continuing"]
ml = groups[groups["event"].isin(levels)].copy()
ml["event_c"] = pd.Categorical(ml["event"], categories=levels).codes
X = ml[["log2_size", "avg_degree", "aging"]].astype(float)
X = sm.add_constant(X)
# Three sets of coefficients at once, each against the dissolving baseline
mn = sm.MNLogit(ml["event_c"], X).fit(disp=0)
print(mn.summary().tables[1])          # the coefficient table

# Step 10 · Multinomial logit: log-odds -> relative risk ratios (session 04, MLR 4)
# Log-odds and RRR, for shrinking, growing and continuing vs dissolving
print(pd.concat({"log-odds": mn.params, "RRR": np.exp(mn.params)}, axis=1)
      .set_axis(["log-odds: shrinking", "log-odds: growing", "log-odds: continuing",
                 "RRR: shrinking", "RRR: growing", "RRR: continuing"], axis=1).round(3))

# Step 11 · Multinomial logit: probabilities (session 04, MLR 5)
# Typical groups (median degree and aging), from 4 to 32 members
grid = pd.DataFrame({"const": 1.0, "log2_size": [2, 3, 4, 5],
                     "avg_degree": 2.7, "aging": 8.5})
out = pd.DataFrame(mn.predict(grid).values, columns=levels, index=grid["log2_size"])
print(out.round(3))
