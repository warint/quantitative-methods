# Session 02 — Lecture (first half, ~90 min)

# Exploratory Data Analysis: Centre, Spread, and Shape

> **Quote of the day**
>
> *"It's tough to make predictions, especially about the future."*
> — Yogi Berra

> **Before you model anything, what does the data actually look like?**

---

## Why this session comes first

Every method in the eleven sessions that follow reduces a column of numbers to a few summaries and
then reasons about those summaries. If you cannot say what the mean of a variable *is*, what it is
sensitive to, and when it stops being the right summary, everything downstream inherits the mistake
silently.

Three questions organise the whole session, and they are the three questions you ask of any new
column of data:

| | Question | Session |
|---|---|---|
| **Centre** | where does the distribution sit? | §2.1 |
| **Spread** | how far from there does it reach? | §2.2 |
| **Shape** | is it symmetric, and how heavy are the tails? | §2.3 |

---

## Let's start with an example

The course data spine holds GDP per capita for thirty European countries over fifteen years. Load
it and ask the first question:

```python
import numpy as np
import pandas as pd

core = pd.read_parquet("data/spine/core.parquet")
gdp = core["gdp_pc_eur"].dropna()

print(f"n        = {len(gdp)}")
print(f"mean     = {gdp.mean():,.0f} EUR")
print(f"median   = {gdp.median():,.0f} EUR")
```

```
n        = 437
mean     = 30,373 EUR
median   = 25,733 EUR
```

The mean sits **€4,640 above the median**. That gap is not a rounding artefact and it is not noise:
it is the single most informative number on this page, and §2.3 explains what produces it.

---

### 2.1 Measuring the centre

**The sample mean.** For a random variable taking values $x_1,\dots,x_k$ with probabilities
$p(x_i)$, the mean is

$$\mu = \sum_{i=1}^{k} x_i\, p(x_i).$$

For a sample of $n$ observations,

$$\bar{x} = \frac{x_1 + x_2 + \cdots + x_n}{n} = \frac{1}{n}\sum_{i=1}^{n} x_i .$$

Natural, easy to compute, and it has properties that make the rest of the course possible — it is
the least-squares minimiser, a fact Session 03 will use. Its weakness is written into the formula:
every observation enters with weight $1/n$, so **one extreme value moves it without limit**.

**The sample median.** Sort the data into increasing order and take the value at position
$(n+1)/2$. It is *resistant*: to move the median you must move the middle of the data, not the
edge. The cost is that it needs a sort, and it ignores everything but the ordering.

**Extensions.**

The **trimmed mean** removes a proportion from each end and averages what remains — resistant like
the median, but still using most of the data:

```python
from scipy import stats

print(f"mean            = {gdp.mean():,.0f}")
print(f"5% trimmed mean = {stats.trim_mean(gdp, 0.05):,.0f}")
print(f"median          = {gdp.median():,.0f}")
```

```
mean            = 30,373
5% trimmed mean = 29,419
median          = 25,733
```

Read the ladder. Trimming just 5% from each end pulls the average down by nearly a thousand euros,
and the median sits lower still. **The three summaries disagree, and the direction of the
disagreement is the finding.**

The **sample quantile** $\tilde q_p$ is the value below which approximately $100p\%$ of the data
falls. The **percentile** is the same idea read in the other direction — given a value, what
fraction lies below it.

```python
print(gdp.quantile([0, 0.25, 0.50, 0.75, 1.0]).round(0))
```

---

### 2.2 Measuring the spread

**Sample variance and standard deviation.**

$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2, \qquad s = \sqrt{s^2}$$

The $n-1$ is not a typo and not a convention: dividing by $n$ gives an estimator biased downward,
because the deviations are taken from $\bar x$ rather than the unknown $\mu$, and $\bar x$ is by
construction the point that makes $\sum(x_i - \cdot)^2$ smallest.

Mathematically tractable and central to everything that follows — and, like the mean, **sensitive
to extreme values**, since the deviations are squared before they are averaged.

**The empirical rule.** For data that is close to normally distributed:

| Within | Contains about |
|---|---|
| $\bar x \pm 1s$ | 68% of observations |
| $\bar x \pm 2s$ | 95% |
| $\bar x \pm 3s$ | 99.7% |

If SAT scores have mean 1500 and standard deviation 300, then roughly 68% of candidates score
between 1200 and 1800, and 95% between 900 and 2100.

> **The rule has a precondition.** It holds for *nearly normal* data. Applying it to a skewed
> variable produces intervals that are wrong in a predictable direction — which is why §2.3 exists.

**The interquartile range.**

$$\mathrm{IQR} = \tilde q_{0.75} - \tilde q_{0.25}$$

Resistant to outliers, because it is built from two order statistics. The cost is that it sees only
the middle 50% and is blind to everything in the tails.

```python
q1, q3 = gdp.quantile(0.25), gdp.quantile(0.75)
print(f"sd  = {gdp.std(ddof=1):,.0f}")
print(f"IQR = {q3 - q1:,.0f}")
```

