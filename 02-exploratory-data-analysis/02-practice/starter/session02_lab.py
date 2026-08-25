"""Session 02 practice — profiling a variable you will have to defend.

Run from the repository root:

    python 02-exploratory-data-analysis/02-practice/starter/session02_lab.py

Replace ANGLE with your group's file (see your data dictionary) and VARS with the
three variables your research question depends on. Everything else is written for
you; the work is deciding what the numbers mean.
"""

import numpy as np
import pandas as pd
from scipy import stats

ANGLE = "data/spine/angle_c_country.parquet"      # <- your group's angle
VARS = ["gdp_pc_eur", "digital_intensity", "rd_pct_gdp"]   # <- your three variables


def centre(x):
    """Mean, 5% trimmed mean, median. When these disagree, the direction is the finding."""
    x = pd.Series(x).dropna()
    return {
        "n": len(x),
        "mean": x.mean(),
        "trim_5%": stats.trim_mean(x, 0.05),
        "median": x.median(),
    }


def spread(x):
    """Standard deviation and IQR — one sensitive to the tails, one blind to them."""
    x = pd.Series(x).dropna()
    return {
        "sd": x.std(ddof=1),
        "IQR": x.quantile(0.75) - x.quantile(0.25),
    }


def empirical_rule(x):
    """What fraction actually falls within 1, 2 and 3 sd? Compare with 68 / 95 / 99.7."""
    x = pd.Series(x).dropna()
    m, s = x.mean(), x.std(ddof=1)
    return {f"within_{k}sd": float(((x - m).abs() <= k * s).mean()) for k in (1, 2, 3)}


def shape(x):
    """Skewness and excess kurtosis, from the definitions in the lecture notes.

    Note the convention: g1 divides the third central moment by s**3 with s the
    *sample* standard deviation (n-1 in the denominator). scipy.stats.skew uses a
    slightly different normalisation, so the two differ in the third decimal. When
    you report a skewness, say which one you used.
    """
    x = pd.Series(x).dropna().to_numpy(float)
    n = len(x)
    xbar, s = x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / s ** 3
    g2 = ((x - xbar) ** 4).mean() / s ** 4 - 3
    return {
        "n": n,
        "g1": g1,
        "g1_threshold": 2 * np.sqrt(6 / n),
        "skewed": abs(g1) > 2 * np.sqrt(6 / n),
        "g2": g2,
        "g2_threshold": 4 * np.sqrt(6 / n),
        "kurtic": abs(g2) > 4 * np.sqrt(6 / n),
    }


def profile(df, col):
    print(f"\n{'=' * 62}\n{col}\n{'=' * 62}")
    c, s_, e, sh = centre(df[col]), spread(df[col]), empirical_rule(df[col]), shape(df[col])

    print(f"  n = {c['n']}")
    print(f"  centre   mean {c['mean']:>14,.2f}   trimmed {c['trim_5%']:>14,.2f}"
          f"   median {c['median']:>14,.2f}")
    gap = (c["mean"] - c["median"]) / s_["sd"]
    print(f"           mean - median = {c['mean'] - c['median']:,.2f}  ({gap:+.2f} sd)")
    print(f"  spread   sd {s_['sd']:>16,.2f}   IQR {s_['IQR']:>16,.2f}")
    print(f"  rule     within 1sd {e['within_1sd']:.1%} (68%) · 2sd {e['within_2sd']:.1%} (95%)"
          f" · 3sd {e['within_3sd']:.1%} (99.7%)")
    print(f"  shape    g1 = {sh['g1']:+.3f}  vs {sh['g1_threshold']:.3f}"
          f"   substantially skewed: {sh['skewed']}")
    print(f"           g2 = {sh['g2']:+.3f}  vs {sh['g2_threshold']:.3f}"
          f"   substantially kurtic: {sh['kurtic']}")


def main():
    core = pd.read_parquet("data/spine/core.parquet")
    mine = pd.read_parquet(ANGLE)
    df = core.merge(mine, on=["geo", "time"], how="inner")
    print(f"merged panel: {df.shape[0]} rows, {df.shape[1]} columns")

    for col in VARS:
        if col not in df.columns:
            print(f"\n  !! {col} is not in this angle — check your data dictionary")
            continue
        profile(df, col)

    print(f"\n{'=' * 62}")
    print("Now the part that carries the marks:")
    print("  1. Which summary would you put in a paper, and why that one?")
    print("  2. What does the shape cost you in Session 03?")
    print("  3. What would you check before trusting this profile?")
    # TODO: plot each variable — histogram and boxplot side by side — and check
    #       that the picture agrees with g1 and g2. Where it does not, there is
    #       usually a second mode, which neither number can see.


if __name__ == "__main__":
    main()
