"""Fetch and treat the chapter portraits.

    python scripts/build_portraits.py            # everything in ROSTER
    python scripts/build_portraits.py 03         # one session

Every portrait is a real public-domain painting or photograph from Wikimedia
Commons, downloaded once into assets/portraits/ and committed. Nothing here
invents a likeness: these are the faces as their contemporaries painted them.

What the script adds is a *uniform treatment*, so that eleven portraits made
across two centuries — an 1840 oil, an 1890 albumen print, an engraving — read
as one set of plates in one book rather than as elevenPictures scraped from the
internet. Each is cropped to the same 4:5, mapped onto the same warm two-tone
range as the book's paper, vignetted, and set in the same gilt frame.

The licence gate is not optional. A file whose Commons metadata does not say
public domain is refused, loudly, and no image is written. If a mathematician
you want is missing from ROSTER it is usually because no free portrait of them
exists — most of the twentieth century is still in copyright — and the honest
options are to pick an earlier figure or to go without.

Attribution for every plate is written to assets/portraits/credits.json and
rendered into the caption by scripts/build_book.py.
"""

import html as htmllib
import io
import json
import re
import sys
from pathlib import Path

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "portraits"

API = "https://commons.wikimedia.org/w/api.php"
UA = "MATH60033A-course-repo/1.0 (https://github.com/warint/quantitative-methods)"

# Licence strings Commons uses for material that is free of copyright.
FREE = ("public domain", "pd", "cc0")

# session -> (slug, name, dates, Commons file, why this person, crop)
#
# crop is an optional (left, top, right, bottom) box in fractions of the source,
# for sheets that hold more than one sitter. Boilly drew Legendre and Fourier on
# one leaf, so Legendre is the left half of it.
ROSTER = {
    "02": [
        # Hering photographed her twice in 1858. The other frame is a
        # full-length carte-de-visite, in which the face is a few dozen pixels
        # across at plate size; this is the bust portrait from the same sitting.
        ("nightingale", "Florence Nightingale", "1820–1910",
         "File:Florence Nightingale (H Hering NPG x82368).jpg",
         "Made the case with a chart rather than a table, and changed policy with it.",
         None),
    ],
    "03": [
        ("gauss", "Carl Friedrich Gauss", "1777–1855",
         "File:Carl Friedrich Gauss 1840 by Jensen.jpg",
         "Least squares, and the theorem that says when it is the best you can do.",
         None),
        ("legendre", "Adrien-Marie Legendre", "1752–1833",
         "File:Legendre and Fourier (1820).jpg",
         "Published least squares first, in 1805. This caricature is the only "
         "likeness of him known to exist.",
         (0.02, 0.02, 0.50, 0.98)),
    ],
    "04": [
        ("verhulst", "Pierre François Verhulst", "1804–1849",
         "File:P.F. Verhulst, PA02415.jpg",
         "Named the logistic curve in 1845, modelling how populations stop growing.",
         None),
    ],
    "07": [
        ("pearson", "Karl Pearson", "1857–1936",
         "File:Portrait of Karl Pearson.jpg",
         "Principal components, 1901 — lines and planes of closest fit.",
         None),
    ],
    "10": [
        ("hume", "David Hume", "1711–1776",
         "File:David Hume Ramsay.jpg",
         "Asked what entitles us to say one thing causes another, and did not "
         "find a satisfying answer. Neither has anyone since.",
         None),
    ],
    "11": [
        ("snow", "John Snow", "1813–1858",
         "File:John Snow.jpg",
         "Mapped cholera deaths in 1854 and read a natural experiment off the "
         "water supply — before the statistics existed to justify it.",
         None),
    ],
}

# Chapters with no plate, and why. Every one of these was looked for:
#   01  an introduction, not a method — nobody in particular to show
#   05  ridge and lasso are 1970 and 1996; Tikhonov, Hoerl, Kennard and
#       Tibshirani are all still in copyright
#   06  Udny Yule is the right figure for spurious regression across groups;
#       Commons has no portrait of him
#   08  k-nearest neighbours is Fix and Hodges, 1951 — no free likeness
#   09  Spearman is the right figure and his photograph is CC BY-SA 4.0, not
#       public domain, so fetch() refuses it
#   12  a presentation chapter; no historical claim to attach a face to
#
# The rule is not negotiable: a real portrait, freely licensed, or none.

# The plate. 4:5 at 900px wide, then framed.
W, H = 900, 1125
SHADOW = (62, 47, 32)        # warm bistre — the darkest ink on the leaf
HIGHLIGHT = (247, 241, 228)  # the book's paper, one shade warmer
PAPER = (242, 236, 222)      # the album leaf the plate is mounted on
RULE = (196, 182, 158)       # the pencil rule around it


