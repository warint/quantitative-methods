"""
MATH60033A — Session 09 lab starter
Building and validating an index from central bank language

Run from this folder:
    python session09_lab.py

Reproducibility rules for this course:
    * set every random seed explicitly
    * never load data from a URL inside the lab — read the cached local file
    * put every preprocessing step inside the cross-validation pipeline
"""

import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 60033
rng = np.random.default_rng(RANDOM_SEED)

def load_data(path):
    """Load the cached dataset for session 09.

    See ../../data/README.md for how to produce the cache file.
    """
    raise NotImplementedError


def main():
    # Work through the tasks in ../README.md in order.
    # Keep each task in its own function so your group can split the work.
    raise NotImplementedError


if __name__ == "__main__":
    main()
