"""
MongoDB connection manager for Uidol.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from Uidol.config.settings import MONGO_URL, MONGO_DB
from Uidol.core.logger import log


class Database:
    def __init__(self):
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        if self._client is not None:
            return

        try:
            self._client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            # Force connection check
            await self._client.admin.command("ping")
            self._db = self._client[MONGO_DB]
            log.info(f"Connected to MongoDB → {MONGO_DB}")
        except Exception as e:
            log.critical(f"Failed to connect to MongoDB: {e}")
            raise

    async def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            log.info("MongoDB connection closed")

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db


# Global instance
db = Database()
