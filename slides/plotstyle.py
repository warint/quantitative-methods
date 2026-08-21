"""
Shared matplotlib style for the lecture figures.

Import it at the top of a deck's first code cell:

    import sys; sys.path.insert(0, "../slides")
    from plotstyle import setup, CL
    setup()

Every figure in the course then shares one palette and one set of defaults, so a
student reading four decks in a row is not re-learning what the colours mean.

The palette class is called `CL`, not `C`: patsy reserves the name `C` for
categorical terms in a model formula, so a deck that imported `C` could not
then write `C(nace_r2)`.

The palette is the one used by the slide theme, which is in turn the palette of
warin.ca — see `warin.scss`. Colours carry consistent meaning across the course:

    CL.ink     the data, or the thing being estimated
    CL.accent  the fitted model, the estimate, the thing you computed
    CL.warn    the trap, the wrong answer, the naive baseline
    CL.good    the correct answer, the honest number
    CL.muted   reference lines, benchmarks, chance
"""

import matplotlib
from typing import ClassVar


class CL:
    """Course palette. Same hex values as slides/warin.scss."""

    bg = "#F7F6F3"
    ink = "#16181A"
    muted = "#6E7275"
    line = "#DEDCD6"
    accent = "#1C73C5"
    warn = "#B4553A"
    good = "#2E7D5B"
    # a categorical ramp for when more than four series are unavoidable
    ramp: ClassVar[list[str]] = ["#1C73C5", "#B4553A", "#2E7D5B",
                                 "#6E7275", "#8FB2FF", "#16181A"]


def setup(width=7.2, height=3.6):
    """Apply the course defaults. Call once per deck, in the first cell.

    The default figure is wide and short because a slide is wide and short: a
    square figure on a 16:9 slide wastes half the frame and forces the type
    smaller than it needs to be.
    """
    # Only force a headless backend when we are NOT inside a Jupyter kernel.
    # Quarto executes deck cells through ipykernel and captures figures via its
    # inline backend; calling matplotlib.use("Agg") here replaces that backend
    # and the figures silently vanish from the rendered deck.
    try:
        get_ipython()          # defined only inside a kernel
        in_kernel = True
    except NameError:
        in_kernel = False
    if not in_kernel:
        matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    # Use IBM Plex only if it is actually installed. Naming a missing family
    # makes matplotlib emit one findfont warning per text object, which buries
    # real errors in a render log.
    have = {f.name for f in font_manager.fontManager.ttflist}
    family = [f for f in ("IBM Plex Sans", "DejaVu Sans") if f in have] or ["sans-serif"]

    plt.rcParams.update({
        "figure.figsize": (width, height),
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "figure.facecolor": CL.bg,
        "axes.facecolor": CL.bg,
        "savefig.facecolor": CL.bg,

        "font.family": family,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,

        "axes.edgecolor": CL.line,
        "axes.labelcolor": CL.ink,
        "axes.titlecolor": CL.ink,
        "text.color": CL.ink,
        "xtick.color": CL.muted,
        "ytick.color": CL.muted,

        # Only the left and bottom spines. Chart junk competes with the point.
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": CL.line,
        "grid.linewidth": 0.6,
        "grid.alpha": 0.8,

        "lines.linewidth": 2.0,
        "lines.markersize": 4,
        "legend.frameon": False,
        "figure.autolayout": True,
    })
    return plt


def annotate(ax, x, y, text, color=None, dx=0, dy=0):
    """A short label placed on the plot rather than in a legend.

    A legend makes the reader look away from the line and back again. On a slide
    that costs more than it saves, so label the line where it is.
    """
    ax.annotate(text, xy=(x, y), xytext=(x + dx, y + dy),
                color=color or CL.ink, fontsize=8.5, fontweight="600")
