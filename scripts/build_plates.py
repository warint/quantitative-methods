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

**No faces of real people.** A generated likeness of Tikhonov or Yule would be
an invented portrait of a real person printed in a textbook — which is exactly
the failure the Legendre plate exists to warn about, except committed on
purpose. Every prompt here depicts instruments, geometry or an anonymous scene.

**Labelled as synthetic.** The caption says so. A reader must never have to
guess which plates are historical documents and which are illustration.

The prompts are the source. They live here, in the repository, so the plates can
be regenerated, criticised and changed like any other build artefact — the same
reason the figures are computed rather than pasted in.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
VENV_PY = ROOT / ".venv" / "bin" / "python"

# One house style, appended to every prompt, so eleven plates look like one set.
# It deliberately echoes the treatment applied to the real portraits: ink and
# wash on cream laid paper, restrained colour, nothing photographic.
HOUSE = (
    "hand-coloured engraving from an early nineteenth-century French scientific "
    "album, fine ink linework with pale watercolour wash, cream laid paper with "
    "visible grain, muted bistre brown and ochre with one restrained accent, "
    "soft even daylight, no lettering, no text, no numbers, no signature, "
    "no people, centred still-life composition, generous margins, "
    "engraved plate for a treatise"
)

# chapter -> (slug, caption title, what it stands for, the subject of the plate)
PROMPTS = {
    "01": (
        "instruments",
        "The instruments of the argument",
        "An introduction has no single figure to show; it has a question — what "
        "entitles a number about the past to say anything about the future.",
        "an hourglass beside an open ledger of handwritten columns of figures, a "
        "brass telescope resting across the page, a pair of dividers",
    ),
    "05": (
        "constraint",
        "The constraint region",
        "Ridge and lasso differ in the shape they are allowed to move inside: a "
        "circle, whose boundary is smooth, and a diamond, whose corners lie on "
        "the axes and are the reason the lasso sets coefficients to zero.",
        "a draughtsman's plate showing a circle and a diamond inscribed within "
        "the same square, drawn in fine ink with compass and set-square lying "
        "beside them on the paper",
    ),
    "06": (
        "panel",
        "The same question, in every country and every year",
        "A panel is two dimensions at once — units and time — and the awkwardness "
        "of that is the chapter.",
        "a folding map of Europe on a table, gridded with fine ruled lines, small "
        "brass pins set at intervals across it, a pantograph beside it",
    ),
    "08": (
        "neighbours",
        "The nearest neighbours",
        "A prediction made by looking at whatever is closest, and the question of "
        "how many neighbours is too few.",
        "an array of small brass pins set in a board, fine silk threads strung "
        "between each pin and its closest few, forming an irregular web",
    ),
    "09": (
        "latent",
        "Measuring what cannot be seen",
        "A latent variable is inferred from its effects, never observed directly.",
        "an apothecary's balance weighing an object concealed beneath a draped "
        "cloth, the pans in equilibrium, brass weights arranged alongside",
    ),
    "12": (
        "assembly",
        "Making someone act on it",
        "The last chapter is about a decision-maker, not a model.",
        "an empty lecture theatre seen from the floor, curved wooden benches "
        "rising in tiers, a lectern and a large blank chart stand in the "
        "foreground",
    ),
}


def prompt_for(chapter):
    _, _, _, subject = PROMPTS[chapter]
    return f"{subject}, {HOUSE}"


def generate(chapter, steps=4, seed=None):
    slug = PROMPTS[chapter][0]
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / f"session-{chapter}-{slug}-raw.png"

    cmd = [
        str(VENV_PY), "-m", "mflux.generate",
        "--model", "schnell",
        "--quantize", "4",
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
            slug, title, why, _ = PROMPTS[ch]
            print(f"\n── chapter {ch} · {slug} · {title}")
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

    for ch in chapters:
        if ch not in PROMPTS:
            raise SystemExit(f"no prompt for chapter {ch}")
        raw = generate(ch)
        img = Image.open(raw).convert("RGB").resize((W, H), Image.LANCZOS)
        rng = np.random.default_rng(int(ch))
        out = OUT / f"session-{ch}-{PROMPTS[ch][0]}.jpg"
        album_leaf(wash(img), rng).save(out, "JPEG", quality=90, optimize=True)
        raw.unlink(missing_ok=True)
        print(f"  wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
