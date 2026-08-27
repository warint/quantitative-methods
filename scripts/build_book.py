"""Assemble the Quarto book from the session decks and the session briefs.

    python scripts/build_book.py
    scripts/render_book.sh

The book is a *derived* artefact. Nothing here is authored: every chapter is
assembled from files that already exist, so the book cannot drift from the
repository the way a hand-maintained second copy would.

Where the content comes from
----------------------------
The lecture `README.md` files are stubs — a few hundred words pointing at the
deck. The substance is in the decks themselves, so a chapter's body is the
deck, converted from slides to prose.

Ten of the eleven decks were imported from warin.ca via pandoc and still carry
that provenance: math arrives as `[\\\\(R\\^2\\\\)]{.math .inline}` spans rather
than `$R^2$`, code and output arrive as pre-baked `.cell-*` divs, and every
heading carries a `{#imported-sNN-NNN .center .scrollable}` attribute block.
`normalise_deck` undoes all of that. It is the bulk of this file.

The shape of a chapter
----------------------
One session is one chapter, and it holds the whole session:

    ## Before the session      the reading and the data (from 00-pre-session/)
    ## <the deck's own sections>
    ## In the practice         the brief (from 02-practice/)

Splitting preparation into a separate appendix was the alternative. This is
better for the thing a book adds over the repository — search. A student who
searches "leverage" should land once, on Session 03, and find the paper that
introduced it, the derivation, and the exercise that uses it, in that order.
Two hits and a page jump is a worse answer to the same query.

Heading levels are normalised rather than fixed: the deck's own top level
becomes `##`, whatever it happens to be. The hand-written decks (01, 05) use
`#` dividers and shift down one; the imports start at `##` and do not move.
Without this the imported chapters would have no `##` at all and their entire
contents would collapse into a flat list in the sidebar.
"""

import datetime
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from course_spec import (SESSIONS, ordered, DATES, ASYNCHRONOUS,  # noqa: E402
                         WHEN, ROOM, MIDTERM_DATE, MIDTERM_AFTER)

BOOK = ROOT / "book"
PORTRAITS = ROOT / "assets" / "portraits"
GH = "https://github.com/warint/quantitative-methods/blob/main/"
PAGES = "https://warint.github.io/quantitative-methods/"


# ---------------------------------------------------------------------------
# Fence-aware line walking.
#
# Every transformation below has to skip code. A Python comment (`# fit the
# model`) is indistinguishable from an h1 by regex alone, and the decks are full
# of them — silently promoting one to a heading would corrupt both the code and
# the sidebar.
# ---------------------------------------------------------------------------
def walk(text):
    """Yield (line, in_code) for every line, tracking fenced blocks."""
    fence = None
    for line in text.split("\n"):
        m = re.match(r"^(\s*)(`{3,}|~{3,})(.*)$", line)
        if m:
            marker = m.group(2)
            if fence is None:
                fence = marker[0] * 3
                yield line, True
                continue
            if marker.startswith(fence):
                fence = None
                yield line, True
                continue
        yield line, fence is not None


def _unescape_math(s):
    r"""Undo pandoc's double-escaping inside a math span.

    `\\mu` is a LaTeX command and must survive as `\mu`; `\^` and `\_` are
    pandoc protecting markdown syntax and must lose the backslash. Doing these
    in the wrong order eats the command, so the doubles are parked on a
    sentinel first.
    """
    s = s.replace("\\\\", "\x00")
    s = re.sub(r"\\([^\w\s])", r"\1", s)
    return s.replace("\x00", "\\")


def fix_math(line):
    r"""Pandoc math -> LaTeX.

    Two forms survive the import, and both appear in the same files. The
    wrapped form `[\\(x\\)]{.math .inline}` is what pandoc emits from
    rendered HTML; the bare form `\\(x\\)` is what it emits from source that
    was already LaTeX. The wrapped rules run first because they are the more
    specific match.
    """
    line = re.sub(r"\[\\\\\\\[(.*?)\\\\\\\]\]\{\.math\s+\.display\}",
                  lambda m: f"$${_unescape_math(m.group(1))}$$", line)
    line = re.sub(r"\[\\\\\((.*?)\\\\\)\]\{\.math\s+\.inline\}",
                  lambda m: f"${_unescape_math(m.group(1))}$", line)
    line = re.sub(r"\\\\\\\[(.+?)\\\\\\\]",
                  lambda m: f"$${_unescape_math(m.group(1))}$$", line)
    line = re.sub(r"\\\\\((.+?)\\\\\)",
                  lambda m: f"${_unescape_math(m.group(1))}$", line)
    return line


