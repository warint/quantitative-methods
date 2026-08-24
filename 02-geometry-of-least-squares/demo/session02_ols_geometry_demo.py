"""Session 02: OLS as projection, calculated without a matrix inverse."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = np.linspace(0, 10, 80)
    y = 3 + 1.7 * x + rng.normal(0, 2.2, x.size)
    X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ beta
    residual = y - fitted

    print(f"beta = {beta.round(3)}")
    print(f"X.T @ residual = {(X.T @ residual).round(10)}")
    print("The near-zero vector is the right-angle condition.")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(x, y, s=22, alpha=0.6)
    ax.plot(x, fitted, lw=3, color="#2563eb")
    for i in range(0, x.size, 8):
        ax.plot([x[i], x[i]], [fitted[i], y[i]], color="#f97316", lw=1)
    ax.set(xlabel="x", ylabel="y", title="OLS chooses residuals orthogonal to every column of X")
    fig.tight_layout()
    fig.savefig(OUT / "ols_projection.png", dpi=180)


if __name__ == "__main__":
    main()
