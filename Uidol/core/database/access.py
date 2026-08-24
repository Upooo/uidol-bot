"""Verified users who may deploy a userbot."""

from datetime import datetime
from typing import List
from Uidol.core.database.connection import db

COL = "access"


async def grant(user_id: int, by: int = 0) -> bool:
    await db.db[COL].update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "granted_by": by, "granted_at": datetime.utcnow()}},
        upsert=True,
    )
    return True


async def revoke(user_id: int) -> bool:
    r = await db.db[COL].delete_one({"user_id": user_id})
    return r.deleted_count > 0


async def has_access(user_id: int) -> bool:
    return await db.db[COL].find_one({"user_id": user_id}) is not None


async def list_access() -> List[int]:
    docs = await db.db[COL].find({}, {"user_id": 1}).to_list(1000)
    return [d["user_id"] for d in docs]