def normalise_divs(text):
    """Flatten pandoc's cell machinery; keep the course's own callout divs.

    `.cell` / `.cell-code` / `.sourceCode` wrappers are dropped outright — the
    fenced block inside them is the content. `.cell-output` divs hold
    four-space-indented output, which is re-emitted as a plain fence so it
    renders as output rather than as a blockquote of indented text.
    """
    out, stack = [], []
    for line, in_code in walk(text):
        if not in_code:
            m = re.match(r"^:::+\s*\{(.*)\}\s*$", line)
            if m:
                attrs = m.group(1)
                if ".cell-output" in attrs:
                    stack.append("output")
                    out.append("```text")
                    continue
                if re.search(r"\.cell\b|\.cell-code|\.sourceCode|#cb\d", attrs):
                    stack.append("drop")
                    continue
                stack.append("keep")
                out.append(line)
                continue
            if re.match(r"^:::+\s*$", line):
                kind = stack.pop() if stack else "keep"
                if kind == "output":
                    out.append("```")
                elif kind == "keep":
                    out.append(line)
                continue
        if stack and stack[-1] == "output":
            line = line[4:] if line.startswith("    ") else line.lstrip()
        out.append(line)
    return "\n".join(out)


HEADING = re.compile(r"^(#{1,6})\s*(.*?)\s*$")
# An attribute block is any trailing {...} carrying an id, a class or a
# key=value pair — `{#imported-s03-001 .center}` and
# `{background-color="#E3120B" style="..."}` are both attribute blocks.
ATTRS = re.compile(r"\s*\{[^{}]*[#.=][^{}]*\}\s*$")


def shift_headings(text, target_top=2):
    """Move the deck's own top heading level to `##`, keeping relative depth.

    Headings whose title is only an attribute block — `## {#imported-s03-008}`,
    a continuation slide with no title — are dropped rather than rendered as an
    empty entry in the sidebar.
    """
    levels = []
    for line, in_code in walk(text):
        if in_code:
            continue
        m = HEADING.match(line)
        if m and ATTRS.sub("", m.group(2)).strip():
            levels.append(len(m.group(1)))
    if not levels:
        return text
    shift = target_top - min(levels)

    out = []
    for line, in_code in walk(text):
        if in_code:
            out.append(line)
            continue
        m = HEADING.match(line)
        if not m:
            out.append(line)
            continue
        title = ATTRS.sub("", m.group(2)).strip()
        if not title:
            continue
        level = min(6, max(1, len(m.group(1)) + shift))
        out.append("#" * level + " " + title)
    return "\n".join(out)


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[text.find("\n", end + 1) + 1:]
    return text


# ---------------------------------------------------------------------------
# Links.
#
# Every source file links relative to its own directory. Flattened into
# `book/`, those paths point at nothing. Known targets are rewritten to their
# chapter; everything still relative afterwards is sent to GitHub, so a stale
# link degrades to "the file on GitHub" rather than to a 404.
# ---------------------------------------------------------------------------
CHAPTER_LINKS = {
    "REPLICATIONS.md": "replications.qmd",
    "setup-vscodium-local-llm.md": "setup.qmd",
    "setup-git-and-github.md": "setup.qmd#git-and-github",
}


