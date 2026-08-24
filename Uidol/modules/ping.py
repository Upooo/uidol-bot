"""
/ping command.
"""

import time
from pyrogram import filters
from pyrogram.types import Message
from Uidol.core.clients.bot import Bot
from Uidol.core.handlers.messages import get_message


def register(bot: Bot):
    @bot.on_message(filters.command("ping") & filters.private)
    async def ping_handler(_, message: Message):
        start = time.time()
        msg = await message.reply_text("...")
        ms = round((time.time() - start) * 1000, 2)
        text = get_message("ping", lang="id", ms=ms)
        await msg.edit_text(text)
