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
    return text


LINES_PER_BR = 3        # each <br> in the paper is three ruled writing lines on the printout


def answer_spaces(text):
    """The paper is sat on paper: give every question ruled lines to write on.

    In the Markdown, a line of <br> tags marks the space after a question (GitHub shows
    it as blank space); on the PDF each <br> becomes LINES_PER_BR ruled lines, and each
    part, and each output of Part C, starts on a fresh page with its questions.
    """
    rule = r"\par\vspace{0.56cm}\noindent\rule{\linewidth}{0.3pt}"

    def lines(m):
        n = m.group(0).count("<br>") * LINES_PER_BR
        return "```{=latex}\n\\par\\nopagebreak[4]" + rule * n + "\\par\\medskip\n```"

    text = re.sub(r"^(?:<br>)+$", lines, text, flags=re.M)
    newpage = "```{=latex}\n\\newpage\n```\n\n"
    text = re.sub(r"^---\n\n(?=# Part)", "", text, flags=re.M)     # no rule above a page break
    return re.sub(r"^(# Part|## C[23]\.)", lambda m: newpage + m.group(1), text, flags=re.M)


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
