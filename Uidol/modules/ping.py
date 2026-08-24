"""Bot /ping and userbot .ping"""

import time
from pyrogram import filters
from pyrogram.types import Message

from Uidol import bot, ubot


@bot.on_message(filters.command("ping") & filters.private)
async def bot_ping(_, message: Message):
    t0 = time.time()
    m = await message.reply_text("<blockquote>…</blockquote>")
    ms = round((time.time() - t0) * 1000, 2)
    await m.edit_text(f"<blockquote><b>Pong</b> ⚡ <code>{ms}ms</code></blockquote>")


@ubot.on_message(ubot.cmd_prefix("ping"))
async def ubot_ping(client, message: Message):
    if not message.from_user or message.from_user.id != client.me.id:
        return
    t0 = time.time()
    m = await message.edit_text("<blockquote>…</blockquote>")
    ms = round((time.time() - t0) * 1000, 2)
    await m.edit_text(f"<blockquote><b>Pong</b> ⚡ <code>{ms}ms</code></blockquote>")
