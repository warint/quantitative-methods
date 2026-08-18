# Research mandates — MATH60033A

**Ten groups of three · five angles · one question per session**

---

## Contents

1. [How this works](#1-how-this-works)
2. [The five angles](#2-the-five-angles)
3. [Group allocation](#3-group-allocation)
4. [The session themes](#4-the-session-themes)
5. [What each angle does, session by session](#5-what-each-angle-does-session-by-session)
6. [The two-minute report](#6-the-two-minute-report)
7. [The data spine](#7-the-data-spine)
8. [Goals and assessment](#8-goals-and-assessment)

---

## 1. How this works

### The shape

Every session has a **big theme** — one question the whole class attacks. In the second half, each
of ten groups answers that question using **its own angle** and its own slice of the data. The last
twenty minutes are ten two-minute reports, after which the class holds five different lights on the
same question.

```
                    SESSION THEME (changes every week)
                             │
       ┌──────────┬──────────┼──────────┬──────────┐
       │          │          │          │          │
   ANGLE A    ANGLE B    ANGLE C    ANGLE D    ANGLE E     (fixed all semester)
   compute     work &    adoption &   trade &    policy
   & energy    skills   productivity dependence  language
       │          │          │          │          │
    2 groups   2 groups   2 groups   2 groups   2 groups
   (different resolutions of the same angle)
       │          │          │          │          │
       └──────────┴──────────┼──────────┴──────────┘
                             │
                   COLLECTIVE ANSWER
              (instructor synthesis, 5 min)
```

### Why the angle is fixed but the theme rotates

The theme changes weekly so that the method being taught is *used to answer something*, not
rehearsed on a toy dataset. The angle stays fixed so that groups accumulate expertise, notice their
data's pathologies, and arrive at Session 12 with eleven weeks of work rather than eleven
disconnected exercises.

There is a cost to this and you should know it: your angle is a constraint. Some session themes will
suit your data better than others. **When a method cannot answer the theme with your columns, saying
so clearly — and showing why — is a full-credit answer.** That judgement is the skill this course
exists to build.

### What is prepared for you

All data are **cleaned, joined and cached** in the repository before each session. You will not
spend lab time downloading, reshaping or debugging encodings. You spend it on the analysis: choosing
variables, changing specifications, testing whether your result survives.

Provenance for every series is recorded in `data/spine/PROVENANCE.md`. You are expected to read it —
knowing that a series is survey-based, or revised, or has a break in 2021, is part of your answer,
not a footnote.

---

## 2. The five angles

Each angle below states a **semester research question**, the **mandate** (what you own), the
**goals** (what you should be able to claim by Session 12), the **data**, and the **known
pitfalls** of that data.

---

### Angle A — Compute, energy and the physical constraint

> **Research question.** Is electrical power the binding constraint on European computing capacity,
> and what does the price and structure of European electricity imply about the cost of a large
> compute buildout?

**Mandate.** You own the physical layer. *Europe 2031* measures technological capability in
**gigawatts** — a choice that embeds a claim, namely that power is what binds. Your job across the
semester is to interrogate that claim empirically: how European electricity prices, generation mix
and industrial demand actually vary, what predicts them, and whether "compute capacity" and
"available power" are the same variable wearing different clothes.

**Goals.**

- Quantify the dispersion in European industrial electricity prices and decompose it into
  generation mix, taxation and network components.
- Establish whether price differences persist after controlling for structure (S02–S03).
- Build a defensible short-horizon forecast of industrial electricity prices (S04, S11).
- Determine how many independent dimensions describe a country's energy position (S08).
- State, with evidence, whether the gigawatt framing of *Europe 2031* is a reasonable proxy or a
  category error.

**Data.**

| Series | Source | Code / location |
|---|---|---|
| Electricity prices, non-household | Eurostat | `nrg_pc_205` |
| Electricity prices, components | Eurostat | `nrg_pc_205_c` |
| Energy balances (final consumption by sector) | Eurostat | `nrg_bal_c` |
| Electricity generation by fuel | Ember (open CSV) | <https://ember-energy.org/data/> |
| Load and generation, hourly | ENTSO-E Transparency (free registration) | <https://transparency.entsoe.eu/> |
| Energy intensity of the economy | Eurostat | `nrg_ind_ei` |

**Known pitfalls.** Price series are semi-annual and band-dependent (consumption bands IA–IF) — a
"price" is meaningless without its band. The 2022 energy shock is a structural break that will
dominate any model that ignores it. Ember and Eurostat generation figures differ in scope; document
which you used. ENTSO-E hourly data has gaps and occasional negative prices that are real, not
errors.

---

### Angle B — Work, skills and the social contract

> **Research question.** Which European occupations and sectors are most exposed to automation by
> AI, and does measured exposure predict what actually happened to employment and pay?

**Mandate.** You own the labour layer. *Europe 2031* claims that automation and labour displacement
weaken wage growth, tax revenues and the fiscal basis of European welfare states — a chain with at
least three links, each testable. You will build an **exposure measure from occupational task
descriptions** (text, in Session 9) and confront it with what employment and earnings actually did.

**Goals.**

- Construct and document a task-based exposure index at the occupation level, and defend its
  validity.
- Establish whether exposure is associated with employment change after controlling for sector
  composition (S02–S03).
- Determine whether exposure has any *predictive* content out of sample (S04–S07).
- Test whether the association survives an honest causal design (S10) — and report clearly if it
  does not.
- State what the evidence does and does not support about the displacement premise of the scenario.

**Data.**

| Series | Source | Code / location |
|---|---|---|
| Employment by occupation (ISCO-08) | Eurostat | `lfsa_egais` |
| Employment by sector (NACE) | Eurostat | `lfsa_egan22d` |
| Earnings, structure of earnings survey | Eurostat | `earn_ses18_*` |
| Unemployment by education | Eurostat | `lfsa_urgaed` |
| Job vacancy rate | Eurostat | `jvs_a_rate_r2` |
| Occupational task statements | O\*NET (public download) | <https://www.onetcenter.org/database.html> |
| EU occupation/skill taxonomy | ESCO | <https://esco.ec.europa.eu/en/use-esco/download> |

**Known pitfalls.** O\*NET describes the *US* labour market; mapping SOC to ISCO is lossy and you
must document your crosswalk. LFS occupation data are survey estimates with real sampling error —
small cells are unreliable and Eurostat flags them. Earnings surveys are quadrennial, not annual.
Any exposure index is a construct; Session 9's validity framework applies to it in full.

---

### Angle C — AI adoption and the productivity question

> **Research question.** Which European firms, sectors and countries are actually adopting AI, what
> stops the others, and is adoption associated with measurable productivity gains?

**Mandate.** You own the adoption layer — and you have the best data in the class. Eurostat's
enterprise survey measures AI use directly, by country, sector and firm size, including an explicit
battery of **barriers** to adoption (cost, expertise, data quality, legal uncertainty, ethics).
*Europe 2031* assumes rapid capability diffusion; your mandate is to find out whether diffusion is
happening, where it stalls, and whether it shows up in productivity statistics at all.

**Goals.**

- Map adoption across countries, sectors and firm-size classes, and identify where the gradient is
  steepest.
- Establish which barriers dominate, and whether they differ systematically by country or firm size.
- Test whether adoption predicts subsequent labour productivity growth (S04–S07) and whether that
  relationship survives a causal design (S10).
- Determine how many independent dimensions underlie the digital-intensity indicators (S08).
- State whether the diffusion premise of the scenario is supported, and on what horizon.

**Data.**

| Series | Source | Code / location |
|---|---|---|
| **AI use by enterprises** (verified live, 2021–2025) | Eurostat | `isoc_eb_ai` |
| Cloud computing services | Eurostat | `isoc_cicce_use` |
| ICT specialists employed | Eurostat | `isoc_ske_itspen` |
| Digital intensity index | Eurostat | `isoc_e_dii` |
| R&D expenditure | Eurostat | `rd_e_gerdtot` |
| Labour productivity and unit labour cost | Eurostat | `nama_10_lp_ulc` |
| Gross fixed capital formation | Eurostat | `nama_10_gdp` |

Key indicator codes within `isoc_eb_ai`: `E_AI_TANY` (uses any AI technology), `E_AI_TML` (machine
learning), `E_AI_TGE3` (three or more technologies), `E_AI_BCST` / `E_AI_BLE` / `E_AI_BDDT` /
`E_AI_BLEG` (barriers: cost, expertise, data, legal), `E_AI_BIAS` (has bias-checking measures).
Unit `PC_ENT` = percentage of enterprises.

**Known pitfalls.** The AI module began in 2021 — your panel is short, which constrains everything
you can say about trends. Question wording changed between waves; check the metadata before
comparing years. Many cells are flagged `u` (low reliability) or `C` (confidential) — dropping them
silently will bias your country coverage toward large economies. Self-reported adoption is not
verified adoption.

---

### Angle D — Trade, inputs and dependence

> **Research question.** How concentrated is Europe's dependence on the United States and China for
> the physical inputs to AI, and is that dependence increasing or decreasing?

**Mandate.** You own the supply chain. The scenario's starting condition asserts that Europe remains
economically dependent on both the US and China, while retaining leverage through ASML and
industrial capability. That is a claim about *bilateral trade concentration in specific product
lines*, and it is directly measurable. Your mandate is to measure it — and to be precise about what
"dependence" means, since the word does a great deal of unexamined work.

**Goals.**

- Construct defensible concentration measures (HHI, top-partner share, and at least one alternative)
  for AI-relevant product lines, and explain what each one assumes.
- Establish the direction of travel: is concentration rising, falling, or flat, and since when?
- Identify which products show genuine single-source exposure versus apparent concentration driven
  by re-export hubs.
- Test whether trade structure clusters countries into recognisable types (S09).
- State what leverage, if any, the data support — including the ASML claim.

**Data.**

| Series | Source | Code / location |
|---|---|---|
| Bilateral trade, HS 6-digit | UN Comtrade (public API) | <https://comtradeplus.un.org/> |
| Harmonised bilateral trade, 1995– | CEPII BACI (open) | <https://www.cepii.fr/CEPII/en/bdd_modele/bdd.asp> |
| EU trade detail | Eurostat COMEXT | `ds-045409` |
| Trade in value added | OECD TiVA | <https://www.oecd.org/sti/ind/measuring-trade-in-value-added.htm> |

Product lines: **8541/8542** semiconductors and integrated circuits · **8486** semiconductor
manufacturing equipment (the ASML line) · **8471** automatic data-processing machines · **8479.50**
industrial robots · **8517** telecommunications equipment.

**Known pitfalls.** Re-exports through the Netherlands, Belgium and Ireland massively distort
apparent bilateral flows — Rotterdam is not a producer. Mirror statistics disagree (A's reported
exports to B ≠ B's reported imports from A), sometimes by a lot; decide which side you trust and
say why. HS codes were revised in 2012, 2017 and 2022; concordances are imperfect. Value and
quantity tell different stories when unit prices move.

---

### Angle E — Institutional language and policy attention

> **Research question.** How has AI moved through European institutional language, and does
> attention in policy text lead, lag or track what happens in the real economy?

**Mandate.** You own the text. Everything the other four angles measure was preceded, accompanied
or followed by somebody writing something down. Your mandate is to turn that corpus into a
quantitative series and then to do the hard part: establish whether it measures anything. This is
the angle with the loosest data and the strictest validity burden.

**Goals.**

- Build at least two indices of AI attention or policy uncertainty — one dictionary-based and
  transparent, one embedding-based — and compare them.
- Validate both against the four criteria of Session 9 (face, convergent, predictive, robustness),
  and report failures honestly.
- Establish whether textual attention has any predictive relationship to investment, adoption or
  market volatility (S04–S07).
- Determine whether documents cluster into recognisable institutional or national types (S09).
- State whether policy language is a leading indicator, a lagging record, or neither.

**Data.**

| Source | Access | Notes |
|---|---|---|
| ECB press releases, statements, speeches | <https://www.ecb.europa.eu/press/> | Public; also available as a bulk speech dataset |
| EUR-Lex (EU legal instruments) | <https://eur-lex.europa.eu/> — open API/SPARQL | Full text, structured metadata, CELEX identifiers |
| National AI strategies | OECD.AI Policy Observatory <https://oecd.ai/> | Structured policy database |
| Bank of England / Bank of Canada speeches | Respective public sites | For the comparative variant |
| VSTOXX / VIX | Public market data | Convergent-validity check |

**Known pitfalls.** Corpus composition drives everything — if the ECB simply published more
documents in 2023, a raw count rises without any change in attention. Normalise, and say how.
Translation and multilingual sources introduce systematic differences you cannot ignore in a
European setting. Embedding models encode the priors of their training data; a locally-run model is
auditable in principle but you must actually audit it. Dictionary methods are transparent and often
outperform — do not assume sophistication wins.

---

## 3. Group allocation

Two groups per angle, differentiated by **unit of analysis**. Same question, different resolution —
so your findings are comparable but not duplicated, and disagreement between you is informative
rather than an error.

| Group | Angle | Unit of analysis | Distinctive task |
|---|---|---|---|
| **G01** | A — Compute & energy | country × year | Price levels, components and trajectories |
| **G02** | A — Compute & energy | country × sector × year | Industrial energy demand and intensity |
| **G03** | B — Work & skills | occupation × country | Task-based exposure, cross-section |
| **G04** | B — Work & skills | sector × country × year | Employment and earnings panel |
| **G05** | C — AI adoption | country × year × indicator | Adoption levels, barriers, trajectories |
| **G06** | C — AI adoption | country × sector × size class | Who adopts, and where the gradient is steepest |
| **G07** | D — Trade & dependence | reporter × partner × year | Bilateral concentration and direction of travel |
| **G08** | D — Trade & dependence | product × year × reporter | Product-level single-source exposure |
| **G09** | E — Policy language | institution × time (central banks) | Attention series from monetary communication |
| **G10** | E — Policy language | country × document (EUR-Lex, strategies) | Cross-national regulatory language |

**The pairing is a feature.** When G01 and G02 reach different conclusions about the same angle, at
least one of three things is true: the aggregation level matters substantively, one specification is
wrong, or the effect is not robust. Identifying which is the most valuable thing either group can
report.

---

## 4. The session themes

| # | Method taught | **Theme of the session** |
|---|---|---|
| 02 | OLS geometry, FWL | **How much of the measured gap is real, and how much is composition?** |
| 03 | Inference, robust SEs, OVB | **Which of these differences would survive a referee?** |
| 04 | Bias–variance, cross-validation | **Are we predicting, or only describing the past?** |
| 05 | Ridge, lasso, elastic net | **Of two hundred indicators, which few actually carry the signal?** |
| 06 | Logistic and penalised logistic | **Can we flag a country or sector falling behind one year ahead — and what does a false alarm cost?** |
| 07 | Trees, forests, boosting | **Is the relationship non-linear — and can you still explain it to a minister?** |
| 08 | PCA and factor models | **How many independent things are we actually measuring?** |
| 09 | Clustering and text as data | **Do European countries fall into types — and does the language of policy track them?** |
| 10 | Double machine learning | **Did the policy do anything, or did we just measure the countries that were already ahead?** |
| 11 | Forecasting, drift, governance | **If this were a monitoring dashboard for a European agency, would you sign it?** |

Session 01 has no mandate work — it establishes the environment and the *Europe 2031* framing.
Session 12 is the final presentation of accumulated work.

**Two sessions carry a designed collective payoff.** In **Session 08**, each angle extracts factors
from its own columns; the class then pools the five leading factors and asks whether *those* are
independent. That is a direct empirical test of the scenario's premise that compute is the dominant
measure of capability. In **Session 09**, each angle clusters its countries and the class compares
memberships across angles using the adjusted Rand index — do energy types match labour types match
trade types?

---

## 5. What each angle does, session by session

> Read the row for your angle. The **theme** is the same for everyone; the **execution** is yours.

### Session 02 — *How much of the gap is composition?*

Everyone regresses their headline indicator on structural controls and uses Frisch–Waugh–Lovell to
isolate what survives.

| Angle | Outcome | Partial out | The question |
|---|---|---|---|
| A | Industrial electricity price | generation mix, consumption band, tax component | Is there a residual price gap after structure? |
| B | Employment share of exposed occupations | sector composition, education distribution | Is exposure just industry mix? |
| C | AI adoption rate | firm-size distribution, sector mix, GDP per capita | Is the adoption gap a composition artefact? |
| D | Import share from top partner | total trade volume, GDP, distance | Is concentration just gravity? |
| E | AI-term frequency | document length, institution, year | Is attention rising, or is output rising? |

### Session 03 — *Would it survive a referee?*

Same specifications; now robust and clustered standard errors, a variance-inflation check, and a
signed omitted-variable argument. Every group must name the level at which it clusters and defend it.

### Session 04 — *Predicting or describing?*

Build the cross-validation harness that matches your data's dependence structure — `GroupKFold` by
country for cross-sections, rolling-origin for time series, both for panels. Then hunt your own
leakage. Report in-sample versus honest out-of-sample performance and the size of the gap.

### Session 05 — *Which few indicators carry the signal?*

Throw the full column family at elastic net. Report $\lambda_{\min}$ and $\lambda_{1se}$, and run
the bootstrap stability analysis. **Collective payoff:** five stability plots side by side reveal
whether robustness is a property of the method or of the data domain.

### Session 06 — *Can we flag it a year ahead?*

Each angle defines a binary "falling behind" label appropriate to its data — bottom-quartile growth,
a price-spike event, an adoption stall, a concentration threshold crossing, an attention surge —
and predicts it one period ahead. Then the decision analysis: what does a false alarm cost a
European agency relative to a missed signal, and what threshold follows?

### Session 07 — *Non-linear, and still explainable?*

Random forest and gradient boosting against your Session 05 elastic net on **identical folds**.
Then PDP, ICE and SHAP. The deliverable question is not which model wins but whether the gain
justifies what you give up.

### Session 08 — *How many things are happening?*

Extract factors from your own columns; report the Bai–Ng criteria; label your leading factor and
then argue against your own label. **Then the collective step:** the five leading factors are pooled
and the class examines their correlation structure. If they collapse to one dimension, the
scenario's compute-centrism gains support. If they do not, it loses some.

### Session 09 — *Types, and does language track them?*

Angles A–D cluster their countries; Angle E builds the text indices. The class then compares cluster
memberships pairwise with the adjusted Rand index. Angle E asks whether policy language sorts
countries the same way their economies do.

### Session 10 — *Did the policy do anything?*

Each angle nominates a plausible treatment with a date, and runs DML with its columns as controls.

| Angle | Candidate treatment |
|---|---|
| A | A national energy price intervention or capacity-market reform |
| B | A national training/reskilling programme or minimum-wage change |
| C | Adoption of a national AI strategy; Digital Europe funding |
| D | An export control or investment-screening measure |
| E | Entry into force of an EU regulatory instrument |

**Expected outcome:** most groups will find that identification fails or that the estimate is too
imprecise to act on. Demonstrating that clearly, with the overlap diagnostic and a named unmeasured
confounder, is a full-credit answer. A confident causal claim from observational data with weak
overlap is not.

### Session 11 — *Would you sign it?*

Backtest properly (purge and embargo where features are windowed), run the Diebold–Mariano test
against a hard benchmark, run the train-versus-deploy shift diagnostic, and complete the
[governance file](11-forecasting-drift-and-governance/02-lab/governance-file-template.md).

---

## 6. The two-minute report

Ten groups × 2 minutes, at the end of every lab. Strictly timed.

**One slide. Three sentences.**

1. **What I did.** *"We regressed X on Y for [unit], partialling out [Z]."*
2. **The number.** One figure or one estimate, with its uncertainty or its benchmark.
3. **The catch.** What surprised you, what you cannot claim, or where your data failed you.

**Rules.**

- No method exposition. Everyone in the room learned the method ninety minutes ago.
- No code, no screenshots of terminals.
- Sentence 3 is the one that earns the two minutes. A group that reports only a result has wasted
  the slot; a group that reports a result *and what would undermine it* has contributed something
  the others can use.
- If your angle could not answer the theme this week, say that in sentence 1 and spend sentences 2
  and 3 on **why**. That is a contribution, not a failure.

**Then five minutes of instructor synthesis:** what did the five angles jointly say about this
week's theme, and where did they contradict each other?

**Lab timing.**

| Minutes | |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + synthesis |

---

## 7. The data spine

### Structure

One panel, assembled once, extended as the semester proceeds. Keys: `geo` (country, ISO-2 /
Eurostat code), `time` (year), and where the angle requires it `nace_r2` (sector), `isco08`
(occupation), `size_emp` (firm size class), `partner` (trade), `doc_id` (text).

```
data/spine/
├── PROVENANCE.md                  what the files are, how built, flags, breaks, checksums
├── MANIFEST.csv                   machine-readable file list
├── dictionaries/G01.md … G10.md   one page per group: every column, unit, range, trap
├── core.parquet                   geo × time — shared by everyone
├── angle_a_country.parquet        G01   country × time
├── angle_a_sector.parquet         G02   country × sector × time
├── angle_b_occupation.parquet     G03   occupation × country × time
├── angle_b_sector.parquet         G04   sector × country × time
├── angle_c_country.parquet        G05   country × time
├── angle_c_sector_size.parquet    G06   country × sector × size class × time
├── angle_d_partner.parquet        G07   reporter × partner × time
├── angle_d_product.parquet        G08   reporter × product × time
├── angle_e_centralbank.parquet    G09   documents
└── angle_e_national.parquet       G10   documents
```

`core.parquet` is shared: every angle joins to it on `(geo, time)`, so outcomes and controls are
common across the class and results are comparable. It also carries `falling_behind_next`, the
Session 06 label.

**Start with your [data dictionary](data/spine/dictionaries/).** Each one documents every column
with its unit, range and missingness, lists the **traps** in that particular file, and gives three
*first look* checks to run before you model anything.

### Building it

```bash
python scripts/verify_sources.py                    # do the dataset codes still resolve?
python scripts/build_spine/build.py                 # fetch, clean, join, write
python scripts/build_spine/make_dictionaries.py     # regenerate the column documentation
```

`build.py` needs outbound access to Eurostat, Comtrade and the ECB, so it runs on the instructor's
machine, once per term. The resulting parquet files are **committed** — a deliberate exception to
the usual rule that data are never committed, made so that labs have zero download friction.

`verify_sources.py` checks every endpoint in this document and prints a pass/fail table. Public
statistical agencies retire and rename dataset codes without notice; run it at the start of each
term, before the build.

> ### ⚠️ What is in the repository right now
>
> **Teaching fixtures**, generated by `scripts/build_spine/make_fixtures.py`. They carry the real
> schema, country and year coverage, observation flags, missingness patterns and structural breaks
> — built from a known latent structure so that every method in the course behaves exactly as it
> would on the genuine sources. The composition effects, the correlated predictors, the confounded
> treatment and the recoverable factor structure are all really there, and were verified.
>
> **No number in them is a fact about Europe.** Running `build.py` replaces them with the real
> thing. See [`PROVENANCE.md`](data/spine/PROVENANCE.md).

### Rules that still apply

- Nothing is downloaded at runtime during a lab.
- Every transformation applied during the build is recorded in `PROVENANCE.md`.
- If you extend your angle with a series of your own, you add it to `PROVENANCE.md` with its source,
  date and licence. This is an ongoing obligation, not a one-off.

---

## 8. Goals and assessment

### What a group should be able to do by Session 12

1. **State a research question and answer it** with a number, an interval, and a named benchmark.
2. **Say what the number does not mean.** Every group's angle has a limit; knowing yours precisely
   is the point.
3. **Show that the result is not an artefact** — of composition, of leakage, of a specification
   choice, of a single sample.
4. **Distinguish what you predicted from what you identified**, and never present the first as the
   second.
5. **Hand the work to a stranger**, who can run it and know when to stop trusting it.

### Weighting

Lab work across Sessions 02–11 is **formative**: it is commented on, not marked. The graded
submission is presented in Session 12 and draws on the accumulated work.

| Component | Weight |
|---|---|
| Model governance file | 30% |
| Reproducible analysis | 30% |
| Revised Session 1 memo and change log | 20% |
| Presentation and defence | 20% |

Full detail and rubric: [Session 12](12-group-presentations/README.md).

### What earns credit that students often do not expect

- A clearly demonstrated **negative result**.
- A specification that **fails robustly**, with the reason identified.
- Catching your **local LLM** in an error and documenting how you established it — required in every
  deliverable.
- Reporting that your **angle could not answer** the session theme, with the reason.
- Disagreeing with your **paired group** and diagnosing the source of the disagreement.

### The standard

> When you report a number, be able to say in one sentence where it came from and what would
> falsify it.

That is the whole course. The mathematics is in service of it.

---

*Related: [course overview](README.md) · [Europe 2031 reading
brief](01-foundations-scenarios-and-tools/00-pre-session/reading-europe-2031.md) · [Session
12](12-group-presentations/README.md)*
