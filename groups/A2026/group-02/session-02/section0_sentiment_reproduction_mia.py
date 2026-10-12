# Part 1 : First look at the data

import pandas as pd

path = "02-exploratory-data-analysis/data/replication/public/data/news_sentiment.csv"
df = pd.read_csv(path)
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

cols = ["sentiment_country", "sentiment_local", "sentiment_global"]

print(df.shape)
print(df["country"].nunique(), "pays")
print(df["date"].min(), "->", df["date"].max())
print(df[cols].describe())
print(df[cols].isna().sum())


# Part 2 : N per country, 1991-2015 (comparison with Table A4)

df15 = df[df["date"] <= "2015-12-31"]
n_par_pays = df15.groupby("country")["sentiment_country"].count()
print(n_par_pays)
print(n_par_pays.sum())

rows_all = df15.groupby("country").size()
rows_with_value = df15.groupby("country")["sentiment_country"].count()
print(rows_all.head())
print(rows_with_value.head())


# Part 3 : Shape of the distribution (skewness and kurtosis)

import numpy as np

def shape(x):
    x = pd.Series(x).dropna().to_numpy(float)
    n = len(x)
    xbar, s = x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / s ** 3
    g2 = ((x - xbar) ** 4).mean() / s ** 4 - 3
    return n, g1, g2, 2 * np.sqrt(6 / n), 4 * np.sqrt(6 / n)

n, g1, g2, t1, t2 = shape(df15["sentiment_country"])
print(f"n  = {n}")
print(f"g1 = {g1:+.3f}   threshold {t1:.3f}   substantially skewed: {abs(g1) > t1}")
print(f"g2 = {g2:+.3f}   threshold {t2:.3f}   substantially kurtic: {abs(g2) > t2}")


# Part 4 : The authors' own output, Figure 2a

REP = "02-exploratory-data-analysis/data/replication/public"
fig2a = pd.read_csv(f"{REP}/results/figure_2a.csv")
print(fig2a.shape)
print(fig2a.head())