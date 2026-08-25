"""Session 09: clustering numeric points and vectorising short documents."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    centers = np.array([[-2, -1], [0, 2], [2.5, -0.5]])
    X = np.vstack([c + rng.normal(scale=.55, size=(70, 2)) for c in centers])
    model = KMeans(n_clusters=3, n_init=20, random_state=SEED).fit(X)
    print(f"Silhouette score: {silhouette_score(X, model.labels_):.3f}")

    documents = [
        "policy uncertainty increased after the shock",
        "inflation expectations remain anchored",
        "trade policy uncertainty weighs on investment",
        "labour markets remain resilient",
    ]
    tfidf = TfidfVectorizer().fit_transform(documents)
    print(f"TF-IDF shape: {tfidf.shape}; sparsity: {1 - tfidf.nnz / np.prod(tfidf.shape):.1%}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X[:, 0], X[:, 1], c=model.labels_, cmap="Blues", s=24)
    ax.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], marker="X", s=180, c="#f97316")
    ax.set(title="An algorithm always returns clusters; validation asks whether they mean anything")
    fig.tight_layout()
    fig.savefig(OUT / "kmeans_clusters.png", dpi=180)


if __name__ == "__main__":
    main()
