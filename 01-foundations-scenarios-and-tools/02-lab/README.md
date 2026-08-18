# Session 01 — Group lab (second half, ~90 min)

# Stress-testing an assumption with a local LLM

---

## Brief

Groups of 3-4. Each group is assigned **one** assumption from the *Europe 2031*
critical-reading table (see `00-pre-session/reading-europe-2031.md`, section 5). Your task is to
turn a narrative claim into something a statistician could actually test.

You will use your **local** LLM as a sparring partner, not as an oracle. Everything it tells you
must be checked. Record at least one instance where you caught it being wrong or unverifiable -
this is a graded part of the deliverable.

---

## Tasks

1. Run `python 00-pre-session/verify_environment.py`. Paste the output into your notebook. If it fails, fix it before continuing.
2. State your assigned assumption in one sentence, in your own words. Then state its *negation*.
3. Propose **two** observable indicators that would move your belief about the assumption. For each, name the publishing institution and the release frequency.
4. For each indicator, specify a trigger point and horizon in the form: *'If I_t exceeds tau before date T, the assumption gains support.'*
5. Ask your local LLM to argue **against** your indicators. Copy its strongest objection into your notebook and respond to it in two or three sentences.
6. Identify one claim the LLM made that you could not verify. Flag it explicitly. Explain how you would verify it.
7. Open `02-lab/starter/session01_lab.py` and complete the `simulate_indicator` function so it generates a synthetic indicator path and marks the first crossing of your trigger point. Plot it.

---

## Deliverable

A one-page memo (`02-lab/submissions/group-XX.md`) containing: the assumption,
its negation, two indicators with sources and frequencies, two trigger points with horizons, one
falsifier, the LLM's strongest objection with your reply, and one flagged unverifiable claim.
Attach your indicator plot. **Five minutes of oral presentation** in the last 20 minutes of class.

Create your group's folder as `submissions/group-XX/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this lab requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "Argue that the following indicator is a poor proxy for the underlying assumption. Be specific about measurement problems: <paste indicator>"
- "List three ways this trigger point could be crossed for reasons unrelated to the assumption it is meant to test."
- "I will give you a claim. Tell me what data source would falsify it, and tell me if you are uncertain whether that source exists."

**Required in every deliverable:** at least one instance where you identified an LLM output as
wrong, unverifiable, or misleading — with an explanation of how you established that.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Read the brief, split the tasks, agree on interfaces |
| 10–70 | Implementation |
| 70–80 | Write the deliverable text (not an afterthought) |
| 80–90 | Presentations and cross-group questions |

---

[Back to session 01](../README.md) · [<- Lecture notes](../01-lecture/README.md)