def rewrite_links(text, num=None):
    def repl(m):
        label, target = m.group(1), m.group(2).strip()
        if target.startswith(("http://", "https://", "#", "mailto:", "images/")):
            return m.group(0)

        base, _, frag = target.partition("#")
        name = Path(base).name

        # The three parts of a session now live in one chapter, so links
        # between them become anchors rather than files.
        if num:
            if re.fullmatch(r"\.\./01-lecture/README\.md", base):
                return f"[{label}](#the-lecture)"
            if re.fullmatch(r"\.\./02-practice/README\.md", base):
                return f"[{label}](#in-the-practice)"
            if re.fullmatch(r"\.\./00-pre-session/README\.md", base):
                return f"[{label}](#before-the-session)"
            if re.fullmatch(r"\.\./README\.md", base):
                return f"[{label}](session-{num}.qmd)"

        # Another session's folder.
        seg = re.match(r"(?:\.\./)*(\d{2})-[a-z0-9-]+/", base)
        if seg and seg.group(1) in SESSIONS:
            return f"[{label}](session-{seg.group(1)}.qmd)"

        if name in CHAPTER_LINKS:
            t = CHAPTER_LINKS[name]
            return f"[{label}]({t}{'#' + frag if frag and '#' not in t else ''})"

        clean = re.sub(r"^(\.\./)+", "", base)
        return f"[{label}]({GH}{clean}{'#' + frag if frag else ''})"

    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", repl, text)


def fix_relative_paths(text):
    """Deck cells run two levels deep; book chapters run one.

    Session 05 is the only deck with live cells, and they read
    `../../data/spine/...` and `sys.path.insert(0, "../../slides")`. From
    `book/` those resolve above the repository root.
    """
    return text.replace('"../../', '"../').replace("'../../", "'../")


IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


def localise_assets(text, num, source_dir):
    """Copy the figures a deck references into the book, and point at them.

    The decks keep their figures beside themselves, in 01-lecture/economist-assets/
    and 01-lecture/imported-assets/. Flattened into book/, those relative paths
    resolve to nothing, and the link rewriter's fallback sent them to GitHub —
    stripping the session directory on the way, and to /blob/ rather than /raw/,
    which serves an HTML page rather than an image. Eighty-seven references
    across seven chapters pointed at 404s.

    A book should not be fetching its own illustrations over the network in any
    case, so they are copied in. The destination name flattens the path
    (`imported-assets/index_files/figure-revealjs/x.png` becomes one filename)
    which also keeps the result clear of the `*_files/` ignore rule that would
    otherwise stop the copies from ever being committed.
    """
    dest = BOOK / "images" / "decks"

    def repl(m):
        label, target = m.group(1), m.group(2).strip()
        if target.startswith(("http://", "https://", "#", "data:")):
            return m.group(0)
        base = target.partition("#")[0]
        if not base.lower().endswith(IMAGE_SUFFIXES):
            return m.group(0)

        src = (source_dir / base).resolve()
        if not src.exists():
            return m.group(0)

        flat = f"session-{num}-" + re.sub(r"[^A-Za-z0-9._-]", "-", base.strip("./"))
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest / flat)
        return f"![{label}](images/decks/{flat})"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, text)

    # The imported decks also carry raw <img src="..."> inside HTML blocks —
    # pandoc left them there — and those need the same treatment.
    def repl_tag(m):
        rewritten = repl(_FakeMatch(m.group(0), "", m.group(1)))
        if rewritten.startswith("!["):
            return m.group(0).replace(m.group(1), rewritten.split("(", 1)[1].rstrip(")"))
        return m.group(0)

    return re.sub(r'<img[^>]*\ssrc="([^"]+)"', repl_tag, text)


class _FakeMatch:
    """Lets the markdown replacer above be reused for an <img> tag."""

    def __init__(self, whole, label, target):
        self._g = (whole, label, target)

    def group(self, i):
        return self._g[i]


def normalise_deck(path):
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    text = normalise_divs(text)
    text = "\n".join(l if c else fix_math(l) for l, c in walk(text))
    text = shift_headings(text)
    text = fix_relative_paths(text)
    return text.strip()


def normalise_brief(path, num, drop_heading_lines=0):
    """A session brief, demoted to sit under a chapter's `##` section."""
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    lines = text.split("\n")
    if drop_heading_lines:
        lines = lines[drop_heading_lines:]
    text = "\n".join(lines)
    text = shift_headings(text, target_top=3)
    text = rewrite_links(text, num)
    return text.strip()


# ---------------------------------------------------------------------------
# Chapters
# ---------------------------------------------------------------------------
def _when(num):
    d = datetime.date.fromisoformat(DATES[num])
    tail = " · **asynchronous**" if num in ASYNCHRONOUS else ""
    return f"{d:%A %-d %B %Y} · {WHEN.split()[1]} · {ROOM}{tail}"


