"""
.ping for userbot clients.
"""

import time
from pyrogram import filters
from pyrogram.types import Message
from Uidol.config.settings import USERBOT_PREFIX


def register(bot):
    pass


def register_userbot(client):
    prefix = USERBOT_PREFIX

    @client.on_message(filters.me & filters.command("ping", prefixes=prefix))
    async def ubot_ping(_, message: Message):
        start = time.time()
        msg = await message.edit_text("...")
        ms = round((time.time() - start) * 1000, 2)
        await msg.edit_text(f"Pong! ⚡ `{ms}ms`")
