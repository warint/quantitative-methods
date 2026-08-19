"""
Session 11 lab starter
Final-project workshop: backtest, shift diagnostic, governance file

Run from this folder:
    python session11_lab.py

Reproducibility rules for this course:
    * set every random seed explicitly
    * never load data from a URL inside the lab — read the cached local file
    * put every preprocessing step inside the cross-validation pipeline
"""

import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 60033
rng = np.random.default_rng(RANDOM_SEED)

def rolling_origin_splits(n, initial, horizon, step=1, purge=0):
    """Yield (train_idx, test_idx) for an expanding-window backtest.

    `purge` leaves a gap between train and test to prevent leakage through
    overlapping horizons or windowed features. Set purge >= horizon - 1.
    """
    raise NotImplementedError


def diebold_mariano(e1, e2, horizon, loss=lambda e: e ** 2):
    """DM statistic with a Newey-West variance, lag truncation >= horizon - 1.

    Returns (stat, pvalue). Not valid for nested models on the same sample.
    """
    raise NotImplementedError


def shift_diagnostic(X_train, X_deploy, seed=60033):
    """Train a classifier to tell the two periods apart; return its AUC.

    AUC near 0.5  -> distributions look alike
    AUC near 1.0  -> your evaluation period is not your training period
    """
    raise NotImplementedError


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
