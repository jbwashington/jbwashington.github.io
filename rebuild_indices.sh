#!/bin/bash
# Rebuild the utils, free-game and archive index pages

set -e

echo "Rebuilding indices..."
echo ""

python3 build_utils_index.py
python3 build_freegame_index.py

# Archive needs the private .inventory/ (gitignored); skip quietly where it doesn't exist.
if [ -d .inventory ]; then
    uv run build_archive.py build
fi

echo ""
echo "✓ All indices rebuilt successfully!"
echo ""
echo "Remember to commit the updated index.html files:"
echo "  git add utils/index.html free-game/index.html _data/archive.json archive/"
echo "  git commit -m 'Update indices'"
