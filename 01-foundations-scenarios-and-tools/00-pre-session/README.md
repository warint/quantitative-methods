# Session 01 — Pre-session preparation

> Four things, in this order. Budget **2–3 hours** in total. None of it is optional.

---

## What is in this folder, and what each thing is for

| File | What it is | When you use it |
|---|---|---|
| **`MATH60033A-S01-Pre-Session.pptx`** | **The walkthrough.** Every install step, in order, with checks. | Work through it at your desk. **Start here.** |
| `setup-vscodium-local-llm.md` | A one-page checklist and the troubleshooting table | When something breaks, or to confirm you missed nothing |
| `reading-europe-2031.md` | The critical apparatus for the scenario | *After* reading the scenario itself |
| `verify_environment.py` | The script that proves your setup works | Last — bring its output to class |
| `the-supervised-learning-problem.md` | *Optional.* The vocabulary Session 02 uses, with the derivations written out | If you want a head start on the mathematics |

> The slides and the checklist are **not two explanations of the same thing.** The slides walk you
> through it; the checklist is what you scan afterwards. If they ever disagree, the slides are right.

---

## 1. Build your workstation — 60–90 min

Open **`MATH60033A-S01-Pre-Session.pptx`** and follow it. In order:

1. VS Codium
2. Extensions
3. **The course materials** — download the repository as a ZIP, unzip it directly on your Desktop,
   and keep the folder name `quantitative-methods`
4. Python and the virtual environment
5. Ollama and Qwen 2.5 Coder
6. aider, the agent in your terminal

Then confirm against the [checklist](setup-vscodium-local-llm.md).

> **Session 1 does not include installation time.** Arriving without a working environment means you
> cannot take part in either half.

---

## 2. Read *Europe 2031* — 45–60 min

**<https://europe2031.ai>**

Online, as a [PDF](https://europe2031.ai/europe-2031.pdf), in
[French](https://europe2031.ai/fr), or as audio — all linked from the site.

Published 11 June 2026 by the ARQ Foundation. Twenty-three dated chapters in three parts: a
fact-based prologue, a speculative scenario, an epilogue.

**Annotate as you go.** You will be asked what you underlined and why.

---

## 3. Read the critical brief — 45–60 min

[`reading-europe-2031.md`](reading-europe-2031.md)

The apparatus for the text you have just read: its architecture, where the evidence stops, and the
table of assumptions the conversation works from. It is not a summary and does not replace the
scenario.

---

## 4. Run the verification script — 5 min

From the course folder, with your environment activated:

```bash
python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py
```

Five checks should pass. **Bring the output to class.**

If one fails, the script prints what to do. If you are still stuck, ask your local model — that is
itself a test of whether it works.

---

## Optional, and worth it

**ISLR ch. 2**, free at <https://www.statlearning.com/>. Sections 2.1–2.2 give the vocabulary — $f$,
$\varepsilon$, reducible and irreducible error — used from Session 02 onward.

**[`the-supervised-learning-problem.md`](the-supervised-learning-problem.md)** covers the same
ground in forty minutes, with the derivations written out and five self-check questions: the model
$Y = f(X) + \varepsilon$, loss and risk, why $\mathbb{E}[Y \mid X]$ is the best predictor there is,
and what the irreducible error $\sigma^2$ means.

Neither is needed for Session 01, which has no mathematics in it, and neither is examinable.
Session 02 introduces everything it needs.

---

## What Session 01 actually is

| Half | What happens |
|---|---|
| **First** (~90 min) | [The syllabus](../01-lecture/README.md) — how the course works, how you are judged |
| **Second** (~90 min) | [A conversation](../02-practice/README.md) — *Europe 2031*, and what AI actually is |

No practice session, no code, no deliverable. The methods begin in Session 02 — for which you need
[git and a GitHub account](../../02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md).

---

[Session 01 overview](../README.md)
