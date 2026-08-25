"""Session 08: PCA compresses correlated series into a few directions."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    n, p = 180, 20
    factors = rng.normal(size=(n, 3))
    loadings = rng.normal(size=(3, p))
    X = factors @ loadings + rng.normal(scale=.55, size=(n, p))
    Z = StandardScaler().fit_transform(X)
    pca = PCA().fit(Z)
    cumulative = np.cumsum(pca.explained_variance_ratio_)
    keep = int(np.argmax(cumulative >= .80) + 1)
    print(f"Components needed for at least 80% variance: {keep}")
    print(f"First three shares: {pca.explained_variance_ratio_[:3].round(3)}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(np.arange(1, p + 1), cumulative, marker="o")
    ax.axhline(.80, ls="--", color="#f97316")
    ax.axvline(keep, ls="--", color="#f97316")
    ax.set(xlabel="number of components", ylabel="cumulative explained variance", ylim=(0, 1.02),
           title="PCA asks how many directions carry most of the movement")
    fig.tight_layout()
    fig.savefig(OUT / "pca_scree.png", dpi=180)


if __name__ == "__main__":
    main()