def _decks(num):
    kinds = [("lecture", "Lecture slides"), ("pre-session", "Pre-session slides"),
             ("practice", "Practice slides")]
    if num == "12":
        kinds = [k for k in kinds if k[0] != "practice"]
    return " · ".join(f"[{label}]({PAGES}session-{num}-{slug}.html)" for slug, label in kinds)


def plate(num):
    """The chapter's portrait, with its attribution taken from credits.json.

    The credit is not decoration. These are real paintings and photographs by
    named artists, and the licence that lets the book use them is conditional
    on saying so.
    """
    creds = PORTRAITS / "credits.json"
    if not creds.exists():
        return ""
    entry = json.loads(creds.read_text(encoding="utf-8")).get(f"session-{num}")
    if not entry:
        return ""

    src = Path(entry["file"]).name
    artist = entry["artist"]
    when = entry["date"]
    return (
        '::: {.plate}\n'
        f'![](images/{src}){{fig-alt="Portrait of {entry["name"]}, {entry["dates"]}."}}\n\n'
        f'**{entry["name"]}** · {entry["dates"]}\n\n'
        f'{entry["why"]}\n\n'
        f'[{artist}, {when}. {entry["licence"]}, via Wikimedia Commons.]'
        '{.plate-credit}\n'
        ':::\n'
    )


def chapter_prose(d, num):
    """The authored chapter for this session, and what it declares about itself.

    book/ is generated, so nothing written into book/session-NN.qmd survives a
    rebuild. Long-form prose therefore lives beside the deck and the brief, in
    the session's own directory, and is assembled in like everything else.

    An optional front matter block lets the prose override what surrounds it:

        title:       replaces the session title for this chapter
        standalone:  true — the chapter is the prose and nothing else, with no
                     deck transcript, practice brief or session facts appended

    Returns (declared, text); (dict(), None) when no chapter has been written.
    """
    path = d / "chapter.md"
    if not path.exists():
        return {}, None

    raw = path.read_text(encoding="utf-8")
    declared = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep:
                declared[key.strip()] = value.strip().strip("\"'")

    text = strip_frontmatter(raw)
    return declared, text.replace("{{portrait}}", plate(num)).strip()


def chapter(num, s):
    d = ROOT / s["dir"]
    declared, prose = chapter_prose(d, num)
    title = declared.get("title") or s["title"]

    # A standalone chapter is prose and nothing else: no deck transcript, no
    # practice brief, no session facts. Chapter 1 is written this way — it is
    # an introduction to the book, not a record of the first class.
    if declared.get("standalone") == "true":
        return f'---\ntitle: "{title}"\n---\n\n{prose}\n'

    parts = [f"""---
title: "{title}"
---

::: {{.chapter-meta}}
{_decks(num)}
:::

> **{s['question']}**
"""]

    facts = [("Theme of the practice", s["theme"])]
    if s.get("reading"):
        facts.append(("Reading", f"{s['reading']} · [article]({s['reading_url']})"))
    if s.get("dataverse"):
        facts.append(("Replication package",
                      f"[{s['dataverse']}](https://doi.org/{s['dataverse']})"))
    if s.get("dataset"):
        facts.append(("Data", f"`qmib.load(\"{s['dataset']}\")` — {s['dataset_note']}"))
    parts.append("| | |\n|---|---|\n" +
                 "\n".join(f"| **{k}** | {v} |" for k, v in facts) + "\n")

    if num == MIDTERM_AFTER:
        md = datetime.date.fromisoformat(MIDTERM_DATE)
        parts.append(f"""::: {{.warn}}
**This is the last session examined by the midterm**, written {md:%A %-d %B %Y}. Everything from
Session 1 to here is examinable.
:::
""")

    # Pre-session logistics — download the package, unzip it here, arrive with
    # these four things — is instruction for the week, not part of a chapter.
    # It stays in the deck and the session README, where a student looks for it.
    # A chapter that has been written keeps the space for explanation instead.
    pre = d / "00-pre-session/README.md"
    if pre.exists() and not prose:
        parts.append("## Before the session\n\n"
                     + localise_assets(normalise_brief(pre, num, 2), num, pre.parent))

    if prose:
        parts.append(prose)

    deck = d / f"01-lecture/MATH60033A-S{num}-Lecture.qmd"
    if deck.exists():
        parts.append("## The lecture\n\n::: {.muted}\nDelivered from "
                     f"[the slides]({PAGES}session-{num}-lecture.html). "
                     "What follows is the same material as prose.\n:::\n\n"
                     + rewrite_links(localise_assets(normalise_deck(deck), num, deck.parent), num))
    else:
        lec = d / "01-lecture/README.md"
        if lec.exists():
            parts.append("## The lecture\n\n" + normalise_brief(lec, num, 2))

    prac = d / "02-practice/README.md"
    if prac.exists():
        parts.append("## In the practice\n\n"
                     + localise_assets(normalise_brief(prac, num, 2), num, prac.parent))

    return "\n\n".join(parts) + "\n"


