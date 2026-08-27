## The line, and where it came from

Adrien-Marie Legendre published the method of least squares in 1805, in an
appendix to a book about the orbits of comets. Four years later Carl Friedrich
Gauss published it too, in *Theoria Motus*, and added that he had been using it
since 1795. The priority quarrel that followed was bitter and is still not
entirely settled. What matters here is what Gauss added that Legendre did not
have: not the recipe, but the *justification*. Legendre offered least squares as
a sensible way to reconcile discordant observations. Gauss asked a different
question — under what conditions is this the best you can do? — and that
question is the subject of this chapter.

{{portrait}}

Set the problem up. You have $n$ observations, a response $y$, and a matrix $X$
holding a column of ones and $p-1$ predictors. You want coefficients $\beta$
such that $X\beta$ is close to $y$. Least squares defines "close" as the sum of
squared vertical distances, and chooses

$$
\hat\beta \;=\; \arg\min_{\beta} \; \lVert y - X\beta \rVert^2 .
$$

Differentiate, set to zero, and you get the *normal equations* $X^{\top}X\beta =
X^{\top}y$, whose solution — whenever $X^{\top}X$ can be inverted — is

$$
\hat\beta \;=\; (X^{\top}X)^{-1} X^{\top} y .
$$

That is an algebraic fact. It requires no assumption about the world, no
probability, no error term. Feed it any numbers and it returns coefficients.
This is exactly why diagnostics are necessary: **the formula never refuses.**
It has no way to tell you that the relationship is curved, that one country is
dragging the whole line, or that the standard errors it reports are fiction.
It returns the same confident four decimal places either way.

The statistical content arrives only when you attach a model,

$$
y \;=\; X\beta + \varepsilon ,
$$

and make claims about $\varepsilon$. The Gauss–Markov theorem says that if the
model is correctly specified, if $\operatorname{E}[\varepsilon \mid X] = 0$, and
if the errors have constant variance and are mutually uncorrelated, then
$\hat\beta$ is the Best Linear Unbiased Estimator: no other estimator that is
both linear in $y$ and unbiased has smaller variance. Note what is *not* on that
list. Normality is not required for Gauss–Markov. It is required for something
else — the exactness of the $t$ and $F$ distributions in small samples — and
confusing the two is one of the most common errors in applied work.

The word "regression" itself arrived later and by accident. Francis Galton,
studying the heights of parents and children, found that tall parents had
children who were tall but *less* tall, and called this "regression towards
mediocrity" [@galton1886]. He was naming a substantive biological phenomenon.
The name stuck to the statistical method he had used to find it, which is why a
technique for fitting conditional means is called by a word that means moving
backwards.

## Adequacy, validity, robustness

These three words get used loosely and they are not synonyms. The distinction
organises everything that follows.

::: {.definition}
[**Adequacy**]{.term} — whether the model describes the data you actually have.
An adequate model leaves residuals with no remaining structure: nothing in what
is left over could have been used to predict $y$ better. Adequacy is assessed
against the sample, and it is mostly a question you answer with plots.
:::

::: {.definition}
[**Validity**]{.term} — whether the inferences you draw from the model are
warranted: whether the standard errors, confidence intervals and $p$-values mean
what they claim. A model can be adequate and its inference invalid, most
commonly because the errors are heteroscedastic or dependent. Validity is a
question about the *sampling distribution*, not about fit.
:::

::: {.definition}
[**Robustness**]{.term} — whether your conclusions survive reasonable changes to
the specification, the sample or the estimator. A robust finding is one that
does not depend on a single influential observation, one functional form, or one
way of computing standard errors. Robustness is a question about *stability*.
:::

A model with $R^2 = 0.95$ can fail all three. This is not a hypothetical:
Anscombe's celebrated four datasets share, to two decimal places, the same
means, variances, correlation, regression line and $R^2$, and they are utterly
different [@anscombe1973].

