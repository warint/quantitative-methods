---
title: "K-Nearest Neighbours and the Bias–Variance Trade-off"
standalone: true
---

## A method with no model

Every method so far has assumed a form. Least squares assumes a line, logistic
regression assumes a curve, and the penalties in chapter 5 assume the line is
worth shrinking toward. Each assumption is a claim that can be wrong, and
chapter 3 was about detecting when it is.

Nearest neighbours makes no such claim. To predict for a new observation, find
the $k$ observations in the training data closest to it, and average their
outcomes:

$$
\hat f(x_0) \;=\; \frac{1}{k} \sum_{i \in N_k(x_0)} y_i ,
$$

where $N_k(x_0)$ is the set of the $k$ nearest training points. For a
classification problem, take the majority vote instead. There is no fitting
stage, no coefficient, no optimisation — the training data *is* the model.

This looks like getting something for nothing, and the chapter is about what it
actually costs. The method is not assumption-free; it has simply moved its
assumption. Averaging the neighbours presumes that the function is smooth enough
that points close in $x$ have similar $y$, and it presumes you know what "close"
means. Both presumptions can fail badly, and neither shows up as a diagnostic
plot.

::: {.muted}
No portrait accompanies this chapter. The method is due to Evelyn Fix and
Joseph Hodges, in a 1951 technical report for the US Air Force School of
Aviation Medicine that went unpublished for nearly forty years [@fix1951], and
no freely licensed likeness of either author appears to exist. The convention
this book follows is a real portrait or none.
:::

## The floor nobody beats

Before asking how well a classifier does, ask how well anything could.

::: {.definition}
[**Bayes classifier**]{.term} — the rule that assigns each $x$ to the most
probable class given $x$: predict class $j$ where $\Pr(Y = j \mid X = x)$ is
largest. Its error rate, the *Bayes rate*, is the lowest achievable by any
classifier whatsoever.
:::

The proof is a one-liner: at each $x$, any rule either picks the most probable
class or does not, and picking it minimises the chance of being wrong there.
Integrating over $x$ gives the result.

The Bayes classifier is not a method, because computing it requires
$\Pr(Y \mid X)$ — which is the thing you are trying to estimate. Its value is
conceptual and it is considerable. **A non-zero Bayes rate means that error is
not evidence of a bad model.** If the outcome is genuinely uncertain given the
predictors, no amount of flexibility, data or cleverness removes the remaining
error, and a practitioner who keeps adding complexity to chase it is chasing
noise.

The regression analogue is the irreducible error $\sigma^2$: the variance of
$y$ around $f(x)$, which no estimator of $f$ can touch. It appears explicitly in
the decomposition below.

## Where prediction error comes from

Take a target $y = f(x) + \varepsilon$ with $\operatorname{E}[\varepsilon] = 0$
and $\operatorname{Var}(\varepsilon) = \sigma^2$. Let $\hat f$ be an estimate
built from a random training sample. The expected squared error at a point $x_0$,
averaged over training samples and over the noise in a new observation, splits
into three:

$$
\operatorname{E}\big[(y_0 - \hat f(x_0))^2\big]
\;=\;
\underbrace{\sigma^2}_{\text{irreducible}}
\;+\;
\underbrace{\big(\operatorname{E}[\hat f(x_0)] - f(x_0)\big)^2}_{\text{bias}^2}
\;+\;
\underbrace{\operatorname{Var}\big(\hat f(x_0)\big)}_{\text{variance}} .
$$

Chapter 5 used the last two terms to argue for a biased estimator. Here all three
matter, and the first is the one that makes the others meaningful: because
$\sigma^2 > 0$, the total error has a floor, and the *only* quantity a modeller
controls is how the remaining budget is split between bias and variance.

The words are worth being precise about. **Bias** is how far the method's
*average* prediction is from the truth — an error it makes systematically, in
every sample. **Variance** is how much the prediction moves when the training
sample changes — an error it makes differently each time. A rigid method has high
bias and low variance; a flexible one has the reverse.

For nearest neighbours, $k$ is the dial. Small $k$ averages few points, follows
the data closely, and changes a lot when the data change: low bias, high
variance. Large $k$ averages many points, smooths across regions where the truth
differs, and barely moves between samples: high bias, low variance.

The decomposition is usually presented as algebra and left there. It is
measurable, if you are willing to simulate a world whose truth you know.

