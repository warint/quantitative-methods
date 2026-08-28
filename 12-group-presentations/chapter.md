---
title: "Conclusion"
standalone: true
---

## One argument, twelve times

The introduction asked when a number about the past can be used to make a claim
about the future, and said that every method in this book is an answer to some
version of that question, each with conditions attached. Eleven chapters later
the conditions are the thing worth collecting, because the methods will be
looked up again and the conditions will not.

The single sentence the book has been making is this: **a quantitative result is
an argument, and the arithmetic is only its smallest part.** What makes a number
worth acting on is the case that can be made for the conditions under which it
means what it appears to mean — and that case is constructed by the analyst, not
computed by the software.

Five things recurred often enough to be worth naming as the book's actual
content.

## The arithmetic never refuses

Chapter 3 put it first because everything else depends on it. The normal
equations return coefficients for any numbers you feed them. Logistic regression
converges on separated data by running its coefficients to infinity, and reports
a large number rather than an error. Nearest neighbours predicts confidently
outside the range of its training data. A structural equation model fits the
covariance matrix implied by an entirely wrong causal diagram.

None of these failures announces itself. A misspecified model does not raise an
exception; it returns four decimal places in the same typeface as a correct one.
This is the reason diagnostics exist as a discipline rather than a formality, and
the reason the phrase "the model says" is never a complete sentence.

## The same data answer differently depending on what you ask

Chapter 6 is the clearest case. One dataset, one pair of variables, three
defensible specifications, and estimates spanning a factor of four — 1,111
pooled, 275 with country effects, 1,149 with country and year effects. Each was
correct for the question its identifying variation could answer, and a reader
shown any one alone would draw a different conclusion.

The same pattern appeared everywhere once the book started looking. Chapter 2's
slope fell 26% when two controls were added, because "controlling for" is
literally a residual regression. Chapter 10's estimate ran from +6.07 to +2.68
depending on whether selection was addressed. Chapter 7's first component
explained 97.5% of the variance or 47%, depending only on whether the columns had
been standardised.

The lesson is not that results are arbitrary. It is that **a coefficient is
meaningless without the specification that produced it**, and reporting one
without the other is reporting half a result.

## Fit does not identify structure

Chapter 7 showed that a factor solution and its rotation fit identically to eight
decimal places while telling different stories. Chapter 9 showed two structural
models with opposite causal arrows returning identical $\chi^2$, identical
degrees of freedom, identical CFI and identical AIC. Chapter 3 showed four
datasets sharing every summary statistic and differing completely.

In each case the data were silent between the alternatives, and the choice was
made by the analyst on grounds outside the data. That is not a defect to be
engineered away. It is the permanent condition of empirical work, and the honest
response is to name the alternative you rejected and say why — which is a
different activity from reporting a fit index.

## Flexibility is a purchase, not a virtue

Chapter 5 introduced a deliberately biased estimator and showed it beating the
unbiased one, because unbiasedness is worth nothing if the variance is large
enough. Chapter 8 made the trade explicit and then measured it: squared bias,
variance and irreducible error summing to the test error at every setting of $k$,
with a minimum somewhere in the middle.

Then chapter 8 spent its own method's budget and reported the bill. Nearest
neighbours on real data scored an AUC of 0.51 — a coin flip — where logistic
regression, the rigid method with the strong assumption, reached 0.68. The
flexibility did not earn its keep, and on accuracy alone the comparison would
have shown all methods identical and concluded that nothing worked.

**Complexity has to be justified against a simpler alternative that was actually
fitted.** Not against an imagined one.

## Selection is the problem, and it is not a technicality

The last two chapters were about the gap between an association and an effect,
and the size of that gap is worth remembering as a number rather than a warning.
In chapter 10 the naive comparison overstated a known effect of +2.4 percentage
points by more than 150%, because the countries that adopted the policy were
already different. Nothing in the fit statistics of that naive comparison would
have suggested a problem.

That gap is the reason for the whole apparatus of matching, balance diagnostics,
parallel trends and event studies — none of which removes the need for an
argument about *why* treatment arrived where it did.

## What the book checked, and what it could not

Something unusual was possible here. Because the course data are fixtures
generated from a known structure, several claims could be *verified* rather than
asserted, which is the form of evidence this book has been arguing for
throughout.

