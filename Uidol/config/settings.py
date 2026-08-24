"""
Uidol Configuration
All settings are loaded from environment variables.
No hardcoded secrets allowed.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default)


# ======================
# Telegram
# ======================
API_ID: int = int(_require("API_ID"))
API_HASH: str = _require("API_HASH")
BOT_TOKEN: str = _require("BOT_TOKEN")
OWNER_ID: int = int(_require("OWNER_ID"))

# ======================
# MongoDB
# ======================
MONGO_URL: str = _require("MONGO_URL")
MONGO_DB: str = _optional("MONGO_DB", "uidol_bot")

# ======================
# Security
# ======================
ENCRYPTION_KEY: str = _require("ENCRYPTION_KEY")

# ======================
# Limits & Behavior
# ======================
MAX_USERBOTS: int = int(_optional("MAX_USERBOTS", "20"))
LOG_LEVEL: str = _optional("LOG_LEVEL", "INFO").upper()

# ======================
# Paths
# ======================
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)
