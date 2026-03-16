#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "[JARVIS] Starting with Docker Compose..."
  docker compose up -d --build
  echo "[JARVIS] Ready at http://localhost:8787"
  exit 0
fi

echo "[JARVIS] Docker not found. Falling back to Python local install..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
uvicorn server:app --app-dir app --host 0.0.0.0 --port 8787
