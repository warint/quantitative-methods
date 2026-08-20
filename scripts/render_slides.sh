#!/usr/bin/env bash
#
# Render every deck to revealjs (.html) and PowerPoint (.pptx).
#
#     scripts/render_slides.sh              # all decks
#     scripts/render_slides.sh 05           # just the sessions matching 05
#
# Only files named slides*.qmd are treated as decks. Other .qmd files in the
# repository — the practice report template, for instance — are documents, not
# presentations, and are deliberately skipped.
#
# Requires Quarto: https://quarto.org/docs/download/  (`quarto --version`)
#
# The .html is the real presentation — the theme, the two-column layouts and
# the callouts only exist there. The .pptx is the fallback, because GitHub
# will not render an HTML file when you click it in the browser.

set -euo pipefail
cd "$(dirname "$0")/.."

# Decks execute Python to build their figures, so Quarto needs an interpreter
# that has pandas, scikit-learn, statsmodels and matplotlib. Prefer the
# project's own .venv; fall back to whatever QUARTO_PYTHON already names.
if [ -z "${QUARTO_PYTHON:-}" ] && [ -x ".venv/bin/python" ]; then
    export QUARTO_PYTHON="$PWD/.venv/bin/python"
fi
if [ -n "${QUARTO_PYTHON:-}" ]; then
    echo "Executing deck code with: $QUARTO_PYTHON"
    if ! "$QUARTO_PYTHON" -c "import pandas, sklearn, statsmodels, matplotlib" 2>/dev/null; then
        echo "  WARNING: that interpreter is missing packages the figures need." >&2
        echo "           Activate .venv and: pip install -r requirements.txt" >&2
    fi
else
    echo "No .venv found — Quarto will use its default Python."
    echo "If figures come out missing, create .venv per the Session 01 setup guide."
fi

if ! command -v quarto >/dev/null 2>&1; then
    echo "quarto not found — install from https://quarto.org/docs/download/" >&2
    exit 1
fi

filter="${1:-}"
found=0
failed=0

while IFS= read -r deck; do
    if [ -n "$filter" ] && [[ "$deck" != *"$filter"* ]]; then
        continue
    fi
    found=$((found + 1))
    printf '\n=== %s\n' "$deck"
    if ( cd "$(dirname "$deck")" && quarto render "$(basename "$deck")" ); then
        :
    else
        echo "  FAILED: $deck" >&2
        failed=$((failed + 1))
    fi
done < <(find . -name 'slides*.qmd' -not -path './.git/*' | sort)

printf '\n%d deck(s) rendered, %d failed.\n' "$found" "$failed"

# Slides that overflow their frame are not a render error, so check separately.
if [ -f scripts/check_slides.py ]; then
    printf '\nChecking slide density:\n'
    python3 scripts/check_slides.py || true
fi

exit $(( failed > 0 ))
