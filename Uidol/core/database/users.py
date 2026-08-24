from datetime import datetime
from typing import List, Dict, Any
from Uidol.core.database.connection import db

COL = "users"


async def upsert_user(user_id: int, first_name: str = "", last_name: str = "", username: str = ""):
    now = datetime.utcnow()
    await db.db[COL].update_one(
        {"user_id": user_id},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name or "",
                "username": username or "",
                "last_seen": now,
            },
            "$setOnInsert": {"user_id": user_id, "created_at": now},
            "$inc": {"start_count": 1},
        },
        upsert=True,
    )


async def list_users(limit: int = 50) -> List[Dict[str, Any]]:
    return await db.db[COL].find().sort("last_seen", -1).limit(limit).to_list(limit)


async def count_users() -> int:
    return await db.db[COL].count_documents({})
