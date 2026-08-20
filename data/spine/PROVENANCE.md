# Data spine — provenance

> ## ⚠️ These are TEACHING FIXTURES, not observed data.

They carry the **schema, country and year coverage, observation flags, missingness patterns and
structural breaks** of the real sources, generated from a known latent structure so that every
method in the course behaves as it would on the real thing.

**Do not cite any number in these files as a fact about Europe.**

To replace them with real data:

```bash
python scripts/verify_sources.py              # confirm the dataset codes still resolve
python scripts/build_spine/build.py           # fetch from Eurostat / Comtrade / ECB
python scripts/build_spine/make_dictionaries.py
```

`build.py` overwrites these files and rewrites this page from the live sources.

Generated: **2026-07-31T17:19:26** · generator: `scripts/build_spine/make_fixtures.py` · seed **60033**

---

## Files

| File | Group | Rows | Cols | Keys | Missing | sha256 (16) |
|---|---|---|---|---|---|---|
| `core.parquet` | core | 450 | 11 | geo, time | 2.73% | `05199d18c485b429` |
| `angle_a_country.parquet` | G01 | 450 | 11 | geo, time | 4.16% | `71ba1dc1e712bbf6` |
| `angle_a_sector.parquet` | G02 | 3,150 | 7 | geo, time, nace_r2 | 2.74% | `9113e5eeb101d170` |
| `angle_b_occupation.parquet` | G03 | 3,600 | 9 | geo, time, isco08 | 4.36% | `0e28ac36a082f1e3` |
| `angle_b_sector.parquet` | G04 | 3,150 | 8 | geo, time, nace_r2 | 3.48% | `6ae1e41e3b37d216` |
| `angle_c_country.parquet` | G05 | 330 | 33 | geo, time | 24.0% | `8dacad5d4a277e82` |
| `angle_c_sector_size.parquet` | G06 | 2,520 | 10 | geo, time, nace_r2, size_emp | 5.73% | `a5e32e1ffe73dee6` |
| `angle_d_partner.parquet` | G07 | 3,150 | 7 | geo, time, partner | 1.24% | `f297ec37dd82d2f8` |
| `angle_d_product.parquet` | G08 | 2,700 | 8 | geo, time, hs | 2.58% | `e785e1c60d7b0b42` |
| `angle_e_centralbank.parquet` | G09 | 1,980 | 7 | doc_id | 0.0% | `3b104f364f3c74b3` |
| `angle_e_national.parquet` | G10 | 1,280 | 7 | doc_id | 0.0% | `b1d4c5a193a23e56` |

Column-level documentation, one page per group: [`dictionaries/`](dictionaries/).

---

## What is deliberately built in

Each session's lesson depends on a property of the data. These were engineered and then verified:

| Session | Property | Verified |
|---|---|---|
| 02 | Composition effects are real | `share_fossil` coefficient moves −61% once mix and intensity are controlled |
| 03 | Heteroskedasticity, clustering, an omittable confounder | error variance scales with country size |
| 04 | Temporal dependence | AR(0.92) latent factors — random K-fold is genuinely wrong |
| 05 | Correlated predictors, few true signals | max pairwise \|corr\| 0.95; only 2 of 28 variables stable at 60% across bootstraps |
| 06 | Rare event with imperfect signal | `falling_behind_next` base rate 10.0% |
| 08 | Low-rank factor structure | 3 latent factors; first 3 PCs recover most variance |
| 09 | Country types that actually exist | 4 types; k-means recovers them at adjusted Rand 0.77 |
| 10 | Confounded treatment with a known effect | true effect +2.4 pp; naive difference in means +4.2 pp (1.7× inflated) |
| 11 | Distribution shift | regime change after 2021 |

The latent factors, the true cluster labels and the true treatment effect are in
`scripts/build_spine/.truth/ground_truth.json` — **instructor only**, and git-ignored.

---

## Flags

| Flag | Meaning | What to do |
|---|---|---|
| `u` | low reliability | Do not drop silently — it biases coverage toward large economies |
| `c` | confidential | Value is NaN. Report how many you lost |
| `b` | break in series | A modelling problem, not a data error |
| `p` | provisional | Relevant to any real-time or vintage claim |

---

## Structural breaks

| From | To | What | Affects |
|---|---|---|---|
| 2020 | 2021 | COVID-19 | employment, energy demand — every group |
| 2021 | — | AI module begins | angle C has no AI observations before 2021 |
| 2022 | — | European energy price shock | angle A; dominates any model that ignores it |
| 2012 | 2022 | HS classification revisions | angle D; concordances are imperfect |

---

## Missingness is not random

It is heavier in small countries. Listwise deletion shifts your sample toward large economies.
Whatever you do about it, do it **inside** the cross-validation loop and report which countries
you lost.

---

## Adding your own series

Append a row to the file table with source, dataset code, download date, licence and known
issues. This is an ongoing obligation and part of what the Session 12 governance file is
assessed on.
