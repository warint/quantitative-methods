"""Session 10: cross-fitted residualisation for a treatment effect."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    n = 1200
    X = rng.normal(size=(n, 5))
    propensity = 1 / (1 + np.exp(-(0.8 * X[:, 0] - 0.5 * X[:, 1])))
    d = rng.binomial(1, propensity)
    true_effect = 2.0
    y = true_effect * d + np.sin(X[:, 0]) + X[:, 1] ** 2 + rng.normal(size=n)
    y_resid = np.empty(n)
    d_resid = np.empty(n)
    folds = KFold(5, shuffle=True, random_state=SEED)

    for train, test in folds.split(X):
        outcome = RandomForestRegressor(n_estimators=150, min_samples_leaf=8, random_state=SEED)
        treatment = RandomForestRegressor(n_estimators=150, min_samples_leaf=8, random_state=SEED + 1)
        outcome.fit(X[train], y[train])
        treatment.fit(X[train], d[train])
        y_resid[test] = y[test] - outcome.predict(X[test])
        d_resid[test] = d[test] - treatment.predict(X[test])

    theta = np.dot(d_resid, y_resid) / np.dot(d_resid, d_resid)
    score = d_resid * (y_resid - theta * d_resid)
    se = np.sqrt(np.mean(score ** 2) / (np.mean(d_resid ** 2) ** 2 * n))
    print(f"True effect: {true_effect:.3f}")
    print(f"DML estimate: {theta:.3f} (SE {se:.3f})")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(d_resid, y_resid, s=13, alpha=.35)
    grid = np.linspace(d_resid.min(), d_resid.max(), 100)
    ax.plot(grid, theta * grid, lw=3, color="#f97316")
    ax.set(xlabel="treatment residual", ylabel="outcome residual", title="DML estimates the slope after cross-fitted residualisation")
    fig.tight_layout()
    fig.savefig(OUT / "dml_residuals.png", dpi=180)


if __name__ == "__main__":
    main()
