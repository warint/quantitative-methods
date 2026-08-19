# Session 08 — Unsupervised Learning I: PCA, the SVD, and Factor Models in Macroeconomics

> **Two hundred macro series move together. How many things are actually happening?**

`MATH60033A` · Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### How many independent things are we actually measuring?

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your angle, unit of analysis and data.

---


## Learning objectives

By the end of this session you should be able to:

- Derive principal components as the successive maximisers of projected variance, and via the SVD.
- Prove the Eckart-Young theorem's consequence: PCA gives the best low-rank approximation.
- Connect PCA to the approximate factor model of Stock & Watson and to diffusion-index forecasting.
- Select the number of factors using scree plots, cumulative variance, and the Bai-Ng information criteria.
- Build a nowcasting model from extracted factors and evaluate it out-of-sample.

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

**FRED-MD (revisited, from Session 5) + a target series for nowcasting**

Source: Federal Reserve Bank of St. Louis
URL: https://www.stlouisfed.org/research/economists/mccracken/fred-databases

Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

`02-lab/submissions/group-XX/` with the factor-selection comparison table, the
loadings interpretation with its self-critique, the three-way forecast comparison, and a 300-word
note quantifying the look-ahead bias and explaining to a non-technical reader why it is fraud rather
than optimism.

---

## Before the next session

- ISLR ch. 12.4 (clustering) before Session 9.

---

[<- Session 07: Trees, Forests, and Gradient Boosting](../07-trees-forests-boosting/README.md) | [Session 09: Unsupervised Learning II: Clustering, Embeddings, and Text as Data ->](../09-clustering-and-text-as-data/README.md)
