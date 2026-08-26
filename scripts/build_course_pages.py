"""Write the per-session pages and the course tables from scripts/course_spec.py.

    python scripts/build_course_pages.py

Sessions 01, 02, 05 and 12 are hand-written and are left alone; the spec marks
them `generated=False`. Everything else — README, pre-session, practice brief,
data page — is regenerated, and the session tables in README.md and SYLLABUS.md
are rewritten between markers so the three can never disagree.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from course_spec import SESSIONS, ordered, generated, MIDTERM_AFTER  # noqa: E402

PREV_NEXT = {k: (f"{int(k)-1:02d}", f"{int(k)+1:02d}") for k in SESSIONS}


def link(num):
    s = SESSIONS.get(num)
    return f"[Session {num}: {s['title']}](../{s['dir']}/README.md)" if s else ""


def session_readme(num, s):
    prev, nxt = PREV_NEXT[num]
    objectives = "\n".join(f"- {o}" for o in s["objectives"])
    return f"""# Session {num} — {s['title']}

> **{s['question']}**

> **[Open the lecture slides](https://warint.github.io/quantitative-methods/session-{num}-lecture.html)** — or read the source at
> [`01-lecture/MATH60033A-S{num}-Lecture.qmd`](01-lecture/MATH60033A-S{num}-Lecture.qmd).

Quantitative Methods in International Business · duration 3h00

---

## Theme of the second half

> ### {s['theme']}

All ten groups attack this question from their own angle, then report in two minutes each.
See [`RESEARCH-MANDATES.md`](../RESEARCH-MANDATES.md) for your project, unit of analysis and data.

---

## Learning objectives

By the end of this session you should be able to:

{objectives}

---

## How this session runs

| Phase | When | What | Where |
|---|---|---|---|
| **Pre-session** | Before class | The reading, and the data it uses | [`00-pre-session/`](00-pre-session/README.md) |
| **First half** (~90 min) | In class | Lecture: {s['methods']} | [`01-lecture/`](01-lecture/README.md) |
| **Second half** (~90 min) | In class | Group work in VS Codium with your local LLM | [`02-practice/`](02-practice/README.md) |

The pre-session work is **not optional**. The lecture assumes you arrive having read the paper; the
practice assumes you arrive with the data loaded.

---

## Data for this session

**{s['dataset_note'].capitalize()}** — one line to load it:

```python
import qmib
data = qmib.load("{s['dataset']}")
```

See [`data/README.md`](data/README.md) and your group's
[data dictionary](../data/spine/dictionaries/).

---

## Deliverable

In `02-practice/submissions/group-XX/`: {s['deliverable']}.

---

[<- {link(prev)}](../{SESSIONS[prev]['dir']}/README.md) | [{link(nxt)} ->](../{SESSIONS[nxt]['dir']}/README.md)
""" if nxt in SESSIONS else ""


def pre_session(num, s):
    return f"""# Session {num} — Pre-session preparation

> **{s['question']}**

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
data = qmib.load("{s['dataset']}")
print(data.shape)
```

{s['dataset_note'].capitalize()}.

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

[Session {num} overview](../README.md) · [The lecture](../01-lecture/README.md)
"""


def practice(num, s):
    loses = "\n".join(f"- {m}" for m in s["loses_marks"])
    return f"""# Session {num} — Group practice (second half, ~90 min)

# {s['title']}

---

## The theme of this session

> # {s['theme']}

All ten groups attack this question, each on **its own project**, and the last twenty minutes
assemble the answers.

---

## What you are doing

The lecture showed the method on the session's dataset. You now apply it to **your own angle**, and
to the question your group is actually trying to answer
([`RESEARCH-MANDATES.md`](../../RESEARCH-MANDATES.md)).

The deliverable is not a printout. It is a **decision**, with the reason written down.

---

## Before you start

Everyone in the group pushes at least once this session. Replace `XX` with your group number —
group 07 uses `group-07`.

```bash
git checkout -b group-XX
mkdir -p {s['dir']}/02-practice/submissions/group-XX
```

---

## 1 · Reproduce one result from the paper — 20 min

Take the result the pre-session reading rests on, and reproduce it — or establish that you cannot,
and say precisely where it breaks. A failed reproduction that is diagnosed earns full marks; one
that is not attempted earns none.

```python
import qmib
data = qmib.load("{s['dataset']}")
```

---

## 2 · Apply the method to your own angle — 35 min

```python
core = qmib.load("core")
mine = qmib.load("angle_c_country")     # your angle — see your dictionary
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

Fit the session's method on your own data. Report what the lecture said to report, in the units of
your own variables.

---

## 3 · Break one assumption — 15 min

Every method in this course rests on something. Find the assumption this one rests on hardest, break
it deliberately, and record what happened to your answer. **This is the part that carries the
marks.**

---

## 4 · Write it down — 20 min

A 250-word note in your submissions folder:

- What you found, in units
- Which assumption you broke, and what it did
- What this result does **not** license you to claim

---

## Submitting

```bash
git add {s['dir']}/02-practice/submissions/group-XX
git commit -m "Session {num} practice — group XX"
git push -u origin group-XX
```

Everyone pushes at least once. The log is the record of participation.

---

## What loses marks

{loses}

---

[<- The lecture](../01-lecture/README.md) · [Session {num} overview](../README.md)
"""


def data_page(num, s):
    return f"""# Session {num} — Data

**{s['dataset_note'].capitalize()}**

```python
import qmib
data = qmib.load("{s['dataset']}")
```

One call. It resolves a local cache first, then the committed spine, then the published URL —
downloading once and caching as parquet. After the first run the practice works offline.

- Everything available: `qmib.catalog()`
- Your group's columns, units and traps: [data dictionaries](../../data/spine/dictionaries/)
- Provenance and flags: [`data/spine/PROVENANCE.md`](../../data/spine/PROVENANCE.md)

---

## Rules for this folder

- Raw data files are **git-ignored**. Never commit them; `qmib` fetches and caches instead.
- The synthetic spine is the exception: small, licence-free, committed deliberately so the
  practice runs with no network.
- If you bring in a dataset of your own, record its source, date and licence in `PROVENANCE.md`.
"""


def replace_between(text, start_marker, end_marker, new):
    a = text.index(start_marker) + len(start_marker)
    b = text.index(end_marker)
    return text[:a] + new + text[b:]


def session_table(link_prefix=""):
    rows = []
    for num, s in ordered():
        rows.append(f"| [{num}]({link_prefix}{s['dir']}/README.md) | {s['title']} | "
                    f"{s['methods']} | {s['question'] if num in ('01', '12') else s['theme']} |")
        if num == MIDTERM_AFTER:
            rows.append("| — | **MIDTERM** *(in class, covering Sessions 1–6)* | | |")
    return "\n".join(rows)


def main():
    written = 0
    for num, s in generated():
        d = ROOT / s["dir"]
        (d / "README.md").write_text(session_readme(num, s), encoding="utf-8")
        (d / "00-pre-session").mkdir(exist_ok=True)
        (d / "00-pre-session/README.md").write_text(pre_session(num, s), encoding="utf-8")
        (d / "02-practice").mkdir(exist_ok=True)
        (d / "02-practice/README.md").write_text(practice(num, s), encoding="utf-8")
        (d / "data").mkdir(exist_ok=True)
        (d / "data/README.md").write_text(data_page(num, s), encoding="utf-8")
        written += 4
        print(f"  session {num}: 4 pages")
    print(f"\n{written} pages written from the spec")


if __name__ == "__main__":
    main()
