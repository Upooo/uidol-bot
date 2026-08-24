"""
Developer / owner management commands.
"""

import asyncio
import os
import sys
import time
from pathlib import Path

from pyrogram import filters
from pyrogram.types import Message

from Uidol.core.clients.bot import Bot
from Uidol.core.clients.manager import manager
from Uidol.core.permissions import owner_only, sudo_only
from Uidol.core.database import users as db_users
from Uidol.core.database import userbots as db_userbots
from Uidol.core.logger import log, log_event
from Uidol.utils.helpers import format_uptime, mention
from Uidol.config.settings import OWNER_ID, MAX_USERBOTS, LOG_GROUP_ID

_START_TIME = time.time()
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def register(bot: Bot):
    @bot.on_message(filters.command("status") & filters.private)
    @sudo_only
    async def status_cmd(_, message: Message):
        uptime = format_uptime(time.time() - _START_TIME)
        total_users = await db_users.count_users()
        total_ubots = await db_userbots.count_userbots()
        active_ubots = manager.count

        text = (
            f"**Uidol Status**\n\n"
            f"⏱ Uptime: `{uptime}`\n"
            f"👥 Users: `{total_users}`\n"
            f"🤖 Userbots (DB): `{total_ubots}`\n"
            f"🟢 Online: `{active_ubots}` / `{MAX_USERBOTS}`\n"
            f"📢 Log group: `{'set' if LOG_GROUP_ID else 'not set'}`"
        )
        await message.reply_text(text)

    @bot.on_message(filters.command("users") & filters.private)
    @sudo_only
    async def users_cmd(_, message: Message):
        rows = await db_users.list_users(limit=30)
        if not rows:
            return await message.reply_text("Belum ada user.")
        lines = []
        for u in rows:
            uname = f"@{u['username']}" if u.get("username") else "-"
            lines.append(f"• `{u['user_id']}` | {u.get('first_name', '')} | {uname}")
        await message.reply_text("**Users (30 terbaru)**\n\n" + "\n".join(lines))

    @bot.on_message(filters.command("ubots") & filters.private)
    @sudo_only
    async def ubots_cmd(_, message: Message):
        rows = await db_userbots.list_userbots(limit=30)
        if not rows:
            return await message.reply_text("Belum ada userbot.")
        lines = []
        for u in rows:
            online = "🟢" if u["user_id"] in manager.userbots else "🔴"
            active = "on" if u.get("is_active") else "off"
            lines.append(
                f"{online} `{u['user_id']}` | {u.get('name', '')} | {active}"
            )
        await message.reply_text("**Userbots**\n\n" + "\n".join(lines))

    @bot.on_message(filters.command("git") & filters.private)
    @owner_only
    async def git_cmd(_, message: Message):
        args = message.text.split(maxsplit=1)
        action = args[1].strip().lower() if len(args) > 1 else "status"

        if action not in ("status", "pull"):
            return await message.reply_text("Pakai: `/git status` atau `/git pull`")

        if action == "status":
            proc = await asyncio.create_subprocess_shell(
                "git status -sb && git log -1 --oneline",
                cwd=str(_REPO_ROOT),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out, err = await proc.communicate()
            text = (out or err).decode()[:3500] or "(empty)"
            await message.reply_text(f"**git status**\n```\n{text}\n```")
            return

        msg = await message.reply_text("⏳ git pull...")
        proc = await asyncio.create_subprocess_shell(
            "git pull --ff-only",
            cwd=str(_REPO_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        text = (out or err).decode()[:3500] or "(empty)"
        await msg.edit_text(f"**git pull**\n```\n{text}\n```")
        await log_event(f"🔧 git pull by `{message.from_user.id}`\n```{text[:500]}```")

    @bot.on_message(filters.command("restart") & filters.private)
    @owner_only
    async def restart_cmd(_, message: Message):
        await message.reply_text("♻️ Restarting...")
        await log_event(f"♻️ Bot restart by {mention(message.from_user)}")
        await manager.stop_all()
        os.execv(sys.executable, [sys.executable, "-m", "Uidol"])

    @bot.on_message(filters.command("myubot") & filters.private)
    async def myubot_cmd(_, message: Message):
        user_id = message.from_user.id
        doc = await db_userbots.get_userbot(user_id)
        if not doc:
            return await message.reply_text("Kamu belum punya userbot. /deploy")
        online = user_id in manager.userbots
        text = (
            f"**Userbot kamu**\n\n"
            f"ID: `{user_id}`\n"
            f"Nama: {doc.get('name', '-')}\n"
            f"Active: `{doc.get('is_active')}`\n"
            f"Online: `{'yes' if online else 'no'}`"
        )
        await message.reply_text(text)

    @bot.on_message(filters.command("restartubot") & filters.private)
    async def restartubot_cmd(_, message: Message):
        user_id = message.from_user.id
        doc = await db_userbots.get_userbot(user_id)
        if not doc:
            return await message.reply_text("Kamu belum punya userbot. /deploy")
        msg = await message.reply_text("⏳ Restarting your userbot...")
        ubot = await manager.restart_one(user_id)
        if ubot:
            await msg.edit_text("✅ Userbot restarted.")
            await log_event(f"🔄 Ubot restart\nUser: {mention(message.from_user)}")
        else:
            await msg.edit_text("❌ Gagal restart. Hubungi owner.")
