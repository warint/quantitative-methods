# Session 01 — Foundations: Scenarios, Tools, and the Supervised Learning Problem

> **Before we can model the future, what exactly are we claiming to know about it?**

`MATH60033A` · Quantitative Methods in International Business · duration 3h00

---


## Learning objectives

By the end of this session you should be able to:

- Distinguish a **scenario** from a **forecast**, and explain why the difference matters for any quantitative model you build.
- State the supervised learning problem formally: the data-generating process, the loss function, and the target of estimation.
- Articulate the **prediction vs. inference** distinction and identify which one a given economic question requires.
- Operate a fully local analytical workstation: VS Codium, a Python environment, and a locally hosted LLM.
- Convert a narrative assumption into a **measurable indicator** with an explicit trigger point.

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

**No external dataset (environment smoke test only)**

Source: Generated locally by `00-pre-session/verify_environment.py`


Download instructions: [`data/README.md`](data/README.md)

---

## Deliverable

A one-page memo (`02-lab/submissions/group-XX.md`) containing: the assumption,
its negation, two indicators with sources and frequencies, two trigger points with horizons, one
falsifier, the LLM's strongest objection with your reply, and one flagged unverifiable claim.
Attach your indicator plot. **Five minutes of oral presentation** in the last 20 minutes of class.

---

## Before the next session

- ISLR ch. 3.1-3.2 (simple and multiple linear regression) before Session 2.
- Optional: skim the European Commission JRC's four reference foresight scenarios for 2040 and note how they differ in *method* from *Europe 2031*.

---

[Session 02: Data, Vectors, and the Geometry of Least Squares ->](../02-geometry-of-least-squares/README.md)
