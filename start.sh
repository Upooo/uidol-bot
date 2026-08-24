#!/usr/bin/env bash
set -e

# Simple launcher for Uidol
# Usage: bash start.sh

if [ ! -f ".env" ]; then
    echo "[ERROR] .env file not found!"
    echo "Please copy .env.example to .env and fill the required values."
    exit 1
fi

echo "[Uidol] Starting..."
python3 -m Uidol
