"""Write the pre-session and practice decks for sessions 02–11.

    python scripts/build_session_decks.py
    scripts/render_session_lectures.sh
    python scripts/build_docs.py

Session 01's three decks are hand-written — its pre-session is a software install
and its practice is a discussion, neither of which fits the pattern below. Session
12 is the presentations. Everything in between takes the same shape:

  pre-session   the paper, the data, the self-check
  practice      reproduce, apply to your own angle, break an assumption, report

The content comes from scripts/course_spec.py, so a deck cannot describe a
session differently from that session's README.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from course_spec import SESSIONS  # noqa: E402

RED, PAPER = "#E3120B", "#F7F4ED"


def header(num, kind, title, subtitle):
    return f"""---
title: "Session {int(num)}: {title}"
subtitle: "{subtitle}"
author: "Thierry Warin, PhD"
institute: "HEC Montréal"
course-session: "{num}"
format:
  revealjs:
    theme: [default, ../../slides/economist.scss]
    embed-resources: true
    slide-number: c/t
    slide-level: 2
    history: false
    transition: none
    navigation-mode: linear
    controls: true
    progress: true
    width: 1280
    height: 760
    margin: 0.06
    smaller: true
    footer: "MATH60033A · Session {num} {kind} · Thierry Warin, PhD · HEC Montréal"
---
"""


GIT_SLIDES = """
# Session 02 only: your group repository {{background-color="{RED}" style="color:{PAPER}"}}

::: {{style="margin-top: 1.0em; color:{PAPER}"}}
### From this session on, your commit history is part of the record
:::

## Install git — you may already have it

```bash
git --version
```

::: {{.check}}
**macOS.** Git ships with Apple's Command Line Tools, so most Macs already have it. If the command
is not found, macOS offers to install them — accept — or run `xcode-select --install`.
**You do not need Homebrew.**
:::

