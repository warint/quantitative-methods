# The supervised learning problem

**Session 01 · pre-session reading**

> **What every session after this one assumes you already have.**

---

Session 01 itself spends its ninety minutes on the syllabus and on *Europe 2031*. The mathematics
starts in Session 02 — and it starts *mid-sentence*, because Session 02 opens by asking which
$\hat\beta$ minimises a squared error, and takes for granted that you know what a squared error is
*for*.

This page is that missing sentence. It is four ideas and it takes forty minutes.

> **This page is optional and is not examinable.** Session 02 introduces everything it needs from
> first principles. Read this if you would rather arrive with the vocabulary already in hand — many
> students find the rest of the course easier for it.

---

## 0.1 The problem, stated once

You observe pairs $(x_i, y_i)$, $i = 1,\dots,n$. You believe they were produced by

$$Y = f(X) + \varepsilon, \qquad \mathbb{E}[\varepsilon \mid X] = 0, \qquad
\mathrm{Var}(\varepsilon) = \sigma^2 .$$

Three objects, and they are not the same kind of thing:

| | | |
|---|---|---|
| $f$ | the **systematic** part | a fixed, unknown function of $X$ — the thing you are trying to learn |
| $\varepsilon$ | the **noise** | everything driving $Y$ that $X$ does not observe |
| $\hat f$ | your **estimate** | a function you construct from the data, which is therefore random |

> **The distinction that trips people up.** $f$ is fixed and unknown; $\hat f$ is known and random.
> Every confidence interval in this course is a statement about the second, made in order to say
> something about the first.

You want $\hat f$ for one of two reasons, and they lead to different choices:

- **Prediction.** You want $\hat f(x)$ to be close to $y$ for new $x$. The internals of $\hat f$ are
  of no interest; a black box that predicts well is a success.
- **Inference.** You want to know *how* $Y$ depends on $X$ — which components matter, in which
  direction, by how much, and how sure you are. Here a black box is a failure even if it predicts
  perfectly.

Sessions 02–03 are inference. Sessions 04–09 are prediction. Session 10 is what happens when you
need a third thing — **causation** — and discover that neither of the first two gives it to you.

---

## 0.2 Loss and risk

To say one $\hat f$ is better than another you must first say what "worse" costs. A **loss
function** $L(y, \hat y)$ prices a single mistake.

| Loss | $L(y,\hat y)$ | Used for |
|---|---|---|
| Squared error | $(y-\hat y)^2$ | continuous outcomes; Sessions 02–05 |
| Absolute error | $\lvert y - \hat y\rvert$ | continuous outcomes, robust to outliers |
| 0–1 loss | $\mathbb{1}\{y \neq \hat y\}$ | classification; Session 06 |
| Log loss | $-\log \hat p_y$ | probability forecasts; Sessions 06–07 |

The **risk** of a predictor $g$ is its expected loss over the whole population — not over your
sample:

$$R(g) = \mathbb{E}\big[L(Y, g(X))\big] .$$

> **Read the expectation carefully.** It averages over *new* draws of $(X, Y)$, including draws you
> have never seen. That is what makes risk the quantity you care about and the sample average the
> quantity you can actually compute. The gap between the two is the subject of Session 04.

Squared error is the default in this course not because mistakes really are quadratic in cost, but
because it makes the next section come out cleanly. **Choosing a loss is a modelling decision.**
Session 06 makes you choose one deliberately, with money attached.

---

## 0.3 The best predictor there is

Suppose, for a moment, that you knew the entire joint distribution of $(X, Y)$ — no estimation, no
sample, perfect knowledge. What would you predict?

Under squared-error loss the answer is the **conditional expectation**, sometimes called the
regression function:

$$f^\star(x) = \mathbb{E}[Y \mid X = x] .$$

**The derivation, which is three lines.** Take any competing predictor $g$. Add and subtract
$\mathbb{E}[Y\mid X]$ inside the square:

$$R(g) = \mathbb{E}\Big[\big(\underbrace{Y - \mathbb{E}[Y\mid X]}_{\text{noise}}
+ \underbrace{\mathbb{E}[Y\mid X] - g(X)}_{\text{your error}}\big)^2\Big] .$$

Expanding gives three terms. The cross term vanishes by the **tower property** of conditional
expectation (the law of iterated expectations, $\mathbb{E}[Z] = \mathbb{E}\big[\mathbb{E}[Z\mid X]\big]$):
condition on $X$ first, and since $\mathbb{E}[Y\mid X] - g(X)$ is a function of $X$ it passes
outside the inner expectation, leaving

$$\mathbb{E}\big[(Y - \mathbb{E}[Y\mid X])\,(\mathbb{E}[Y\mid X] - g(X))\big]
= \mathbb{E}\Big[(\mathbb{E}[Y\mid X] - g(X))\underbrace{\mathbb{E}\big[Y - \mathbb{E}[Y\mid X]
\;\big|\; X\big]}_{= \,0}\Big] = 0 .$$

So what is left is

$$\boxed{\;R(g) = \sigma^2 + \mathbb{E}\big[(\mathbb{E}[Y\mid X] - g(X))^2\big]\;}$$

