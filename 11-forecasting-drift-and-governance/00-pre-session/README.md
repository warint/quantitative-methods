# Session 11 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## Step 1 — Reading

**Mitchell et al. (2019), 'Model Cards for Model Reporting', FAccT**  
Source: https://doi.org/10.1145/3287560.3287596  
*Why:* The documentation template you will complete for your final project.

**Diebold & Mariano (1995), 'Comparing Predictive Accuracy', JBES 13(3)**  
Source: https://doi.org/10.1080/07350015.1995.10524599  
*Why:* The test that turns 'lower RMSE' into a statement you can defend.

**Your own Session 1 memo**  
Source: `../01-foundations-scenarios-and-tools/02-lab/submissions/`  
*Why:* You revise it for the Session 12 deliverable. Re-read it now, before the governance material.


---

## Step 2 — Concepts to review

This session closes the methodological loop and sets up your final deliverable.

In Session 1 you were asked to turn a narrative assumption into a measurable indicator, and most of
you found it harder than expected. You now have ten sessions of machinery: you can estimate a
relationship (2-3), avoid fooling yourself about it (4), handle more predictors than observations
(5-6), classify and set a decision threshold from costs (6), capture non-linearity and explain it
(7), extract latent structure from many series (8), measure constructs that exist only as text (9),
and estimate an effect you could act on (10).

**Bring two things to class:** your Session 1 memo, and a working draft of your final-project
analysis. The second half of this session is a workshop on both.

---

## Step 3 — Your data this week

Your data are **already cleaned and cached**. There is nothing to download.

| Group | Angle | Your file | Unit | Columns |
|---|---|---|---|---|
| **G01** | A | `angle_a_country.parquet` | country × time | [dictionary](../../data/spine/dictionaries/G01.md) |
| **G02** | A | `angle_a_sector.parquet` | country × sector × time | [dictionary](../../data/spine/dictionaries/G02.md) |
| **G03** | B | `angle_b_occupation.parquet` | occupation × country × time | [dictionary](../../data/spine/dictionaries/G03.md) |
| **G04** | B | `angle_b_sector.parquet` | sector × country × time | [dictionary](../../data/spine/dictionaries/G04.md) |
| **G05** | C | `angle_c_country.parquet` | country × time | [dictionary](../../data/spine/dictionaries/G05.md) |
| **G06** | C | `angle_c_sector_size.parquet` | country × sector × size × time | [dictionary](../../data/spine/dictionaries/G06.md) |
| **G07** | D | `angle_d_partner.parquet` | reporter × partner × time | [dictionary](../../data/spine/dictionaries/G07.md) |
| **G08** | D | `angle_d_product.parquet` | reporter × product × time | [dictionary](../../data/spine/dictionaries/G08.md) |
| **G09** | E | `angle_e_centralbank.parquet` | document | [dictionary](../../data/spine/dictionaries/G09.md) |
| **G10** | E | `angle_e_national.parquet` | document | [dictionary](../../data/spine/dictionaries/G10.md) |

```python
import pandas as pd
core = pd.read_parquet("data/spine/core.parquet")
mine = pd.read_parquet("data/spine/<your file>.parquet")
df   = mine.merge(core, on=["geo", "time"], how="left")   # not for angle E
```

**Before class:** Bring a working draft of your final analysis. This lab is a workshop on it, not a new exercise, and groups arriving without one will spend the session catching up.

> Read your [data dictionary](../../data/spine/dictionaries/) first. Its **Traps** section lists
> the things that have cost somebody a week, and its **First look** items take ten minutes. Knowing
> that a series is survey-based, breaks in 2021, or is structurally absent before a given year is
> part of your answer — not a footnote.
>
> ⚠️ The spine currently holds **teaching fixtures**: real schema, real coverage, real flags and
> real pathologies, generated from a known structure. Every method behaves as it would on the
> genuine sources, but no number in them is a fact about Europe. See
> [`PROVENANCE.md`](../../data/spine/PROVENANCE.md).

<details>
<summary>Teaching dataset for the method exercise (optional)</summary>

**Your group's own final-project data**

Source: Chosen by Session 10 and approved by the instructor


Final projects use a dataset of the group's choosing, subject to two constraints: it
must be publicly reproducible, and it must be relevant to a question posed or implied by
*Europe 2031*.

If your project is time-dependent, you will also want a **real-time vintage** source
(ALFRED, or the Philadelphia Fed's real-time dataset) — see section 11.1 on why.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your project**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. Why can a model with excellent backtest performance fail immediately in deployment, even with no coding error?
2. Distinguish covariate shift ($P(X)$ changes) from concept drift ($P(Y|X)$ changes). Which does retraining fix?
3. What is the minimum information another analyst needs to reproduce your result in three years?
4. Name one method from this course you would *not* use for a policy decision, and say why.

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Design a monitoring plan for a model that forecasts regional unemployment quarterly. What do I track, and what triggers a review?"
- "Review my backtest for look-ahead bias. Be specific about which line leaks: <paste>"
- "Explain when the Diebold-Mariano test is invalid, and what to use instead."
- "Read my governance file's Limitations section and tell me what a regulator would say is missing."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 11](../README.md)
