"""Session 03: the same coefficient with classical and robust uncertainty."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    rng = np.random.default_rng(SEED)
    x = rng.uniform(0, 10, 500)
    error = rng.normal(0, 0.35 + 0.28 * x)
    y = 2 + 0.9 * x + error
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    robust = model.get_robustcov_results(cov_type="HC3")

    print(f"slope: {model.params[1]:.3f}")
    print(f"classical SE: {model.bse[1]:.3f}")
    print(f"HC3 robust SE: {robust.bse[1]:.3f}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(model.fittedvalues, model.resid, s=16, alpha=0.45)
    ax.axhline(0, color="0.25", lw=1)
    ax.set(xlabel="fitted value", ylabel="residual", title="A widening residual fan signals heteroskedasticity")
    fig.tight_layout()
    fig.savefig(OUT / "residual_fan.png", dpi=180)


if __name__ == "__main__":
    main()
