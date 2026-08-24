"""Userbot sessions — always encrypted at rest."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from Uidol.core.database.connection import db
from Uidol.core.security.encryption import protect, reveal

COL = "userbots"


async def add_ubot(user_id: int, session_string: str, name: str = "") -> bool:
    enc = protect(session_string)
    doc = {
        "user_id": user_id,
        "session": enc,
        "name": name or str(user_id),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    await db.db[COL].update_one({"user_id": user_id}, {"$set": doc}, upsert=True)
    return True


async def get_ubot(user_id: int) -> Optional[Dict[str, Any]]:
    return await db.db[COL].find_one({"user_id": user_id})


async def get_session(user_id: int) -> Optional[str]:
    doc = await get_ubot(user_id)
    if not doc or not doc.get("session"):
        return None
    return reveal(doc["session"])


async def get_all_active() -> List[Dict[str, Any]]:
    return await db.db[COL].find({"is_active": True}).to_list(1000)


async def remove_ubot(user_id: int) -> bool:
    r = await db.db[COL].delete_one({"user_id": user_id})
    return r.deleted_count > 0


async def set_active(user_id: int, active: bool) -> bool:
    r = await db.db[COL].update_one(
        {"user_id": user_id},
        {"$set": {"is_active": active, "updated_at": datetime.utcnow()}},
    )
    return r.modified_count > 0


async def count_ubots(active_only: bool = False) -> int:
    q = {"is_active": True} if active_only else {}
    return await db.db[COL].count_documents(q)


async def list_ubots(limit: int = 50) -> List[Dict[str, Any]]:
    return await db.db[COL].find({}, {"session": 0}).sort("created_at", -1).limit(limit).to_list(limit)
