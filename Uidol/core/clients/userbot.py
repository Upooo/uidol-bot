"""
Userbot client class.
"""

from pyrogram import Client
from Uidol.config.settings import API_ID, API_HASH
from Uidol.core.logger import log


class Userbot(Client):
    def __init__(self, session_string: str, name: str = "userbot"):
        super().__init__(
            name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            in_memory=True,
            workers=4,
        )
        self._uidol_name = name

    async def start(self):
        await super().start()
        me = await self.get_me()
        log.info(f"Userbot started: {me.first_name} ({me.id})")
        return me

    async def stop(self):
        await super().stop()
        log.info(f"Userbot stopped: {self._uidol_name}")
