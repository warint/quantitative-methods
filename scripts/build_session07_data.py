"""Write the four session-07 data files: one CSV per paper, read by URL.

    python scripts/build_session07_data.py

Why this exists
---------------
Session 07 runs four papers' data through the models of sessions 3 to 5. The
students do it in a fresh folder of their own, with plain Python and pip, not
inside a clone of this repository — so the scripts cannot read the replication
files that sessions 2 to 6 download into the clone, nor call qmib. Each script
instead reads one CSV from the course site:

    https://warint.github.io/quantitative-methods/data/session-07/<file>.csv

This script writes those CSVs into 07-replication-workshop/data/, where they
are committed (the raw replication files are git-ignored, so the site must be
rebuildable without them); scripts/build_docs.py copies them to the site.

Only the columns the models use are kept, which takes the Fraiberger file from
104 MB to under 6. The rows are left alone: every filter the analysis applies
is in the student's script, where they can see it.

Licences: the three Dataverse deposits are CC0 1.0 (Fraiberger et al.
doi:10.7910/DVN/QNKFJF, Saganowski et al. doi:10.7910/DVN/ONOFS7, Topalova and
Khandelwal doi:10.7910/DVN/8WEXYD). The FDI table is the course's own rebuild
from public sources (scripts/build_fdi_determinants.py), already in the repo.

Needs the replication files of sessions 02, 04 and 06 downloaded into the
clone (see each session's README), and the FDI spine file.
"""

import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "07-replication-workshop" / "data"

FRAIBERGER = ROOT / "02-exploratory-data-analysis/data/replication/public/data/regression_sample.dta"
SAGANOWSKI = ROOT / ("04-logistic-ordinal-multinomial/data/replication/12 IrvineMessages_s7o3_infomap_1state/"
                     "12 IrvineMessages_s7o3_infomap_1state.partition.1.fold.1.csv")
TOPALOVA = ROOT / "06-advanced-regression/data/replication/prod_dataregression.dta"


def main():
    import qmib
    OUT.mkdir(parents=True, exist_ok=True)
    missing = [p for p in (FRAIBERGER, SAGANOWSKI, TOPALOVA) if not p.exists()]
    if missing:
        sys.exit("Download the replication files first; missing:\n  " +
                 "\n  ".join(str(p.relative_to(ROOT)) for p in missing))

    files = {}

    # Paper 1: a country-day. The five columns the script reads.
    files["paper1_fraiberger_2021.csv"] = pd.read_stata(
        FRAIBERGER, columns=["iso", "DATE", "F0_index", "L1_sent1_best", "L1_vix"])

    # Paper 2: the authors' own CSV, unchanged (it is small).
    shutil.copy2(SAGANOWSKI, OUT / "paper2_saganowski_2019.csv")

    # Paper 3: the FDI table, as qmib.load("fdi") returns it.
    files["paper3_blonigen_piger_2014.csv"] = qmib.load("fdi")

    # Paper 4: a firm-year. The columns the script reads, every year.
    files["paper4_topalova_khandelwal_2011.csv"] = pd.read_stata(TOPALOVA)[
        ["companyname", "yr", "tfp1000", "lagtariff", "laginputariff", "prgroup",
         "govown", "foreign", "medium", "small", "age"]]

    for name, df in files.items():
        df.to_csv(OUT / name, index=False)
    for f in sorted(OUT.glob("*.csv")):
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
