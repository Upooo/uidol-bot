"""
Users who interacted with the management bot.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from Uidol.core.database.connection import db

COLLECTION = "users"


async def upsert_user(
    user_id: int,
    first_name: str = "",
    last_name: str = "",
    username: str = "",
) -> None:
    now = datetime.utcnow()
    await db.db[COLLECTION].update_one(
        {"user_id": user_id},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name or "",
                "username": username or "",
                "last_seen": now,
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": now,
            },
            "$inc": {"start_count": 1},
        },
        upsert=True,
    )


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    return await db.db[COLLECTION].find_one({"user_id": user_id})


async def list_users(limit: int = 100) -> List[Dict[str, Any]]:
    cursor = db.db[COLLECTION].find().sort("last_seen", -1).limit(limit)
    return await cursor.to_list(length=limit)


async def count_users() -> int:
    return await db.db[COLLECTION].count_documents({})
