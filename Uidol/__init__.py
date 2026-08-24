"""
Uidol — Secure Multi-Client Userbot Framework
v1.0.0-Beta
"""

import logging
import re
import sys

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from Uidol.config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    LOG_LEVEL,
    USERBOT_PREFIX,
)

__version__ = "1.0.0-Beta"

_log = logging.getLogger("Uidol")
_log.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
if not _log.handlers:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)-7s | %(message)s", "%H:%M:%S"))
    _log.addHandler(h)

for noisy in ("pyrogram", "pyrogram.session", "pyrogram.connection", "motor", "asyncio"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

log = _log


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

    def on_message(self, filters=None, group: int = 0):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def on_callback_query(self, filters=None, group: int = 0):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func
        return decorator

    async def start(self):
        await super().start()
        me = await self.get_me()
        log.info(f"Bot @{me.username} ({me.id})")


class Ubot(Client):
    _ubot: list = []
    _prefix: dict = {}
    _ids: list = []

    def __init__(self, session_string: str = None, name: str = "ubot", **kwargs):
        super().__init__(
            name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            in_memory=True,
            workers=4,
            **kwargs,
        )

    def on_message(self, filters=None, group: int = 0):
        def decorator(func):
            for u in list(self._ubot):
                u.add_handler(MessageHandler(func, filters), group)
            if not hasattr(Ubot, "_pending_handlers"):
                Ubot._pending_handlers = []
            Ubot._pending_handlers.append((func, filters, group))
            return func
        return decorator

    def cmd_prefix(self, cmd: str):
        command_re = re.compile(r"""(['\"])(.*?)\1|(\S+)""")

        async def func(_, client, message):
            if not message.text:
                return False
            text = message.text.strip()
            prefixes = self._prefix.get(client.me.id, [USERBOT_PREFIX])
            username = client.me.username or ""
            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue
                body = text[len(prefix):]
                for command in cmd.split("|"):
                    if not re.match(
                        rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                        body,
                        flags=re.IGNORECASE | re.UNICODE,
                    ):
                        continue
                    rest = re.sub(
                        rf"{command}(?:@?{username})?\s?",
                        "",
                        body,
                        count=1,
                        flags=re.IGNORECASE | re.UNICODE,
                    )
                    message.command = [command] + [
                        re.sub(r"""\\(['\"])""", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(rest)
                    ]
                    return True
            return False

        return filters.create(func)

    async def start(self):
        await super().start()
        me = await self.get_me()
        self._prefix[me.id] = [USERBOT_PREFIX]
        if self not in self._ubot:
            self._ubot.append(self)
        if me.id not in self._ids:
            self._ids.append(me.id)
        for func, filt, group in getattr(Ubot, "_pending_handlers", []):
            try:
                self.add_handler(MessageHandler(func, filt), group)
            except Exception:
                pass
        log.info(f"Userbot {me.first_name} ({me.id})")
        return me

    async def stop(self):
        try:
            me_id = self.me.id if self.me else None
        except Exception:
            me_id = None
        await super().stop()
        if self in self._ubot:
            self._ubot.remove(self)
        if me_id and me_id in self._ids:
            self._ids.remove(me_id)


bot = Bot()
ubot = Ubot(name="UidolUbot")
