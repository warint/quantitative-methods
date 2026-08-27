#!/usr/bin/env bash
# Rebuild the course book: assemble book/ from the decks and the briefs, then
# render it into docs/book/ where GitHub Pages serves it.
# Usage: scripts/render_book.sh [--render-only]
#
# Nothing in book/ is authored — scripts/build_book.py regenerates every
# chapter from files that already exist, so edit the deck or the brief and run
# this. Pass --render-only to skip the assembly and just re-render what is
# already in book/.

set -euo pipefail
cd "$(dirname "$0")/.."

if [ -z "${QUARTO_PYTHON:-}" ] && [ -x ".venv/bin/python" ]; then
    export QUARTO_PYTHON="$PWD/.venv/bin/python"
fi
python_bin="${QUARTO_PYTHON:-python3}"

if ! command -v quarto >/dev/null 2>&1; then
    echo "quarto not found — install it from https://quarto.org/docs/download/" >&2
    exit 1
fi

# Session 05 is the one chapter that executes its cells; the other eighteen
# carry pre-baked output from the deck import. Quarto drives it through a
# Jupyter kernel, so the kernel packages have to be there too.
missing=$("$python_bin" - <<'PY'
import importlib.util
print(" ".join(m for m in ("numpy", "pandas", "sklearn", "matplotlib",
                           "pyarrow", "yaml", "nbclient", "ipykernel")
                 if not importlib.util.find_spec(m)))
PY
)
if [ -n "$missing" ]; then
    echo "missing python packages: $missing" >&2
    echo "  $python_bin -m pip install -r requirements.txt" >&2
    echo "(or point QUARTO_PYTHON at an interpreter that has them)" >&2
    exit 1
fi

if [ "${1:-}" != "--render-only" ]; then
    # The bibliography is fetched from Crossref, so only rebuild it when the
    # DOI list has actually changed. A render should not need the network.
    if [ ! -f assets/references.bib ] || [ references.dois -nt assets/references.bib ]; then
        echo "=== fetching bibliography from Crossref"
        "$python_bin" scripts/build_bibliography.py
    fi

    echo "=== assembling book/ from the decks and briefs"
    "$python_bin" scripts/build_book.py
fi

echo "=== rendering to docs/book/"
(cd book && quarto render)

echo "=== checking every referenced asset exists"
"$python_bin" scripts/check_book_assets.py

cat <<'DONE'

Book written to docs/book/.

  preview   open docs/book/index.html
  publish   git add docs/book && git commit && git push

docs/book/ is committed on purpose — Pages serves it from main. The .gitignore
exceptions that let it through are scoped to that directory; deck HTML
elsewhere stays ignored.
DONE
