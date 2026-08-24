"""
/start /help /ping for management bot.
"""

import time
from pyrogram import filters
from pyrogram.types import Message

from Uidol.core.clients.bot import Bot
from Uidol.core.handlers.messages import get_message
from Uidol.core.database import users as db_users
from Uidol.core.logger import log_event
from Uidol.utils.helpers import mention


def register(bot: Bot):
    @bot.on_message(filters.command("start") & filters.private)
    async def start_handler(_, message: Message):
        user = message.from_user
        await db_users.upsert_user(
            user_id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            username=user.username or "",
        )
        text = get_message("start", lang="id", mention=mention(user))
        await message.reply_text(text)
        await log_event(
            f"👤 /start\n{mention(user)}\nID: `{user.id}`"
            + (f"\n@{user.username}" if user.username else "")
        )

    @bot.on_message(filters.command("help") & filters.private)
    async def help_handler(_, message: Message):
        await message.reply_text(get_message("help", lang="id"))

    @bot.on_message(filters.command("ping") & filters.private)
    async def ping_handler(_, message: Message):
        start = time.time()
        msg = await message.reply_text("...")
        ms = round((time.time() - start) * 1000, 2)
        await msg.edit_text(get_message("ping", lang="id", ms=ms))