```{python}
#| label: fig-bias-variance
#| code-summary: "Show the code"
#| fig-cap: "The decomposition, measured. Four hundred training samples are drawn from a known function; for each $k$ the squared bias and the variance of the prediction are computed across samples. Their sum plus the irreducible error tracks the test error to within 0.002 everywhere."

import sys, warnings
sys.path.insert(0, "../slides"); sys.path.insert(0, "..")
warnings.filterwarnings("ignore")
from plotstyle import setup, CL
plt = setup()

import numpy as np, pandas as pd, qmib
from sklearn.neighbors import KNeighborsRegressor

rng = np.random.default_rng(60033)

def truth_fn(x):
    return np.sin(2 * np.pi * x) + 0.5 * x

SIGMA, N, REPS = 0.35, 120, 400
x_test = np.linspace(0.05, 0.95, 60).reshape(-1, 1)
f_true = truth_fn(x_test.ravel())

ks = [1, 2, 3, 5, 8, 12, 20, 30, 45, 60, 80]
rows = []
for k in ks:
    preds = np.empty((REPS, len(x_test)))
    mses = np.empty(REPS)
    for r in range(REPS):
        xs = rng.uniform(0, 1, N).reshape(-1, 1)
        ys = truth_fn(xs.ravel()) + rng.normal(0, SIGMA, N)
        preds[r] = KNeighborsRegressor(n_neighbors=k).fit(xs, ys).predict(x_test)
        mses[r] = np.mean((f_true + rng.normal(0, SIGMA, len(x_test)) - preds[r]) ** 2)
    rows.append(dict(k=k,
                     bias2=np.mean((preds.mean(0) - f_true) ** 2),
                     var=np.mean(preds.var(0)),
                     mse=mses.mean()))

bv = pd.DataFrame(rows)
bv["total"] = bv.bias2 + bv["var"] + SIGMA ** 2

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(bv.k, bv.bias2, marker="o", ms=4, lw=1.8, color=CL.warn, label="bias$^2$")
ax.plot(bv.k, bv["var"], marker="s", ms=4, lw=1.8, color=CL.accent, label="variance")
ax.axhline(SIGMA ** 2, ls=":", lw=1.4, color=CL.muted, label=r"irreducible $\sigma^2$")
ax.plot(bv.k, bv.total, marker="^", ms=4, lw=2.2, color=CL.ink, label="sum")
ax.plot(bv.k, bv.mse, ls="--", lw=1.4, color=CL.good, label="measured test MSE")
best = bv.loc[bv.total.idxmin(), "k"]
ax.axvline(best, color=CL.muted, lw=1, alpha=0.6)
ax.set_xlabel("$k$"); ax.set_ylabel("expected squared error")
ax.set_xscale("log"); ax.set_xticks(ks); ax.set_xticklabels(ks)
ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout()

print(f"{'k':>4}{'bias²':>10}{'variance':>11}{'σ²':>9}{'sum':>10}{'test MSE':>11}")
for _, r in bv.iterrows():
    print(f"{int(r.k):>4}{r.bias2:10.5f}{r['var']:11.5f}{SIGMA**2:9.5f}"
          f"{r.total:10.5f}{r.mse:11.5f}")
print(f"\nminimum total error at k = {int(best)}")
```

Read the table rather than the shape. Variance falls by a factor of sixteen
between $k = 1$ and $k = 80$; squared bias rises by a factor of several hundred.
The sum is U-shaped with a minimum in between, and the identity holds — the sum
of the three estimated components matches the independently measured test error
at every $k$. That is the decomposition being *verified*, not illustrated.

Note also what happens at the extremes. At $k = 1$ the method has essentially no
bias and all the error is variance plus noise. At $k = 80$, two thirds of the
sample is averaged into every prediction and the bias dominates. Neither
extreme is a modelling failure; both are the same dial at different settings.

::: {.definition}
[**Effective degrees of freedom**]{.term} — for $k$-nearest neighbours, roughly
$n/k$. At $k = 1$ the method has as many effective parameters as observations,
which is why it interpolates the training data exactly; at $k = n$ it has one,
and predicts the global mean everywhere. It is the same quantity chapter 5's
penalty controlled continuously.
:::

## Distance is not given, it is chosen

Nearest neighbours needs a definition of "near". The default is Euclidean
distance,

$$
d(x_0, x_i) \;=\; \sqrt{\textstyle\sum_{j=1}^{p} (x_{0j} - x_{ij})^2},
$$

and that formula adds squared differences measured in different units. A
difference of one euro and a difference of one index point are treated as
identical quantities. In practice the variable with the largest numerical range
determines the neighbours entirely, and every other predictor is decoration.

This is the third time this book has reached the same conclusion — PCA in
chapter 7, the penalties in chapter 5, and now here — and the reason is always
the same: any method that compares magnitudes across variables must first make
them comparable. **Standardise before computing a distance.** The alternative is
a method whose answer depends on whether you recorded revenue in dollars or
millions of dollars.

## The curse of dimensionality

The deeper problem is that "near" stops existing as the number of predictors
grows, and it does so much faster than intuition suggests.

