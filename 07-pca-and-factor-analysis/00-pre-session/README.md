# Session 07 — Pre-session preparation

> **How many independent things are actually being measured?**

Budget **60–90 minutes**. None of it is optional.

---

## 1. Read the paper — 45–60 min

See [`REPLICATIONS.md`](../../REPLICATIONS.md) for this session's article and its replication
package. Read it for the **argument**, not for coverage:

| | What to look for |
|---|---|
| **1** | The research question, in one sentence |
| **2** | The method or design, and why they chose it |
| **3** | The strongest single piece of evidence |
| **4** | One limitation you would raise as a referee |

**Annotate as you go.** You will be asked what you underlined and why.

---

## 2. Load the data — 10 min

The practice uses the same data the lecture does. Load it once so it is cached before class:

```python
import qmib
data = qmib.load("movies")
print(data.shape)
```

45,000 films — budget, popularity, revenue, runtime and votes.

> Run this **before** you arrive. It downloads once and caches locally, so the practice works
> whatever the room's wifi is doing.

---

## 3. Self-check — 15 min

Answer on paper, before the lecture. If you cannot, that is what the lecture is for.

1. In one sentence: what does this session's method let you claim that the previous one did not?
2. What must be true of your data for it to apply?
3. Which of the four evaluations in the paper above rests on this method?

---

## What the lecture assumes

That you have read the paper, run the two lines above, and attempted the self-check.

---

[Session 07 overview](../README.md) · [The lecture](../01-lecture/README.md)
