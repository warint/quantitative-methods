# Session 06 — Data

**Statlog German Credit (1,000 applicants, 20 features) + Polish/Taiwanese company bankruptcy (wide and severely imbalanced)**

- **Source:** UCI Machine Learning Repository
- **URL:** <https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data>

---

**German Credit** ships with an explicit **cost matrix**: classifying a bad customer
as good is stated to be five times worse than the reverse. This is unusual and pedagogically
valuable - it forces the threshold question into the open rather than letting 0.5 pass unexamined.

```python
from sklearn.datasets import fetch_openml
d = fetch_openml("credit-g", version=1, as_frame=True, parser="auto")
d.frame.to_parquet("data/credit_g.parquet")
```

**Bankruptcy data** (<https://archive.ics.uci.edu/dataset/365/polish+companies+bankruptcy+data>)
supplies the high-dimensional half: 64 highly correlated financial ratios, 2-5% positive rate,
substantial missingness. Every pathology in the lecture appears in it.

```python
from scipy.io import arff
import pandas as pd
data, meta = arff.loadarff("data/3year.arff")
pd.DataFrame(data).to_parquet("data/polish_3y.parquet")
```

---

## Rules for this folder

- Data files are **git-ignored**. Never commit raw data.
- Download **once**, cache as parquet, and read from the cache. The lab must run offline.
- Record your download date and, where available, a checksum in `PROVENANCE.md`.
- If you extend the dataset yourself, document the source and respect its licence.

```bash
# record provenance after downloading
echo "$(date -Iseconds)  $(shasum -a 256 <file>)" >> PROVENANCE.md
```
