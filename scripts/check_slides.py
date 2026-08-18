#!/usr/bin/env python3
"""
Flag slides that will overflow the frame.

    python scripts/check_slides.py                 # every deck
    python scripts/check_slides.py path/to/x.qmd   # one deck

Slides overflow silently: reveal.js scales them down until they are unreadable,
and PowerPoint simply runs the text off the bottom of the sheet. Neither tells
you. This script counts what is on each slide and reports the ones that are too
heavy, so a deck can be checked before it is presented rather than during.

The budget is a weighted line count, because a table row costs more vertical
space than a bullet and a code line costs more than either. The thresholds are
empirical: they were tuned against decks rendered at the theme's 26px root.
"""

import glob
import sys

# Vertical cost of one line of each kind, in units of "one body line".
COST = {"text": 1.0, "bullet": 1.0, "code": 1.15, "table": 1.35, "math": 1.6}

BUDGET = 15.0        # a slide above this is likely to overflow
TIGHT = 12.5         # above this, worth a second look


def classify(line, in_code):
    s = line.strip()
    if not s:
        return None
    if in_code:
        return "code"
    if s.startswith("|") and s.endswith("|"):
        return "table"
    if s.startswith("$$") or s == "$$":
        return "math"
    if s.startswith((":::", "<!--")):
        return None                       # container markers take no space
    if s.startswith(("-", "*", "+")) or (s[0].isdigit() and s[1:3] in (". ", ") ")):
        return "bullet"
    return "text"


def measure(path):
    """Return [(slide_title, weighted_cost, raw_line_count)] for one deck."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    # skip YAML front matter
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break

    slides, title, cost, raw, in_code = [], None, 0.0, 0, False
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        # a new slide begins at ## (level 2) or # (section divider)
        if not in_code and (s.startswith("## ") or s == "##" or s.startswith("# ")):
            if title is not None:
                slides.append((title, cost, raw))
            title = s.lstrip("#").strip() or "(untitled)"
            cost, raw = 0.0, 0
            continue
        kind = classify(line, in_code)
        if kind:
            cost += COST[kind]
            raw += 1
    if title is not None:
        slides.append((title, cost, raw))
    return slides


def main(argv):
    targets = argv[1:] or sorted(glob.glob("**/*.qmd", recursive=True))
    if not targets:
        print("no .qmd files found")
        return 0

    total_over = 0
    for path in targets:
        slides = measure(path)
        over = [s for s in slides if s[1] > TIGHT]
        status = "OK" if not any(s[1] > BUDGET for s in slides) else "OVERFLOW"
        print(f"\n{path}  ({len(slides)} slides)  [{status}]")
        if not over:
            print("   every slide within budget")
        for title, cost, raw in over:
            mark = "!!" if cost > BUDGET else " ~"
            total_over += cost > BUDGET
            print(f"   {mark} {cost:5.1f}  {raw:3d} lines   {title[:58]}")

    print(f"\n{total_over} slide(s) over budget ({BUDGET}).")
    return 1 if total_over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