def flat_page(title, source, extra=""):
    text = strip_frontmatter(Path(source).read_text(encoding="utf-8"))
    text = re.sub(r"^#\s+.*\n", "", text, count=1)          # its own H1 becomes the title
    text = shift_headings(text, target_top=2)
    return f'---\ntitle: "{title}"\n---\n\n{extra}{rewrite_links(text)}\n'


def preface():
    rows = []
    for num, s in ordered():
        d = datetime.date.fromisoformat(DATES[num])
        star = " *(asynchronous)*" if num in ASYNCHRONOUS else ""
        rows.append(f"| [{int(num)}](session-{num}.qmd) | "
                    f"{s['title']}{star} | {s['question']} |")
        if num == MIDTERM_AFTER:
            md = datetime.date.fromisoformat(MIDTERM_DATE)
            rows.append(f"| — | **Midterm** — on paper, closed book | "
                        f"**Chapters 1–{int(MIDTERM_AFTER)}** |")
    table = "\n".join(rows)
    return f"""---
number-sections: false
---

# Foreword {{.unnumbered}}

Ukraine supplied around seventy per cent of the world's neon. Russia controlled some forty-four
per cent of its palladium. Taiwan fabricates close to two-thirds of its semiconductors. None of
those three facts was secret, and none of them appeared on the balance sheet of a company that
depended on all three — until a pandemic and a war made them appear at once [@warin-supplychains].
Firms discovered the shape of their own supply chains by watching them break.

That is the difficulty this book is written against. The transformations that matter most in
international business are not hidden. They are *unmeasured* by the people they will affect, and
the received account of how the world economy works quietly supplies the missing numbers with
assumptions. Chief among them is the assumption that global value chains, having been optimised
for decades, must be efficient — an assumption that survives largely because so few people test
it against data [@warin-notefficient].

A second difficulty is that the unit of analysis is wrong in most public discussion. Countries do
not trade; firms do [@warin-firms]. Aggregate statistics on bilateral flows describe the sum of
decisions taken inside firms, under constraints — freight, insurance, policy wedges, the cost of
switching a supplier — that the aggregate cannot show [@warin-gravity]. Work at the level where
the decision is actually made requires data at that level, and methods equal to it.

And the ground itself is moving. The central economic shift of this decade is not digitisation
but a pivot from producing goods and knowledge toward *valuing the data generated in the course of
producing them* — in agriculture, manufacturing, health, logistics and public administration
alike [@warin-middlepowers]. An economy organised around data capture and platform intermediation
concentrates advantage differently than one organised around factories, and it rewards the
institutions and the analysts who can read what the data say [@warin-economiedonnees].

None of that is an argument that quantitative methods produce certainty. It is an argument that
they are the only way to hold a claim about the world economy to account — to say what would have
to be true for it to hold, and to notice when it stops holding. Trade theory has been rewritten
repeatedly, from the mercantilists through Ricardo to the platform economy, and each rewriting
followed evidence that the previous account could not absorb [@warin-evolution].

::: {{.step}}
**This book teaches the methods, on real data, from the first week.** Teaching statistics in a
business school pulls in two directions: real data are messy, and pedagogical data are false. This
course resolves it in favour of the mess [@warin-statcan]. Every technique here is applied to
actual European economic series, with the missing values, the influential observations and the
awkward panel structure left in.
:::

Twelve chapters follow the arc from describing data to defending a causal claim. Each one asks a
single question — *can this regression be trusted?*, *did the policy do anything?* — and each ends
where a referee would begin.

## How to use it

| If you want to | Go to |
|---|---|
| Prepare for next week | the session's **Before the session** |
| Re-read a derivation you lost in class | the session's lecture sections |
| Know what the group work asks for | the session's **In the practice** |
| Find where something was covered | the **search box**, top of the sidebar |
| Know how you are graded | [the syllabus](https://github.com/warint/quantitative-methods/blob/main/SYLLABUS.md), in the course repository |
| Get your machine working | [Setting up your tools](setup.qmd) |

::: {{.check}}
**The search box is the reason this book exists.** Slides are good for a room and bad for finding
something three weeks later. Search covers every session at once, so a term you half-remember —
*leverage*, *soft-thresholding*, *parallel trends* — takes you to the session that introduced it.
:::

## The slides

Each chapter links to the three decks it was built from. The slides remain the version delivered
in class; the book is the same material set as continuous prose, which is the better form for
reading afterwards.

## The twelve chapters

| | Chapter | Question |
|---|---|---|
{table}

::: {{.muted}}
Source: [github.com/warint/quantitative-methods](https://github.com/warint/quantitative-methods) ·
{{{{< meta date >}}}}
:::
"""


