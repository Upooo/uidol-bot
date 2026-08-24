"""join / leave / invite / staff."""

from pyrogram.types import Message
from pyrogram.errors import (
    UserAlreadyParticipant,
    InviteHashExpired,
    InviteHashInvalid,
    RPCError,
)

from Uidol.core.helpers.decorators import PY

try:
    from pyrogram.enums import ChatMembersFilter

    _ADMIN_FILTER = ChatMembersFilter.ADMINISTRATORS
except Exception:
    _ADMIN_FILTER = "administrators"


@PY.UBOT("join")
async def cmd_join(client, message: Message):
    args = message.command[1:] if message.command else []
    if not args:
        await message.edit_text(
            "<blockquote><b>Join</b></blockquote>\n\n"
            "<code>.join @username</code> atau link invite."
        )
        return
    link = args[0]
    try:
        if link.startswith("https://") or link.startswith("t.me/"):
            await client.join_chat(link)
        else:
            await client.join_chat(link.lstrip("@"))
        await message.edit_text(f"<blockquote><b>Joined</b></blockquote>\n\n<code>{link}</code>")
    except UserAlreadyParticipant:
        await message.edit_text("<blockquote>Sudah di dalam chat itu.</blockquote>")
    except (InviteHashExpired, InviteHashInvalid):
        await message.edit_text("<blockquote><b>Link invalid / expired</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal join</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("leave")
async def cmd_leave(client, message: Message):
    args = message.command[1:] if message.command else []
    chat_id = message.chat.id
    if args:
        target = args[0]
        try:
            if target.isdigit() or (target.startswith("-") and target[1:].isdigit()):
                chat_id = int(target)
            else:
                chat = await client.get_chat(target.lstrip("@"))
                chat_id = chat.id
        except Exception:
            await message.edit_text("<blockquote>Chat tidak ditemukan.</blockquote>")
            return

    try:
        await message.edit_text("<blockquote><b>Leaving…</b></blockquote>")
        await client.leave_chat(chat_id)
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal leave</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("invite")
async def cmd_invite(client, message: Message):
    try:
        link = await client.export_chat_invite_link(message.chat.id)
        await message.edit_text(
            f"<blockquote><b>Invite link</b></blockquote>\n\n<code>{link}</code>"
        )
    except RPCError as e:
        await message.edit_text(
            f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>"
        )


@PY.UBOT("staff|admins")
async def cmd_staff(client, message: Message):
    try:
        admins = []
        async for m in client.get_chat_members(message.chat.id, filter=_ADMIN_FILTER):
            u = m.user
            if not u:
                continue
            status = str(getattr(m, "status", "") or "").upper()
            tag = "👑" if "OWNER" in status else "🛡"
            un = f"@{u.username}" if u.username else (u.first_name or str(u.id))
            admins.append(f"{tag} {un} — <code>{u.id}</code>")
        if not admins:
            text = "<blockquote><b>Staff</b></blockquote>\n\nTidak ada."
        else:
            text = "<blockquote><b>Staff</b></blockquote>\n\n" + "\n".join(admins[:50])
        await message.edit_text(text)
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")
    except Exception as e:
        await message.edit_text(
            f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{type(e).__name__}</code>"
        )
