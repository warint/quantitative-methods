#!/usr/bin/env python3
"""Check that docs/ is a working site before it is pushed to Pages.

    python scripts/check_site.py

Run after:

    scripts/render_session_lectures.sh
    python scripts/build_docs.py

GitHub Pages serves whatever is in `docs/` without validating any of it. A deck
that failed to render, a cheatsheet that was never rebuilt, a link to a file
that moved — all of them publish silently and are found by a student, in the
week they need the file. This checks the four things that actually break:

1. **Every session is present** — pre-session, lecture and practice deck for
   each session the spec knows about, plus its cheatsheet.
2. **Every local link resolves** — every `href` and `src` in every page under
   `docs/` that points at a local file, including the ones the index generates.
3. **Nothing is a stub** — a deck that failed mid-render still writes an HTML
   file, just a very small one.
4. **The decks are not stale** — a `.qmd` newer than the `.html` beside it means
   the deck was edited and never re-rendered, which is the failure that reaches
   a classroom.

Exit status is non-zero if anything fails, so it can gate a push.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urldefrag

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from course_spec import SESSIONS, ordered  # noqa: E402

DOCS = ROOT / "docs"

# A deck that rendered is self-contained and megabytes wide. A deck that died
# half way still leaves a file behind.
MIN_DECK_BYTES = 200_000
MIN_PDF_BYTES = 10_000

LINK = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)


def problems():
    """Yield one string per thing wrong with the site."""
    if not DOCS.is_dir():
        yield "docs/ does not exist — run scripts/build_docs.py"
        return

    # ---- 1 · every session's artefacts are published --------------------
    for num, s in ordered():
        for kind in ("pre-session", "lecture", "practice"):
            f = DOCS / f"session-{num}-{kind}.html"
            src = list((ROOT / s["dir"]).glob(f"0*/MATH60033A-S{num}-*.qmd"))
            expected = any(kind.replace("-", "").lower() in q.stem.replace("-", "").lower()
                           for q in src)
            if not expected:
                continue                       # session 12 has no practice deck
            if not f.exists():
                yield f"missing: {f.relative_to(ROOT)}"
            elif f.stat().st_size < MIN_DECK_BYTES:
                yield (f"stub: {f.relative_to(ROOT)} is only "
                       f"{f.stat().st_size / 1024:.0f} KB — did the render fail?")

        sheet = DOCS / f"python-cheatsheet-{num}.pdf"
        if not sheet.exists():
            yield f"missing: {sheet.relative_to(ROOT)}"
        elif sheet.stat().st_size < MIN_PDF_BYTES:
            yield f"stub: {sheet.relative_to(ROOT)} is {sheet.stat().st_size} bytes"

    if not (DOCS / "index.html").exists():
        yield "missing: docs/index.html"

    # ---- 2 · every local link resolves ----------------------------------
    # Only the small pages are scanned. The decks are self-contained, so their
    # every asset is inlined and the only links they carry are external.
    for page in sorted(DOCS.glob("*.html")):
        if page.stat().st_size > MIN_DECK_BYTES:
            continue
        for raw in LINK.findall(page.read_text(encoding="utf-8", errors="ignore")):
            target = unquote(urldefrag(raw)[0])
            if not target or target.startswith(("http://", "https://", "mailto:",
                                                "data:", "#", "//")):
                continue
            resolved = (page.parent / target).resolve()
            if not resolved.exists():
                yield f"broken link: {page.name} -> {target}"

    # ---- 3 · the decks are not stale ------------------------------------
    for qmd in sorted(ROOT.glob("[0-9][0-9]-*/0[0-2]-*/MATH60033A-S*.qmd")):
        html = qmd.with_suffix(".html")
        if not html.exists():
            yield f"never rendered: {qmd.relative_to(ROOT)}"
        elif qmd.stat().st_mtime > html.stat().st_mtime:
            yield f"stale: {qmd.relative_to(ROOT)} is newer than its .html"

    for sheet in sorted(ROOT.glob("[0-9][0-9]-*/PYTHON-CHEATSHEET.qmd")):
        pdf = sheet.with_suffix(".pdf")
        if pdf.exists() and sheet.stat().st_mtime > pdf.stat().st_mtime:
            yield f"stale: {sheet.relative_to(ROOT)} is newer than its .pdf"


def main():
    found = list(problems())
    n_decks = len(list(DOCS.glob("session-*.html"))) if DOCS.is_dir() else 0
    n_sheets = len(list(DOCS.glob("python-cheatsheet-*.pdf"))) if DOCS.is_dir() else 0
    print(f"docs/: {n_decks} decks, {n_sheets} cheatsheets, "
          f"{len(SESSIONS)} sessions in the spec")

    if not found:
        print("\nthe site is complete and every local link resolves.")
        return 0
    print()
    for p in found:
        print(f"  {p}")
    print(f"\n{len(found)} problem(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
