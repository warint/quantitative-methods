"""Generate the emblem plates for chapters that have no portrait.

    python scripts/build_plates.py            # every chapter in PROMPTS
    python scripts/build_plates.py 05         # one chapter
    python scripts/build_plates.py --list     # print the prompts, generate nothing

Six chapters have no free likeness of the person whose work they teach — the
reasons are recorded in scripts/build_portraits.py. Rather than leave them bare,
each gets an *emblem*: an object or a scene standing for the method, drawn in
the same register as the album leaves so the book keeps one visual voice.

These images are generated, locally, with FLUX via mflux. Two rules govern them,
and neither is negotiable.

**Never presented as a likeness.** These portraits are inventions. No face is
being reproduced, because for these figures no free image exists to reproduce.
Each caption says so in as many words — "generated image, a free interpretation
based on various sources, not a likeness" — so a reader is never left to guess
which plates are historical documents and which are illustration. That is the
whole basis on which they belong in the book at all.

**Only the dead.** Hoerl, Kennard and Tibshirani are alive, so chapter 5 takes
Tikhonov instead. Manufacturing the face of a living person is a different act
from imagining a Victorian statistician, and this script will not do it.

The prompts are the source. They live here, in the repository, so the plates can
be regenerated, criticised and changed like any other build artefact — the same
reason the figures are computed rather than pasted in.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
MFLUX = ROOT / ".venv" / "bin" / "mflux-generate"

# A pre-quantised, ungated mirror. black-forest-labs/FLUX.1-schnell is gated and
# needs a Hugging Face login; this is the same model at 4-bit, about 9.6 GB
# rather than 24, published by the mflux community organisation.
MODEL_REPO = "mflux-community/flux-1-schnell-mflux-q4"
MODEL_GB = 9.7
HEADROOM_GB = 5.0


def check_disk():
    """Refuse to start if the download would leave the disk uncomfortably full.

    Written after a previous run pulled a 31 GB model in the background and took
    the machine to 98% full before anyone noticed. A model download is the one
    thing this repository does that can fill a disk, so it asks first.
    """
    free_gb = shutil.disk_usage(ROOT).free / 1e9
    cached = Path.home() / ".cache/huggingface/hub" / ("models--" + MODEL_REPO.replace("/", "--"))
    if cached.exists():
        return
    needed = MODEL_GB + HEADROOM_GB
    if free_gb < needed:
        raise SystemExit(
            f"Not enough disk. {MODEL_REPO} is about {MODEL_GB:.0f} GB and this "
            f"leaves {HEADROOM_GB:.0f} GB of headroom, so {needed:.0f} GB is "
            f"wanted and {free_gb:.1f} GB is free.\n"
            f"Free some space, or generate the plates elsewhere and drop them in "
            f"{OUT.relative_to(ROOT)}/."
        )
    print(f"  disk: {free_gb:.1f} GB free, model is about {MODEL_GB:.0f} GB")

# One house style, appended to every prompt, so eleven plates look like one set.
# It deliberately echoes the treatment applied to the real portraits: ink and
# wash on cream laid paper, restrained colour, nothing photographic.
_COMMON = (
    "fine ink linework with pale watercolour wash, cream laid paper with visible "
    "grain, muted bistre brown and ochre with one restrained accent, soft even "
    "daylight, no lettering, no text, no numbers, no signature, generous margins"
)

HOUSE = {
    # Still lifes: explicitly no people.
    "emblem": ("hand-coloured engraving from an early nineteenth-century French "
               "scientific album, centred still-life composition, no people, "
               f"{_COMMON}, engraved plate for a treatise"),
    # Portraits: the same palette and paper, but a sitter rather than objects.
    "invented": ("hand-coloured portrait plate from a nineteenth-century "
                 "scientific album, single sitter, head and shoulders, centred, "
                 f"{_COMMON}, painted in oils, plain unadorned background"),
}

# chapter -> (slug, caption title, what it stands for, the subject of the plate)
#
# Two kinds of plate live here.
#
# INVENTED PORTRAITS, for chapters whose figure has no freely licensed likeness.
# These are *not* likenesses. Nobody's face is being reproduced: the prompt asks
# for a period-appropriate imagined portrait, and the caption says so in the
# words the user chose — "free interpretation based on various sources". The one
# line not crossed is that every subject is long dead. Hoerl, Kennard and
# Tibshirani are alive, so chapter 5 takes Tikhonov, who is not.
#
# EMBLEMS, for chapters with no person at all — an introduction and a conclusion
# have no face to put on them.
PROMPTS = {
    "01": (
        "instruments",
        "The instruments of the argument",
        "An introduction has no single figure to show; it has a question — what "
        "entitles a number about the past to say anything about the future.",
        "an hourglass beside an open ledger of handwritten columns of figures, a "
        "brass telescope resting across the page, a pair of dividers",
        "emblem",
    ),
    "05": (
        "tikhonov",
        "Andrey Tikhonov · 1906–1993",
        "Regularisation of ill-posed problems, the idea ridge regression rests "
        "on. Hoerl, Kennard and Tibshirani are living, so the chapter's plate "
        "is Tikhonov.",
        "an imagined painted portrait of a mid-twentieth-century Russian "
        "mathematician, seated three-quarter view, dark suit, spectacles, "
        "thoughtful expression, plain muted background",
        "invented",
    ),
    "06": (
        "yule",
        "George Udny Yule · 1871–1951",
        "Showed in 1903 that an association can reverse when groups are "
        "combined — the aggregation warning this chapter is built on.",
        "an imagined painted portrait of a late-Victorian British statistician, "
        "seated, high collar and dark academic coat, moustache, three-quarter "
        "view, plain muted background",
        "invented",
    ),
    "08": (
        "fix",
        "Evelyn Fix · 1904–1965",
        "With Joseph Hodges, wrote the 1951 report that introduced nearest "
        "neighbours — unpublished for nearly forty years.",
        "an imagined painted portrait of a mid-twentieth-century American woman "
        "mathematician, seated at a desk, short waved hair, plain jacket, "
        "calm direct gaze, plain muted background",
        "invented",
    ),
    "09": (
        "spearman",
        "Charles Spearman · 1863–1945",
        "Argued in 1904 for a general factor behind correlated abilities, and "
        "began the tradition of measuring what cannot be observed.",
        "an imagined painted portrait of an early-twentieth-century British "
        "psychologist, elderly, seated, wing collar and dark jacket, white "
        "moustache, three-quarter view, plain muted background",
        "invented",
    ),
    "12": (
        "assembly",
        "Making someone act on it",
        "The last chapter is about a decision-maker, not a model.",
        "an empty lecture theatre seen from the floor, curved wooden benches "
        "rising in tiers, a lectern and a large blank chart stand in the "
        "foreground",
        "emblem",
    ),
}


def prompt_for(chapter):
    subject, kind = PROMPTS[chapter][3], PROMPTS[chapter][4]
    return f"{subject}, {HOUSE[kind]}"


def generate(chapter, steps=4, seed=None):
    slug = PROMPTS[chapter][0]
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / f"session-{chapter}-{slug}-raw.png"

    check_disk()
    cmd = [
        str(MFLUX),
        "--model", MODEL_REPO,
        "--base-model", "schnell",
        "--steps", str(steps),
        "--height", "1024", "--width", "832",     # 4:5, the album proportion
        "--seed", str(seed if seed is not None else 60033 + int(chapter)),
        "--prompt", prompt_for(chapter),
        "--output", str(raw),
    ]
    print(f"  generating session-{chapter} ({slug}) …")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        tail = (result.stderr or result.stdout or "").strip().splitlines()[-6:]
        raise SystemExit(f"mflux failed for chapter {chapter}:\n  " + "\n  ".join(tail))
    return raw


def main():
    args = [a for a in sys.argv[1:]]
    if "--list" in args:
        for ch in sorted(PROMPTS):
            slug, title, why, _, kind = PROMPTS[ch]
            print(f"\n── chapter {ch} · {slug} · {title}  [{kind}]")
            print(f"   stands for: {why}")
            print(f"   prompt: {prompt_for(ch)}")
        return

    only = next((a for a in args if a.isdigit() or (len(a) == 2 and a.isdigit())), None)
    chapters = [only] if only else sorted(PROMPTS)

    # The album treatment lives with the portraits; the emblems wear the same one.
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_portraits import album_leaf, wash, W, H
    import numpy as np
    from PIL import Image

    import json
    credits_path = OUT / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}

    for ch in chapters:
        if ch not in PROMPTS:
            raise SystemExit(f"no prompt for chapter {ch}")
        slug, title, why, subject, kind = PROMPTS[ch]
        raw = generate(ch)
        img = Image.open(raw).convert("RGB").resize((W, H), Image.LANCZOS)
        rng = np.random.default_rng(int(ch))
        out = OUT / f"session-{ch}-{PROMPTS[ch][0]}.jpg"
        album_leaf(wash(img), rng).save(out, "JPEG", quality=90, optimize=True)
        raw.unlink(missing_ok=True)

        # The disclosure travels with the image, so a caption can never be
        # rendered without it.
        note = ("Generated image — a free interpretation based on various "
                "sources, not a likeness." if kind == "invented"
                else "Generated image — an emblem, not a historical document.")
        credits[f"session-{ch}"] = {
            "slug": slug, "name": title, "why": why, "kind": kind,
            "file": out.relative_to(ROOT).as_posix(),
            "generated": True, "note": note,
            "model": "FLUX.1-schnell at 4-bit, via mflux",
            "prompt": prompt_for(ch),
        }
        print(f"  wrote {out.relative_to(ROOT)}  [{kind}]")

    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n")
    print(f"\ncredits written to {credits_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
