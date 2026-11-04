"""Write the session-08 data file: the paper's predictors, one CSV, read by URL.

    python scripts/build_session08_data.py

Why this exists
---------------
Session 08's pre-session and practice run in a folder of the student's own,
with plain Python and four packages — no clone, no qmib. The publisher's site
refuses plain Python downloads, so the scripts read one CSV from the course
site instead:

    https://warint.github.io/quantitative-methods/data/session-08/jst_crises.csv

This script writes that CSV into 08-knn-and-bias-variance/data/, where it is
committed; scripts/build_docs.py copies it to the site. It starts from qmib's
cached copy of the database (qmib.load("jst"), which derives the predictors
Bluwstein et al. 2023 use), and keeps only the identifiers, the crisis dates
and those predictors. No row is dropped: every filter is in the student's script.

Licence. The Jorda-Schularick-Taylor Macrohistory Database is licensed CC
BY-NC-SA 4.0 (https://www.macrohistory.net/database/): non-commercial sharing
is allowed with attribution, under the same licence. The derived file is
therefore shared under CC BY-NC-SA 4.0, and must be cited as:
    Oscar Jorda, Moritz Schularick and Alan M. Taylor (2017), "Macrofinancial
    History and the New Business Cycle Facts", NBER Macroeconomics Annual 2016,
    vol. 31, University of Chicago Press.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import qmib  # noqa: E402

OUT = ROOT / "08-knn-and-bias-variance" / "data" / "jst_crises.csv"

KEEP = [
    "country", "iso", "year",
    "crisisjst",        # 1 in the first year of a systemic banking crisis
    "crisis_next2",     # 1 if a crisis starts in the next two years   <- the outcome
    # the predictors, all two-year changes (Bluwstein et al. 2023, section 3)
    "credit_growth",    # change in bank credit / GDP
    "yield_slope",      # long-term rate minus short-term rate (a level, not a change)
    "money_growth",     # change in broad money / GDP
    "cpi_growth",       # % change in consumer prices
    "pubdebt_change",   # change in public debt / GDP
    "ca_gdp",           # current account / GDP (a level)
    "investment_change",  # change in investment / GDP
]

jst = qmib.load("jst")[KEEP]
OUT.parent.mkdir(parents=True, exist_ok=True)
jst.to_csv(OUT, index=False, float_format="%.6g")
print(f"wrote {OUT.relative_to(ROOT)}: {jst.shape[0]} rows, {jst.shape[1]} columns, "
      f"{OUT.stat().st_size / 1e3:.0f} kB")
