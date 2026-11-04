# Session 08 — Lecture (first half, ~90 min)

# K-Nearest Neighbours and the Bias–Variance Trade-off

> **Flexible, or just unstable?**

---

> **Python cheatsheet — [session 08](https://warint.github.io/quantitative-methods/python-cheatsheet-08.pdf)** (PDF) ·
> source: [`PYTHON-CHEATSHEET.qmd`](../PYTHON-CHEATSHEET.qmd)
>
> How to start Python in VS Codium on your platform, how to make a file and run it,
> the DataFrame basics, and every name taught in sessions 1 to 8 with a
> line showing it in use. Print it.

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-08-lecture.html)** ·
> source: [`MATH60033A-S08-Lecture.qmd`](MATH60033A-S08-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is plain **Python** with four packages
(`pandas numpy matplotlib scikit-learn`), and reads its data by URL: copy the blocks in order into a
file of your own and run it. The financial example is two files, to download into the same folder:

- [`session08_1_train.py`](https://warint.github.io/quantitative-methods/session-08/session08_1_train.py) —
  chooses $K$ by cross-validation, judges the model once on 2005, and saves it
- [`session08_2_predict.py`](https://warint.github.io/quantitative-methods/session-08/session08_2_predict.py) —
  loads the saved model and predicts one new date, out of sample

---

## What the lecture covers

1. **K-nearest neighbours, explained** — classification, the vote of the neighbours, KNN by hand,
   the choice of $K$ and the bias–variance trade-off
2. **Cross-validation: why it is magical** — the power of sampling, out-of-sample prediction, and
   how it compares with the classical, in-sample way of judging a model
3. **A financial example** — can KNN predict the stock market? Two files: one trains with
   cross-validation, one predicts a new date
4. **Big lessons from ML**

---

## Learning objectives

By the end of the session you should be able to:

- Explain how KNN classifies, by **the vote of the $K$ nearest neighbours**
- Compute a Euclidean distance and find nearest neighbours **by hand**
- Explain why KNN requires **standardised** predictors
- Choose $k$ by cross-validation, and read the trade-off the curve shows
- Say why **cross-validation** estimates out-of-sample error, and what classical in-sample fit cannot tell you
- Say what happens to KNN as the number of predictors grows

---

## The data

**Smarket: 1,250 days of S&P 500 returns, 2001–2005 (ISLR)**, read by URL:

```python
import pandas as pd
URL = "https://raw.githubusercontent.com/intro-stat-learning/ISLP/main/ISLP/data/Smarket.csv"
smarket = pd.read_csv(URL)
```

---

## Running the code

In a folder of your own, opened in VS Codium, once:

```bash
pip install pandas numpy matplotlib scikit-learn
python session08_1_train.py      # trains, and writes knn_smarket.joblib next to it
python session08_2_predict.py    # loads it, and predicts one new date
```

On macOS with Python from python.org, if reading the data fails with `CERTIFICATE_VERIFY_FAILED`,
run `open /Applications/Python\ 3*/Install\ Certificates.command` once.

---

## What loses marks

- Running KNN on unstandardised predictors
- Choosing $k$ on the test set
- Reporting accuracy with no benchmark
- Treating a low training error as evidence of anything

---

[Back to session 08](../README.md) · [On to the practice ->](../02-practice/README.md) · [The lab for this session ↗](https://warin.ca/qmib-labs/qmib-lab-08.html)
