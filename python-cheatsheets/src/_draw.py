"""Small drawing helpers shared by the package cheatsheets.

Diagrams are SVG strings (crisp at any size); plots are matplotlib figures in the
course's own style, drawn on the course data.
"""


def grid(x, y, rows, cols, cell=13, fills=None, label=None, stroke="#555"):
    """A small table drawn as cells; fills maps (r, c) -> colour."""
    fills = fills or {}
    out = []
    for r in range(rows):
        for c in range(cols):
            f = fills.get((r, c), fills.get(("row", r), fills.get(("col", c), "#fff")))
            out.append(f'<rect x="{x + c * cell}" y="{y + r * cell}" width="{cell}" '
                       f'height="{cell}" fill="{f}" stroke="{stroke}" stroke-width="0.8"/>')
    if label:
        out.append(f'<text x="{x + cols * cell / 2}" y="{y + rows * cell + 10}" '
                   f'font-size="8" text-anchor="middle" fill="#333">{label}</text>')
    return "".join(out)


def arrow(x1, y1, x2, y2, color="#555", label=None):
    out = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2" '
           f'marker-end="url(#ah)"/>')
    if label:
        out += (f'<text x="{(x1 + x2) / 2}" y="{min(y1, y2) - 3}" font-size="7.5" '
                f'text-anchor="middle" fill="{color}">{label}</text>')
    return out


def svg(width, height, body):
    return (f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Helvetica, Arial, sans-serif">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker>'
            f'</defs>{body}</svg>')


def text(x, y, s, size=8, anchor="middle", color="#333", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
            f'font-weight="{weight}">{s}</text>')


def small(w=3.0, h=1.6):
    """A small matplotlib figure in the course's style."""
    from plotstyle import setup
    plt = setup()
    fig, ax = plt.subplots(figsize=(w, h))
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=7)
    return fig, ax
