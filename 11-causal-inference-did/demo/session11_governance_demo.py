"""Session 11: rolling-origin evaluation and a shift diagnostic."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def rolling_origin(n: int, initial: int, horizon: int, step: int):
    for stop in range(initial, n - horizon + 1, step):
        yield np.arange(stop), np.arange(stop, stop + horizon)


def main() -> None:
    rng = np.random.default_rng(SEED)
    n = 180
    y = np.zeros(n)
    for t in range(1, n):
        level_shift = 1.0 if t >= 130 else 0.0
        y[t] = 0.75 * y[t - 1] + level_shift + rng.normal(scale=.65)

    errors = []
    for train, test in rolling_origin(n, initial=60, horizon=1, step=1):
        prediction = y[train[-12:]].mean()  # named benchmark: trailing-year mean
        errors.append(y[test[0]] - prediction)
    print(f"Rolling-origin RMSE: {np.sqrt(np.mean(np.square(errors))):.3f}")

    feature = np.column_stack([y[:-1], np.arange(n - 1) / n])
    period = (np.arange(n - 1) >= 129).astype(int)
    shift_model = LogisticRegression().fit(feature, period)
    shift_auc = roc_auc_score(period, shift_model.predict_proba(feature)[:, 1])
    print(f"Train-vs-deploy shift AUC: {shift_auc:.3f}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(y, lw=2)
    ax.axvline(130, ls="--", color="#f97316", label="distribution shift")
    ax.set(xlabel="time", ylabel="outcome", title="A model can be correct for yesterday and wrong for tomorrow")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "forecast_shift.png", dpi=180)


if __name__ == "__main__":
    main()