```{python}
#| label: fig-anscombe
#| echo: false
#| fig-cap: "Anscombe's quartet. Identical means, variances, correlations, fitted lines and $R^2$ — and only the first is a dataset the line describes. Data from @anscombe1973, Table 1."

import sys, warnings
sys.path.insert(0, "../slides"); sys.path.insert(0, "..")
warnings.filterwarnings("ignore")
from plotstyle import setup, CL
plt = setup()
import numpy as np

x1 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
quartet = {
    "I — the line is right":        (x1, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II — the relation is curved":  (x1, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III — one outlier tilts it":   (x1, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV — one point defines it":    ([8]*10 + [19], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 5.56, 7.91, 6.89, 12.50]),
}

fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.4), sharex=True, sharey=True)
for ax, (name, (x, y)) in zip(axes.ravel(), quartet.items()):
    x, y = np.asarray(x, float), np.asarray(y, float)
    b = np.polyfit(x, y, 1)
    gx = np.linspace(2, 20, 50)
    ax.plot(gx, np.polyval(b, gx), color=CL.warn, lw=1.6, zorder=2)
    ax.scatter(x, y, s=36, color=CL.accent, zorder=3, edgecolor="white", linewidth=0.8)
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    ax.set_title(name, fontsize=10, loc="left", color=CL.ink)
    ax.text(0.97, 0.06, f"$R^2={r2:.2f}$", transform=ax.transAxes,
            ha="right", fontsize=9, color=CL.muted)
    ax.set_xlim(2, 20); ax.set_ylim(2, 14)
fig.tight_layout()
```

Every one of those four panels reports $R^2 = 0.67$ and the same fitted line.
Only in the first is that line a description of the data. In the second the
relationship is deterministic and curved — the model is not wrong about the
strength of the association so much as wrong about its *shape*. In the third a
single aberrant point has tilted a line that would otherwise pass almost exactly
through the rest. In the fourth every $x$ but one is identical, so the slope is
determined entirely by one observation: delete it and the slope is undefined.

Anscombe's point was not that summary statistics are useless. It was that they
are *insufficient*, and that the missing information is available for the cost
of a plot.

## What the residual knows

Write $\hat y = X\hat\beta$. Substituting the estimator,

$$
\hat y \;=\; X(X^{\top}X)^{-1}X^{\top} y \;=\; Hy ,
$$

where $H = X(X^{\top}X)^{-1}X^{\top}$ is the *hat matrix* — so named because it
puts the hat on $y$. It is the orthogonal projection onto the column space of
$X$, which gives it two properties worth remembering: it is symmetric
($H = H^{\top}$) and idempotent ($HH = H$). The residual vector is what is left
after the projection,

$$
e \;=\; y - \hat y \;=\; (I - H)\, y .
$$

Now the useful consequence. If $\operatorname{Var}(\varepsilon) = \sigma^2 I$,
then

$$
\operatorname{Var}(e) \;=\; \sigma^{2}(I - H),
\qquad\text{so}\qquad
\operatorname{Var}(e_i) \;=\; \sigma^{2}\,(1 - h_{ii}).
$$

**The residuals do not have constant variance even when the errors do.** An
observation with large $h_{ii}$ has a residual that is squeezed towards zero as
a matter of arithmetic, not because the model fits it well. This is why raw
residuals are the wrong thing to plot, and why every diagnostic below is built
on the *standardised* residual

$$
r_i \;=\; \frac{e_i}{s\sqrt{1 - h_{ii}}},
$$

with $s^2 = e^{\top}e/(n-p)$. Plotting $r_i$ against $\hat y_i$ is the single
most informative diagnostic there is [@anscombe1963]. Under an adequate model
the cloud is structureless: flat, centred on zero, of even width. Curvature
means the functional form is wrong. A widening fan means the variance is not
constant. Both are visible instantly and neither is visible in $R^2$.

```{python}
#| label: fig-diagnostics
#| echo: false
#| fig-cap: "Diagnostics for GDP per capita on the productivity index, the regression Session 02 fitted. Left: standardised residuals against fitted values. Right: the scale–location plot, which makes non-constant variance easier to see by removing the sign."

import pandas as pd, statsmodels.api as sm
import qmib

d = qmib.load("core").dropna(subset=["gdp_pc_eur", "productivity_idx"])
X = sm.add_constant(d["productivity_idx"])
model = sm.OLS(d["gdp_pc_eur"], X).fit()
infl = model.get_influence()
std_resid = infl.resid_studentized_internal
fitted = model.fittedvalues

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9))

ax1.axhline(0, color=CL.muted, lw=1, zorder=1)
ax1.scatter(fitted, std_resid, s=16, color=CL.accent, alpha=0.55,
            edgecolor="none", zorder=3)
lo = pd.Series(std_resid).rolling(45, center=True, min_periods=10).mean()
ax1.plot(np.sort(fitted), lo[np.argsort(fitted)], color=CL.warn, lw=1.8, zorder=4)
ax1.set_xlabel("fitted value"); ax1.set_ylabel("standardised residual")
ax1.set_title("Residuals vs fitted", fontsize=10, loc="left")

ax2.scatter(fitted, np.sqrt(np.abs(std_resid)), s=16, color=CL.accent,
            alpha=0.55, edgecolor="none", zorder=3)
lo2 = pd.Series(np.sqrt(np.abs(std_resid))).rolling(45, center=True, min_periods=10).mean()
ax2.plot(np.sort(fitted), lo2[np.argsort(fitted)], color=CL.warn, lw=1.8, zorder=4)
ax2.set_xlabel("fitted value"); ax2.set_ylabel(r"$\sqrt{|\,r_i\,|}$")
ax2.set_title("Scale–location", fontsize=10, loc="left")

fig.tight_layout()
```

