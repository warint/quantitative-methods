# The data spine

One panel, assembled once, extended as the semester proceeds. Full specification:
[`RESEARCH-MANDATES.md`, section 7](../../RESEARCH-MANDATES.md#7-the-data-spine).

```
data/spine/
├── PROVENANCE.md                  what the files are, flags, breaks, checksums
├── MANIFEST.csv                   machine-readable file list
├── dictionaries/G01.md … G10.md   one page per group — every column, unit, range, trap
├── core.parquet                   shared: GDP, population, employment, productivity, GFCF,
│                                  and `falling_behind_next` (the Session 06 label)
├── angle_a_country.parquet        G01   angle_a_sector.parquet        G02
├── angle_b_occupation.parquet     G03   angle_b_sector.parquet        G04
├── angle_c_country.parquet        G05   angle_c_sector_size.parquet   G06
├── angle_d_partner.parquet        G07   angle_d_product.parquet       G08
└── angle_e_centralbank.parquet    G09   angle_e_national.parquet      G10
```

`core.parquet` is shared: every angle joins to it, so outcomes and controls are common across the
class and results are comparable.

## For students

These files are **already built**. Read them, do not rebuild them:

```python
import pandas as pd
core = pd.read_parquet("data/spine/core.parquet")
mine = pd.read_parquet("data/spine/angle_c_country.parquet")   # your angle (see your dictionary)
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

**Start with your own [data dictionary](dictionaries/)** — every column with its unit, range and
missingness, the traps specific to your file, and three *first look* checks to run before you model
anything. Then read [`PROVENANCE.md`](PROVENANCE.md). Knowing that a series is survey-based, or
revised, or has a break in 2021, is part of your answer — not a footnote.

If you add a series of your own, add it to `PROVENANCE.md` with its source, download date and
licence. This is an ongoing obligation.

## For the instructor

Build scripts live in [`../../scripts/build_spine/`](../../scripts/build_spine/). Verify the
sources first:

```bash
python scripts/verify_sources.py                    # do the codes still resolve?
python scripts/build_spine/build.py                 # writes the parquet files here
python scripts/build_spine/make_dictionaries.py     # regenerate the column documentation
```

To regenerate the teaching fixtures instead (no network needed):

```bash
python scripts/build_spine/make_fixtures.py
python scripts/build_spine/make_dictionaries.py
```

The parquet fixtures **are committed** — a deliberate exception to the rule that data are never
committed, made so that labs have zero download friction. The `.gitignore` allows `data/spine/*.parquet`.
