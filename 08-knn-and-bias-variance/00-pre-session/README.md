# Session 08 — Pre-session preparation

> **Flexible, or just unstable?**

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-08-pre-session.html)** ·
> source: [`MATH60033A-S08-Pre-Session.qmd`](MATH60033A-S08-Pre-Session.qmd)

Two things to do before class, and they are the two halves of the practice.
Budget **60–90 minutes**.

| | Before class | Used in the practice for |
|---|---|---|
| **1** | Read the paper | reproducing one of its results |
| **2** | Get both datasets | that, and applying the method to your own angle |

---

## 1. The reading — 45–60 min

**Bluwstein, Buckmann, Joseph, Kapadia & Şimşek (2023), *Credit growth, the yield curve and financial crisis prediction: evidence from a machine learning approach*, Journal of International Economics 145**
[Read the article](https://doi.org/10.1016/j.jinteco.2023.103773)

Read for the **argument**, not for coverage:

| | What to look for |
|---|---|
| **1** | The research question, in one sentence |
| **2** | The method or design, and why they chose it |
| **3** | The strongest single piece of evidence |
| **4** | One limitation you would raise as a referee |

**Annotate as you go.** You will be asked what you underlined and why.

---

## 2. The data — 10 min

You need **two** datasets in the practice, and both should be on your machine before you arrive.

### a) The paper's data

This is what you work against in the first twenty minutes of the practice.

The paper has **no replication deposit**, but it rests on the Jordà–Schularick–Taylor
Macrohistory Database — 18 economies, 1870–2020, 88 financial crises. The course site serves it
with the paper's predictors already derived. In a folder of your own (set up as on the last
pre-session slide: a `.venv` and `pip install pandas numpy matplotlib scikit-learn`):

```python
import pandas as pd

SITE = "https://warint.github.io/quantitative-methods/data/"
jst = pd.read_csv(SITE + "session-08/jst_crises.csv")
print(jst.shape)                              # (2718, 12)
```

### b) The course data, for your own angle

This is what you apply the method to in the second half.

```python
core = pd.read_csv(SITE + "core.csv")                  # shared by every group
mine = pd.read_csv(SITE + "angle_c_country.csv")       # YOUR angle — see your dictionary
print(core.shape, mine.shape)
```

Your group's file, columns, units and traps are in your
[data dictionary](../../data/spine/dictionaries/). Then download the practice script into the same
folder: [`session08_practice.py`](https://warint.github.io/quantitative-methods/session-08/session08_practice.py).

> **macOS, Python from python.org:** if reading fails with `CERTIFICATE_VERIFY_FAILED`, run
> `open /Applications/Python\ 3*/Install\ Certificates.command` once.

---

## 3. Self-check — 15 min

Answer on paper. If you cannot, that is what the lecture is for.

1. In one sentence: what does this session's method let you claim that the previous one did not?
2. What must be true of your data for it to apply?
3. Which claim in the paper rests on this method — and how hard does it lean on it?

---

## Arrive with

- [ ] The paper read and annotated
- [ ] Both datasets read once on your machine
- [ ] `session08_practice.py` saved in your session-08 folder
- [ ] Your self-check answers, on paper

---

[Session 08 overview](../README.md) · [The lecture](../01-lecture/README.md) ·
[The practice](../02-practice/README.md)