Read @fig-diagnostics the way a referee would. The left panel is not flat: the
smoothed line drifts, which says the straight line is missing curvature in the
relationship between productivity and income. The right panel trends upward,
which says the spread of the residuals grows with the fitted value. Neither
finding is fatal. Both change what you are allowed to say.

## Leverage: which observations *can* move the line

::: {.definition}
[**Leverage**]{.term} — the diagonal element $h_{ii}$ of the hat matrix, equal
to $\partial \hat y_i / \partial y_i$: how much the fitted value at observation
$i$ responds to a change in the observed value at $i$. Leverage is a property of
$X$ alone. It does not involve $y$, so an observation can have high leverage
while fitting perfectly.
:::

Because $H$ is a projection onto a $p$-dimensional space,
$\sum_i h_{ii} = \operatorname{tr}(H) = p$, so the average leverage is exactly
$p/n$ and each $h_{ii}$ lies in $[0, 1]$. The conventional flag is $h_{ii} >
2p/n$ — twice the average — which is a rule of thumb and nothing more
[@hoaglin1978]. In simple regression it has a transparent form,

$$
h_{ii} \;=\; \frac{1}{n} + \frac{(x_i - \bar x)^2}{\sum_j (x_j - \bar x)^2},
$$

which says exactly what leverage means: distance from the centre of the
predictor space, in units of the spread of the predictors. The fourth Anscombe
panel is the extreme case — one point at $x = 19$ among ten at $x = 8$ carries
leverage close to 1, and the line has no choice but to pass through it.

Leverage is *potential*. It says an observation is positioned to move the line.
Whether it actually does depends on whether its $y$ is surprising, and that
requires combining leverage with the residual.

## Influence: separating the outlier from the point that matters

