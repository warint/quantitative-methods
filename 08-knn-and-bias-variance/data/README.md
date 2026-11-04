# Session 08 — Data

**The Jordà–Schularick–Taylor Macrohistory Database — 18 economies, 1870–2020, 88 financial crises, with the paper's predictors already derived**

Session 08 runs in a folder of the student's own, with plain Python — no clone, no `qmib`. Every
file is read by URL from the course site:

```python
import pandas as pd

SITE = "https://warint.github.io/quantitative-methods/data/"
jst  = pd.read_csv(SITE + "session-08/jst_crises.csv")   # the paper's data
core = pd.read_csv(SITE + "core.csv")                    # shared by every group
mine = pd.read_csv(SITE + "angle_c_country.csv")         # YOUR angle — see your dictionary
```

| File | What | Source |
|---|---|---|
| `jst_crises.csv` (here, and on the site) | identifiers, crisis dates, the outcome `crisis_next2` and the seven predictors of Bluwstein et al. (2023) | written by [`scripts/build_session08_data.py`](../../scripts/build_session08_data.py) from the JST database |
| `core.csv`, `angle_*.csv` (site only) | the synthetic spine, as CSV | written by `scripts/build_docs.py` from `data/spine/*.parquet` |

The publisher's own site refuses plain Python downloads, which is why the paper's data is served
from the course site.

## Licence and citation

The JST Macrohistory Database is licensed **CC BY-NC-SA 4.0**
([macrohistory.net/database](https://www.macrohistory.net/database/)); `jst_crises.csv` is a
derived subset and is shared under the same licence. Cite it as:

> Òscar Jordà, Moritz Schularick and Alan M. Taylor (2017), "Macrofinancial History and the New
> Business Cycle Facts", *NBER Macroeconomics Annual 2016*, vol. 31, University of Chicago Press.

- Your group's columns, units and traps: [data dictionaries](../../data/spine/dictionaries/)
- Provenance and flags of the spine: [`data/spine/PROVENANCE.md`](../../data/spine/PROVENANCE.md)