```{python}
#| label: check-curse
#| code-summary: "Run it: watch 'nearest' stop meaning anything"

rng2 = np.random.default_rng(7)
print(f"{'dimensions':>11}{'nearest':>10}{'farthest':>10}{'contrast':>11}")
for p in [1, 2, 5, 10, 25, 50, 100, 500]:
    X = rng2.uniform(0, 1, (500, p))
    q = rng2.uniform(0, 1, (1, p))
    dist = np.sqrt(((X - q) ** 2).sum(axis=1))
    print(f"{p:>11}{dist.min():10.3f}{dist.max():10.3f}"
          f"{(dist.max() - dist.min())/dist.min():11.3f}")
```

The last column is what matters: the gap between the nearest and the farthest
point, relative to the nearest. In one dimension the farthest point is around a
thousand times further away than the nearest. By fifty dimensions it is half
again as far; by five hundred, a fifth. All the points are approximately the same
distance from the query, so "the ten nearest" is close to a random selection of
ten [@beyer1999].

There is a second, geometric way to see the same thing. To capture a fixed
fraction $r$ of the data in a hypercube of $p$ dimensions, the neighbourhood must
span $r^{1/p}$ of the range of *each* variable. Capturing 1% of the data needs
10% of the range in two dimensions, 63% in ten, and 95% in a hundred — a
"neighbourhood" covering almost the entire space, which is not local in any
useful sense.

The consequence for practice is blunt. Nearest neighbours works well with few
predictors and abundant data, and degrades quickly as predictors are added.
Adding a variable to a linear model costs one parameter; adding one to a nearest
neighbour method costs a dimension of the space in which distance must remain
meaningful.

## Choosing $k$, and why training error lies

The training error of $1$-nearest-neighbour is exactly zero: every training point
is its own nearest neighbour, so it predicts itself perfectly. That number is
not a measure of anything, and any procedure that selects $k$ by fitting error
will select $k = 1$ every time.

Cross-validation is the answer, as it was in chapter 5. Split, fit on the rest,
measure on the held-out part, rotate.

```{python}
#| label: fig-choose-k
#| code-summary: "Show the code"
#| fig-cap: "Training error against cross-validated error for the same data. Training error rises monotonically with $k$ and is zero at $k=1$; only the cross-validated curve has a minimum, and it is not at $k=1$."

from sklearn.model_selection import cross_val_score, KFold

xs = rng.uniform(0, 1, 200).reshape(-1, 1)
ys = truth_fn(xs.ravel()) + rng.normal(0, SIGMA, 200)
grid = [1, 2, 3, 5, 8, 12, 20, 30, 45, 60, 90, 130]

train_err, cv_err = [], []
for k in grid:
    m = KNeighborsRegressor(n_neighbors=k).fit(xs, ys)
    train_err.append(np.mean((ys - m.predict(xs)) ** 2))
    cv_err.append(-cross_val_score(KNeighborsRegressor(n_neighbors=k), xs, ys,
                                   cv=KFold(10, shuffle=True, random_state=0),
                                   scoring="neg_mean_squared_error").mean())

fig, ax = plt.subplots(figsize=(7.0, 4.3))
ax.plot(grid, train_err, marker="o", ms=4, lw=1.8, color=CL.muted, label="training error")
ax.plot(grid, cv_err, marker="s", ms=4, lw=2.0, color=CL.accent, label="10-fold CV error")
ax.axhline(SIGMA ** 2, ls=":", lw=1.4, color=CL.warn, label=r"irreducible $\sigma^2$")
ax.axvline(grid[int(np.argmin(cv_err))], color=CL.ink, lw=1, ls="--")
ax.set_xlabel("$k$"); ax.set_ylabel("mean squared error")
ax.set_xscale("log"); ax.set_xticks(grid); ax.set_xticklabels(grid)
ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout()

print(f"training error at k=1: {train_err[0]:.6f}  (exactly zero — every point is its own neighbour)")
print(f"CV chooses k = {grid[int(np.argmin(cv_err))]}, CV error {min(cv_err):.4f}")
print(f"irreducible floor σ² = {SIGMA**2:.4f}")
```

Two things are visible. The training curve is monotone and useless for selection.
And the cross-validated minimum sits close to, but above, the irreducible floor —
which is what a well-tuned method looks like. A cross-validated error *below*
$\sigma^2$ would indicate a leak between the folds rather than a triumph.

## Did the flexibility earn its keep?

Now the real question, on real data. Nearest neighbours is flexible; flexibility
costs variance; and the only justification for paying is that the truth is
non-linear in a way a linear model misses. Whether that holds is an empirical
question, and it is answered by comparison rather than by assertion.

