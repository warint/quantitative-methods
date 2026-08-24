"""Session 01: loss, risk, and the conditional mean.

Run from the repository root:
    python 01-foundations-scenarios-and-tools/demo/session01_foundations_demo.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = np.linspace(-3, 3, 160)
    truth = 1.5 + 0.8 * x + 0.9 * np.sin(1.5 * x)  # E[Y|X=x]
    y = truth + rng.normal(0, 0.8, x.size)
    constant = np.repeat(y.mean(), x.size)

    print(f"MSE, constant predictor: {np.mean((y - constant) ** 2):.3f}")
    print(f"MSE, conditional-mean oracle: {np.mean((y - truth) ** 2):.3f}")
    print("The remaining error is noise: better modelling cannot remove it.")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(x, y, s=16, alpha=0.45, label="observed Y")
    ax.plot(x, truth, lw=3, label="E[Y | X]")
    ax.axhline(y.mean(), ls="--", color="0.35", label="constant predictor")
    ax.set(xlabel="X", ylabel="Y", title="Prediction separates signal from irreducible noise")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "conditional_mean.png", dpi=180)


if __name__ == "__main__":
    main()
