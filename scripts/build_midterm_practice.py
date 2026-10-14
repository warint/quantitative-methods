"""Render the midterm practice questions, the sample paper, and their answer keys to PDF.

    python scripts/build_midterm_practice.py

The questions live as Markdown (assessments/midterm/PRACTICE.md, EXAM.md and
their answer keys), which GitHub renders and which is easy to edit. Students
sit the midterm on paper, though, so they practise from a printout: this
script turns each file into a PDF in the house style of MIDTERM-SUMMARY.pdf,
and scripts/build_docs.py publishes them next to the summary.

The page style is read from MIDTERM-SUMMARY.qmd rather than copied, so the
documents cannot drift apart. Relative links become absolute ones: a
printed PDF opened from the site has no repository beside it.
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MID = ROOT / "assessments" / "midterm"
SITE = "https://warint.github.io/quantitative-methods/"
REPO = "https://github.com/warint/quantitative-methods/blob/main/assessments/midterm/"

DOCS = {
    "PRACTICE.md": "Midterm Practice Questions · Sessions 2 to 6",
    "PRACTICE-ANSWERS.md": "Midterm Practice Questions · Answer Key",
    "EXAM.md": "Midterm Sample Paper · 2 hours 30 minutes",
    "SOLUTIONS.md": "Midterm Sample Paper · Answer Key",
}

# Where each relative link should point once the file is a PDF on the site.
LINKS = {
    "PRACTICE.md": SITE + "midterm-practice.pdf",
    "PRACTICE-ANSWERS.md": SITE + "midterm-practice-answers.pdf",
    "MIDTERM-SUMMARY.pdf": SITE + "midterm-summary.pdf",
    "EXAM.md": SITE + "midterm-sample.pdf",
    "SOLUTIONS.md": SITE + "midterm-sample-answers.pdf",
}


def page_style():
    """The YAML of MIDTERM-SUMMARY.qmd, minus its title and subtitle."""
    text = (MID / "MIDTERM-SUMMARY.qmd").read_text(encoding="utf-8")
    yaml = text.split("---", 2)[1]
    return "\n".join(l for l in yaml.splitlines()
                     if not l.startswith(("title:", "subtitle:"))).strip("\n")


def body(md):
    """The Markdown without its own title block (the PDF title replaces it)."""
    text = (MID / md).read_text(encoding="utf-8")
    text = text.split("\n---\n", 1)[1]           # drop the heading and byline

    def absolute(m):
        target = m.group(2)
        if target.startswith(("http", "#")):
            return m.group(0)
        return f"[{m.group(1)}]({LINKS.get(target, REPO + target)})"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", absolute, text)
    if md == "EXAM.md":
        text = answer_spaces(text)
    elif md == "PRACTICE.md":
        text = practice_spaces(text)
    else:
        return text
    return KEEP_TOGETHER + text


LINES_PER_BR = 3        # each <br> in the paper is three ruled writing lines on the printout

# The practice set has no <br> markers: its space is set by part, the way the paper sets it by points.
PRACTICE_LINES = {"I": 14, "II": 4, "B": 6, "C": 6, "D": 14}   # II: per sub-question, (a) to (d)
# Never split a question across a page: no single line left behind or carried over.
KEEP_TOGETHER = "```{=latex}\n\\clubpenalty=10000 \\widowpenalty=10000\n```\n\n"
NEWPAGE = "```{=latex}\n\\newpage\n```\n\n"


def ruled(n):
    """n ruled writing lines, kept with the question above them."""
    rule = r"\par\vspace{0.56cm}\noindent\rule{\linewidth}{0.3pt}"
    return "```{=latex}\n\\par\\nopagebreak[4]" + rule * n + "\\par\\medskip\n```"


def new_pages(text, also=None):
    """Each part on a fresh page, without the rule that would end the page before it."""
    text = re.sub(r"^---\n\n(?=# Part)", "", text, flags=re.M)
    heads = r"# Part" + (f"|{also}" if also else "")
    return re.sub(rf"^({heads})", lambda m: NEWPAGE + m.group(1), text, flags=re.M)


def answer_spaces(text):
    """The paper is sat on paper: give every question ruled lines to write on.

    In the Markdown, a line of <br> tags marks the space after a question (GitHub shows
    it as blank space); on the PDF each <br> becomes LINES_PER_BR ruled lines, and each
    part, and each output of Part C, starts on a fresh page with its questions.
    """
    text = re.sub(r"^(?:<br>)+$", lambda m: ruled(m.group(0).count("<br>") * LINES_PER_BR),
                  text, flags=re.M)
    return new_pages(text, also=r"## C[23]\.")


def practice_spaces(text):
    """Ruled lines after every written question of the practice set (not the multiple choice).

    A question is a paragraph opening with its label (**B7.**); a code block that follows
    it belongs to it, so the lines go after the code. Part II asks the same four
    sub-questions of every reading, so each reading gets four labelled spaces, on a page of its own.
    """
    blocks, fence = [], False
    for chunk in text.split("\n\n"):              # keep fenced code in one block
        if fence:
            blocks[-1] += "\n\n" + chunk
        else:
            blocks.append(chunk)
        if chunk.count("```") % 2:
            fence = not fence

    out, part, pending = [], None, None
    for b in blocks:
        if pending and not b.startswith("```"):
            out.append(pending)
            pending = None
        if part == "II" and re.match(r"\*\*II[2-9]\.\*\*", b):
            out.append(NEWPAGE.strip())         # a reading and its four spaces fill a page
        out.append(b)
        if m := re.match(r"# Part (\w+)", b):
            part = m.group(1)
        elif part in PRACTICE_LINES and re.match(rf"\*\*{part}\d+\.\*\*", b):
            n = PRACTICE_LINES[part]
            pending = ("\n\n".join(f"*({s})*\n\n" + ruled(n) for s in "abcd")
                       if part == "II" else ruled(n))
    if pending:
        out.append(pending)
    return new_pages("\n\n".join(out))


def main():
    style = page_style()
    with tempfile.TemporaryDirectory() as tmp:
        for md, title in DOCS.items():
            qmd = Path(tmp) / (Path(md).stem + ".qmd")
            qmd.write_text(f'---\ntitle: "{title}"\n'
                           f'subtitle: "MATH60033A · Quantitative Methods in International Business"\n'
                           f"{style}\n---\n\n{body(md)}", encoding="utf-8")
            subprocess.run(["quarto", "render", qmd.name, "--to", "pdf"],
                           cwd=tmp, check=True, capture_output=True)
            shutil.copy2(qmd.with_suffix(".pdf"), MID / (Path(md).stem + ".pdf"))
            print(f"  {MID.relative_to(ROOT) / (Path(md).stem + '.pdf')}")


if __name__ == "__main__":
    main()