```{python}
#| label: check-real
#| code-summary: "Run it: kNN against a baseline and against logistic regression"

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

core = qmib.load("core").dropna(
    subset=["falling_behind_next", "gdp_pc_eur", "productivity_idx",
            "employment_ths", "gfcf_meur"])
Xc = core[["gdp_pc_eur", "productivity_idx", "employment_ths", "gfcf_meur"]]
yc = core["falling_behind_next"]
cv = StratifiedKFold(5, shuffle=True, random_state=0)

print(f"n = {len(core)}   base rate = {yc.mean():.3f}   "
      f"majority-class accuracy = {1 - yc.mean():.4f}\n")
print(f"{'model':30}{'accuracy':>10}{'ROC AUC':>10}")
models = [
    ("kNN, k=5, standardised",  make_pipeline(StandardScaler(), KNeighborsClassifier(5))),
    ("kNN, k=25, standardised", make_pipeline(StandardScaler(), KNeighborsClassifier(25))),
    ("logistic regression",     make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
]
for name, mdl in models:
    acc = cross_val_score(mdl, Xc, yc, cv=cv, scoring="accuracy").mean()
    auc = cross_val_score(mdl, Xc, yc, cv=cv, scoring="roc_auc").mean()
    print(f"{name:30}{acc:10.4f}{auc:10.4f}")
```

The result is unflattering to the method this chapter is about, and it is the
most useful output in it.

**On accuracy, nothing beats predicting the majority class.** All three models
score about 0.899, which is exactly what you get by declaring that no country
falls behind, ever. Chapter 4 warned about this: with a base rate of 10%,
accuracy is a measure of the base rate rather than of the model.

**On AUC, the models separate completely.** Nearest neighbours at $k=5$ scores
0.51 — a coin flip, no information whatsoever. At $k=25$ it recovers to 0.56.
Logistic regression, the rigid method with the strong assumption, reaches 0.68.

So the flexibility did not earn its keep. There is signal in these predictors, a
linear model finds it, and the flexible method spends its budget on variance and
comes back with almost nothing. Had the comparison been made on accuracy alone,
all three would have looked identical and the conclusion would have been that
nothing works — which is false, and would have been the wrong lesson.

## What nearest neighbours cannot do

**It cannot explain.** There are no coefficients, so there is nothing to
interpret, no marginal effect, no test of a hypothesis about a mechanism. It is
a prediction machine, and chapter 1's distinction applies with full force.

**It cannot extrapolate.** A query outside the range of the training data is
answered by whichever training points happen to be least far away, which will be
the boundary points, no matter how far outside you go. The prediction is
confidently wrong and nothing signals it.

**It is slow where it matters.** Fitting is free and predicting is expensive: the
entire training set must be searched for every query. That is the opposite of the
profile you usually want in production.

**It is exposed to irrelevant variables.** Adding a predictor that carries no
information does not merely fail to help — it actively corrupts the distances,
diluting the informative dimensions. Chapter 5's penalties can shrink a useless
variable to zero; a distance cannot.

## A short review of the literature

::: {.lit}
The method originates in an unpublished 1951 technical report by @fix1951, whose
belated reprinting in 1989 is the citable version. @cover1967 proved the result
that made it respectable: as the sample grows, the error rate of the
1-nearest-neighbour rule is bounded above by twice the Bayes rate — so the
simplest possible classifier, using one point, is asymptotically within a factor
of two of the best any method can do. @stone1977 established the conditions
under which nearest-neighbour regression is consistent, completing the
theoretical case.

The trade-off itself is stated in its modern form by @geman1992, who framed it as
a dilemma rather than a choice: any method flexible enough to fit an arbitrary
function is flexible enough to fit the noise, and the resolution has to come from
outside the data, as a restriction, a penalty, or a tuning parameter chosen by
resampling.

@beyer1999 is the reference for the failure in high dimensions, showing that
under broad conditions the distance to the nearest neighbour approaches the
distance to the farthest as dimension grows — so the query on which the whole
method depends becomes meaningless, not merely imprecise.
:::

## What to report

1. **The baseline first.** Majority-class accuracy, or the mean for regression.
   Every subsequent number is read against it.
2. **A metric the base rate does not dominate.** AUC, balanced accuracy or a
   proper scoring rule. Accuracy on a 10% outcome tells you the outcome is 10%.
3. **How $k$ was chosen**, with the cross-validation curve, and the training
   curve alongside it if you want to make the point that it is uninformative.
4. **That the predictors were standardised**, and how many there are. With more
   than a handful, say what you did about the dimensionality.
5. **The comparison against a rigid model.** Flexibility is a purchase, and the
   report should say what it bought. If a linear model does as well or better,
   that is the finding.
6. **What the method cannot support.** No interpretation, no extrapolation, and
   no claim about mechanism — only about prediction, within the range of the
   training data.