::: {.definition}
[**Cook's distance**]{.term} — a measure of how much the entire vector of fitted
values changes when observation $i$ is deleted, scaled so that it is comparable
across observations and models:
$$
D_i \;=\; \frac{(\hat y - \hat y_{(i)})^{\top}(\hat y - \hat y_{(i)})}{p\,s^2}
\;=\; \frac{r_i^{2}}{p}\cdot\frac{h_{ii}}{1 - h_{ii}} .
$$
:::

The second form is the one to internalise [@cook1977]. Cook's distance is a
product of two things: how badly the point is fitted ($r_i^2$) and how much
power it has to pull ($h_{ii}/(1-h_{ii})$). Either factor alone is harmless.

- **High residual, low leverage** — an outlier sitting in the middle of the
  predictor range. It inflates $s$ and hurts your standard errors, but it barely
  moves $\hat\beta$, because it has no lever to pull on.
- **Low residual, high leverage** — a point far out in $X$ that the line happens
  to pass through. It is *supporting* your slope rather than distorting it, but
  your slope now depends on it, which is a robustness problem even though no
  diagnostic will flag it as misfit.
- **High on both** — the case that changes conclusions. This is what Cook's
  distance is built to find.

Common cutoffs are $D_i > 1$ or $D_i > 4/n$; both are conventions, and
[@belsley1980] is properly sceptical of treating any of them as a test. The
useful discipline is not the threshold. It is that you *look*, you *name* the
observations that stand out, and you say what happens to your conclusion with
and without them. Deleting an influential point silently is misconduct.
Reporting that Luxembourg is influential, and that your slope falls by a third
without it, is a finding.

```{python}
#| label: fig-influence
#| echo: false
#| fig-cap: "Left: the influence plot for the fitted regression — standardised residual against leverage, point area proportional to Cook's distance, dashed contours at $D=4/n$. Right: the same data with a single observation moved to a high-leverage position, to show what influence looks like when it is present. The right panel is a constructed illustration, not a feature of the data."

lev = infl.hat_matrix_diag
cooks = infl.cooks_distance[0]
n, p = int(model.nobs), int(model.df_model) + 1
thresh = 4 / n

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.2, 4.0))

def influence_panel(ax, lev, resid, cooks, title, hi=None):
    ax.axhline(0, color=CL.muted, lw=1)
    size = 18 + 900 * np.clip(cooks, 0, None)
    ax.scatter(lev, resid, s=size, color=CL.accent, alpha=0.45,
               edgecolor="white", linewidth=0.6, zorder=3)
    gl = np.linspace(max(lev.min(), 1e-4), lev.max() * 1.05, 200)
    for sign in (1, -1):
        ax.plot(gl, sign * np.sqrt(thresh * p * (1 - gl) / gl),
                ls="--", lw=1.1, color=CL.warn, zorder=2)
    if hi is not None:
        ax.scatter([lev[hi]], [resid[hi]], s=90, facecolor="none",
                   edgecolor=CL.warn, linewidth=1.8, zorder=5)
    ax.set_xlabel("leverage $h_{ii}$"); ax.set_ylabel("standardised residual")
    ax.set_title(title, fontsize=10, loc="left")
    ax.set_xlim(left=0)

influence_panel(axL, lev, std_resid, cooks, f"As fitted — max $D_i$ = {cooks.max():.3f}")

d2 = d.copy().reset_index(drop=True)
j = int(d2["productivity_idx"].idxmax())
d2.loc[j, "productivity_idx"] = d2["productivity_idx"].max() * 2.1
d2.loc[j, "gdp_pc_eur"] = d2["gdp_pc_eur"].min()
m2 = sm.OLS(d2["gdp_pc_eur"], sm.add_constant(d2["productivity_idx"])).fit()
i2 = m2.get_influence()
influence_panel(axR, i2.hat_matrix_diag, i2.resid_studentized_internal,
                i2.cooks_distance[0],
                f"One point moved — max $D_i$ = {i2.cooks_distance[0].max():.2f}", hi=j)

fig.tight_layout()
```

The left panel of @fig-influence is what a clean diagnostic looks like: maximum
Cook's distance around 0.04, every point comfortably inside the contours, no
single observation carrying the result. That is a reportable finding in its own
right, and it is worth saying explicitly rather than leaving as an absence. The
right panel moves one observation to a position of high leverage and poor fit;
its Cook's distance jumps by two orders of magnitude and the fitted slope moves
with it. Nothing about $R^2$ warns you which panel you are in.

## When the variance is not constant

Heteroscedasticity is the failure most often misdiagnosed, so be precise about
what it costs. Under heteroscedasticity, $\hat\beta$ remains **unbiased** and
**consistent**. The coefficients are not wrong. What breaks is
$\operatorname{Var}(\hat\beta)$: the usual formula $s^2 (X^{\top}X)^{-1}$ is no
longer the right one, so the standard errors, the $t$ statistics, the
confidence intervals and the $p$-values are all computed from a formula that
does not apply. You have the right answer with the wrong uncertainty attached to
it — which, if the question is whether an effect is distinguishable from zero,
is the part that matters.

The formal test regresses the squared residuals on the predictors and asks
whether they explain anything [@breusch1979]. It is worth running, but the
scale–location plot usually tells you first, and the test has the usual
weakness of all diagnostic tests: with $n = 428$ it will reject on
heteroscedasticity too mild to matter, and with $n = 30$ it will fail to reject
heteroscedasticity severe enough to invalidate everything.

The modern response is not to fix the variance but to stop relying on the
assumption. White's heteroscedasticity-consistent estimator replaces the
misapplied middle of the sandwich with the squared residuals themselves
[@white1980]:

$$
\widehat{\operatorname{Var}}(\hat\beta)
= (X^{\top}X)^{-1}
\Big(\textstyle\sum_i e_i^2 \, x_i x_i^{\top}\Big)
(X^{\top}X)^{-1}.
$$

This is consistent whatever the pattern of the variance, without your having to
model that pattern. Its small-sample behaviour is poor, however, which motivated
the corrected variants HC1, HC2 and HC3 [@mackinnon1985]. The practical
recommendation is settled and worth memorising: **use HC3 by default**, and
certainly whenever $n < 250$ [@long2000]. In `statsmodels` that is
`fit(cov_type="HC3")`, a single argument, and there is no good reason to omit
it.

Non-constant variance is not the only specification failure worth a test. The
RESET procedure adds powers of the fitted values back into the regression and
tests whether they matter [@ramsey1969]; if $\hat y^2$ has explanatory power,
some non-linearity you have not modelled remains.

## Comparing models: what AIC is, and what it is not

Having diagnosed a problem, you will usually fit an alternative — a quadratic
term, a log transform, an extra control. You now need a basis for preferring
one. $R^2$ cannot supply it, because adding any variable, however irrelevant,
cannot decrease $R^2$.

Akaike's criterion comes at it from prediction rather than fit. It estimates the
expected Kullback–Leibler divergence between the fitted model and the process
that generated the data, and reduces to

$$
\mathrm{AIC} \;=\; -2 \log \hat{L} + 2k
$$

for a model with $k$ estimated parameters and maximised likelihood $\hat L$
[@akaike1974]. The first term rewards fit; the second charges two units per
parameter. Lower is better. The Bayesian criterion replaces the penalty with
$k \log n$, which is harsher for any $n > 7$ and is aiming at a different
target — the true model, if one is in the candidate set, rather than the best
predictor [@schwarz1978].

Three cautions, in order of how often they are violated.

First, **AIC is comparative and unitless**. A single AIC value means nothing
whatsoever. Only differences between models fitted to *the same observations*
are interpretable, which means that dropping rows through missing data
invalidates the comparison. As a convention, $\Delta_i = \mathrm{AIC}_i -
\mathrm{AIC}_{\min}$ below about 2 is weak evidence of any difference
[@burnham2004].

Second, **AIC does not check adequacy**. It ranks the candidates you supply. If
every model you supply is misspecified, it will rank them and hand you a winner,
in exactly the confident tone it uses when one of them is right. It is a
comparison, not a diagnostic, and it is not a substitute for the plots.

Third — the one that ends careers — **selecting a model and then reporting its
$p$-values as though the specification were chosen in advance is invalid.**
Freedman demonstrated the size of the problem with pure noise: regress a random
$y$ on 50 random predictors, keep the significant ones, refit, and the second
regression looks impressive [@freedman1983]. Nothing was there. The same
mechanism operates whenever the data guide the specification and the resulting
$p$-values are reported as if they had not — the "garden of forking paths",
which requires no dishonesty at all, only the ordinary practice of looking at
your data before deciding what to fit [@gelman2014]. If you select on AIC, say
so, and treat the resulting inference as exploratory.

## A short review of the literature

::: {.lit}
The diagnostic tradition begins with @anscombe1963, who argued that residuals
should be examined systematically rather than summarised, and set out the plots
still in use. @anscombe1973 made the case unforgettable with four datasets
constructed to share every conventional summary while differing completely — a
demonstration reproduced in @fig-anscombe and in nearly every regression text
since.

The geometry was formalised in the 1970s. @hoaglin1978 gave the hat matrix its
expository treatment and the $2p/n$ convention. @cook1977 introduced the
distance measure that separates outlying from influential observations, and
@belsley1980 assembled the apparatus into a book-length treatment, with a
scepticism about mechanical cutoffs that has aged well.

Robust inference developed in parallel. @white1980 provided a covariance
estimator consistent under arbitrary heteroscedasticity, complementing the
earlier @breusch1979 test. @mackinnon1985 showed White's estimator performs
badly in small samples and proposed corrections; @long2000 evaluated them in
practice and recommended HC3, which is now the applied default. Specification
error more broadly is treated by @ramsey1969.

Model comparison follows @akaike1974 and @schwarz1978, whose criteria differ in
penalty and in target — prediction against identification — a distinction
@burnham2004 makes carefully and much applied work does not. The cost of
ignoring it was quantified early by @freedman1983 and framed for a modern
audience by @gelman2014: inference conditional on a specification chosen from
the data is not the inference the $p$-value describes.

The through-line, from 1963 to now, is a single claim — that a fitted model is a
hypothesis about the data, not a summary of it, and that the residuals are where
that hypothesis is tested.
:::

## What to report

A diagnostic section that earns its place answers four questions in order, and
takes about a page.

1. **Is the functional form right?** Residuals against fitted, with a smoother.
   Say what structure you looked for and whether you found it.
2. **Is the variance constant?** Scale–location. If it is not, report HC3
   standard errors and say that you did — do not quietly switch and leave the
   reader to notice the numbers changed.
3. **Does any observation carry the result?** Leverage against standardised
   residual, sized by Cook's distance. Name the observations that stand out,
   identify them substantively — Luxembourg, Ireland, 2020 — and report the
   coefficient with and without them.
4. **Would a different specification do better?** Compare on AIC over the same
   rows, report $\Delta$, and state plainly whether the specification was chosen
   before or after seeing the data.

The failure mode this chapter exists to prevent is reporting $R^2$ and stopping.
The four datasets in @fig-anscombe all have $R^2 = 0.67$. Three of them should
never be described by a straight line, and no amount of staring at $0.67$ will
tell you which three.