def setup_page():
    a = ROOT / "01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md"
    b = ROOT / "02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md"
    body = ['---\ntitle: "Setting up your tools"\n---\n',
            "::: {.warn}\nBudget **60–90 minutes for the first half, before Session 1**, and "
            "**45 minutes for git, before Session 2**. Installation time is not class time.\n:::\n"]
    for path, anchor in ((a, "vs-codium-python-and-a-local-model"), (b, "git-and-github")):
        if not path.exists():
            continue
        text = strip_frontmatter(path.read_text(encoding="utf-8"))
        m = re.match(r"^#\s+(.*)", text)
        title = m.group(1).strip() if m else path.stem
        text = re.sub(r"^#\s+.*\n", "", text, count=1)
        text = shift_headings(text, target_top=3)
        body.append(f"## {title} {{#{anchor}}}\n\n" + rewrite_links(text))
    return "\n\n".join(body) + "\n"


def data_api_page():
    return f'''---
title: "The data API"
---

Every dataset in this course loads with one call. There is no path to get right, no download step
in the practice, and no dependence on the room's wifi.

```python
import qmib

df = qmib.load("core")        # the course spine
qmib.catalog()                # everything available
```

::: {{.step}}
`load()` resolves in three steps and stops at the first that works: a **parquet cache** in `data/`,
then the **committed spine** in `data/spine/`, then the **published copy** on GitHub Pages. The
first call downloads; every call after it reads the cache.
:::

::: {{.check}}
**Why it matters for the practice.** Run `qmib.load()` once at home and the ninety minutes in class
work offline. A room of thirty people downloading the same file at 15:35 is the single most
reliable way to lose the first twenty minutes of a session.
:::

## Outside a clone

In Colab, or anywhere without the repository checked out, point the module at the published copy:

```python
import qmib
qmib.REMOTE = "{PAGES}data"
df = qmib.load("core")
```

## What is where

- Columns, units and traps, per group: [data dictionaries]({GH}data/spine/dictionaries/)
- Provenance and flags: [`PROVENANCE.md`]({GH}data/spine/PROVENANCE.md)
- The module itself: [`qmib.py`]({GH}qmib.py)

::: {{.warn}}
Raw data files are git-ignored on purpose. Never commit one — `qmib` fetches and caches instead.
The synthetic spine is the deliberate exception: small, licence-free, and committed so the practice
runs with no network at all.
:::
'''


QUARTO_YML = """# Generated by scripts/build_book.py — edit that, not this.
project:
  type: book
  output-dir: ../docs/book

book:
  title: "Quantitative Methods in International Business"
  subtitle: "MATH60033A · HEC Montréal"
  author: "Thierry Warin, PhD"
  date: last-modified
  date-format: "D MMMM YYYY"
  search: true
  repo-url: https://github.com/warint/quantitative-methods
  repo-branch: main
  repo-actions: [source, issue]
  page-navigation: true
  sidebar:
    style: docked
    collapse-level: 1
  page-footer:
    left: "MATH60033A · HEC Montréal"
    right: "Built from the course repository"
  chapters:
    - index.qmd
    - part: "The twelve chapters"
      chapters:
{chapters}
  appendices:
    - setup.qmd
    - data-api.qmd
    - replications.qmd

bibliography: references.bib
link-citations: true

format:
  html:
    theme: [cosmo, book.scss]
    toc: true
    toc-depth: 3
    code-copy: true
    code-overflow: wrap
    link-external-newwindow: true
    df-print: kable

execute:
  freeze: auto
  warning: false
"""


