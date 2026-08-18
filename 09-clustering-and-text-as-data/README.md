# Session 09 — Unsupervised Learning II: Clustering, Embeddings, and Text as Data

> **How do you measure something that only exists as words?**

`MATH60033A` · Machine Learning Methods for Economics · duration 3h00

---

## Theme of the second half

> ### Do European countries fall into types — and does the language of policy track them?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your angle, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- State the k-means objective, derive Lloyd's algorithm, and explain why it converges but not to a global optimum.
- Compare k-means, hierarchical clustering, and Gaussian mixtures in terms of the assumptions each imposes.
- Choose $k$ using silhouette, gap statistic, and the elbow - and explain why none is definitive.
- Construct document representations: TF-IDF, and dense embeddings from a local model.
- Build a quantitative index from an unstructured corpus and defend its validity.

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | Reading, concept review, data download, self-check | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: the mathematics of the method | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-lab/`](02-lab/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive with the reading done and
a working environment; the lab assumes you arrive with the data already downloaded.

---

## Data for this session

**A corpus of central bank communications (ECB / Bank of Canada / Fed statements) + a regional economic panel**

Source: ECB press releases; Eurostat regional accounts
URL: https://www.ecb.europa.eu/press/pr/date/html/index.en.html

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-lab/submissions/group-XX/` with the cluster map, the three-criterion $k$
selection, the null-data comparison, both uncertainty indices plotted together, and a 500-word
validity report structured under the four headings in section 9.5. **A negative finding, clearly
demonstrated, receives full marks.**

---

## Before the next session

- Chernozhukov et al. (2018) on double/debiased ML - the introduction and section 1 - before Session 10.
- Groups must confirm their final-project dataset with the instructor before Session 10.

---

[<- Session 08: Unsupervised Learning I: PCA, the SVD, and Factor Models in Macroeconomics](../08-pca-and-factor-models/README.md) | [Session 10: Causal Machine Learning: Double/Debiased ML and Heterogeneous Effects ->](../10-causal-machine-learning/README.md)
