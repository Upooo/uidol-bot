"""
Multi-client Manager.
Handles starting / stopping multiple userbots safely.
"""

from typing import Dict, Optional
from Uidol.core.clients.userbot import Userbot
from Uidol.core.database import userbots as db_userbots
from Uidol.core.logger import log
from Uidol.config.settings import MAX_USERBOTS


class ClientManager:
    def __init__(self):
        self.userbots: Dict[int, Userbot] = {}

    async def start_all(self) -> None:
        """Start all active userbots from database."""
        records = await db_userbots.get_all_active_userbots()
        count = 0

        for record in records:
            if count >= MAX_USERBOTS:
                log.warning(f"Reached MAX_USERBOTS limit ({MAX_USERBOTS})")
                break

            user_id = record["user_id"]
            session = await db_userbots.get_plain_session(user_id)
            if not session:
                log.warning(f"Skipping userbot {user_id} – cannot decrypt session")
                continue

            try:
                ubot = Userbot(session_string=session, name=str(user_id))
                await ubot.start()
                self.userbots[user_id] = ubot
                count += 1
            except Exception as e:
                log.error(f"Failed to start userbot {user_id}: {e}")
                # Optionally deactivate broken session
                await db_userbots.set_active(user_id, False)

        log.info(f"Started {len(self.userbots)} userbot(s)")

    async def stop_all(self) -> None:
        for user_id, ubot in list(self.userbots.items()):
            try:
                await ubot.stop()
            except Exception as e:
                log.error(f"Error stopping userbot {user_id}: {e}")
        self.userbots.clear()
        log.info("All userbots stopped")

    def get(self, user_id: int) -> Optional[Userbot]:
        return self.userbots.get(user_id)

    @property
    def count(self) -> int:
        return len(self.userbots)


# Global instance
manager = ClientManager()
