"""Uidol config — all from environment, no hardcoded secrets."""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _req(key: str) -> str:
    v = os.getenv(key)
    if not v:
        raise RuntimeError(f"Missing env: {key}")
    return v


def _opt(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _ids(raw: str) -> list:
    out = []
    for p in raw.split(","):
        p = p.strip()
        if p.isdigit():
            out.append(int(p))
    return out


API_ID = int(_req("API_ID"))
API_HASH = _req("API_HASH")
BOT_TOKEN = _req("BOT_TOKEN")
OWNER_ID = int(_req("OWNER_ID"))
SUDO_USERS = _ids(_opt("SUDO_USERS"))
LOG_GROUP_ID = int(_opt("LOG_GROUP_ID", "0"))
MONGO_URL = _req("MONGO_URL")
MONGO_DB = _opt("MONGO_DB", "uidol_bot")
ENCRYPTION_KEY = _req("ENCRYPTION_KEY")
MAX_USERBOTS = int(_opt("MAX_USERBOTS", "20"))
LOG_LEVEL = _opt("LOG_LEVEL", "INFO").upper()
USERBOT_PREFIX = _opt("USERBOT_PREFIX", ".")
DEPLOY_TIMEOUT = int(_opt("DEPLOY_TIMEOUT", "300"))
FORCE_JOIN = [x.strip() for x in _opt("FORCE_JOIN").split(",") if x.strip()]

STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


def is_owner(uid: int) -> bool:
    return uid == OWNER_ID


def is_sudo(uid: int) -> bool:
    return uid == OWNER_ID or uid in SUDO_USERS
