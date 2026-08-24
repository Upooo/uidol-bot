"""
/start and /help commands for the management bot.
"""

from pyrogram import filters
from pyrogram.types import Message
from Uidol.core.clients.bot import Bot
from Uidol.core.handlers.messages import get_message
from Uidol.config.settings import OWNER_ID


# We need a way to register handlers on the bot instance.
# For v0.0.1 we use a simple approach that works with auto-loader.

def register(bot: Bot):
    @bot.on_message(filters.command("start") & filters.private)
    async def start_handler(_, message: Message):
        lang = "id"  # later can detect from user
        text = get_message(
            "start",
            lang=lang,
            mention=message.from_user.mention,
        )
        await message.reply_text(text)

    @bot.on_message(filters.command("help") & filters.private)
    async def help_handler(_, message: Message):
        lang = "id"
        text = get_message("help", lang=lang)
        await message.reply_text(text)
