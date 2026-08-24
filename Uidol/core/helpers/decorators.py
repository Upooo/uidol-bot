"""Command / callback decorators — Goo style, cleaner."""

from pyrogram import filters
from pyrogram.types import Message
from Uidol.config import is_owner, is_sudo


class PY:
    @staticmethod
    def BOT(commands, prefixes: str | list = "/"):
        def decorator(func):
            from Uidol import bot

            @bot.on_message(filters.command(commands, prefixes=prefixes) & filters.private)
            async def wrapper(client, message: Message):
                await func(client, message)

            return wrapper

        return decorator

    @staticmethod
    def CALLBACK(data: str):
        def decorator(func):
            from Uidol import bot

            @bot.on_callback_query(filters.regex(f"^{data}"))
            async def wrapper(client, callback):
                await func(client, callback)

            return wrapper

        return decorator

    @staticmethod
    def OWNER(func):
        async def wrapper(client, update):
            user = getattr(update, "from_user", None)
            if not user or not is_owner(user.id):
                if hasattr(update, "answer"):
                    await update.answer("Owner only.", show_alert=True)
                elif hasattr(update, "reply_text"):
                    await update.reply_text("<blockquote><b>Owner only.</b></blockquote>")
                return
            return await func(client, update)

        return wrapper

    @staticmethod
    def SUDO(func):
        async def wrapper(client, update):
            user = getattr(update, "from_user", None)
            if not user or not is_sudo(user.id):
                if hasattr(update, "answer"):
                    await update.answer("Sudo only.", show_alert=True)
                elif hasattr(update, "reply_text"):
                    await update.reply_text("<blockquote><b>Sudo only.</b></blockquote>")
                return
            return await func(client, update)

        return wrapper

    @staticmethod
    def UBOT(command: str):
        def decorator(func):
            from Uidol import ubot

            filt = ubot.cmd_prefix(command)

            @ubot.on_message(filt)
            async def wrapper(client, message: Message):
                if not message.from_user:
                    return
                if message.from_user.id != client.me.id:
                    return
                await func(client, message)

            return wrapper

        return decorator