BOOK_SCSS = """/*-- scss:defaults --*/
//
// The book wears the same palette as the slides (slides/economist.scss), so a
// chapter and the deck it was built from are recognisably one document. What
// changes is the register: a deck is read from ten metres, a book from forty
// centimetres, so the type is smaller and the measure is narrower.

$econ-paper:  #F7F4ED;
$econ-ink:    #222222;
$econ-muted:  #6B6B67;
$econ-red:    #E3120B;
$econ-blue:   #356B8C;
$econ-teal:   #2A8C82;
$econ-gold:   #D49A00;
$econ-grid:   #D8D3C8;

$body-bg:     $econ-paper;
$body-color:  $econ-ink;
$link-color:  $econ-blue;
$font-family-sans-serif: 'Helvetica Neue', Inter, system-ui, -apple-system, 'Segoe UI', sans-serif;
$font-family-monospace:  ui-monospace, 'SF Mono', Menlo, 'IBM Plex Mono', monospace;
$font-size-root: 17px;
$toc-color: $econ-muted;
$code-bg: rgba(255, 255, 255, 0.72);
$code-color: $econ-ink;

/*-- scss:rules --*/

h1, h2, h3, h4 { letter-spacing: -0.017em; font-weight: 700; }

// The signature device from the slides: a short red rule announcing a section.
main h2::before {
  content: "";
  display: block;
  width: 2.05em;
  height: 0.19em;
  background: $econ-red;
  margin: 0 0 0.42em 0;
}

main h2 { margin-top: 2.1rem; }

// Rules are hairline and horizontal. No boxes, no shadows.
hr { border: 0; border-top: 1px solid $econ-grid; }

table { border-collapse: collapse; }
thead th { border-bottom: 2px solid $econ-ink; text-align: left; }
tbody td { border-bottom: 1px solid $econ-grid; }
td, th { font-variant-numeric: tabular-nums; padding: 0.3em 0.75em 0.3em 0; }

blockquote {
  border-left: 3px solid $econ-red;
  padding: 0.15em 0 0.15em 0.9em;
  margin-left: 0;
  color: $econ-ink;
  font-style: normal;
}

pre { border: 1px solid $econ-grid; background: $code-bg; }
pre code { font-size: 0.86em; }

// The course callout classes, carried over from the decks. The rule down the
// left edge carries the meaning; there are no tinted boxes.
.step  { border-left: 3px solid $econ-blue; padding-left: 0.9em; margin: 1em 0; }
.check { border-left: 3px solid $econ-teal; padding-left: 0.9em; margin: 1em 0; }
.warn  { border-left: 3px solid $econ-red;  padding-left: 0.9em; margin: 1em 0; }
.get   { border-left: 3px solid $econ-gold; padding-left: 0.9em; margin: 1em 0; }
.muted { color: $econ-muted; font-size: 0.92em; }
.tight li { margin-bottom: 0.15em; }

// The dateline under a chapter title.
.chapter-meta {
  color: $econ-muted;
  font-size: 0.92em;
  border-bottom: 1px solid $econ-grid;
  padding-bottom: 0.7em;
  margin-bottom: 1.2em;
}

// Imported decks put output in a plain fence; mark it as output, not input.
.cell-output pre { background: none; border-left: 3px solid $econ-grid; border-width: 0 0 0 3px; }

.sidebar-title { font-weight: 700; letter-spacing: -0.015em; }

/* ---- Chapter plates ---------------------------------------------------- */
/* The portraits are already framed and toned by scripts/build_portraits.py.
   All the page adds is the measure, the caption register and the credit. */

.plate {
  margin: 2.4rem auto;
  max-width: 24rem;
  text-align: center;

  img {
    width: 100%;
    height: auto;
    box-shadow: 0 2px 10px rgba(34, 26, 12, 0.22);
  }

  p { margin: 0.55rem 0 0; }

  strong {
    font-size: 1.02rem;
    letter-spacing: 0.01em;
  }

  /* The 'why this person' line. */
  p:nth-of-type(2) {
    color: $econ-muted;
    font-size: 0.9rem;
    line-height: 1.45;
    font-style: italic;
  }
}

.plate-credit {
  display: block;
  margin-top: 0.5rem;
  color: $econ-muted;
  font-size: 0.76rem;
  line-height: 1.4;
}

/* ---- Definitions ------------------------------------------------------- */
/* A term being defined, not an aside. Marked with a rule in the accent colour
   so a reader scanning for "what does leverage actually mean" can find it. */

.definition {
  margin: 1.6rem 0;
  padding: 0.85rem 1.1rem;
  border-left: 3px solid $econ-blue;
  background: rgba(53, 107, 140, 0.05);

  > p:first-child { margin-top: 0; }
  > p:last-child  { margin-bottom: 0; }

  .term {
    font-weight: 600;
    color: $econ-blue;
  }
}

/* ---- Literature review ------------------------------------------------- */
/* Slightly tighter than body text: it is a survey, read faster than argument. */

.lit {
  margin: 1.6rem 0;
  padding-left: 1.1rem;
  border-left: 1px solid $econ-grid;
  font-size: 0.95rem;

  p { line-height: 1.55; }
}

/* Citations should be visible as citations without shouting. */
.citation a {
  color: $econ-teal;
  text-decoration: none;
  border-bottom: 1px dotted rgba(42, 140, 130, 0.5);
}

/* The reference list at the end of the book. */
#refs {
  font-size: 0.92rem;

  .csl-entry { margin-bottom: 0.7rem; }
}
"""