```{python}
#| label: check-closing
#| code-summary: "Run it: three identities, re-checked"

import sys, warnings
sys.path.insert(0, "../slides"); sys.path.insert(0, "..")
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, statsmodels.api as sm, qmib

core = qmib.load("core").dropna(
    subset=["gdp_pc_eur", "productivity_idx", "employment_ths", "population"])
y = core["gdp_pc_eur"]

# 1. Pythagoras — chapter 2. The residual is orthogonal to the fit, so the
#    sums of squares add exactly.
fit = sm.OLS(y, sm.add_constant(core[["productivity_idx"]])).fit()
tss = ((y - y.mean()) ** 2).sum()
ess = ((fit.fittedvalues - y.mean()) ** 2).sum()
rss = (fit.resid ** 2).sum()

# 2. Frisch-Waugh-Lovell — chapter 2. "Controlling for" is residual regression.
others = sm.add_constant(core[["employment_ths", "population"]])
multi = sm.OLS(y, sm.add_constant(
    core[["productivity_idx", "employment_ths", "population"]])).fit()
fwl = sm.OLS(sm.OLS(y, others).fit().resid,
             sm.OLS(core["productivity_idx"], others).fit().resid).fit()

# 3. Leverage — chapter 3. The hat matrix diagonal sums to the number of
#    parameters, always, for every regression ever fitted.
X = sm.add_constant(core[["productivity_idx"]]).to_numpy()
h = np.einsum("ij,jk,ik->i", X, np.linalg.inv(X.T @ X), X)

print(f"{'identity':44}{'discrepancy':>14}")
print(f"{'TSS - (ESS + RSS)':44}{tss - ess - rss:14.3e}")
print(f"{'multiple regression - FWL residual slope':44}"
      f"{abs(multi.params['productivity_idx'] - fwl.params.iloc[0]):14.3e}")
print(f"{'sum of leverages - p':44}{abs(h.sum() - X.shape[1]):14.3e}")
print("\nThese are not approximations that happened to work on this dataset.")
print("They are algebraic identities, and they hold for every regression.")
```

Those hold exactly. Other things the book checked did not, and the failures were
more instructive than the successes: the lasso retained three pure-noise columns
out of ten after cross-validated selection; regression adjustment on proxy
covariates left 0.7 percentage points of bias; a measurement model taken from an
exploratory factor solution failed every fit index; and a post-treatment control
moved an estimate *closer* to the truth while being methodologically wrong.

That last one is the book's most useful result. **Being closer to the right
answer is not the same as using the right method**, and outside a textbook you
never learn which one you had.

## What is not here

A book of twelve chapters leaves out more than it contains, and knowing the shape
of the gap matters when you meet a problem this book did not prepare you for.

**Time series proper.** The panels here are short and wide. Long series bring
autocorrelation structure, unit roots, cointegration and forecasting — a
substantial field that chapter 6's clustering only gestures at.

**Bayesian inference.** Everything here is frequentist. The Bayesian treatment
answers a different question — the probability of a parameter given the data,
rather than of the data given a parameter — and is often the more natural framing
for the decision problems in this book's examples.

**Modern machine learning at scale.** Gradient boosting, random forests and
neural networks are absent. Chapter 8's bias–variance framework is the right
foundation for all of them, and chapter 5's regularisation is the mechanism they
use, but the methods themselves and their tooling are a course of their own.

**Text, networks and unstructured data.** The introduction cited work measuring
policy uncertainty from newspaper archives and productive capability from export
composition. Constructing quantities from unstructured sources is where much of
the growth in this field is, and it is not covered here.

**Causal machine learning.** Double machine learning, causal forests and the
literature that lets flexible methods estimate treatment effects sit exactly at
the junction of chapters 5, 8 and 10, and are the natural next thing to read.

## What to carry

Six habits, which will outlast every technique in this book.

1. **Look at the data before modelling it.** Nearly every analysis that goes
   wrong went wrong before the model was fitted.
2. **Say the units.** A coefficient without units cannot be checked against
   anything a reader knows, and checking against what you already know is the
   fastest way to catch an implausible result.
3. **Report the uncertainty, and say what kind.** Classical, robust, clustered —
   they differed by more than a factor of two on one coefficient in chapter 6.
4. **Name the assumption that identifies the estimate**, and say whether it is
   testable. Most of the important ones are not, which is exactly why they must
   be argued rather than assumed.
5. **Fit the simpler thing too.** Complexity should have to beat something.
6. **Say what the result does not license.** Every chapter here ends with that
   section because it is the part that distinguishes analysis from assertion with
   numbers attached.

And the one that subsumes them: **a well-argued refusal is a complete result.**
"This cannot be claimed from these data, and here is what would be needed" is
often the most valuable output of a serious analysis, and it is the answer that
takes the most expertise to produce.

## Where the work goes now

The methods in this book are ordinary. What is not ordinary — and what the
introduction argued the field is short of — is the judgement to know which
question a given number can answer, and the discipline to say so when it cannot.
Language models have made the arithmetic and the code effectively free. They have
not made that judgement free, and there is no sign that they will.

That is the argument for learning to derive a method before using it. Not because
the derivation will be needed at the keyboard, but because it is what lets you
notice that the answer on the screen cannot be right.
