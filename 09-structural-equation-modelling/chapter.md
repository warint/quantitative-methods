---
title: "Structural Equation Modelling"
standalone: true
---

## Measuring what cannot be observed

Some of the most important quantities in international business are not
measured, because they cannot be. *Absorptive capacity*, *institutional
quality*, *brand strength*, *digital maturity* — each is meant to be a real
property of a firm or a country, each is invoked in explanations, and none of
them appears in any dataset. What appears instead is a set of indicators, each a
noisy and partial reflection of the thing.

Chapter 7 met this and handled it descriptively: factor analysis found a small
number of common factors behind a battery of correlated items. This chapter
takes the same idea and makes it a model you can *state and test* — a set of
explicit claims about which indicators measure which construct, and about how the
constructs relate to one another.

The apparatus divides into two parts, and keeping them apart is the first thing
to learn.

::: {.definition}
[**Measurement model**]{.term} — the part that links unobserved constructs to
observed indicators. It answers: *does this battery of questions measure one
thing, and how well does each item measure it?* Its coefficients are loadings.
:::

::: {.definition}
[**Structural model**]{.term} — the part that links constructs to each other. It
answers: *does this construct predict that one?* Its coefficients are path
coefficients, and they are regression coefficients between quantities that were
never observed.
:::

A model can have both, and much of what makes SEM valuable is estimating them
jointly: the structural relationships are corrected for the unreliability of the
measurement, which a two-step approach of "build a scale, then regress it" does
not do.

::: {.muted}
No portrait accompanies this chapter. The natural figure is Charles Spearman,
whose 1904 argument for a general factor began the tradition; the only
photograph of him on Wikimedia Commons is licensed CC BY-SA 4.0 rather than
released into the public domain, so the plate builder refuses it. The rule is a
real portrait, freely licensed, or none.
:::

## Wright's diagrams, and what a path meant

::: {.archive}
[From the archive · Wright, 1918–1934]{.archive-label}

Sewall Wright was a geneticist working on the inheritance of coat colour in
guinea pigs, and he needed to express something regression could not: a system in
which variables cause each other in a specified pattern, some directly and some
through intermediaries. He drew it — variables as boxes, causal claims as
arrows — and worked out the algebra that lets the correlations be decomposed
along the paths [@wright1934].

Two features of that invention survive intact into every SEM package in use
today. The diagram *is* the model: each arrow is a parameter to be estimated,
and an arrow you do not draw is a claim that the effect is zero. And the
implied correlation between any two variables is the sum of the contributions
along every path connecting them, which is what makes the model testable — it
predicts a whole covariance matrix, not a single coefficient.

Wright was explicit that the method could not discover the diagram. It required
the causal structure to be supplied from outside, on subject-matter grounds, and
it then estimated the strengths and checked the implications. Ninety years of
software has not changed that, and the section on equivalent models below is what
happens when it is forgotten.
:::

## Reading a model description

The notation, standard since `lavaan` made it so [@rosseel2012] and used by
`semopy` in Python, is close to readable English:

| operator | means |
|---|---|
| `=~` | *is measured by* — a latent construct and its indicators |
| `~` | *is regressed on* — a structural path |
| `~~` | *covaries with* — an unanalysed association |

So `value =~ price + resale_value + maintenance` asserts that a construct called
*value* exists, that these three observed items are reflections of it, and — by
what is absent — that nothing else in the model measures it.

The corresponding equation for indicator $j$ of construct $\xi$ is

$$
x_j \;=\; \lambda_j \xi + \delta_j ,
$$

with $\lambda_j$ the loading and $\delta_j$ everything specific to that
indicator: its own content, and its measurement error. This is chapter 7's
factor model written one indicator at a time, and the interpretive move is the
same — the construct is what the indicators have in common, and nothing else.

**Identification.** A latent variable has no units, so a scale must be imposed
before anything can be estimated. Two conventions exist: fix one loading to 1,
which gives the construct the units of that indicator, or fix the construct's
variance to 1, which makes it standardised. Software picks the first by default,
which is why one loading in every output has no standard error — it was not
estimated. Reading it as "the strongest indicator" is a common and complete
misunderstanding.

## What is actually being fitted

The model does not fit the data. It fits the *covariance matrix* of the data.

Every parameter set $\theta$ implies a covariance matrix $\Sigma(\theta)$ among
the observed variables, and estimation chooses $\theta$ to make that as close as
possible to the observed $S$. The discrepancy is what all the fit statistics
measure, and the $\chi^2$ test is a formal test of

$$
H_0: \; \Sigma = \Sigma(\theta) ,
$$

that is, of *exact* fit. Its degrees of freedom are the number of distinct
elements in the covariance matrix minus the number of free parameters, which is
why a model can be tested at all: it says more about the covariances than it has
parameters to absorb.

