from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from Uidol.config import MONGO_URL, MONGO_DB


class Database:
    def __init__(self):
        self._client = None
        self._db = None

    async def connect(self):
        if self._client:
            return
        self._client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        await self._client.admin.command("ping")
        self._db = self._client[MONGO_DB]
        print(f"[DB] Connected → {MONGO_DB}")

    async def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    @property
    def db(self):
        if self._db is None:
            raise RuntimeError("DB not connected")
        return self._db


db = Database()
