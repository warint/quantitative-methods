"""Verify every local asset the rendered book references actually exists.

    python scripts/check_book_assets.py

Run after a render. Exits non-zero, listing what is missing, if any page asks
for a stylesheet, script, image or font that is not on disk.

This exists because the book shipped unstyled and nobody noticed from the
build. Every page referenced

    site_libs/bootstrap/bootstrap-<hash>.min.css

and the whole site_libs/ directory had been deleted — by an unquoted
`rm -rf $(find ...)` where a path containing a space, "site_libs 2", split into
two arguments and took the real directory with it. Quarto did not complain: it
renders the HTML and writes the reference whether or not the target survives
afterwards. The failure is only visible in a browser, which is a bad place to
find out.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs" / "book"

# href/src on link, script, img, source — plus url() inside inline styles.
REF = re.compile(r'(?:href|src)="([^"]+)"|url\((["\']?)([^)"\']+)\2\)')


def local_refs(html):
    for m in REF.finditer(html):
        target = m.group(1) or m.group(3)
        if not target:
            continue
        if target.startswith(("//", "#")):
            continue
        parsed = urlparse(target)
        # Anything with a scheme is somebody else's problem: http, data,
        # mailto, and javascript:void(0) from Quarto's own code toggle.
        if parsed.scheme:
            continue
        yield unquote(parsed.path)


def main():
    if not SITE.exists():
        raise SystemExit(f"no rendered book at {SITE.relative_to(ROOT)} — run scripts/render_book.sh")

    missing, checked = {}, 0
    for page in sorted(SITE.glob("*.html")):
        html = page.read_text(encoding="utf-8", errors="replace")
        for ref in local_refs(html):
            if not ref or ref.endswith("/"):
                continue
            # References are relative to the page's own directory.
            target = (page.parent / ref).resolve()
            checked += 1
            if not target.exists():
                missing.setdefault(ref, []).append(page.name)

    if missing:
        print(f"{len(missing)} referenced asset(s) missing:\n", file=sys.stderr)
        for ref, pages in sorted(missing.items()):
            where = pages[0] if len(pages) == 1 else f"{len(pages)} pages"
            print(f"  {ref}\n      referenced by {where}", file=sys.stderr)
        raise SystemExit("\nThe book would render without them. Re-run scripts/render_book.sh.")

    print(f"  {checked} local references checked across "
          f"{len(list(SITE.glob('*.html')))} pages — all present")


if __name__ == "__main__":
    main()
