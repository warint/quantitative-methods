"""
MATH60033A — Session 06 lab starter
Credit scoring and bankruptcy prediction: from probability to decision

Run from this folder:
    python session06_lab.py

Reproducibility rules for this course:
    * set every random seed explicitly
    * never load data from a URL inside the lab — read the cached local file
    * put every preprocessing step inside the cross-validation pipeline
"""

import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 60033
rng = np.random.default_rng(RANDOM_SEED)

def soft_threshold(rho, lam):
    """Session 5's operator. Reuse your own implementation."""
    raise NotImplementedError


def logistic_irls(X, y, tol=1e-8, max_iter=100):
    """Track A: unpenalised logistic regression by Newton-Raphson / IRLS.

    Returns (beta, cov) where cov = inv(X.T @ W @ X).
    Watch for perfect separation: beta will diverge. Detect it and say so.
    """
    raise NotImplementedError


def logistic_elastic_net(X, y, lam, alpha, tol=1e-6, max_iter=100, w_floor=1e-5):
    """Track B: outer IRLS loop, inner coordinate descent on the penalised WLS problem.

    Clamp the IRLS weights at `w_floor` or the adjusted response explodes for
    well-classified points. This is the bug the lecture warned you about.
    """
    raise NotImplementedError


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
