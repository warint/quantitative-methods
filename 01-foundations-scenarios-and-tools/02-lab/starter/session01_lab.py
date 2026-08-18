"""
MATH60033A — Session 01 lab starter
Stress-testing an assumption with a local LLM

Run from this folder:
    python session01_lab.py

Reproducibility rules for this course:
    * set every random seed explicitly
    * never load data from a URL inside the lab — read the cached local file
    * put every preprocessing step inside the cross-validation pipeline
"""

import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 60033
rng = np.random.default_rng(RANDOM_SEED)

def simulate_indicator(n_periods=60, drift=0.02, sigma=0.05, trigger=1.5, seed=0):
    """Simulate a candidate indicator path and locate the first trigger crossing.

    TASK (Session 1, lab item 7)
    ---------------------------
    Complete this function so that it:
      1. simulates a random-walk-with-drift path of length `n_periods`, starting at 1.0;
      2. returns the path AND the index of the first period where it exceeds `trigger`
         (or None if it never does).

    Then answer, in your memo: if you re-run this with a different seed, how often does
    the trigger fire? What does that tell you about reading a single realised history
    as evidence?
    """
    rng = np.random.default_rng(seed)
    # --- your code here ---
    raise NotImplementedError


def main():
    path, first_cross = simulate_indicator()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(path, lw=1.5)
    ax.axhline(1.5, ls="--", color="crimson", label="trigger point")
    if first_cross is not None:
        ax.axvline(first_cross, ls=":", color="grey", label=f"first crossing (t={first_cross})")
    ax.set_xlabel("period")
    ax.set_ylabel("indicator")
    ax.legend()
    fig.tight_layout()
    fig.savefig("indicator.png", dpi=150)
    print("saved indicator.png")


if __name__ == "__main__":
    main()