The first term does not depend on $g$ at all. The second is a squared quantity, so it is
non-negative, and it is zero exactly when $g(x) = \mathbb{E}[Y\mid X=x]$.

> **Therefore:** no predictor, however clever, however flexible, however much data it was trained
> on, can achieve a squared-error risk below $\sigma^2$. And the conditional expectation achieves
> it.

**For classification.** Under 0–1 loss the same argument gives the **Bayes classifier** — predict
the most probable class,

$$g^\star(x) = \arg\max_k \; P(Y = k \mid X = x),$$

whose risk, the **Bayes error rate**, is $1 - \mathbb{E}\big[\max_k P(Y=k\mid X)\big]$.

Every method in this course is an attempt to approximate $\mathbb{E}[Y\mid X]$ or
$P(Y = k \mid X)$ from a finite sample. That is the *whole* subject:

| Session | How it approximates $\mathbb{E}[Y\mid X]$ |
|---|---|
| **02–03** | assume it is linear in $X$, and estimate the coefficients |
| **05** | assume it is linear and **sparse**, and penalise |
| **06** | model $P(Y=1\mid X)$ through a logistic link |
| **07** | approximate it by a **piecewise constant** function on a learned partition |
| **08** | approximate $X$ itself first, by a few factors |

---

## 0.4 The irreducible error

$\sigma^2$ is called **irreducible** for the reason the box above makes precise: it survives even
when you use the optimal predictor with perfect knowledge of the distribution.

It is not a defect of your method. It is a statement about your **variables**: it measures
everything that moves $Y$ and is not visible in $X$ — unmeasured determinants, genuine randomness,
measurement error in $Y$.

Three consequences you will use repeatedly:

1. **There is a ceiling on performance, and you do not know where it is.** An $R^2$ of 0.30 may be
   excellent or dreadful; nothing in the output tells you which.
2. **You reduce $\sigma^2$ only by measuring more things** — better data, not better algorithms.
   This is why Session 08's answer to "more series" is the opposite of Session 05's.
3. **A validation error below $\sigma^2$ is impossible.** So if you ever see one, you have not
   discovered anything; you have leaked. Session 04 is a catalogue of how.

> **The sentence to carry.** *Irreducible* means irreducible by any method. It does not mean
> irreducible by any dataset.

---

## 0.5 Why prediction and inference pull apart

Both goals are served by estimating $f$, so it is tempting to think a better $\hat f$ is better for
both. It is not, and the course spends eleven weeks on the consequences.

| | Prediction asks | Inference asks |
|---|---|---|
| **Target** | $\hat f(x)$ close to $y$ | $\hat\beta_j$ close to $\beta_j$, with an honest interval |
| **Judged by** | error on data never seen | coverage of the interval |
| **Flexibility is** | a resource — use it | a hazard — it inflates variance and voids standard errors |
| **Correlated predictors** | mostly harmless | fatal (Session 03) |
| **Fails when** | the future differs from the past (Session 11) | the model is misspecified, or a confounder is missing |

And a third question, which looks like the second and is not:

> **Causation.** *If we changed $X$, what would happen to $Y$?*

Nothing in $Y = f(X) + \varepsilon$ answers that. The model describes an association in the
population that generated your data; it says nothing about a population in which someone
intervened. A model can predict perfectly, have tight standard errors, and still be a completely
wrong guide to policy. **Session 10 is where that is confronted**, and it is deliberately
uncomfortable.

---

## Self-check

Answer these on paper before Session 01. If you cannot, re-read the relevant section — not the
whole page.

1. State the difference between $f$, $\hat f$ and $\mathbb{E}[Y\mid X]$ in one sentence each.
2. Show that the cross term in §0.3 vanishes. **Name** the property of conditional expectation you
   used, and say where in the argument you used it.
3. A colleague reports a cross-validated $R^2$ of $0.98$ on a macro forecasting problem where every
   published model reaches $0.4$. Give two explanations, and say which you would check first.
4. Give an example of a variable that is an excellent **predictor** of an outcome and a useless
   **policy lever**. Say in one sentence why the two can differ.
5. Under 0–1 loss, what does the Bayes error rate measure, and why can no classifier beat it?

---

## Notation reminders used throughout the course

| Symbol | Meaning |
|---|---|
| $n$, $p$ | number of observations, number of predictors |
| $X$ | $n \times p$ design matrix (first column ones, unless stated) |
| $y$ | $n$-vector of outcomes |
| $\hat\beta$ | estimated coefficient vector |
| $\hat y = X\hat\beta$ | fitted values |
| $H = X(X^\top X)^{-1}X^\top$ | hat (projection) matrix |
| $\lambda$, $\alpha$ | penalty strength, elastic-net mixing parameter |
| $L(y,\hat y)$ | loss function |
| $R(g)$ | risk — expected loss of the predictor $g$ |
| $\sigma^2$ | irreducible error, $\mathrm{Var}(\varepsilon)$ |

> **Rendering the mathematics.** These notes use LaTeX. In VS Codium, install the
> *Markdown+Math* or *Markdown Preview Enhanced* extension and open the preview with
> `Ctrl/Cmd+K V`. See the [setup guide](setup-vscodium-local-llm.md).

---

[Back to the pre-session](README.md) · [On to Session 02 ->](../../02-geometry-of-least-squares/README.md)
