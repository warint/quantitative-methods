"""Session 07: compare a tree, random forest, and gradient boosting."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    X = rng.uniform(-3, 3, size=(500, 4))
    y = np.sin(1.5 * X[:, 0]) + X[:, 1] ** 2 - 0.7 * X[:, 2] * X[:, 3] + rng.normal(0, .5, 500)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.35, random_state=SEED)
    models = {
        "Tree": DecisionTreeRegressor(max_depth=4, random_state=SEED),
        "Forest": RandomForestRegressor(n_estimators=250, min_samples_leaf=4, random_state=SEED),
        "Boosting": GradientBoostingRegressor(n_estimators=250, learning_rate=.04, max_depth=2, random_state=SEED),
    }
    mse = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        mse[name] = mean_squared_error(y_test, model.predict(X_test))
        print(f"{name:8s} test MSE = {mse[name]:.3f}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(list(mse), list(mse.values()), color=["#94a3b8", "#2563eb", "#f97316"])
    ax.set(ylabel="test MSE", title="Ensembling stabilises flexible trees")
    fig.tight_layout()
    fig.savefig(OUT / "ensemble_comparison.png", dpi=180)


if __name__ == "__main__":
    main()