```{python}
#| label: check-measurement
#| code-summary: "Run it: a two-factor measurement model"

import sys, warnings
sys.path.insert(0, "../slides"); sys.path.insert(0, "..")
warnings.filterwarnings("ignore")
from plotstyle import setup, CL
plt = setup()

import numpy as np, pandas as pd, qmib, semopy

survey = qmib.load("efa").select_dtypes("number").dropna()
qmib.view(survey, n=6)

# Two constructs, built from the varimax groupings chapter 7 found.
description = """
value      =~ price + resale_value + maintenance + fuel_efficiency
experience =~ safety + space_comfort + technology + after_sales_service
"""
model = semopy.Model(description)
model.fit(survey)

est = model.inspect(std_est=True)
loadings = est[(est["op"] == "~") & (est["rval"].isin(["value", "experience"]))]
print(f"n = {len(survey)}\n")
print(f"{'construct':12}{'indicator':22}{'loading':>9}{'std':>8}{'p':>10}")
for _, r in loadings.iterrows():
    p = "fixed" if r["p-value"] == "-" else f"{float(r['p-value']):.4f}"
    print(f"{r['rval']:12}{r['lval']:22}{r['Estimate']:9.3f}{r['Est. Std']:8.3f}{p:>10}")
```

## The fit indices, and what each would have to be

The $\chi^2$ test is the only one with a null hypothesis, and it is almost never
used alone, for a reason worth being honest about: with a large sample it rejects
models that are approximately right, and with a small one it fails to reject
models that are badly wrong. It is a test of exact fit, and no model is exactly
right.

The alternatives are *approximate* fit indices, and three are conventionally
reported together.

::: {.definition}
[**CFI**]{.term} — comparative fit index [@bentler1990]. How far the model has
moved from a baseline in which all observed variables are uncorrelated, toward
perfect fit. Scaled to $[0,1]$; **above about 0.95** is the modern convention.
:::

::: {.definition}
[**TLI**]{.term} — Tucker–Lewis index, the same comparison with a penalty for
parameters, so adding a path that does not help can *lower* it. Not bounded
above by 1 in practice. **Above about 0.95.**
:::

::: {.definition}
[**RMSEA**]{.term} — root mean square error of approximation [@browne1992]. The
misfit per degree of freedom, so it rewards parsimony directly. **Below about
0.06** is good, above 0.10 poor, and it comes with a confidence interval that
should be reported with it.
:::

Those thresholds come from a simulation study [@hu1999] that has been cited tens
of thousands of times and whose authors were careful to say they were not
proposing universal cut-offs. They are conventions, and the honest use is to
report the numbers and let the reader apply their own judgement.

```{python}
#| label: check-fit
#| code-summary: "Run it: the fit of the model just estimated"

stats = semopy.calc_stats(model)
get = lambda k: float(stats[k].iloc[0])

print(f"{'index':10}{'value':>10}{'convention':>14}   verdict")
rows = [
    ("chi2",   get("chi2"),   "p > 0.05",  get("chi2 p-value") > 0.05),
    ("CFI",    get("CFI"),    "> 0.95",    get("CFI") > 0.95),
    ("TLI",    get("TLI"),    "> 0.95",    get("TLI") > 0.95),
    ("RMSEA",  get("RMSEA"),  "< 0.06",    get("RMSEA") < 0.06),
]
for name, val, rule, ok in rows:
    print(f"{name:10}{val:10.4f}{rule:>14}   {'pass' if ok else 'FAIL'}")
print(f"\nchi2 p-value {get('chi2 p-value'):.6f} on {int(get('DoF'))} degrees of freedom")
```

Every index fails. That is the useful outcome, and it is worth dwelling on
because published papers rarely show one.

The model was not invented arbitrarily — it was taken from the varimax solution
in chapter 7, which grouped these items in exactly this way. An exploratory
factor analysis suggested a structure; stated as a confirmatory model and tested,
the structure is rejected. That is precisely what the two methods are for, and it
is why running EFA and CFA on the same sample and reporting the confirmation is
circular: the second was fitted to the pattern the first found.

**What to do about a failing model.** Not, in the first instance, to modify it
until it passes. Software offers modification indices — the improvement in
$\chi^2$ from freeing each fixed parameter — and following them is how a
theoretical model becomes an atheoretical one that fits this sample. If you use
them, say so, and treat the result as exploratory.

The disciplined diagnosis starts with the indicators.

```{python}
#| label: check-indicators
#| code-summary: "Run it: which indicators are pulling their weight?"

std = loadings.assign(std=loadings["Est. Std"].astype(float))
std["communality"] = std["std"] ** 2

print(f"{'indicator':22}{'std loading':>13}{'shared var':>12}   assessment")
for _, r in std.sort_values("std").iterrows():
    if r["std"] < 0.4:
        verdict = "weak — consider dropping"
    elif r["std"] < 0.7:
        verdict = "acceptable"
    else:
        verdict = "strong"
    print(f"{r['lval']:22}{r['std']:13.3f}{r['communality']:12.3f}   {verdict}")
```

A standardised loading is the correlation between the indicator and the
construct; its square is the share of the indicator's variance the construct
explains. Below about 0.4 the item has little to do with the thing it is
supposed to measure, and keeping it degrades the construct rather than enriching
it. Here `safety` loads at 0.29 — it shares under a tenth of its variance with
the construct it was assigned to, which is a substantive finding about the
questionnaire rather than a technical nuisance.

