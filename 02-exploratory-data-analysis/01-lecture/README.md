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

### 2.4 From data to models: fitting a straight line

Everything so far described **one variable at a time**. The moment you ask whether two things move
together, you are building a model. This section is the smallest possible one — and every method in
the rest of the course is a variation on it.

**The question, in international-business terms.** European countries differ enormously in how much
output a worker produces in an hour. Do the more productive countries also have higher income per
head? We have both numbers for thirty countries over fifteen years.

#### Always look first

```python
import pandas as pd
import matplotlib.pyplot as plt

core = pd.read_parquet("data/spine/core.parquet")
d = core.dropna(subset=["gdp_pc_eur", "productivity_idx"])

plt.scatter(d["productivity_idx"], d["gdp_pc_eur"], s=12, alpha=0.6)
plt.xlabel("Labour productivity index (EU average = 100)")
plt.ylabel("GDP per capita (EUR)")
plt.show()
```

Line by line: `read_parquet` loads the table; `dropna(subset=[...])` throws away rows where either
number is missing, because you cannot plot a point with a hole in it; `scatter` draws one dot per
country-year; `s=12` makes the dots small and `alpha=0.6` makes them see-through, so you can tell
where they pile up.

You should see a cloud sloping upward. **Draw the picture before you fit anything.** A straight line
fitted to a curved cloud is still a straight line, and the software will not warn you.

#### The model, and what each piece is

$$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$$

| Symbol | Name | In this example |
|---|---|---|
| $y_i$ | the **outcome** (dependent variable) | GDP per capita of country-year $i$ |
| $x_i$ | the **predictor** (independent variable) | its productivity index |
| $\beta_0$ | the **intercept** | predicted $y$ when $x = 0$ |
| $\beta_1$ | the **slope** | how much $y$ changes when $x$ rises by one |
| $\varepsilon_i$ | the **error** | everything about $y_i$ that $x_i$ does not explain |

$\beta_0$ and $\beta_1$ are fixed numbers we do not know. What we compute from the data are
**estimates**, written $\hat\beta_0$ and $\hat\beta_1$ — Session 03 is about how much to trust them.

#### Choosing the line: least squares

Infinitely many straight lines pass through that cloud. We pick the one that makes the vertical
misses as small as possible — specifically, the one minimising the **sum of squared residuals**:

$$\min_{\beta_0,\, \beta_1} \sum_{i=1}^{n} \big(y_i - \beta_0 - \beta_1 x_i\big)^2$$

Why squared, rather than the plain distance? Two reasons a beginner should hold on to. Squaring
makes every miss positive, so misses above and below cannot cancel out. And it punishes one large
miss more than several small ones — which, as §2.1 showed for the mean, is a **choice**, not a law.

> This is the same idea as §2.1. The mean is the number minimising $\sum(x_i - c)^2$; the regression
> line is the *line* minimising the same quantity. Least squares is the mean, done conditionally.

#### Fitting it in Python

```python
import statsmodels.formula.api as smf

model = smf.ols("gdp_pc_eur ~ productivity_idx", data=d).fit()
print(model.params)
```

```
Intercept          -86118.1
productivity_idx     1111.3
```

`smf.ols` means *ordinary least squares*. The string `"gdp_pc_eur ~ productivity_idx"` is a
**formula**: read the `~` as "explained by". `data=d` says which table the names come from, and
`.fit()` does the arithmetic. `model.params` holds the two estimates.

#### Reading the numbers, in units

**The slope is the sentence you will actually write.** $\hat\beta_1 = 1111.3$ means: comparing two
country-years that differ by **one point** of productivity index, the one with higher productivity
has on average **€1,111 more** GDP per capita.

Always say the units aloud. A slope is *outcome units per predictor unit*, here euros per index
point. A slope without units is not a finding.

> **The intercept is often nonsense, and that is fine.** $\hat\beta_0 = -86{,}118$ says a country
> with productivity index 0 would have GDP per capita of minus eighty-six thousand euros. No such
> country exists — the index runs from 72 to 129 in our data. The intercept is where the line
> crosses $x = 0$, which is far outside the range we observed. **Do not interpret an intercept you
> have no data near.**

#### Fitted values and residuals

For any country-year, the line gives a **fitted value** $\hat y_i$, and what is left over is the
**residual** $e_i = y_i - \hat y_i$.

Germany in 2022 had a productivity index of 121.2 and GDP per capita of €54,239:

$$\hat y = -86{,}118 + 1{,}111.3 \times 121.2 = 48{,}606$$
$$e = 54{,}239 - 48{,}606 = +5{,}633$$

Germany sits **€5,633 above** the line. That residual is not an error in the arithmetic — it is
everything about German income that productivity alone does not account for. Session 03 is largely
about reading residuals.

```python
d = d.copy()
d["fitted"] = model.fittedvalues
d["residual"] = model.resid
print(d.loc[(d["geo"] == "DE") & (d["time"] == 2022),
            ["geo", "time", "productivity_idx", "gdp_pc_eur", "fitted", "residual"]])
```

#### How much did the line explain? $R^2$

```python
print(f"R-squared = {model.rsquared:.3f}")
```

```
R-squared = 0.627
```

$R^2$ is the share of the variation in $y$ that the model accounts for — here **62.7%**. It runs
from 0 to 1.

> **What $R^2$ does not tell you.** It does not say the model is correct, that the relationship is
> causal, or that the line will predict a new country well. A high $R^2$ on a badly specified model
> is common. Session 04 asks what happens on data you have not seen.

#### Two predictors, and what "controlling for" means

Rich countries are also countries that invest heavily. So is the productivity effect real, or is
productivity standing in for investment? Add investment and look:

```python
d2 = core.dropna(subset=["gdp_pc_eur", "productivity_idx", "gfcf_meur"])
model2 = smf.ols("gdp_pc_eur ~ productivity_idx + gfcf_meur", data=d2).fit()
print(model2.params)
print(f"R-squared = {model2.rsquared:.3f}")
```

```
Intercept          -71211.8
productivity_idx      928.3
gfcf_meur              68.7
R-squared = 0.692
```

The productivity slope falls from **1,111 to 928** — about 16% — and $R^2$ rises from 0.627 to
0.692.

**Read that carefully, because it is the single most important idea in the section.** The slope on
productivity now answers a *different question*: comparing two country-years **with the same level
of investment**, one point more productivity goes with €928 more GDP per capita. Some of what the
first model credited to productivity actually belonged to investment.

> "Controlling for investment" does not mean investment has been removed from the world. It means
> the comparison is now between country-years that resemble each other in investment. Which
> comparison you want is a question about your research question, not about the software.

#### Correlation is not causation

The slope says productivity and income **move together**. It does not say raising productivity by
one point *would* raise income by €928.

Three explanations survive every regression in this section, and nothing in the output distinguishes
them:

1. Productivity raises income.
2. Higher income lets countries buy the capital and training that raise productivity — the arrow
   points the other way.
3. Something else — institutions, education, market size — drives both.

Sessions 10 and 11 are entirely about what extra evidence it takes to choose between these. Until
then, write **"is associated with"**, and mean it.

---

### 2.5 What this buys you in the rest of the course

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
