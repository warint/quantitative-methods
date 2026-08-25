#!/usr/bin/env bash
# Render the transferred MATH60033A lecture decks to self-contained RevealJS.
# Usage: scripts/render_session_lectures.sh [two-digit session filter]

set -euo pipefail
cd "$(dirname "$0")/.."

if [ -z "${QUARTO_PYTHON:-}" ] && [ -x ".venv/bin/python" ]; then
    export QUARTO_PYTHON="$PWD/.venv/bin/python"
fi

if ! command -v quarto >/dev/null 2>&1; then
    echo "quarto not found — install it from https://quarto.org/docs/download/" >&2
    exit 1
fi

filter="${1:-}"
found=0
failed=0

while IFS= read -r deck; do
    if [ -n "$filter" ] && [[ "$deck" != *"-S${filter}-"* ]]; then
        continue
    fi

    found=$((found + 1))
    printf '\n=== %s\n' "$deck"
    if (cd "$(dirname "$deck")" && quarto render "$(basename "$deck")" --to revealjs); then
        :
    else
        failed=$((failed + 1))
        echo "  FAILED: $deck" >&2
    fi
done < <(find . -path './[0-9][0-9]-*/01-lecture/MATH60033A-S*-Lecture.qmd' -print | sort)

printf '\n%d lecture deck(s) rendered, %d failed.\n' "$found" "$failed"
if [ "$found" -eq 0 ]; then
    echo "No matching lecture decks found." >&2
    exit 1
fi

exit $((failed > 0))