## Good fit is not evidence that the model is correct

This is the chapter's most important section and the objective most often
recited without being understood.

A model that fits well has demonstrated one thing: the covariances it implies
are close to the covariances observed. It has *not* demonstrated that its causal
structure is right, because **other models — with different, even opposite,
causal claims — can imply exactly the same covariance matrix.** They are called
equivalent models, they exist for almost every model anyone fits, and no amount
of data distinguishes them.

```{python}
#| label: check-equivalent
#| code-summary: "Run it: two opposite causal stories, one fit"

three = survey[["price", "resale_value", "maintenance"]].copy()
three.columns = ["x", "y", "z"]

candidates = {
    "x → y → z": "y ~ x\nz ~ y",
    "z → y → x": "y ~ z\nx ~ y",
}
print(f"{'model':14}{'chi2':>10}{'dof':>6}{'CFI':>9}{'AIC':>10}")
for name, desc in candidates.items():
    m = semopy.Model(desc)
    m.fit(three)
    s = semopy.calc_stats(m)
    print(f"{name:14}{float(s['chi2'].iloc[0]):10.4f}{int(s['DoF'].iloc[0]):6d}"
          f"{float(s['CFI'].iloc[0]):9.4f}{float(s['AIC'].iloc[0]):10.4f}")

print("\nIdentical, to four decimal places, on every index including AIC.")
print("One says price drives resale value drives maintenance cost;")
print("the other says the causation runs the other way. The data are silent.")
```

Identical $\chi^2$, identical degrees of freedom, identical CFI, identical AIC —
for two models asserting opposite causal directions. No fit index can prefer one,
because fit indices measure distance from the observed covariances and both
reproduce them equally.

This is the same structural fact as chapter 7's rotation indeterminacy, in a more
dangerous costume: there, the alternatives were obviously arbitrary and everyone
knew a rotation had been chosen; here, the alternative is a different theory of
how the world works, and the output looks like a result.

The consequence for practice is exact. **The direction of the arrows is an
assumption you supply, and the fit statistics cannot audit it.** What can audit
it is subject knowledge, temporal order — a cause cannot follow its effect — and
design, which is what chapters 10 and 11 are about.

## What SEM does not fix

**It does not make cross-sectional data longitudinal.** Estimating a path from
$A$ to $B$ measured at the same moment identifies a direction only because you
declared one.

**It does not remove confounding.** An omitted common cause of two constructs
biases the path between them exactly as it biases a regression coefficient. The
latent variables absorb measurement error, not confounders.

**It is demanding of sample size.** With a small $n$ the $\chi^2$ test has little
power to reject a wrong model, and the fit indices are themselves unstable — so
"good fit" in a small sample is the weakest possible evidence.

**Comparisons across groups require an extra assumption.** Comparing a construct
between, say, countries presumes it is measured the same way in each. That is
*measurement invariance*, it is testable by fitting the model with loadings
constrained equal across groups, and comparing means without testing it can
manufacture a difference out of a translation [@cheung2002].

## A short review of the literature

::: {.lit}
The method has two ancestors that met in the 1970s. @wright1934 developed path
analysis in genetics, with the diagram as the model and the decomposition of
correlations along paths; @spearman1904 and the factor-analytic tradition
supplied latent variables measured by indicators. @joreskog1971 combined them
into the general covariance-structure model that all current software
implements, and @rosseel2012 gave the modern open-source implementation whose
syntax `semopy` follows in Python.

Assessment of fit is where the applied literature has moved most. @bentler1990
introduced the comparative fit index and @browne1992 the RMSEA, both as responses
to the chi-square test's sensitivity to sample size. @hu1999 proposed the
cut-offs now universally quoted — CFI and TLI above 0.95, RMSEA below 0.06 —
while cautioning against exactly the mechanical application that followed.

@maccallum2000 reviewed a decade of applied practice and found the recurring
faults to be the ones this chapter warns about: models modified until they fit
and then reported as though specified in advance, equivalent models never
considered, and causal language attached to cross-sectional designs.
@cheung2002 supplies the invariance testing that any cross-group comparison
requires and most omit.
:::

## What to report

1. **The model, as a diagram or as its description.** Every arrow is a claim; a
   reader cannot evaluate claims they cannot see.
2. **How the latent scale was set** — a fixed loading or a fixed variance — so
   nobody misreads the parameter without a standard error.
3. **Standardised loadings for every indicator**, not only the significant ones,
   and what you did about weak items. Dropping an indicator after seeing its
   loading is a data-dependent decision; say so.
4. **The chi-square with its degrees of freedom and p-value**, alongside CFI, TLI
   and RMSEA with its confidence interval. Reporting only the indices that pass
   is the single most common failure.
5. **Whether the model was modified after fitting**, and on what grounds. A model
   reached through modification indices is exploratory whatever its fit.
6. **At least one equivalent model, named.** If you cannot think of one, that is
   a reason to look harder rather than evidence there is none.
7. **What the arrows do not license.** Direction was assumed, not discovered.
   With cross-sectional data the model estimates the strength of a relationship
   under a causal structure you supplied, and a good fit is consistent with that
   structure being wrong.
