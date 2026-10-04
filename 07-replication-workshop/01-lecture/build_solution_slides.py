"""Write the two solution slides for each paper of the session 07 deck.

    python 07-replication-workshop/01-lecture/build_solution_slides.py

For every starter script in ../02-practice/starter/ this writes an include file,
_solutions-rN.qmd, holding two slides:

  * "The script, to copy" — a link to the file on GitHub, and the whole file in
    consecutive tabs short enough to fit on screen, to paste in order;
  * "The solutions, step by step" — one tab per `# Step N ·` block of the script,
    executed when the deck renders, so the code and the results on the slides
    are the script's own.

The deck pulls them in with {{< include _solutions-rN.qmd >}}. Re-run this after
editing a starter script, then re-render the deck. Never edit the include files
by hand: they are regenerated from the scripts.
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STARTER = HERE.parent / "02-practice" / "starter"

PAPERS = [
    ("r1", "r1_fraiberger_2021.py"),
    ("r2", "r2_amsili_2024.py"),
    ("r3", "r3_saganowski_2019.py"),
    ("r4", "r4_blonigen_piger_2014.py"),
    ("r5", "r5_topalova_khandelwal_2011.py"),
]

STEP = re.compile(r"^# Step (\d+) · (.*)$", re.M)


def split(script):
    """The set-up (docstring dropped) and the numbered steps of one script."""
    body = re.sub(r'\A""".*?"""\n+', "", script, flags=re.S)
    marks = list(STEP.finditer(body))
    setup = body[:marks[0].start()].strip()
    steps = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        steps.append((m.group(1), m.group(2).strip(), body[m.start():end].strip()))
    return setup, steps


GITHUB = "https://github.com/warint/quantitative-methods/blob/main/07-replication-workshop/02-practice/starter/"
RAW = "https://raw.githubusercontent.com/warint/quantitative-methods/main/07-replication-workshop/02-practice/starter/"
MAX_LINES = 20      # what fits on one tab of a 1280 x 760 slide, under the footer


def parts(script):
    """The whole script, cut into consecutive pieces short enough for one tab.

    Cuts fall at a `# Step` heading where possible, then at a blank line, and
    only as a last resort mid-block; pasted in order, the pieces are the file.
    """
    lines = script.strip().split("\n")
    out, cur = [], []
    for i, line in enumerate(lines):
        starts_step = bool(STEP.match(line))
        if cur and (len(cur) >= MAX_LINES or (starts_step and len(cur) >= MAX_LINES // 2)):
            # back up to the last blank line if that keeps the piece reasonable
            cut = len(cur)
            if not starts_step:
                blanks = [k for k, l in enumerate(cur) if not l.strip() and k >= MAX_LINES // 2]
                if blanks:
                    cut = blanks[-1] + 1
            out.append(cur[:cut]); cur = cur[cut:]
        cur.append(line)
    if cur:
        out.append(cur)
    pieces, start = [], 1
    for chunk in out:
        while chunk and not chunk[-1].strip():
            chunk = chunk[:-1]
        pieces.append((start, start + len(chunk) - 1, "\n".join(chunk)))
        start += len(chunk)
        while start <= len(lines) and not lines[start - 1].strip():
            start += 1
    return pieces


# Steps whose code and output together are taller than a slide, measured on the
# rendered deck. Re-measure after editing a script; add the step here if it spills.
LONG = {"r2": {"5", "6", "8"}, "r3": {"10"}, "r4": {"10"}, "r5": {"3", "7"}}
WIDE = {("r5", "7")}     # a model summary too long for one column


def long_step(key, n, code):
    return n in LONG.get(key, set())


def cell(code):
    return f"```{{python}}\n#| echo: true\n{code}\n```"


def slides(key, fn):
    script = (STARTER / fn).read_text(encoding="utf-8")
    setup, steps = split(script)
    tabs = [f"### Set-up\n\nThe lines that open every script: find the repository, import what the "
            f"steps use.\n\n{cell(setup)}"]
    for n, title, code in steps:
        if long_step(key, n, code):
            # Code and result side by side would not fit: show the code (not run),
            # then run it once with the code hidden. Still one execution per step.
            tabs.append(f"### {n} · code\n\n**Step {n} · {title}**\n\n"
                        f"```python\n{code}\n```")
            opts = "#| echo: false"
            prints_more_than_saved = any("print(" in l and '"saved"' not in l
                                         for l in code.split("\n"))
            if (key, n) in WIDE:
                opts += "\n#| classes: result-wide"   # one long printout, in two columns
            elif ("plt." in code or ".plot(" in code) and prints_more_than_saved:
                opts += "\n#| layout-ncol: 2"         # the printout and the figure side by side
            tabs.append(f"### {n} · result\n\n**Step {n} · {title}** — what it prints\n\n"
                        f"```{{python}}\n{opts}\n{code}\n```")
        else:
            tabs.append(f"### {n}\n\n**Step {n} · {title}**\n\n{cell(code)}")
    tabset = "\n\n".join(tabs)
    code_tabs = "\n\n".join(f"### Lines {a}–{b}\n\n```python\n{code}\n```"
                              for a, b, code in parts(script))
    return f"""<!-- Generated by build_solution_slides.py from ../02-practice/starter/{fn}.
     Do not edit: change the script, then re-run the builder. -->

## The script, to copy {{.scrollable}}

::::::: panel-tabset
### Get the file

The whole script is one file: **[view it on GitHub]({GITHUB}{fn})** or
**[download it]({RAW}{fn})** (right-click → *Save link as…*). It is the same file as
`02-practice/starter/{fn}`.

Or build it by hand: in VS Codium, **File → New File…** → *Python File*, then paste the
parts in the next tabs **in order**, one under the other. **Save it inside the
`quantitative-methods` folder** (for example as `{key}.py`), and press **Run** ▷.

{code_tabs}
:::::::

## The solutions, step by step {{.scrollable}}

Each tab is one step, run when these slides were built: the code, then what it prints. Compare
your own output with it line by line.

:::::::: panel-tabset
{tabset}
::::::::
"""


def main():
    for key, fn in PAPERS:
        out = HERE / f"_solutions-{key}.qmd"
        out.write_text(slides(key, fn), encoding="utf-8")
        print(f"  {out.name}  <- {fn}")


if __name__ == "__main__":
    main()
