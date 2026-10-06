"""Session 02 — where do the modes come from? Break the variables down by sector and year."""

import matplotlib.pyplot as plt
import pandas as pd

ANGLE = "data/spine/angle_a_sector.parquet"
VARS = ["elec_use_gwh", "gva_meur", "energy_cost_share"]
OUTDIR = "groups/A2026/group-02/session-02"

df = pd.read_parquet(ANGLE)

# 1. Median of each variable by sector (first-look question 1)
print("Median by sector")
print(df.groupby("nace_r2")[VARS].median().round(4))

# 2. Median energy cost share by year
print("\nMedian energy_cost_share by year")
print(df.groupby("time")["energy_cost_share"].median().round(4))

# 3. Who is in the top cluster?
high = df[df["energy_cost_share"] > 0.075]
print(f"\nObservations with energy_cost_share > 0.075: {len(high)}")
print(pd.crosstab(high["nace_r2"], high["time"]))

# 4. One histogram per sector, overlaid
for col in ["gva_meur", "energy_cost_share"]:
    fig, ax = plt.subplots(figsize=(10, 4))
    value_range = (df[col].min(), df[col].max())
    for sector, group in df.groupby("nace_r2"):
        ax.hist(group[col].dropna(), bins=50, range=value_range, alpha=0.5, label=sector)
    ax.set_title(f"{col} by sector")
    ax.set_xlabel(col)
    ax.set_ylabel("Number of observations")
    ax.legend(title="Sector")
    fig.tight_layout()
    fig.savefig(f"{OUTDIR}/{col}_by_sector.png", dpi=150)
    plt.close(fig)

# 5. Median of each variable by year
print("\nMedian by year")
print(df.groupby("time")[VARS].median().round(4))

# 6. Manufacturing (C): before vs after the 2022 energy shock
c = df[df["nace_r2"] == "C"]
fig, ax = plt.subplots(figsize=(10, 4))
value_range = (c["energy_cost_share"].min(), c["energy_cost_share"].max())
ax.hist(c.loc[c["time"] < 2022, "energy_cost_share"].dropna(),
        bins=30, range=value_range, alpha=0.6, label="2010–2021")
ax.hist(c.loc[c["time"] >= 2022, "energy_cost_share"].dropna(),
        bins=30, range=value_range, alpha=0.6, label="2022–2024")
ax.set_title("energy_cost_share, manufacturing (C): before vs after 2022")
ax.set_xlabel("energy_cost_share")
ax.set_ylabel("Number of observations")
ax.legend(title="Years")
fig.tight_layout()
fig.savefig(f"{OUTDIR}/energy_cost_share_C_by_period.png", dpi=150)
plt.close(fig)

# 7. Median gross value added by country
print("\nMedian gva_meur by country")
print(df.groupby("geo")["gva_meur"].median().sort_values().round(0))

# 8. Electricity per unit of GVA, by sector (first-look question 2)
df["elec_per_gva"] = df["elec_use_gwh"] / df["gva_meur"]
print("\nMedian electricity per million EUR of GVA (GWh per MEUR), by sector")
print(df.groupby("nace_r2")["elec_per_gva"].median().sort_values(ascending=False).round(3))

# 9. Did the 2022 shock hit all sectors equally? (first-look question 3)
df["period"] = (df["time"] >= 2022).map({False: "2010-2021", True: "2022-2024"})
shock = df.groupby(["nace_r2", "period"])["energy_cost_share"].median().unstack()
shock["ratio"] = shock["2022-2024"] / shock["2010-2021"]
print("\nMedian energy_cost_share before and after 2022, by sector")
print(shock.sort_values("ratio", ascending=False).round(4))
