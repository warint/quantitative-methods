# Session 01 — Pre-session preparation

> Complete **all four steps** before class. Expect 90–120 minutes.

---

## ⚠️ Session 1 only — install your environment first

Before anything else, work through **[`setup-vscodium-local-llm.md`](setup-vscodium-local-llm.md)**.
Budget 60–90 minutes. Session 1 does **not** include installation time; students arriving without a
working environment will not be able to participate in the lab.

Then read **[`reading-europe-2031.md`](reading-europe-2031.md)**.

---

## Step 1 — Reading

**Europe 2031: a future scenario for Europe - reading brief**  
Source: `00-pre-session/reading-europe-2031.md` (in this folder)  
*Why:* The framing case for the whole course. Read it as a *stress test*, not a prediction.

**Setup guide: VS Codium + local LLM**  
Source: `00-pre-session/setup-vscodium-local-llm.md` (in this folder)  
*Why:* You must arrive with a working environment. Session 1 does not include installation time.

**James, Witten, Hastie & Tibshirani, *An Introduction to Statistical Learning* (ISLR), ch. 2**  
Source: Free PDF: https://www.statlearning.com/  
*Why:* Sections 2.1-2.2 give the vocabulary (f, epsilon, reducible vs. irreducible error) we use from Session 2 onward.


---

## Step 2 — Concepts to review

Three ideas from the reading you should be able to restate in your own words before class.

**1. A scenario is a conditional object.** *Europe 2031* is published as an independent narrative
(11 June 2026), with a fact-based prologue running January 2025 - June 2026 and a speculative path
running August 2026 - March 2031, plus a June 2034 epilogue. It is **not** an official European
Union forecast. Its numbers are *internal parameters of a story*, not measured predictions.

**2. Its numbers are parameters, not estimates.** The narrative assigns the United States
255.1 GW of AI compute in 2031 against Europe's 20.9 GW - a ratio of roughly 12.2 - and annual
buildout of 29.3 GW against 1.9 GW, a ratio of roughly 15.7. Ask yourself: what would have to be
*true* for these to be the right order of magnitude? That question is the seed of every model in
this course.

**3. Every model you will build in this course is also a scenario.** A regression is a story about
how the world generates data, with the story's assumptions written as equations. The honesty of a
model lies in how explicitly those assumptions are stated - which is precisely the standard we will
apply to *Europe 2031*.

---

## Step 3 — Your data this week

Session 01 uses no external dataset — the environment check generates its own. Your angle and its file are assigned in class; see [`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md).

<details>
<summary>Teaching dataset for the method exercise (optional)</summary>

**No external dataset (environment smoke test only)**

Source: Generated locally by `00-pre-session/verify_environment.py`


Session 1 uses a synthetic dataset created on your own machine. This confirms your
environment works before we depend on real downloads in Session 2.

Use this if you want to see the method work on known ground before turning it on your own angle.
The result you report must come from **your angle**.

</details>

---

## Step 4 — Self-check

Answer these **in writing** before class. You will not hand them in, but the lecture assumes you
have attempted them. If you cannot answer one, bring the question.

1. In one sentence, what is the difference between *Europe 2031* and a European Commission forecast?
2. The scenario reports a US:EU compute ratio of about 12.2 in 2031. Is that number evidence, or an assumption? Justify your answer.
3. Give one economic question that requires **prediction** and one that requires **inference**. What changes in how you would evaluate the model?
4. Open a terminal and run `python -c "import numpy, pandas, sklearn; print('ok')"`. Does it print `ok`?
5. Ask your local LLM to explain the bias-variance tradeoff. Did it answer without any network connection? How would you verify that?

---

## Using your local LLM on the preparation

Your local model is a study partner, not an answer key. Ask it to *explain*, to *quiz you*, and to
*argue against you*. Verify everything it says against the reading.

Prompts that work well for this session:

- "Argue that the following indicator is a poor proxy for the underlying assumption. Be specific about measurement problems: <paste indicator>"
- "List three ways this trigger point could be crossed for reasons unrelated to the assumption it is meant to test."
- "I will give you a claim. Tell me what data source would falsify it, and tell me if you are uncertain whether that source exists."

> **Standing rule for this course.** Whenever you use the LLM in a deliverable, you must be able to
> say what you checked and how. An unverified claim from a language model has the same evidential
> status as an unverified claim from a stranger.

---

[Back to session 01](../README.md)
