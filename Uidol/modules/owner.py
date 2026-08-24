"""Owner panel — inline + /grant /revoke commands."""

import asyncio
import os
import sys
import time
from pathlib import Path

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from Uidol import bot, ubot, log
from Uidol.config import is_owner, is_sudo, MAX_USERBOTS, OWNER_ID
from Uidol.core.database import users as db_users
from Uidol.core.database import userbots as db_ubot
from Uidol.core.database import access as db_access
from Uidol.core.helpers import BTN, MSG
from Uidol.core.helpers.logger import log_event
from Uidol.core.helpers.tools import format_uptime, mention

_START = time.time()
_ROOT = Path(__file__).resolve().parent.parent.parent
_pending_grant = {}


async def _do_grant(message: Message, target: int):
    await db_access.grant(target, by=message.from_user.id)
    await message.reply_text(MSG.access_granted(target), reply_markup=BTN.owner_panel())
    try:
        await bot.send_message(
            target,
            "<blockquote><b>Akses deploy diberikan</b></blockquote>\n\n"
            "Kamu sekarang bisa pasang userbot. Ketik /start.",
        )
    except Exception:
        pass
    await log_event(
        bot,
        f"<blockquote><b>Grant akses</b></blockquote>\n"
        f"by {mention(message.from_user)}\n"
        f"→ <code>{target}</code>",
    )


async def _do_revoke(message: Message, target: int):
    await db_access.revoke(target)
    await message.reply_text(MSG.access_revoked(target), reply_markup=BTN.owner_panel())
    await log_event(
        bot,
        f"<blockquote><b>Revoke akses</b></blockquote>\n"
        f"by {mention(message.from_user)}\n"
        f"→ <code>{target}</code>",
    )


# ─── Commands: /grant <id>  /revoke <id> ─────────────────────────────────────

