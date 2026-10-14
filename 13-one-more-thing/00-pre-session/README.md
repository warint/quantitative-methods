# Session 13 — Pre-session preparation

> **How many independent things are actually being measured?**

> **[Open the pre-session slides](https://warint.github.io/quantitative-methods/session-13-pre-session.html)** ·
> source: [`MATH60033A-S13-Pre-Session.qmd`](MATH60033A-S13-Pre-Session.qmd)

Two things to do before class, and they are the two halves of the practice.
Budget **60–90 minutes**.

| | Before class | Used in the practice for |
|---|---|---|
| **1** | Read the paper | reproducing one of its results |
| **2** | Get both datasets | that, and applying the method to your own angle |

---

## 1. The reading — 45–60 min

**Gygli, Haelg, Potrafke & Sturm (2019), *The KOF Globalisation Index — revisited*, Review of International Organizations 14(3)**
[Read the article](https://doi.org/10.1007/s11558-019-09344-2)

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

The paper has **no replication deposit**, but it rests on a database its publisher puts online for anyone. The course loader fetches it once and caches it, so there is nothing to download by hand:

```python
import qmib

data = qmib.load("kof")
```

Run it **before** class: it is a single download, and thirty people fetching it at once in the room is not a download.

### b) The course data, for your own angle

This is what you apply the method to in the second half.

```python
import qmib

data = qmib.load("kof")      # what the lecture uses
core = qmib.load("core")                 # shared by every group
mine = qmib.load("angle_c_country")      # YOUR angle — see your dictionary

print(data.shape, core.shape, mine.shape)
```

The KOF Globalisation Index — 180 countries, 1970–2023, six sub-dimensions each split into de facto and de jure.

> Run this **before** class. It downloads once and caches as parquet, so the practice works
> whatever the room's wifi is doing. `qmib.catalog()` lists everything available.

Your group's file, columns, units and traps are in your
[data dictionary](../../data/spine/dictionaries/).

---

## 3. Self-check — 15 min

Answer on paper. If you cannot, that is what the lecture is for.

1. In one sentence: what does this session's method let you claim that the previous one did not?
2. What must be true of your data for it to apply?
3. Which claim in the paper rests on this method — and how hard does it lean on it?

---

## Arrive with

- [ ] The paper read and annotated
- [ ] The replication package downloaded and unzipped
- [ ] `qmib.load()` run at least once, so the cache exists
- [ ] Your self-check answers, on paper

---

[Session 13 overview](../README.md) · [The lecture](../01-lecture/README.md) ·
[The practice](../02-practice/README.md)
