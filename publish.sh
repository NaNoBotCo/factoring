#!/bin/bash
# Build the site into docs/, checked. GitHub Pages serves docs/ from main.
#
#   ./publish.sh            # facts, figures, pages, into docs/
#   ./publish.sh --draw     # also redraw the raster pictures (build/img/*.jpg)
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONUTF8=1
SITE_URL="${SITE_URL:-https://nanobotco.github.io/factoring}"

STYLE="$HOME/.claude/bin/stylecheck.py"
if [ -f "$STYLE" ]; then
  python3 "$STYLE" tools js data README.md NOTICE.txt || { echo "REFUSED: style. See ~/.claude/STYLE.md"; exit 4; }
fi

python3 tools/compute.py || { echo "REFUSED: a computed check failed"; exit 5; }
if [ "${1:-}" = "--draw" ] || [ ! -f build/img/hero.jpg ]; then python3 tools/draw.py; fi
python3 tools/figures.py
SITE_URL="$SITE_URL" python3 tools/site.py
python3 tools/links.py --quiet || { echo "REFUSED: broken internal links"; exit 3; }
python3 tests/test_site.py

# nothing that names this machine may be published
if grep -rl "/Users/" build/site >/dev/null 2>&1; then
  echo "REFUSED: host paths found in build/site"; exit 2
fi

rm -rf docs
cp -R build/site docs
touch docs/.nojekyll
echo "docs/ ← $(find docs -name 'index.html' | wc -l | tr -d ' ') pages, $(du -sh docs | cut -f1)"
