"""
Session 07 · Part 0 — is everything in place?

Run this first, in your own session-07 folder (not the course repository), with
its environment active:

    python check_setup.py

It checks three things: Python itself, the four packages the scripts use, and
that the four data files on the course site can be reached. Every line should
say OK. It changes nothing on your machine.
"""

import sys
import urllib.request
from importlib import import_module

print(f"Python {sys.version.split()[0]}  ({sys.executable})")
if sys.version_info < (3, 10):
    print("  MISSING  Python 3.10 or newer   ->  install it from python.org")

# The four packages, installed by name: pip install pandas statsmodels scikit-learn matplotlib
print("\nPackages")
for module, package in [("pandas", "pandas"), ("statsmodels", "statsmodels"),
                        ("sklearn", "scikit-learn"), ("matplotlib", "matplotlib")]:
    try:
        version = getattr(import_module(module), "__version__", "")
        print(f"  OK       {package:14} {version}")
    except ImportError:
        print(f"  MISSING  {package:14} ->  pip install {package}")

# The four data files, one per paper, on the course site
DATA = "https://warint.github.io/quantitative-methods/data/session-07/"
print("\nData")
for paper, name in [("1 · Fraiberger et al.", "paper1_fraiberger_2021.csv"),
                    ("2 · Saganowski et al.", "paper2_saganowski_2019.csv"),
                    ("3 · Blonigen & Piger", "paper3_blonigen_piger_2014.csv"),
                    ("4 · Topalova & Khandelwal", "paper4_topalova_khandelwal_2011.csv")]:
    try:
        with urllib.request.urlopen(urllib.request.Request(DATA + name, method="HEAD"), timeout=15) as r:
            size = int(r.headers.get("Content-Length", 0)) / 1e6
        print(f"  OK       {paper:26} {size:.1f} MB")
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e) and sys.platform == "darwin":
            # Python from python.org on macOS ships without certificates until its
            # one-time "Install Certificates" command has been run.
            v = f"{sys.version_info.major}.{sys.version_info.minor}"
            print(f"  MISSING  {paper:26} ->  certificates not installed. Once, in the terminal:\n"
                  f'           open "/Applications/Python {v}/Install Certificates.command"')
        else:
            print(f"  MISSING  {paper:26} ->  no connection to the course site? ({e})")
