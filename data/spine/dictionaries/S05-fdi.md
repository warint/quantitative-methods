# Session 05 — data dictionary

**Determinants of bilateral foreign direct investment**
**Unit of analysis:** parent country × host country, 2019

The 56 candidate determinants of FDI from Blonigen & Piger (2014), rebuilt from the sources
the paper names, for a year two decades after theirs. One row is a directed country pair:
what country A holds in country B.

```python
import qmib

fdi = qmib.load("fdi")
cov = [c for c in fdi.columns if c not in ("parent", "host", "year", "fdi_stock_musd")]
d   = fdi[fdi.fdi_stock_musd > 0].dropna(subset=cov)   # the log-levels sample
```

| | |
|---|---|
| **File** | `data/spine/fdi_determinants.parquet` |
| **Rows** | 7,051 directed pairs |
| **Candidate covariates** | 56 |
| **Keys** | `parent`, `host` |
| **Positive FDI position** | 3,427 rows |
| **Complete across all 56** | 765 rows |
| **Parents / hosts** | 37 / 226 |
| **Built by** | `scripts/build_fdi_determinants.py` |

> **This is real data.** Every number comes from the OECD, CEPII, the World Bank or Freedom
> House. Unlike the rest of the spine, nothing here is a teaching fixture.

---

## Columns

| Column | Meaning | Unit | Range / values | Missing | Source |
|---|---|---|---|---|---|
| `parent` | Parent (investing) country | ISO3 | 37 values: AUS, BEL, CAN, CHE, CHL … | 0.0% |  |
| `host` | Host (receiving) country | ISO3 | 226 values: ABW, AFG, AGO, AIA, ALB … | 0.0% |  |
| `year` | Reference year | year | 2019 | 0.0% |  |
| `fdi_stock_musd` | Outward FDI position of PARENT in HOST | US$ millions | -21,251 … 909,242 | 0.0% | OECD |
| `parent_gdp` | PARENT GDP | current US$ | 24,857,740 … 21,372,572,437 | 2.8% | CEPII |
| `host_gdp` | HOST GDP | current US$ | 54,223 … 21,372,572,437 | 13.5% | CEPII |
| `distance` | Distance between the most populous cities | km | 2 … 19,806 | 6.2% | CEPII |
| `parent_gdp_pc` | PARENT GDP per capita | US$ | 6.42 … 113 | 2.8% | CEPII |
| `host_gdp_pc` | HOST GDP per capita | US$ | 0.224 … 169 | 13.5% | CEPII |
| `gdp_sum` | Sum of HOST and PARENT GDP | current US$ | 24,911,964 … 35,652,509,938 | 15.9% | derived |
| `gdp_similarity` | GDP similarity index (share × share) | 0–0.25 | 2.54e-06 … 0.25 | 15.9% | derived |
| `gdp_diff_sq` | Squared GDP difference | US$² | 64,366,748 … 456,784,534,801,392,795,648 | 15.9% | derived |
| `gdp_pc_diff_sq` | Squared GDP per capita difference | US$² | 1.6e-05 … 26,449 | 15.9% | derived |
| `host_urban` | HOST urban population | % of total | 13.9 … 100 | 7.1% | WDI |
| `parent_urban` | PARENT urban population | % of total | 53.4 … 94 | 0.0% | WDI |
| `contiguity` | Shared land border | 0/1 | 0/1 (mean 0.017) | 6.2% | CEPII |
| `host_remoteness` | HOST distance from all others, GDP-weighted | km | 5,886 … 13,289 | 0.0% | derived |
| `parent_remoteness` | PARENT distance from all others, GDP-weighted | km | 5,886 … 13,289 | 0.0% | derived |
| `timezone_diff` | Time-zone difference | hours | 0 … 21 | 6.2% | CEPII |
| `host_education` | HOST tertiary enrolment | % gross | 2.86 … 144 | 41.7% | WDI |
| `host_skill` | HOST labour force with advanced education | % of working age | 57.8 … 92.3 | 46.4% | WDI |
| `parent_education` | PARENT tertiary enrolment | % gross | 19.4 … 144 | 2.9% | WDI |
| `parent_skill` | PARENT labour force with advanced education | % of working age | 72.3 … 90.2 | 0.0% | WDI |
| `education_diff_sq` | Squared education difference | %² | 9.09e-07 … 19,911 | 43.5% | derived |
| `skill_diff_sq` | Squared skill difference | %² | 8.1e-05 … 1,045 | 46.4% | derived |
| `gdpdiff_x_edudiff` | GDP difference × education difference | interaction | -1,812,171,486,226 … 1,229,540,603,479 | 47.6% | derived |
| `gdpdiff_x_skilldiff` | GDP difference × skill difference | interaction | -322,120,881,476 … 394,546,523,488 | 49.6% | derived |
| `host_capital_per_worker` | HOST investment per worker † | US$ per worker | 154 … 82,066 | 28.7% | WDI |
| `parent_capital_per_worker` | PARENT investment per worker † | US$ per worker | 2,734 … 82,066 | 0.0% | WDI |
| `capital_per_worker_diff_sq` | Squared difference in investment per worker † | (US$/worker)² | 0.584 … 6,709,483,921 | 28.7% | derived |
| `host_land` | HOST land area | km² | 10 … 16,376,870 | 7.1% | WDI |
| `parent_land` | PARENT land area | km² | 2,574 … 9,147,420 | 0.0% | WDI |
| `host_pop_density` | HOST population density | people per km² | 0.137 … 20,426 | 7.1% | WDI |
| `host_is_oil` | HOST is a fuel exporter (fuel > 30% of exports) | 0/1 | 0/1 (mean 0.125) | 0.0% | WDI |
| `common_language_official` | Shared official language | 0/1 | 0/1 (mean 0.089) | 9.5% | CEPII |
| `common_language_overlap` | Language spoken by ≥9% in both | 0/1 | 0/1 (mean 0.094) | 9.5% | CEPII |
| `colonial_link` | Colonial relationship, ever | 0/1 | 0/1 (mean 0.028) | 6.2% | CEPII |
| `host_openness` | HOST trade openness (exports + imports) | % of GDP | 22.8 … 383 | 19.8% | WDI |
| `parent_openness` | PARENT trade openness | % of GDP | 26.3 … 383 | 0.0% | WDI |
| `edudiff_x_hostopen` | Education difference × HOST openness | interaction | -23,248 … 47,666 | 47.3% | derived |
| `skilldiff_x_hostopen` | Skill difference × HOST openness | interaction | -2,962 … 4,837 | 50.0% | derived |
| `regional_trade_agreement` | Regional trade agreement in force | 0/1 | 0/1 (mean 0.373) | 6.2% | CEPII |
| `customs_union` | Customs union in force | 0/1 | 0/1 (mean 0.221) | 0.0% | CEPII |
| `services_agreement` | Economic integration agreement in services | 0/1 | 0/1 (mean 0.136) | 0.0% | CEPII |
| `host_new_business_density` | HOST new business density ‡ | per 1,000 adults | 0.0198 … 250 | 28.4% | WDI |
| `host_logistics` | HOST logistics performance index ‡ | 1–5 | 1.95 … 4.2 | 28.7% | WDI |
| `host_unemployment` | HOST unemployment ‡ | % of labour force | 0.1 … 28.5 | 18.1% | WDI |
| `host_secondary_enrolment` | HOST secondary enrolment ‡ | % gross | 20.2 … 157 | 37.0% | WDI |
| `host_tax_revenue` | HOST tax revenue | % of GDP | 0.937 … 35 | 39.1% | WDI |
| `host_is_tax_haven` | HOST identified as a tax haven | 0/1 | 0/1 (mean 0.145) | 0.0% | OECD list |
| `both_wto` | Both are WTO members § | 0/1 | 0/1 (mean 0.679) | 0.0% | CEPII |
| `both_eu` | Both are EU members § | 0/1 | 0/1 (mean 0.080) | 0.0% | CEPII |
| `host_mobile` | HOST mobile subscriptions | per 100 people | 16.3 … 416 | 9.2% | WDI |
| `host_internet` | HOST internet users | % of population | 2.73 … 99.7 | 17.2% | WDI |
| `host_fixed_line` | HOST fixed telephone lines | per 100 people | 0 … 57.5 | 9.6% | WDI |
| `host_domestic_credit` | HOST domestic credit to private sector | % of GDP | 1.7 … 237 | 24.3% | WDI |
| `host_market_cap` | HOST market capitalisation of listed firms | % of GDP | 0.404 … 1,349 | 64.8% | WDI |
| `host_hitech_exports` | HOST high-technology exports | % of manufactured exports | 0 … 95.6 | 26.8% | WDI |
| `host_political_rights` | HOST political rights (1 most free – 7 least) | 1–7 | 1 … 7 | 15.4% | Freedom House |
| `host_civil_liberties` | HOST civil liberties (1 most free – 7 least) | 1–7 | 1 … 7 | 15.4% | Freedom House |