@bot.on_message(filters.command("grant") & filters.private & filters.user(OWNER_ID))
async def cmd_grant(_, message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.reply_text(
            "<blockquote><b>Grant akses</b></blockquote>\n\n"
            "Pakai: <code>/grant user_id</code>\n"
            "Contoh: <code>/grant 123456789</code>"
        )
        return
    target = int(parts[1].strip())
    await _do_grant(message, target)


@bot.on_message(filters.command("revoke") & filters.private & filters.user(OWNER_ID))
async def cmd_revoke(_, message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.reply_text(
            "<blockquote><b>Revoke akses</b></blockquote>\n\n"
            "Pakai: <code>/revoke user_id</code>\n"
            "Contoh: <code>/revoke 123456789</code>"
        )
        return
    target = int(parts[1].strip())
    await _do_revoke(message, target)


# ─── Inline callbacks ─────────────────────────────────────────────────────────

@bot.on_callback_query(filters.regex(r"^menu:owner$"))
async def cb_owner_menu(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    await callback.message.edit_text(MSG.help_owner(), reply_markup=BTN.owner_panel())
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:status$"))
async def cb_sys_status(_, callback: CallbackQuery):
    if not is_sudo(callback.from_user.id):
        await callback.answer("Sudo only.", show_alert=True)
        return
    text = MSG.system_status(
        format_uptime(time.time() - _START),
        await db_users.count_users(),
        await db_ubot.count_ubots(),
        len(ubot._ubot),
        MAX_USERBOTS,
    )
    await callback.message.edit_text(text, reply_markup=BTN.owner_panel())
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:users$"))
async def cb_users(_, callback: CallbackQuery):
    if not is_sudo(callback.from_user.id):
        await callback.answer("Sudo only.", show_alert=True)
        return
    rows = await db_users.list_users(30)
    if not rows:
        text = "<blockquote><b>Users</b></blockquote>\n\nBelum ada."
    else:
        lines = []
        for u in rows:
            un = f"@{u['username']}" if u.get("username") else "-"
            lines.append(f"• <code>{u['user_id']}</code> | {u.get('first_name','')} | {un}")
        text = "<blockquote><b>Users</b></blockquote>\n\n" + "\n".join(lines)
    await callback.message.edit_text(text, reply_markup=BTN.owner_panel())
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:ubots$"))
async def cb_ubots(_, callback: CallbackQuery):
    if not is_sudo(callback.from_user.id):
        await callback.answer("Sudo only.", show_alert=True)
        return
    rows = await db_ubot.list_ubots(30)
    if not rows:
        text = "<blockquote><b>Userbots</b></blockquote>\n\nBelum ada."
    else:
        lines = []
        for u in rows:
            online = "🟢" if u["user_id"] in ubot._ids else "🔴"
            lines.append(
                f"{online} <code>{u['user_id']}</code> | {u.get('name','')} | "
                f"{'on' if u.get('is_active') else 'off'}"
            )
        text = "<blockquote><b>Userbots</b></blockquote>\n\n" + "\n".join(lines)
    await callback.message.edit_text(text, reply_markup=BTN.owner_panel())
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:grant$"))
async def cb_grant(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    _pending_grant[callback.from_user.id] = "grant"
    await callback.message.edit_text(
        "<blockquote><b>Grant akses</b></blockquote>\n\n"
        "Kirim <b>user ID</b> yang mau dikasih akses deploy.\n"
        "Atau pakai command: <code>/grant user_id</code>\n\n"
        "/cancel untuk batalkan.",
        reply_markup=BTN.back_home(),
    )
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:revoke$"))
async def cb_revoke(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    _pending_grant[callback.from_user.id] = "revoke"
    await callback.message.edit_text(
        "<blockquote><b>Revoke akses</b></blockquote>\n\n"
        "Kirim <b>user ID</b> yang mau dicabut aksesnya.\n"
        "Atau pakai command: <code>/revoke user_id</code>\n\n"
        "/cancel untuk batalkan.",
        reply_markup=BTN.back_home(),
    )
    await callback.answer()


@bot.on_message(
    filters.private
    & filters.text
    & filters.user(OWNER_ID)
    & ~filters.command(["start", "help", "ping", "cancel", "grant", "revoke"]),
    group=1,
)
async def owner_text_input(_, message: Message):
    action = _pending_grant.get(message.from_user.id)
    if not action:
        return
    text = message.text.strip()
    if not text.isdigit():
        await message.reply_text("<blockquote>Kirim angka user ID saja.</blockquote>")
        return
    target = int(text)
    _pending_grant.pop(message.from_user.id, None)

    if action == "grant":
        await _do_grant(message, target)
    else:
        await _do_revoke(message, target)


@bot.on_message(filters.command("cancel") & filters.private & filters.user(OWNER_ID))
async def owner_cancel_pending(_, message: Message):
    if message.from_user.id in _pending_grant:
        _pending_grant.pop(message.from_user.id, None)
        await message.reply_text(
            "<blockquote><b>Dibatalkan</b></blockquote>\n\nGrant/revoke dibatalkan.",
            reply_markup=BTN.owner_panel(),
        )


@bot.on_callback_query(filters.regex(r"^owner:git_status$"))
async def cb_git_status(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    proc = await asyncio.create_subprocess_shell(
        "git status -sb && git log -1 --oneline",
        cwd=str(_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    body = (out or err).decode()[:3000] or "(empty)"
    await callback.message.edit_text(
        f"<blockquote><b>Git status</b></blockquote>\n\n<pre>{body}</pre>",
        reply_markup=BTN.owner_panel(),
    )
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:git_pull$"))
async def cb_git_pull(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    await callback.answer("Pulling…")
    proc = await asyncio.create_subprocess_shell(
        "git pull --ff-only",
        cwd=str(_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    body = (out or err).decode()[:3000] or "(empty)"
    await callback.message.edit_text(
        f"<blockquote><b>Git pull</b></blockquote>\n\n<pre>{body}</pre>",
        reply_markup=BTN.owner_panel(),
    )
    await log_event(bot, f"<blockquote><b>git pull</b></blockquote>\nby <code>{callback.from_user.id}</code>")


@bot.on_callback_query(filters.regex(r"^owner:restart$"))
async def cb_restart(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    await callback.message.edit_text(
        "<blockquote><b>Restart bot?</b></blockquote>",
        reply_markup=BTN.confirm("owner:restart_yes"),
    )
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^owner:restart_yes$"))
async def cb_restart_yes(_, callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer("Owner only.", show_alert=True)
        return
    await callback.answer()
    try:
        await callback.message.edit_text("<blockquote><b>Restarting…</b></blockquote>")
    except Exception:
        pass
    await log_event(bot, f"<blockquote><b>Restart</b></blockquote>\nby {mention(callback.from_user)}")

    # Jangan await stop() di dalam handler → deadlock Pyrogram.
    # Schedule di luar, biar handler selesai dulu.
    async def _do_restart():
        await asyncio.sleep(1.5)
        for u in list(ubot._ubot):
            try:
                await asyncio.wait_for(u.stop(), timeout=8)
            except Exception:
                pass
        try:
            await asyncio.wait_for(bot.stop(), timeout=8)
        except Exception:
            pass
        os.execv(sys.executable, [sys.executable, "-m", "Uidol"])

    asyncio.create_task(_do_restart())
