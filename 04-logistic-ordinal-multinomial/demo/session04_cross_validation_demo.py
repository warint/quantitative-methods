"""Session 04: training error falls while validation error turns upward."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = np.sort(rng.uniform(-3, 3, 100))
    y = np.sin(x) + rng.normal(0, 0.35, x.size)
    X = x[:, None]
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    degrees = range(1, 16)
    train_mse, cv_mse = [], []

    for degree in degrees:
        model = make_pipeline(PolynomialFeatures(degree), StandardScaler(), LinearRegression())
        model.fit(X, y)
        train_mse.append(np.mean((y - model.predict(X)) ** 2))
        cv_mse.append(-cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error").mean())

    best = int(np.argmin(cv_mse)) + 1
    print(f"Best degree by 5-fold CV: {best}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(list(degrees), train_mse, marker="o", label="training MSE")
    ax.plot(list(degrees), cv_mse, marker="o", label="5-fold CV MSE")
    ax.axvline(best, ls="--", color="#f97316")
    ax.set(xlabel="polynomial degree", ylabel="MSE", title="Complexity helps until variance takes over")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "bias_variance_cv.png", dpi=180)


if __name__ == "__main__":
    main()
