"""Repair two faults the import left in the decks: blank titles and empty tabs.

    python scripts/fix_deck_slides.py --check    # report, change nothing
    python scripts/fix_deck_slides.py            # repair every deck
    python scripts/fix_deck_slides.py 04         # one session

These decks were converted from a published R course, and the conversion left
two visible defects behind.

**Untitled slides.** Pandoc wrote a continuation slide as `## {#imported-s04-011
.scrollable}` — a heading with an id and no words. Revealjs renders that as a
blank title bar above real content, so a student sees a slide that appears to
have lost its heading. Each one is retitled from its context: a slide that
follows a `.center` divider takes the divider's title, because it is that
section's first slide; a slide that follows an ordinary slide takes its title
with `(cont.)`, because that is what it is.

**Empty tabs.** Inside a `panel-tabset`, a tab such as `### 4` whose body was the
R rendering of the previous tab's code — `1st Qu.`, `Class :character` — was
emptied when the deck's code was made live, because the Python cell now prints
its own output. The tab shell survived, so the deck shows numbered tabs that
open onto nothing. Those are removed, and the numeric labels of the remaining
tabs are closed up so the sequence reads 1, 2, 3 again.

Nothing else is touched. A tab with a name rather than a number keeps its name,
a slide that is deliberately blank — the full-bleed `#` section dividers, which
are a title on a coloured field by design — is left alone, and any tab still
holding content is never removed.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# A slide or tab heading, with the title and attribute block split out.
HEAD = re.compile(r"^(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]*\{([^}]*)\})?[ \t]*$", re.M)

# Text that is markup rather than content. The two need different flags: a
# fenced-div rail is one line, an HTML comment can span many, and combining them
# under DOTALL makes the rail pattern eat the rest of the file.
RAIL = re.compile(r"^:{2,}.*$", re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)

GENERATED = re.compile(
    r"<!-- BEGIN deck-frontmatter.*?<!-- END deck-frontmatter -->", re.S)


def sections(text):
    """Every heading, with the span of body text that belongs to it."""
    ms = [m for m in HEAD.finditer(text) if m.group(1)]
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out.append({
            "level": len(m.group(1)),
            "title": (m.group(2) or "").strip(),
            "attrs": m.group(3) or "",
            "start": m.start(),
            "head_end": m.end(),
            "end": end,
            "body": text[m.end():end],
        })
    return out


def is_blank(body):
    return not RAIL.sub("", COMMENT.sub("", body)).strip()


def in_generated(text, pos):
    return any(g.start() <= pos < g.end() for g in GENERATED.finditer(text))


def title_untitled(text):
    """Give every untitled slide the title its position implies."""
    fixed = []
    while True:
        secs = sections(text)
        target = None
        for i, s in enumerate(secs):
            if s["level"] != 2 or s["title"] or in_generated(text, s["start"]):
                continue
            # Walk back to the nearest slide that has a title.
            prev = next((p for p in reversed(secs[:i])
                         if p["title"] and p["level"] <= 2
                         and not in_generated(text, p["start"])), None)
            if not prev:
                continue
            # A `.center` slide is a section divider: this is that section's
            # first content slide, so it takes the section's name outright.
            # Anything else is a continuation of the slide before it.
            # Strip a "(cont.)" the previous pass added, so a run of four
            # continuation slides reads "The key concept (cont.)" four times
            # rather than accumulating a parenthesis per slide.
            base = re.sub(r"\s*\(cont\.\)\s*$", "", prev["title"])
            new = base if "center" in prev["attrs"] else f"{base} (cont.)"
            target = (s, new)
            break
        if not target:
            return text, fixed
        s, new = target
        head = text[s["start"]:s["head_end"]]
        attrs = f" {{{s['attrs']}}}" if s["attrs"] else ""
        text = text[:s["start"]] + f"## {new}{attrs}" + text[s["head_end"]:]
        fixed.append(new)


def drop_empty_tabs(text):
    """Remove tabs that open onto nothing, then close up the numbering."""
    dropped = []
    while True:
        secs = sections(text)
        hit = None
        for i, s in enumerate(secs):
            if s["level"] != 3 or in_generated(text, s["start"]):
                continue
            if not is_blank(s["body"]):
                continue
            # Only inside a tabset — a blank `###` under a full-bleed `#`
            # divider is a subtitle, and belongs there.
            before = text[:s["start"]]
            if "panel-tabset" not in before[-4000:]:
                continue
            opened = before.rfind("panel-tabset")
            closed = before.rfind(":::", opened)
            if opened == -1:
                continue
            hit = s
            break
        if not hit:
            break
        dropped.append(hit["title"])
        text = text[:hit["start"]] + text[hit["end"]:]

    # Renumber the tabsets whose labels are plain integers.
    def renumber(block):
        labels = re.findall(r"^### +(.+?) *$", block, re.M)
        if len(labels) < 2 or not all(l.isdigit() for l in labels):
            return block
        n = iter(range(1, len(labels) + 1))
        return re.sub(r"^### +\d+ *$", lambda _: f"### {next(n)}", block, flags=re.M)

    return re.sub(r"(?s)(:{2,} *(?:\{[^}]*\.)?panel-tabset.*?)(?=^#{1,2} )",
                  lambda m: renumber(m.group(1)), text, flags=re.M), dropped


def main():
    args = sys.argv[1:]
    check = "--check" in args
    only = next((a for a in args if a.isdigit()), None)

    decks = sorted(ROOT.glob("[01][0-9]-*/0[012]-*/MATH60033A-*.qmd"))
    n_titled = n_tabs = 0

    for q in decks:
        sess = q.parts[-3][:2]
        if only and sess != only:
            continue
        original = q.read_text()
        text, titled = title_untitled(original)
        text, dropped = drop_empty_tabs(text)
        if not titled and not dropped:
            continue
        n_titled += len(titled)
        n_tabs += len(dropped)
        print(f"\n── {q.relative_to(ROOT)}")
        if titled:
            print(f"     titled {len(titled)} slides:")
            for t in titled[:6]:
                print(f"        {t}")
            if len(titled) > 6:
                print(f"        … and {len(titled) - 6} more")
        if dropped:
            print(f"     dropped {len(dropped)} empty tabs: {', '.join(dropped)}")
        if not check:
            q.write_text(text)

    verb = "would fix" if check else "fixed"
    print(f"\n{verb}: {n_titled} blank slide titles, {n_tabs} empty tabs")


if __name__ == "__main__":
    main()
