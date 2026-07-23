#!/usr/bin/env bash
# Rebuild the pygbag web package into web_game/build/web
set -euo pipefail
cd "$(dirname "$0")"

PYTHON_BIN="$(command -v python3 || command -v python)"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "ERROR: python3/python not found" >&2
  exit 1
fi

echo "Using ${PYTHON_BIN} ($("${PYTHON_BIN}" -V 2>&1))"

if [[ ! -x .venv/bin/python ]]; then
  "${PYTHON_BIN}" -m venv .venv
fi

.venv/bin/pip install --upgrade pip 'pygbag==0.9.2'

.venv/bin/python -m pygbag --build \
  --app_name mineral_explorer \
  --title "Mineral Explorer" \
  --ume_block 0 \
  web_game

# CDN is missing pythonrc.py (only cpythonrc.py); serve a local copy.
# Resolve path dynamically — Vercel Python is not always 3.9.
PYTHONRC="$(
  .venv/bin/python - <<'PY'
import pathlib
import pygbag
print(pathlib.Path(pygbag.__file__).resolve().parent / "support" / "cpythonrc.py")
PY
)"
if [[ ! -f "${PYTHONRC}" ]]; then
  echo "ERROR: cpythonrc.py not found at ${PYTHONRC}" >&2
  exit 1
fi
mkdir -p web_game/build/web/archives/0.9
cp "${PYTHONRC}" web_game/build/web/archives/0.9/pythonrc.py

# Background music via HTML5 Audio (HTTP), not mixer — copy next to index.html
mkdir -p web_game/build/web/music
cp -f web_game/music/*.ogg web_game/build/web/music/

echo "Web build ready at: web_game/build/web"
ls -la web_game/build/web | head
