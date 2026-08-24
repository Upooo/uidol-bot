"""
Common helpers for Uidol.
"""

from datetime import datetime, timezone
from pyrogram.types import User


def mention(user: User) -> str:
    name = user.first_name or "User"
    return f'<a href="tg://user?id={user.id}">{name}</a>'


def format_uptime(seconds: float) -> str:
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def safe_username(user: User) -> str:
    return f"@{user.username}" if user.username else str(user.id)