::: {{.tight}}
- **Windows** — [git-scm.com/downloads](https://git-scm.com/downloads), accept the defaults, then
  restart VS Codium
- **Linux** — `sudo apt install git`
:::

## Tell git who you are

```bash
git config --global user.name  "Your Full Name"
git config --global user.email "you@example.com"
```

::: {{.warn}}
Use your **real** name and the email on your GitHub account. The commit log is one of the records
used to check that all three of you did the work — and it only identifies you if you set this.
:::

## Already have your three? Do a trial run

Groups are confirmed in Session 04 — but if you have already agreed to work together, rehearse the
whole cycle now. Ten minutes, and it removes the one thing that reliably eats practice time.

**One person, once:**

```bash
git checkout -b group-07          # your number, not 07
git push -u origin group-07
```

**The other two:**

```bash
git fetch origin
git checkout group-07
```

## Then each of you pushes, one at a time

```bash
git pull                          # always pull before you start

echo "- Ana tested the push" >> \\
  02-exploratory-data-analysis/02-practice/submissions/group-07/NOTES.md

git add 02-exploratory-data-analysis/02-practice/submissions/group-07/NOTES.md
git commit -m "Ana: trial push"
git push
```

::: {{.check}}
When all three are done, `git log --oneline -5` should show **three commits with three different
author names**. That is exactly what the participation record looks like.
:::

::: {{.muted}}
A rejected push almost always means someone pushed in between — `git pull` first. That is normal.
Full guide: [`setup-git-and-github.md`](setup-git-and-github.md)
:::
"""

def pre_session_deck(num, s):
    objectives = "\n".join(f"- {o}" for o in s["objectives"])
    return header(num, "pre-session", "Before the session", s["question"]) + f"""
# Before the session {{background-color="{RED}" style="color:{PAPER}"}}

::: {{style="margin-top: 1.0em; color:{PAPER}"}}
### {s['question']}
:::

## What to do, and how long it takes

| | | |
|---|---|---|
| **1** | Read the paper | 45–60 min |
| **2** | Load the data | 10 min |
| **3** | Attempt the self-check | 15 min |

::: {{.warn}}
The lecture assumes all three are done. The practice assumes the data is already cached on your
machine.
:::

## 1 · Read the paper

The article and its replication package are listed in
[`REPLICATIONS.md`](../../REPLICATIONS.md).

Read for the **argument**, not for coverage. Annotate four things:

| | |
|---|---|
| **1** | The research question, in one sentence |
| **2** | The method or design, and why they chose it |
| **3** | The strongest single piece of evidence |
| **4** | One limitation you would raise as a referee |

::: {{.muted}}
You will be asked what you underlined, and why. Two minutes, three students, at the start.
:::

## 2 · Load the data

{s['dataset_note'].capitalize()}.

```python
import qmib

data = qmib.load("{s['dataset']}")
print(data.shape)
```

::: {{.check}}
Run this **before** you arrive. It downloads once and caches locally, so the practice works
whatever the room's wifi is doing.
:::

::: {{.muted}}
Everything available: `qmib.catalog()`
:::

## 3 · Self-check

Answer on paper. If you cannot, that is what the lecture is for.

::: {{.tight}}
1. In one sentence: what does this session's method let you claim that the previous one did not?
2. What must be true of your data for it to apply?
3. Which claim in the paper rests on this method — and how hard does it lean on it?
:::

## What the session will ask of you

By the end you should be able to:

::: {{.tight}}
{objectives}
:::

::: {{.get}}
Bring: the annotated paper, the cached data, and your self-check answers.
:::

## Running the code

Everything runs in the **VS Codium terminal**, with the project environment active:

```bash
source .venv/bin/activate        # macOS / Linux
python
```

::: {{.muted}}
Missing a package? `pip install -r requirements.txt` from the repository root.
:::

::: {{.muted}}
Session {num}: [`README.md`](../README.md) ·
the lecture: [`01-lecture/`](../01-lecture/README.md)
:::
""" + (GIT_SLIDES.format(RED=RED, PAPER=PAPER) if s.get("pre_session_extra") == "git" else "")


def practice_deck(num, s):
    loses = "\n".join(f"- {m}" for m in s["loses_marks"])
    return header(num, "practice", "Practice", s["theme"]) + f"""
# Practice {{background-color="{RED}" style="color:{PAPER}"}}

::: {{style="margin-top: 1.0em; color:{PAPER}"}}
### {s['theme']}
:::

## Ninety minutes

| | | |
|---|---|---|
| **00–20** | Reproduce | one result from the paper you read |
| **20–55** | Apply | the method, to **your own angle** |
| **55–70** | Break | one assumption, deliberately |
| **70–90** | Write, and report | 250 words, then two minutes to the room |

::: {{.warn}}
The presenter is drawn **at random** when your group is called. All three of you prepare.
:::

## Before you start

Everyone pushes at least once. Replace `XX` with your group number — group 07 uses `group-07`.

```bash
git checkout -b group-XX
mkdir -p {s['dir']}/02-practice/submissions/group-XX
```

::: {{.muted}}
The git log is the participation record. It is not a formality.
:::

## 1 · Reproduce — 20 min

Take the result the paper rests on, and reproduce it.

```python
import qmib

data = qmib.load("{s['dataset']}")
```

::: {{.check}}
A failed reproduction that you **diagnose** earns full marks. One you do not attempt earns none.
:::

::: {{.muted}}
"It did not work" is not a diagnosis. Where did it stop, and what did you check?
:::

## 2 · Apply to your own angle — 35 min

```python
core = qmib.load("core")
mine = qmib.load("angle_c_country")     # your angle — see your dictionary
df   = core.merge(mine, on=["geo", "time"], how="inner")
```

Fit the session's method on **your** data, and report what the lecture said to report — in the
units of your own variables.

::: {{.warn}}
A coefficient without units is not a finding.
:::

## 3 · Break one assumption — 15 min

Every method in this course rests on something.

::: {{.step}}
Find the assumption this one leans on hardest. Break it **deliberately**. Record what happened to
your answer.
:::

::: {{.check}}
This is the part that carries the marks. A group that shows how its result falls apart understands
it; a group that only shows it holding does not yet know.
:::

## 4 · Write it down — 20 min

250 words in your submissions folder:

::: {{.tight}}
- What you found, **in units**
- Which assumption you broke, and what it did
- What this result does **not** license you to claim
:::

::: {{.muted}}
And the standing rule: one LLM output you identified as wrong, and how you established that.
:::

## Submitting

```bash
git add {s['dir']}/02-practice/submissions/group-XX
git commit -m "Session {num} practice — group XX"
git push -u origin group-XX
```

::: {{.get}}
**Deliverable.** {s['deliverable'].capitalize()}.
:::

## What loses marks

::: {{.tight}}
{loses}
:::

::: {{.warn}}
And everywhere in this course: an association described in causal language.
:::

## Two-minute report

| | |
|---|---|
| **One number** | with its units and its uncertainty |
| **One assumption** | the one you broke, and what happened |
| **One limit** | what you cannot claim from this |

::: {{.muted}}
Listen for traceable evidence, not confidence of delivery.
:::
"""


def main():
    written = 0
    for num in sorted(SESSIONS):
        if num in ("01", "12"):
            continue
        s = SESSIONS[num]
        d = ROOT / s["dir"]
        (d / "00-pre-session").mkdir(exist_ok=True)
        (d / "00-pre-session" / f"MATH60033A-S{num}-Pre-Session.qmd").write_text(
            pre_session_deck(num, s), encoding="utf-8")
        (d / "02-practice").mkdir(exist_ok=True)
        (d / "02-practice" / f"MATH60033A-S{num}-Practice.qmd").write_text(
            practice_deck(num, s), encoding="utf-8")
        written += 2
        print(f"  session {num}: pre-session + practice deck")
    print(f"\n{written} decks written")


if __name__ == "__main__":
    main()
