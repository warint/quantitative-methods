"""Session 05: compare OLS, ridge, lasso, and elastic net."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import ElasticNetCV, LassoCV, LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    X, y, truth = make_regression(n_samples=180, n_features=40, n_informative=7, noise=18,
                                  coef=True, random_state=SEED)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=SEED)
    models = {
        "OLS": LinearRegression(),
        "Ridge": make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 40))),
        "Lasso": make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=SEED)),
        "Elastic net": make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=[.2, .5, .8], cv=5, random_state=SEED)),
    }
    scores = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        scores[name] = np.mean((y_test - model.predict(X_test)) ** 2)
        print(f"{name:11s} test MSE = {scores[name]:.1f}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(list(scores), list(scores.values()), color=["#94a3b8", "#60a5fa", "#2563eb", "#f97316"])
    ax.set(ylabel="test MSE", title="A little bias can buy a large variance reduction")
    fig.tight_layout()
    fig.savefig(OUT / "regularisation_comparison.png", dpi=180)


if __name__ == "__main__":
    main()
