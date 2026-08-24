#!/usr/bin/env bash
set -e
if [ ! -f ".env" ]; then
  echo "[ERROR] .env not found. Copy .env.example to .env first."
  exit 1
fi
echo "[Uidol] Starting..."
python3 -m Uidol