---

## Where this departs from the paper

**†** The paper uses the Penn World Table capital *stock* per worker. This is gross fixed
capital formation per worker, a *flow*. A weaker proxy, and you should say so.

**‡** The paper's variables 41–44 — time to enforce a contract, register property, start a
business, resolve insolvency — came from Doing Business, which the World Bank discontinued in
2021 and withdrew. These four host-country cost-and-capacity measures stand in their place.

**§** The paper's variables 47–48 — bilateral investment treaty, double taxation treaty — have
no free machine-readable source. Shared WTO and shared EU membership stand in.

## Traps

- **`fdi_stock_musd` is zero for most pairs, and skewed where it is not.** The paper's preferred
  specification logs everything, which silently drops every zero. Decide what a zero means before
  you drop it: no investment, or no reporting?
- **Only 37 countries appear as parents.** OECD members report; the rest are hosts only. Anything
  you find is conditional on the investor being an OECD economy.
- **`host_market_cap` is missing for nearly half the positive-FDI rows.** Requiring all 56
  covariates costs you most of the sample. Listwise deletion is a choice, not a default.
- **Six covariates are substitutions, not the paper's own.** They are marked above.
- **The interaction terms go collinear under logs**, exactly as the paper notes — which is why its
  table 3 shows `NA` for variables 22, 23, 36 and 37 in the log-levels column.

## First look — ten minutes

1. `d.fdi_stock_musd.describe()`, then the same on the log. Which would you model?
2. Count pairs with a zero position. What fraction does logging discard?
3. The correlation matrix of the 56: report the largest off-diagonal absolute value and name the
   pair. That number is what decides lasso versus elastic net.
4. Which parents invest in most hosts? Which hosts receive from most parents?
