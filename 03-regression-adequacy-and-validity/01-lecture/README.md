# Session 03 — Lecture (first half, ~90 min)

# Regression: Adequacy, Validity, and Robustness

> **You have fitted a regression. Can it be trusted?**

---

> **Python cheatsheet — [session 03](https://warint.github.io/quantitative-methods/python-cheatsheet-03.pdf)** (PDF) ·
> source: [`PYTHON-CHEATSHEET.qmd`](../PYTHON-CHEATSHEET.qmd)
>
> How to start Python in VS Codium on your platform, how to make a file and run it,
> the DataFrame basics, and every name taught in sessions 1 to 3 with a
> line showing it in use. Print it.

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-03-lecture.html)** ·
> source: [`MATH60033A-S03-Lecture.qmd`](MATH60033A-S03-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

The hour is four questions about one fitted line, and it starts by fitting it.

| | Question | Deck section |
|---|---|---|
| | how do we get a line at all? | From data to models |
| **Adequacy** | how much does it explain? | $R^2$, adjusted $R^2$, RSE |
| **Validity** | do its assumptions hold? | linearity, normality, constant variance |
| **Robustness** | which observations move the answer? | leverage, Cook's distance |
| **Parsimony** | would a simpler model do as well? | AIC, BIC |

> **Selection is not here.** Choosing *which* model to fit — stepwise and its successors — is
> session 05. AIC compares models you have already written down; it does not write them for you.

---

### 3.0 From data to models: fitting a straight line

Everything so far described **one variable at a time**. The moment you ask whether two things move
together, you are building a model. This section is the smallest possible one — and every method in
the rest of the course is a variation on it. It opens the hour; everything after it asks whether
the line it produces can be trusted.

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
**estimates**, written $\hat\beta_0$ and $\hat\beta_1$ — the rest of this hour is about how much
to trust them.

#### Choosing the line: least squares

Infinitely many straight lines pass through that cloud. We pick the one that makes the vertical
misses as small as possible — specifically, the one minimising the **sum of squared residuals**:

$$\min_{\beta_0,\, \beta_1} \sum_{i=1}^{n} \big(y_i - \beta_0 - \beta_1 x_i\big)^2$$

Why squared, rather than the plain distance? Two reasons a beginner should hold on to. Squaring
makes every miss positive, so misses above and below cannot cancel out. And it punishes one large
miss more than several small ones — which, as §2.1 of the [session 02
notes](../../02-exploratory-data-analysis/01-lecture/README.md) showed for the mean, is a
**choice**, not a law.

> This is the same idea as §2.1 there. The mean is the number minimising $\sum(x_i - c)^2$; the regression
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
everything about German income that productivity alone does not account for. Reading residuals is
most of what follows.

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

## Learning objectives

By the end of the session you should be able to:

- Fit a simple and a multiple regression, and state the slope **in units**
- Read "controlling for" as the question a second predictor changes
- Read a **residuals-versus-fitted** plot and say what structure it reveals
- Diagnose non-constant variance from a **scale–location** plot
- Compute **leverage** and say which observations have the power to move the line
- Use **Cook's distance** to separate an outlier from an influential point
- Compare candidate models on **AIC**, and say why that is not model selection

---

## The data

**GDP per capita on productivity, thirty European countries over fifteen years** — fitted at
the top of the hour, then interrogated for the rest of it.

```python
import qmib
data = qmib.load("core")
```

Run it once before class; it caches locally and then works offline.

---

## Running the code

Everything in the deck runs in the **VS Codium terminal** with the project environment active:

```bash
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate         # Windows
python
```

If a package is missing, `pip install -r requirements.txt` from the repository root.

---

## What loses marks

- Reporting $R^2$ without a single diagnostic plot
- Deleting an influential point without saying what it was
- Reading a residual plot as "looks fine" with no statement of what you looked for
- Choosing a model on AIC and reporting it as though the data selected it

---

[Back to session 03](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-03.html)
