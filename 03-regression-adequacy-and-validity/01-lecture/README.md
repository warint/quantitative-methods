# Session 03 — Lecture (first half, ~90 min)

# Regression: Adequacy, Validity, and Robustness

> **You have fitted a regression. Can it be trusted?**

---

## How to use this page

The lecture is delivered from the slides:

> **[Open the deck](https://warint.github.io/quantitative-methods/session-03-lecture.html)** ·
> source: [`MATH60033A-S03-Lecture.qmd`](MATH60033A-S03-Lecture.qmd)

This page is the companion: what the session covers, what you should be able to do afterwards, and
what loses marks. Every code example in the deck is **Python**, and every dataset loads with one
call — `qmib.load("core")`.

---

## What the lecture covers

1. **Why Evaluate Models?**
2. **Introduction: Key Aspects of Model Evaluation**
3. **Key Aspects of Model Evaluation**
4. **Models: Assessing the adequacy**
5. **Goodness-of-Fit --- [(R^2)]{.math .inline}**
6. **Adjusted [(R^2)]{.math .inline} and RSE**
7. **Models: assessing the validity**
8. **Normality of Residuals**
9. **The Window Into Model Adequacy**
10. **Model Robustness/Parsimony and Selection**

---

## Learning objectives

By the end of the session you should be able to:

- Read a **residuals-versus-fitted** plot and say what structure it reveals
- Diagnose non-constant variance from a **scale–location** plot
- Compute **leverage** and say which observations have the power to move the line
- Use **Cook's distance** to separate an outlier from an influential point
- Compare candidate models on **AIC**, and say why that is not model selection

---

## The data

**The same regression session 02 fitted — gdp per capita on productivity**

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

[Back to session 03](../README.md) · [On to the practice ->](../02-practice/README.md)
