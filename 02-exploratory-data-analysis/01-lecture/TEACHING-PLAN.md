# Session 02 — teaching plan (first half, 90 min)

# Exploratory Data Analysis: Centre, Spread, and Shape

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

lecture 90 min · practice follows on
*Before you model anything, what does the data actually look like?*

---

## Opening

Put the quote of the day on the board — *"It's tough to make predictions, especially about the
future"*, Yogi Berra — and let them laugh at it before pointing out that it is the course's thesis
in one line.

Then the hook, which is a single number. Show them the mean and median of GDP per capita side by
side:

```
mean     = 30,373 EUR
median   = 25,733 EUR
```

Ask: *"Both of these are 'the average European country'. They differ by four and a half thousand
euros. Which one goes in the press release?"* Do not answer. That question is the session.

---

## Board plan

| Minutes | |
|---|---|
| **0–08** | The hook and the quote. Establish that summarising is already modelling. |
| **08–30** | **Centre.** Mean from the probability-weighted definition, then the sample formula. Emphasise the $1/n$ weight — one observation can move it without bound. Median and the $(n+1)/2$ position. Then the extensions: trimmed mean, quantile, percentile. Show the mean / trimmed / median ladder on the real data and let them read the direction. |
| **30–52** | **Spread.** Variance and SD. **Spend real time on why $n-1$**: the deviations are from $\bar x$, which is itself chosen to minimise them, so dividing by $n$ is biased downward. Empirical rule with the SAT example. Then IQR, and the trade — resistant, but blind outside the middle 50%. |
| **52–80** | **Shape.** Skewness: the cube preserves sign. Kurtosis: the fourth power, and why $-3$ makes normal the origin. Give both thresholds, $2\sqrt{6/n}$ and $4\sqrt{6/n}$, and compute them live for $n=437$. Land on the four-variable table. |
| **80–90** | Close the loop: return to the opening mean-vs-median gap and let them explain it. Then the forward links to Sessions 03, 04 and 10. |

---

## Worked example — do this live

Compute the shape thresholds by hand for $n = 437$:

$$2\sqrt{6/437} = 2\sqrt{0.01373} = 2(0.1172) = 0.234, \qquad 4\sqrt{6/437} = 0.469$$

Then put $g_1 = 0.881$ next to $0.234$ and $g_2 = -0.013$ next to $0.469$. One clears its threshold
by nearly four times; the other does not come close. **The same variable is badly skewed and
perfectly ordinary in its tails.** That contrast is the point of the whole shape section, and it
takes ninety seconds of arithmetic to make.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"`share_renew` has skewness 0.012 — perfectly symmetric. Is it normally distributed?"*

Let someone say yes. Then show $g_2 = -0.656$ against a threshold of $0.479$: substantially
platykurtic. **Symmetry is not normality.** Skewness and kurtosis are independent, and checking one
tells you nothing about the other.

---

## Misconception to pre-empt

> That the mean and the median are two ways of computing the same thing, and you pick whichever is
> convenient.

They answer different questions. The mean is the balance point and the least-squares minimiser — it
is what Session 03 will fit. The median is the middle of the ordering and is resistant. When they
disagree, that disagreement is information about shape, not a problem to be resolved by choosing
one.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the practice

The two shape formulas with their thresholds, and the mean / trimmed mean / median ladder.

---

[Student notes](README.md) · [Practice brief](../02-practice/README.md)
