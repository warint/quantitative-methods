"""Build assets/references.bib from a list of DOIs.

    python scripts/build_bibliography.py

The source of truth is references.dois at the repository root: one DOI per
line, blank lines and # comments ignored. A line may name its own citation key,

    10.1017/dap.2026.10085   key=warin-middlepowers

which matters once several works share a first author and a year: family+year
keys then collide and get disambiguated a, b, c by position in the file, so
inserting one reference silently renumbers the others. Every entry in the bibliography is
fetched from Crossref at build time and written out from the metadata the
publisher registered.

The point is that no reference in this book is typed from memory. A citation
written by hand can be subtly wrong — a year off, an initial wrong, a volume
that does not exist, a paper that does not exist at all — and a reader who
tries to follow it finds nothing. Here a DOI that does not resolve stops the
build, so the failure happens to the author rather than to the student.

Add a reference by adding its DOI. Cite it as @family-year in a chapter.
"""

import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DOIS = ROOT / "references.dois"
OUT = ROOT / "assets" / "references.bib"

API = "https://api.crossref.org/works/{}"
UA = {"User-Agent": "MATH60033A-course-repo/1.0 (mailto:thierry.warin@hec.ca)"}

# Crossref types -> BibTeX types. Anything unlisted becomes @misc.
TYPES = {
    "journal-article": "article",
    "book": "book",
    "book-chapter": "incollection",
    "proceedings-article": "inproceedings",
    "posted-content": "misc",
    "report": "techreport",
}


def citekey(msg, taken, explicit=None):
    if explicit:
        if explicit in taken:
            raise SystemExit(f"duplicate key in references.dois: {explicit}")
        taken.add(explicit)
        return explicit
    author = msg.get("author") or [{}]
    family = author[0].get("family") or msg.get("publisher") or "anon"
    family = re.sub(r"[^A-Za-z]", "", family).lower() or "anon"
    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0] or "nd"
    base = f"{family}{year}"
    key, suffix = base, ord("a")
    while key in taken:
        key = f"{base}{chr(suffix)}"
        suffix += 1
    taken.add(key)
    return key


def escape(text):
    """BibTeX-safe, and brace-protect capitals so styles cannot lowercase them."""
    text = re.sub(r"\s+", " ", str(text)).strip()
    text = text.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
    # Protect any word carrying an interior capital or a lone initial: AIC, R^2,
    # Gauss, Monte Carlo. Lowercasing those is the classic bibliography failure.
    return re.sub(r"(?<![{\\])\b([A-Z][A-Za-z]*[A-Z][A-Za-z]*|[A-Z][a-z]+)\b",
                  r"{\1}", text)


def entry(doi, msg, key):
    kind = TYPES.get(msg.get("type", ""), "misc")
    fields = {}

    authors = []
    for a in msg.get("author", []):
        if a.get("family"):
            authors.append(f"{a['family']}, {a.get('given', '')}".strip().rstrip(","))
        elif a.get("name"):
            authors.append(a["name"])
    if authors:
        fields["author"] = " and ".join(authors)

    if msg.get("title"):
        fields["title"] = escape(msg["title"][0])

    container = (msg.get("container-title") or [None])[0]
    if container:
        fields["journal" if kind == "article" else "booktitle"] = escape(container)

    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
    if year:
        fields["year"] = str(year)

    for src, dst in (("volume", "volume"), ("issue", "number"), ("page", "pages")):
        if msg.get(src):
            fields[dst] = str(msg[src])

    # Crossref reports the imprint as publisher for journal articles ("Informa
    # UK Limited"), which is noise in a reference list. Books need it.
    if kind != "article" and msg.get("publisher"):
        fields["publisher"] = escape(msg["publisher"])

    fields["doi"] = doi
    fields["url"] = f"https://doi.org/{doi}"

    body = ",\n".join(f"  {k:9} = {{{v}}}" for k, v in fields.items())
    return f"@{kind}{{{key},\n{body}\n}}\n"


def main():
    if not DOIS.exists():
        raise SystemExit(f"missing {DOIS.relative_to(ROOT)}")

    wanted = []
    for line in DOIS.read_text().splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        parts = line.split()
        key = next((p[4:] for p in parts[1:] if p.startswith("key=")), None)
        wanted.append((parts[0], key))

    dois = [d for d, _ in wanted]
    if len(set(dois)) != len(dois):
        dupes = {d for d in dois if dois.count(d) > 1}
        raise SystemExit(f"duplicate DOIs in references.dois: {', '.join(sorted(dupes))}")

    entries, taken, failed = [], set(), []
    for doi, explicit in wanted:
        r = requests.get(API.format(doi), headers=UA, timeout=45)
        if r.status_code != 200:
            failed.append((doi, f"HTTP {r.status_code}"))
            continue
        msg = r.json()["message"]
        key = citekey(msg, taken, explicit)
        entries.append((key, entry(doi, msg, key)))
        first = (msg.get("author") or [{}])[0].get("family", "?")
        year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
        print(f"  {key:22} {first}, {year}")

    if failed:
        for doi, why in failed:
            print(f"  FAILED {doi}: {why}", file=sys.stderr)
        raise SystemExit(f"\n{len(failed)} DOI(s) did not resolve — bibliography not written.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = ("% Generated by scripts/build_bibliography.py from references.dois.\n"
              "% Every entry comes from Crossref. Do not edit by hand.\n\n")
    OUT.write_text(header + "\n".join(e for _, e in sorted(entries)), encoding="utf-8")
    print(f"\n{len(entries)} references written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