def fetch(title):
    """Metadata and bytes for one Commons file, or raise if it is not free."""
    r = requests.get(API, params={
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|extmetadata", "titles": title,
    }, headers={"User-Agent": UA}, timeout=60)
    r.raise_for_status()
    pages = r.json()["query"]["pages"]
    page = next(iter(pages.values()))
    if "imageinfo" not in page:
        raise SystemExit(f"not on Commons: {title}")

    info = page["imageinfo"][0]
    meta = info["extmetadata"]

    def field(key):
        # Commons stores these as HTML; entities survive tag-stripping and
        # would print as "Elliott &amp; Fry" in a caption.
        raw = re.sub(r"<[^>]+>", "", str(meta.get(key, {}).get("value", "")))
        return htmllib.unescape(raw).strip()

    licence = field("LicenseShortName")
    if not any(f in licence.lower() for f in FREE):
        raise SystemExit(
            f"REFUSED {title}\n"
            f"  licence is {licence!r}, which is not public domain.\n"
            f"  This script only handles material that is free of copyright."
        )

    img = requests.get(info["url"], headers={"User-Agent": UA}, timeout=120)
    img.raise_for_status()

    # Catalogue annotations belong in a catalogue, not in a caption:
    # "Flameng, Léopold (French painter and engraver, 1831-1911) (artist)".
    artist = re.sub(r"\s*\([^)]*\)", "", field("Artist")).strip(" ,;") or "unknown"

    # Some records carry the file's upload timestamp in the date field. A
    # portrait was not painted at 14:33:54.
    date = re.sub(r"date QS:.*", "", field("DateTimeOriginal")).strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}", date):
        date = ""

    return {
        "commons": page["title"],
        "licence": licence,
        "artist": artist,
        "date": date or "undated",
        "descriptionurl": info.get("descriptionurl", ""),
    }, img.content


def wash(img, keep=0.55):
    """Ink-and-wash: colour held back, blacks lifted to a warm brown.

    Boilly's caricatures are watercolour on cream; the Jensen portrait of Gauss
    is a dark oil. Pushed all the way to one duotone they lose what makes the
    caricature worth looking at. Held part-way — desaturated, shadows warmed,
    highlights taken to paper — a 1820 watercolour and an 1840 oil sit on the
    same page as leaves from one album.
    """
    arr = np.asarray(img).astype(np.float32) / 255.0
    grey = arr @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    arr = arr * keep + grey[..., None] * (1 - keep)

    shadow = np.array(SHADOW, dtype=np.float32) / 255.0
    paper = np.array(HIGHLIGHT, dtype=np.float32) / 255.0
    arr = shadow + (paper - shadow) * arr            # compress onto the ink range
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "RGB")


def deckle(size, rng):
    """A soft, slightly irregular edge — a leaf lifted from an album."""
    w, h = size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle([0, 0, w - 1, h - 1], fill=255)
    m = np.asarray(mask).astype(np.float32)

    # Perturb the border inward by a few pixels of low-frequency noise.
    edge = 9
    for axis, length in ((0, w), (1, h)):
        noise = rng.random(length) * edge
        noise = np.convolve(noise, np.ones(31) / 31, mode="same")
        for i in range(length):
            d = int(noise[i])
            if axis == 0:
                m[:d, i] = 0
                m[h - d:, i] = 0
            else:
                m[i, :d] = 0
                m[i, w - d:] = 0
    return Image.fromarray(m.astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.6))


def album_leaf(plate, rng):
    """Set the plate on cream laid paper, with grain and a drawn rule."""
    pad = 34
    w, h = plate.size
    W, H = w + pad * 2, h + pad * 2

    grain = rng.normal(0, 3.1, (H, W, 1)).astype(np.float32)
    paper = np.clip(np.array(PAPER, dtype=np.float32) + grain, 0, 255)
    canvas = Image.fromarray(paper.astype(np.uint8), "RGB")

    canvas.paste(plate, (pad, pad), deckle(plate.size, rng))

    # A pencil rule just outside the image, the way an album leaf is ruled.
    d = ImageDraw.Draw(canvas)
    d.rectangle([pad - 7, pad - 7, W - pad + 6, H - pad + 6],
                outline=RULE, width=1)
    return canvas


def treat(raw_bytes, crop=None, seed=0):
    img = Image.open(io.BytesIO(raw_bytes))
    img = ImageOps.exif_transpose(img).convert("RGB")

    if crop:
        w, h = img.size
        l, tp, r, b = crop
        img = img.crop((int(w * l), int(h * tp), int(w * r), int(h * b)))

    # Crop to 4:5 about the upper middle — where a portrait keeps its face.
    w, h = img.size
    target = W / H
    if w / h > target:
        new_w = int(h * target)
        img = img.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:
        new_h = int(w / target)
        top = int((h - new_h) * 0.18)
        img = img.crop((0, top, w, top + new_h))

    img = img.resize((W, H), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    rng = np.random.default_rng(seed)
    return album_leaf(wash(img), rng)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    OUT.mkdir(parents=True, exist_ok=True)

    credits_path = OUT / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}

    for num, sitters in sorted(ROSTER.items()):
        if only and num != only:
            continue
        entries = []
        for seed, (slug, name, dates, title, why, crop) in enumerate(sitters):
            print(f"session {num}: {name}")
            meta, blob = fetch(title)
            out = OUT / f"session-{num}-{slug}.jpg"
            treat(blob, crop, seed).save(out, "JPEG", quality=90, optimize=True)
            entries.append({
                "slug": slug, "name": name, "dates": dates, "why": why,
                "file": out.relative_to(ROOT).as_posix(), **meta,
            })
            print(f"  {meta['artist']}, {meta['date']} — {meta['licence']}")
            print(f"  wrote {out.relative_to(ROOT)}")
        credits[f"session-{num}"] = entries

    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n")
    print(f"\ncredits written to {credits_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