# What a build owns, and may therefore delete. Everything else in book/ —
# _freeze/ and .quarto/ — belongs to Quarto and must survive.
GENERATED = ("*.qmd", "*.scss", "_quarto.yml", "references.bib")


def clean():
    """Remove what this script generated, and nothing else.

    This used to be rmtree(BOOK) followed by mkdir, which had two faults. It
    deleted book/_freeze/, the execution cache that `freeze: auto` exists to
    maintain, so every render re-executed every chapter from scratch. And on a
    synced folder — this repository lives on an iCloud Desktop — removing and
    immediately recreating a directory races the sync daemon, which restores
    files it had cached into the directory being rebuilt. macOS renames the
    collisions, and "index 2.qmd" and ".quarto 3/" appear out of nowhere. Once,
    65 of them reached a commit.
    """
    BOOK.mkdir(exist_ok=True)
    for pattern in GENERATED:
        for stale in BOOK.glob(pattern):
            stale.unlink()
    images = BOOK / "images"
    if images.exists():
        shutil.rmtree(images)


def main():
    clean()

    (BOOK / "index.qmd").write_text(preface(), encoding="utf-8")
    (BOOK / "setup.qmd").write_text(setup_page(), encoding="utf-8")
    (BOOK / "data-api.qmd").write_text(data_api_page(), encoding="utf-8")
    (BOOK / "replications.qmd").write_text(
        flat_page("Replication packages", ROOT / "REPLICATIONS.md"), encoding="utf-8")
    (BOOK / "book.scss").write_text(BOOK_SCSS, encoding="utf-8")

    bib = ROOT / "assets" / "references.bib"
    if bib.exists():
        shutil.copy2(bib, BOOK / "references.bib")

    if PORTRAITS.exists():
        images = BOOK / "images"
        images.mkdir(exist_ok=True)
        for jpg in sorted(PORTRAITS.glob("*.jpg")):
            shutil.copy2(jpg, images / jpg.name)

    chapters = []
    for num, s in ordered():
        (BOOK / f"session-{num}.qmd").write_text(chapter(num, s), encoding="utf-8")
        chapters.append(f"        - session-{num}.qmd")
        print(f"  session-{num}.qmd")

    (BOOK / "_quarto.yml").write_text(
        QUARTO_YML.format(chapters="\n".join(chapters)), encoding="utf-8")

    print(f"\n{len(chapters)} session chapters + 7 other pages written to book/")
    print("Next: scripts/render_book.sh")


if __name__ == "__main__":
    main()
