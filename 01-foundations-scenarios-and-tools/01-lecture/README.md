# Session 01 — Lecture (first half, ~90 min)

# Foundations: Scenarios, Tools, and the Supervised Learning Problem

> **Before we can model the future, what exactly are we claiming to know about it?**

---

### 1.1 The supervised learning problem

We observe $n$ pairs $(x_i, y_i)$, with $x_i \in \mathbb{R}^p$ a vector of predictors and
$y_i \in \mathbb{R}$ an outcome. We assume they are drawn from an unknown joint distribution
$P(X, Y)$, and we posit

$$Y = f(X) + \varepsilon, \qquad \mathbb{E}[\varepsilon \mid X] = 0, \quad \operatorname{Var}(\varepsilon) = \sigma^2 .$$

The function $f$ is the *systematic* part - what $X$ tells us about $Y$. The term $\varepsilon$ is
everything else: measurement error, omitted causes, genuine randomness.

**The two goals.**

| | Prediction | Inference |
|---|---|---|
| Object of interest | $\hat f(x)$ evaluated at new $x$ | the parameters or structure of $f$ |
| Quality criterion | out-of-sample loss | bias, consistency, coverage of intervals |
| Is a black box acceptable? | Often yes | No |
| Economic example | Nowcast euro-area GDP | Effect of a training subsidy on wages |

Keep this table beside you all semester. Most disagreements about "which model is better" are
really disagreements about which column you are in.

### 1.2 Loss, risk, and the best possible predictor

Choose a loss function $L(y, \hat y)$. For squared-error loss, $L(y,\hat y) = (y - \hat y)^2$, and
the **risk** (expected prediction error) of a candidate function $g$ is

$$ R(g) = \mathbb{E}_{(X,Y)}\big[(Y - g(X))^2\big]. $$

**Proposition.** The minimiser of $R$ over all measurable $g$ is the conditional expectation
$g^\star(x) = \mathbb{E}[Y \mid X = x]$.

*Proof sketch.* Write $Y - g(X) = \big(Y - \mathbb{E}[Y|X]\big) + \big(\mathbb{E}[Y|X] - g(X)\big)$.
Square and take expectations. The cross term vanishes because
$\mathbb{E}\big[(Y - \mathbb{E}[Y|X])\,h(X)\big] = 0$ for any $h$, by the tower property. What
remains is

$$ R(g) = \underbrace{\sigma^2}_{\text{irreducible}} + \underbrace{\mathbb{E}\big[(\mathbb{E}[Y|X] - g(X))^2\big]}_{\ge 0}, $$

which is minimised at zero when $g = \mathbb{E}[Y|X]$. $\blacksquare$

**Read this economically.** The floor $\sigma^2$ is not a failure of your method. It is the part of
the world your predictors do not see. A large part of applied judgement is knowing when you are
already at the floor - and *Europe 2031* is, in effect, a claim that a great deal of Europe's
economic future is *not* irreducible noise but a function of choices that could be measured.

### 1.3 Why we cannot simply compute $\mathbb{E}[Y \mid X]$

We do not know $P(X,Y)$. We have $n$ draws from it. So we replace risk by **empirical risk**,

$$ \hat R(g) = \frac{1}{n}\sum_{i=1}^n L(y_i, g(x_i)), $$

and minimise over a restricted class $\mathcal{G}$ of candidate functions. Two choices now define
everything that follows in this course:

1. **How rich is $\mathcal{G}$?** (linear? penalised linear? trees? ensembles?)
2. **How do we stop $\hat R$ from lying to us about $R$?** (Sessions 4 onward: cross-validation.)

Session 2 takes the smallest interesting choice - $\mathcal{G}$ = linear functions - and works out
its geometry completely.

### 1.4 From narrative assumption to measurable indicator

A scenario assumption such as *"compute becomes the dominant measure of geopolitical power"* is not
yet a hypothesis. To make it one, specify:

- an **indicator** $I_t$ that is observable and published on a known schedule;
- a **direction** (does the assumption imply $I_t$ rises or falls?);
- a **trigger point** $\tau$ and a horizon, such that observing $I_t > \tau$ before date $T$ would
  materially raise your belief in the assumption;
- a **falsifier**: what observation would count as evidence *against* it.

This is the discipline that separates foresight from storytelling, and it is exactly the discipline
that a well-specified regression imposes.

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

> **Rendering the mathematics.** These notes use LaTeX. In VS Codium, install the
> *Markdown+Math* or *Markdown Preview Enhanced* extension and open the preview with
> `Ctrl/Cmd+K V`. See the [setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).

---

[Back to session 01](../README.md) · [On to the lab ->](../02-lab/README.md)
