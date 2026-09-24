"""
Session 07 · Step 0 — is everything in place?

Run this first, from the repository root (the folder that contains qmib.py):

    python 07-pca-and-factor-analysis/02-practice/starter/check_setup.py

It checks the Python packages the five replications use, and that each paper's
data is where the scripts expect it. Every line should say OK. Anything that
says MISSING tells you what to fix before you start.
"""

from pathlib import Path
import importlib
import os
import sys

# Work from the repository root whichever way the script was started — the Run
# button in VS Codium, or `python` from another folder.
try:
    ROOT = Path(__file__).resolve().parents[3]
except NameError:            # lines sent one by one with Shift+Enter: the
    ROOT = Path.cwd()        # terminal already starts in the repository root
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

print("Python packages")
for name in ["pandas", "numpy", "matplotlib", "scipy", "statsmodels",
             "sklearn", "linearmodels", "openpyxl", "qmib"]:
    try:
        importlib.import_module(name)
        print(f"  OK       {name}")
    except ImportError:
        print(f"  MISSING  {name}   ->  pip install -r requirements.txt"
              if name != "qmib" else
              f"  MISSING  {name}   ->  run this from the repository root")

print("\nThe papers' data")
FILES = {
    "02 · Fraiberger et al.": "02-exploratory-data-analysis/data/replication",
    "03 · Amsili et al.": "03-regression-adequacy-and-validity/data/replication/"
                          "2015-2019_CompleteAWC_w.1and15bar_dataset_toshare.xlsx",
    "04 · Saganowski et al.": "04-logistic-ordinal-multinomial/data/replication",
    "06 · Topalova & Khandelwal": "06-advanced-regression/data/replication/"
                                  "prod_dataregression.dta",
}
for paper, path in FILES.items():
    p = Path(path)
    found = p.exists() and (p.is_file() or any(p.iterdir()))
    print(f"  {'OK     ' if found else 'MISSING'}  {paper:28} {path}")

try:
    import qmib
    fdi = qmib.load("fdi")
    print(f"  OK       {'05 · Blonigen & Piger':28} qmib.load('fdi') -> {fdi.shape}")
except Exception as e:                      # noqa: BLE001 — report, don't crash
    print(f"  MISSING  {'05 · Blonigen & Piger':28} qmib.load('fdi') failed: {e}")

print("\nA MISSING package or file: see the pre-session page, section 2.")
