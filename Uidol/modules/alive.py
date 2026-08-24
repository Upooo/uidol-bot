"""Userbot alive / uptime."""

import time
from pyrogram.types import Message

from Uidol import __version__, ubot
from Uidol.config import USERBOT_PREFIX
from Uidol.core.helpers.decorators import PY
from Uidol.core.helpers.tools import format_uptime

_BOOT = time.time()


@PY.UBOT("alive|on")
async def cmd_alive(client, message: Message):
    me = client.me
    up = format_uptime(time.time() - _BOOT)
    text = (
        f"<blockquote><b>Uidol Alive</b></blockquote>\n\n"
        f"<b>User</b>: {me.first_name}\n"
        f"<b>ID</b>: <code>{me.id}</code>\n"
        f"<b>Version</b>: <code>{__version__}</code>\n"
        f"<b>Prefix</b>: <code>{USERBOT_PREFIX}</code>\n"
        f"<b>Uptime</b>: <code>{up}</code>\n"
        f"<b>Clients</b>: <code>{len(ubot._ubot)}</code>"
    )
    await message.edit_text(text)