```
sd  = 15,420
IQR = 22,215
```

---

### 2.3 Measuring the shape

Centre and spread do not determine a distribution. Two variables can share both and look nothing
alike. Shape is measured by two more numbers.

**Sample skewness** — the degree of symmetry:

$$g_1 = \frac{1}{n}\,\frac{\sum_{i=1}^{n}(x_i - \bar{x})^3}{s^3}$$

The cube preserves sign, so $-\infty < g_1 < \infty$ and the sign tells you the direction: positive
means a long right tail, negative a long left tail. A distribution is **substantially skewed** when

$$|g_1| > 2\sqrt{6/n}.$$

**Sample excess kurtosis** — the degree of tail thickness:

$$g_2 = \frac{1}{n}\,\frac{\sum_{i=1}^{n}(x_i - \bar{x})^4}{s^4} - 3$$

The $-3$ makes the normal distribution the zero point. $g_2 > 0$ is **leptokurtic** — a sharper
peak and heavier tails; $g_2 < 0$ is **platykurtic** — flatter, with thinner tails. The bound is
$-2 \le g_2 < \infty$. Substantial when

$$|g_2| > 4\sqrt{6/n}.$$

**Computing both, from the formulas:**

```python
def shape(x):
    """Skewness and excess kurtosis, exactly as defined above."""
    x = np.asarray(x, float)
    n = len(x)
    xbar, s = x.mean(), x.std(ddof=1)
    g1 = ((x - xbar) ** 3).mean() / s ** 3
    g2 = ((x - xbar) ** 4).mean() / s ** 4 - 3
    return n, g1, g2, 2 * np.sqrt(6 / n), 4 * np.sqrt(6 / n)

n, g1, g2, t1, t2 = shape(gdp)
print(f"g1 = {g1:+.3f}   threshold {t1:.3f}   substantially skewed: {abs(g1) > t1}")
print(f"g2 = {g2:+.3f}   threshold {t2:.3f}   substantially kurtic: {abs(g2) > t2}")
```

```
g1 = +0.881   threshold 0.234   substantially skewed: True
g2 = -0.013   threshold 0.469   substantially kurtic: False
```

**There is the answer to the opening example.** GDP per capita is strongly right-skewed: a handful
of rich country-years pull the right tail out, dragging the mean above the median while leaving the
median where the bulk of the data sits. The kurtosis is essentially zero — the tails are of ordinary
thickness. It is asymmetric, not heavy-tailed, and those are different defects.

> **A note on conventions.** `scipy.stats.skew` and `scipy.stats.kurtosis` use a slightly different
> normalisation by default. On this variable they return $+0.884$ and $+0.000$ against our
> $+0.881$ and $-0.013$ — close, but not identical. When you report a skewness, say which formula
> produced it.

**Four variables, four different shapes.** The same two numbers computed across the spine:

| Variable | $g_1$ | $g_2$ | Reading |
|---|---|---|---|
| `gdp_pc_eur` | $+0.881$ | $-0.013$ | skewed, normal tails |
| `population` | $+0.719$ | $-0.725$ | skewed **and** platykurtic |
| `prod_growth` | $+0.202$ | $+0.056$ | neither — well behaved |
| `share_renew` | $+0.012$ | $-0.656$ | symmetric, but platykurtic |

Skewness and kurtosis are **independent**. `share_renew` is perfectly symmetric and still badly
non-normal; `prod_growth` is the only one of the four you could hand to the empirical rule without
flinching.

---

### 2.4 What this buys you in the rest of the course

Every later session assumes you have done this first.

- **Session 03** fits a mean function by least squares. Its standard errors lean on the spread, and
  its diagnostics are residual shape by another name.
- **Session 04** asks whether a model generalises. A heavy right tail in the outcome is why a model
  can look excellent on average and fail on the cases that matter.
- **Sessions 10–11** compare treated and untreated groups. A difference in means between two skewed
  distributions can be produced entirely by their tails.

The mean, the standard deviation and the empirical rule are not neutral defaults. They are a set of
assumptions about shape, and this session is where you check them.

---

## Notation reminders used throughout the course

| Symbol | Meaning |
|---|---|
| $n$ | number of observations |
| $\bar x$ | sample mean |
| $\tilde q_p$ | sample quantile at proportion $p$ |
| $s^2$, $s$ | sample variance, sample standard deviation |
| $\mathrm{IQR}$ | interquartile range, $\tilde q_{0.75} - \tilde q_{0.25}$ |
| $g_1$, $g_2$ | sample skewness, sample excess kurtosis |
| $\mu$, $\sigma$ | population mean, population standard deviation |

> Greek letters are population quantities you never observe. Roman letters are what you compute
> from a sample. Keeping them apart is the whole of Session 03.

> **Rendering the mathematics.** These notes use LaTeX. In VS Codium, install the
> *Markdown+Math* or *Markdown Preview Enhanced* extension and open the preview with
> `Ctrl/Cmd+K V`. See the [setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).

---

[Back to session 02](../README.md) · [On to the practice ->](../02-practice/README.md)
