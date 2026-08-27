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

import json
import re
import sys
from pathlib import Path

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "portraits"

API = "https://commons.wikimedia.org/w/api.php"
UA = "MATH60033A-course-repo/1.0 (https://github.com/warint/quantitative-methods)"

# Licence strings Commons uses for material that is free of copyright.
FREE = ("public domain", "pd", "cc0")

# session -> (slug, display name, dates, Commons file, why this person)
ROSTER = {
    "03": ("gauss", "Carl Friedrich Gauss", "1777–1855",
           "File:Carl Friedrich Gauss 1840 by Jensen.jpg",
           "Least squares, and the theorem that says when it is the best you can do."),
}

# The plate. 4:5 at 900px wide, then framed.
W, H = 900, 1125
SHADOW = (58, 42, 24)        # warm bistre, the darkest ink in the plate
HIGHLIGHT = (243, 234, 216)  # the book's paper, one shade warmer
FRAME_GOLD = (176, 138, 58)
FRAME_DARK = (74, 58, 30)
MAT = (238, 231, 216)


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
        return re.sub(r"<[^>]+>", "", str(meta.get(key, {}).get("value", ""))).strip()

    licence = field("LicenseShortName")
    if not any(f in licence.lower() for f in FREE):
        raise SystemExit(
            f"REFUSED {title}\n"
            f"  licence is {licence!r}, which is not public domain.\n"
            f"  This script only handles material that is free of copyright."
        )

    img = requests.get(info["url"], headers={"User-Agent": UA}, timeout=120)
    img.raise_for_status()
    return {
        "commons": page["title"],
        "licence": licence,
        "artist": field("Artist") or "unknown",
        "date": re.sub(r"date QS:.*", "", field("DateTimeOriginal")).strip() or "undated",
        "descriptionurl": info.get("descriptionurl", ""),
    }, img.content


def duotone(grey):
    """Map a greyscale plate onto the book's warm two-tone range."""
    ramp = []
    for i in range(256):
        t = i / 255
        ramp += [round(SHADOW[c] + (HIGHLIGHT[c] - SHADOW[c]) * t) for c in range(3)]
    # Image.point wants one flat channel list per band, so split and remap.
    r = grey.point([ramp[i * 3] for i in range(256)])
    g = grey.point([ramp[i * 3 + 1] for i in range(256)])
    b = grey.point([ramp[i * 3 + 2] for i in range(256)])
    return Image.merge("RGB", (r, g, b))


def vignette(img, strength=0.34):
    """Darken the corners, the way an old varnish does.

    A radial falloff computed per pixel, not a drawn ellipse: an ellipse leaves
    a visible rim where its edge lands, which on a plate this size reads as a
    printing fault rather than as age.
    """
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w * 0.70)) ** 2 + ((yy - h / 2) / (h * 0.70)) ** 2)
    # Flat across the middle, then easing away — nothing happens before r=0.55.
    fall = np.clip((r - 0.55) / 0.85, 0, 1) ** 1.6
    mask = np.clip(1.0 - strength * fall, 0, 1)

    arr = np.asarray(img).astype(np.float32)
    dark = np.array(SHADOW, dtype=np.float32)
    out = arr * mask[..., None] + dark * (1 - mask[..., None])
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def frame(plate):
    """Mat and gilt border, identical on every plate in the book."""
    mat_w, gilt_w = 26, 14
    pad = mat_w + gilt_w
    w, h = plate.size
    canvas = Image.new("RGB", (w + pad * 2, h + pad * 2), FRAME_GOLD)
    d = ImageDraw.Draw(canvas)

    # Gilt is flat colour plus two rules, which reads as moulding at book size.
    d.rectangle([2, 2, canvas.width - 3, canvas.height - 3], outline=FRAME_DARK, width=2)
    d.rectangle([gilt_w - 3, gilt_w - 3, canvas.width - gilt_w + 2, canvas.height - gilt_w + 2],
                fill=MAT)
    d.rectangle([pad - 2, pad - 2, canvas.width - pad + 1, canvas.height - pad + 1],
                outline=FRAME_DARK, width=2)
    canvas.paste(plate, (pad, pad))
    return canvas


def treat(raw_bytes):
    img = Image.open(raw_bytes if hasattr(raw_bytes, "read") else __import__("io").BytesIO(raw_bytes))
    img = ImageOps.exif_transpose(img).convert("RGB")

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
    grey = ImageOps.autocontrast(ImageOps.grayscale(img), cutoff=1)
    plate = duotone(grey)
    plate = ImageEnhance.Contrast(plate).enhance(1.06)
    return frame(vignette(plate))


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    OUT.mkdir(parents=True, exist_ok=True)

    credits_path = OUT / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}

    for num, (slug, name, dates, title, why) in sorted(ROSTER.items()):
        if only and num != only:
            continue
        print(f"session {num}: {name}")
        meta, blob = fetch(title)
        out = OUT / f"session-{num}-{slug}.jpg"
        treat(blob).save(out, "JPEG", quality=88, optimize=True)
        credits[f"session-{num}"] = {
            "slug": slug, "name": name, "dates": dates, "why": why,
            "file": out.relative_to(ROOT).as_posix(), **meta,
        }
        print(f"  {meta['artist']}, {meta['date']} — {meta['licence']}")
        print(f"  wrote {out.relative_to(ROOT)}")

    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n")
    print(f"\ncredits written to {credits_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
