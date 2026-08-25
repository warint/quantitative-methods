"""Session 02 demo — centre, spread and shape on the course data spine.

Self-contained. Run from the repository root:

    python 02-exploratory-data-analysis/demo/session02_eda_demo.py

Produces demo/outputs/shape_gallery.png: four real variables, one for each
combination of "substantially skewed" and "substantially kurtic", so you can see
that the two numbers are independent of each other.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "outputs"

INK, ACCENT, WARN, GOOD, MUTED = "#16181A", "#1C73C5", "#B4553A", "#2E7D5B", "#6E7275"


def shape(x):
    """Skewness and excess kurtosis with their significance thresholds."""
    x = np.asarray(pd.Series(x).dropna(), float)
    n = len(x)
    xbar, s = x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / s ** 3
    g2 = ((x - xbar) ** 4).mean() / s ** 4 - 3
    return x, n, g1, g2, 2 * np.sqrt(6 / n), 4 * np.sqrt(6 / n)


def main():
    core = pd.read_parquet(ROOT / "data/spine/core.parquet")
    ener = pd.read_parquet(ROOT / "data/spine/angle_a_country.parquet")
    d = core.merge(ener, on=["geo", "time"])

    variables = [
        ("gdp_pc_eur", "GDP per capita (EUR)"),
        ("population", "Population"),
        ("prod_growth", "Productivity growth (%)"),
        ("share_renew", "Renewable share"),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(13.5, 5.6),
                             gridspec_kw={"height_ratios": [3, 1]})
    for k, (col, label) in enumerate(variables):
        x, n, g1, g2, t1, t2 = shape(d[col])
        skewed, kurtic = abs(g1) > t1, abs(g2) > t2

        ax = axes[0, k]
        ax.hist(x, bins=28, color=ACCENT, alpha=.75, edgecolor="white", linewidth=.4)
        ax.axvline(x.mean(), color=WARN, lw=2.2, label="mean")
        ax.axvline(np.median(x), color=GOOD, lw=2.2, ls="--", label="median")
        ax.set_title(label, fontsize=10, color=INK)
        ax.tick_params(labelsize=7)
        ax.set_yticks([])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        if k == 0:
            ax.legend(fontsize=7.5, frameon=False)

        verdict = []
        verdict.append(f"$g_1$ = {g1:+.3f}   (> {t1:.3f}? {'yes' if skewed else 'no'})")
        verdict.append(f"$g_2$ = {g2:+.3f}   (> {t2:.3f}? {'yes' if kurtic else 'no'})")
        ax.text(.02, .97, "\n".join(verdict), transform=ax.transAxes, va="top",
                fontsize=7.6, color=INK,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=MUTED, lw=.6))

        bx = axes[1, k]
        bx.boxplot(x, orientation="horizontal", widths=.55,
                   patch_artist=True,
                   boxprops=dict(facecolor=ACCENT, alpha=.35, edgecolor=INK),
                   medianprops=dict(color=GOOD, lw=2),
                   flierprops=dict(marker="o", markersize=2.5, markerfacecolor=WARN,
                                   markeredgecolor="none", alpha=.6))
        bx.set_yticks([])
        bx.tick_params(labelsize=7)
        for side in ("top", "right", "left"):
            bx.spines[side].set_visible(False)
        tag = ("skewed · " if skewed else "symmetric · ") + ("kurtic" if kurtic else "normal tails")
        bx.set_xlabel(tag, fontsize=8, color=WARN if (skewed or kurtic) else GOOD)

    fig.suptitle("Skewness and kurtosis are independent: four real variables, four verdicts",
                 fontsize=11.5, color=INK, y=.99)
    fig.tight_layout(rect=(0, 0, 1, .96))

    OUT.mkdir(exist_ok=True)
    path = OUT / "shape_gallery.png"
    fig.savefig(path, dpi=150, facecolor="white")
    print(f"wrote {path.relative_to(ROOT)}")

    print(f"\n{'variable':<22}{'n':>6}{'g1':>9}{'g2':>9}   verdict")
    for col, label in variables:
        _, n, g1, g2, t1, t2 = shape(d[col])
        v = ("skewed" if abs(g1) > t1 else "symmetric") + ", " + \
            ("kurtic" if abs(g2) > t2 else "normal tails")
        print(f"{col:<22}{n:>6}{g1:>+9.3f}{g2:>+9.3f}   {v}")


if __name__ == "__main__":
    main()
