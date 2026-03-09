#!/bin/bash
# Rebuild both utils and free-game index pages

set -e

echo "Rebuilding indices..."
echo ""

python3 build_utils_index.py
python3 build_freegame_index.py

echo ""
echo "✓ All indices rebuilt successfully!"
echo ""
echo "Remember to commit the updated index.html files:"
echo "  git add utils/index.html free-game/index.html"
echo "  git commit -m 'Update indices'"
