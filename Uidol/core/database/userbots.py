"""
Userbot / Session database operations.
All session data is stored encrypted.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from Uidol.core.database.connection import db
from Uidol.core.security.session import protect_session, reveal_session
from Uidol.core.logger import log


COLLECTION = "userbots"


async def add_userbot(
    user_id: int,
    session_string: str,
    name: str = "",
    extra: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Add a new userbot.
    session_string will be encrypted before saving.
    """
    encrypted = protect_session(session_string)

    doc = {
        "user_id": user_id,
        "session": encrypted,
        "name": name or str(user_id),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "extra": extra or {},
    }

    try:
        await db.db[COLLECTION].update_one(
            {"user_id": user_id},
            {"$set": doc},
            upsert=True,
        )
        log.info(f"Userbot {user_id} saved (encrypted)")
        return True
    except Exception as e:
        log.error(f"Failed to save userbot {user_id}: {e}")
        return False


async def get_userbot(user_id: int) -> Optional[Dict[str, Any]]:
    """Get userbot data (session remains encrypted)."""
    return await db.db[COLLECTION].find_one({"user_id": user_id})


async def get_plain_session(user_id: int) -> Optional[str]:
    """
    Get decrypted session string.
    Use with extreme care – only in memory, never log it.
    """
    doc = await get_userbot(user_id)
    if not doc or not doc.get("session"):
        return None
    return reveal_session(doc["session"])


async def get_all_active_userbots() -> List[Dict[str, Any]]:
    """Return all active userbots (sessions still encrypted)."""
    cursor = db.db[COLLECTION].find({"is_active": True})
    return await cursor.to_list(length=1000)


async def remove_userbot(user_id: int) -> bool:
    result = await db.db[COLLECTION].delete_one({"user_id": user_id})
    if result.deleted_count:
        log.info(f"Userbot {user_id} removed")
        return True
    return False


async def set_active(user_id: int, active: bool) -> bool:
    result = await db.db[COLLECTION].update_one(
        {"user_id": user_id},
        {"$set": {"is_active": active, "updated_at": datetime.utcnow()}},
    )
    return result.modified_count > 0


async def count_userbots() -> int:
    return await db.db[COLLECTION].count_documents({})
