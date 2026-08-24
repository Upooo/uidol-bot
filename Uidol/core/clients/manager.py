"""
Multi-client Manager.
Starts / stops userbots and registers modules on them.
"""

from typing import Dict, Optional, Callable, List
from Uidol.core.clients.userbot import Userbot
from Uidol.core.database import userbots as db_userbots
from Uidol.core.logger import log
from Uidol.config.settings import MAX_USERBOTS


class ClientManager:
    def __init__(self):
        self.userbots: Dict[int, Userbot] = {}
        self._module_register_hooks: List[Callable] = []

    def on_userbot_start(self, callback: Callable) -> None:
        self._module_register_hooks.append(callback)

    async def _run_hooks(self, ubot: Userbot) -> None:
        for hook in self._module_register_hooks:
            try:
                hook(ubot)
            except Exception as e:
                log.error(f"Module hook error on {ubot._uidol_name}: {e}")

    async def start_one(self, user_id: int) -> Optional[Userbot]:
        if user_id in self.userbots:
            return self.userbots[user_id]

        if len(self.userbots) >= MAX_USERBOTS:
            log.warning(f"MAX_USERBOTS ({MAX_USERBOTS}) reached")
            return None

        session = await db_userbots.get_plain_session(user_id)
        if not session:
            log.warning(f"No session for userbot {user_id}")
            return None

        try:
            ubot = Userbot(session_string=session, name=str(user_id))
            session = None
            me = await ubot.start()
            if me and me.id != user_id:
                await ubot.stop()
                log.error(f"Userbot ID mismatch: expected {user_id}, got {me.id}")
                return None

            self.userbots[user_id] = ubot
            await db_userbots.mark_started(user_id)
            await self._run_hooks(ubot)
            log.info(f"Userbot online: {user_id}")
            return ubot
        except Exception as e:
            log.error(f"Failed to start userbot {user_id}: {e}")
            await db_userbots.mark_error(user_id)
            return None

    async def start_all(self) -> None:
        records = await db_userbots.get_all_active_userbots()
        for record in records:
            if len(self.userbots) >= MAX_USERBOTS:
                log.warning(f"Reached MAX_USERBOTS limit ({MAX_USERBOTS})")
                break
            await self.start_one(record["user_id"])
        log.info(f"Started {len(self.userbots)} userbot(s)")

    async def stop_one(self, user_id: int) -> bool:
        ubot = self.userbots.pop(user_id, None)
        if not ubot:
            return False
        try:
            await ubot.stop()
        except Exception as e:
            log.error(f"Error stopping userbot {user_id}: {e}")
        return True

    async def restart_one(self, user_id: int) -> Optional[Userbot]:
        await self.stop_one(user_id)
        return await self.start_one(user_id)

    async def stop_all(self) -> None:
        for user_id in list(self.userbots.keys()):
            await self.stop_one(user_id)
        log.info("All userbots stopped")

    def get(self, user_id: int) -> Optional[Userbot]:
        return self.userbots.get(user_id)

    @property
    def count(self) -> int:
        return len(self.userbots)

    def list_ids(self) -> List[int]:
        return list(self.userbots.keys())


manager = ClientManager()
