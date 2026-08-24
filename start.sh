#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -f ".env" ]; then
  echo "[ERROR] .env not found. Copy .env.example → .env dulu."
  exit 1
fi
echo "[Uidol] Starting…"
exec python3 -m Uidol
