"""
Uidol Configuration
All settings loaded from environment. No hardcoded secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _parse_int_list(raw: str) -> list:
    if not raw.strip():
        return []
    result = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            result.append(int(part))
    return result


API_ID = int(_require("API_ID"))
API_HASH = _require("API_HASH")
BOT_TOKEN = _require("BOT_TOKEN")
OWNER_ID = int(_require("OWNER_ID"))
SUDO_USERS = _parse_int_list(_optional("SUDO_USERS", ""))
LOG_GROUP_ID = int(_optional("LOG_GROUP_ID", "0"))
MONGO_URL = _require("MONGO_URL")
MONGO_DB = _optional("MONGO_DB", "uidol_bot")
ENCRYPTION_KEY = _require("ENCRYPTION_KEY")
MAX_USERBOTS = int(_optional("MAX_USERBOTS", "20"))
LOG_LEVEL = _optional("LOG_LEVEL", "INFO").upper()
USERBOT_PREFIX = _optional("USERBOT_PREFIX", ".")
DEPLOY_TIMEOUT = int(_optional("DEPLOY_TIMEOUT", "300"))
FORCE_JOIN = [x.strip() for x in _optional("FORCE_JOIN", "").split(",") if x.strip()]
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


def is_sudo(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS
