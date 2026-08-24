"""
Management Bot client.
"""

from pyrogram import Client
from Uidol.config.settings import API_ID, API_HASH, BOT_TOKEN
from Uidol.core.logger import log


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="UidolBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True,
            workers=8,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        log.info(f"Bot started as @{me.username} ({me.id})")

    async def stop(self):
        await super().stop()
        log.info("Bot stopped")
