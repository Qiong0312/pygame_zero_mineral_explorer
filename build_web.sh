#!/usr/bin/env bash
# Rebuild the pygbag web package into web_game/build/web
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip 'pygbag==0.9.2'
fi
.venv/bin/python -m pygbag --build \
  --app_name mineral_explorer \
  --title "Mineral Explorer" \
  web_game
# CDN is missing pythonrc.py (only cpythonrc.py); serve a local copy
mkdir -p web_game/build/web/archives/0.9
cp .venv/lib/python3.9/site-packages/pygbag/support/cpythonrc.py \
  web_game/build/web/archives/0.9/pythonrc.py
# Background music is played via HTML5 Audio (HTTP), not mixer — copy next to index.html
mkdir -p web_game/build/web/music
cp -f web_game/music/*.ogg web_game/build/web/music/
echo "Web build ready at: web_game/build/web"
