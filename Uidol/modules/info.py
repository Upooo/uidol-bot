"""id / info / whois — user & chat info."""

from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatType

from Uidol.core.helpers.decorators import PY


def _user_line(u: User) -> str:
    name = u.first_name or ""
    if u.last_name:
        name = f"{name} {u.last_name}".strip()
    un = f"@{u.username}" if u.username else "-"
    dc = getattr(u, "dc_id", None) or "-"
    lines = [
        f"<b>Name</b>: {name}",
        f"<b>ID</b>: <code>{u.id}</code>",
        f"<b>Username</b>: {un}",
        f"<b>DC</b>: <code>{dc}</code>",
        f"<b>Bot</b>: <code>{'ya' if u.is_bot else 'tidak'}</code>",
        f"<b>Premium</b>: <code>{'ya' if getattr(u, 'is_premium', False) else 'tidak'}</code>",
    ]
    if u.status:
        lines.append(f"<b>Status</b>: <code>{u.status}</code>")
    return "\n".join(lines)


@PY.UBOT("id")
async def cmd_id(client, message: Message):
    if message.reply_to_message:
        r = message.reply_to_message
        if r.from_user:
            u = r.from_user
            text = (
                f"<blockquote><b>User ID</b></blockquote>\n\n"
                f"{_user_line(u)}"
            )
        elif r.sender_chat:
            c = r.sender_chat
            text = (
                f"<blockquote><b>Chat ID</b></blockquote>\n\n"
                f"<b>Title</b>: {c.title}\n"
                f"<b>ID</b>: <code>{c.id}</code>"
            )
        else:
            text = f"<blockquote><b>Chat</b></blockquote>\n\n<code>{message.chat.id}</code>"
    else:
        chat = message.chat
        text = (
            f"<blockquote><b>ID</b></blockquote>\n\n"
            f"<b>Chat</b>: <code>{chat.id}</code>\n"
            f"<b>Your ID</b>: <code>{message.from_user.id if message.from_user else client.me.id}</code>"
        )
        if chat.username:
            text += f"\n<b>Username</b>: @{chat.username}"
    await message.edit_text(text)


@PY.UBOT("info|whois")
async def cmd_info(client, message: Message):
    target = None
    args = message.command[1:] if message.command else []

    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
    elif args:
        q = args[0]
        try:
            if q.isdigit() or (q.startswith("-") and q[1:].isdigit()):
                target = await client.get_users(int(q))
            else:
                target = await client.get_users(q)
        except Exception:
            await message.edit_text(
                "<blockquote><b>Tidak ditemukan</b></blockquote>\n\nUser/chat tidak valid."
            )
            return
    else:
        target = message.from_user or client.me

    if isinstance(target, User):
        text = f"<blockquote><b>User Info</b></blockquote>\n\n{_user_line(target)}"
        try:
            common = await client.get_common_chats(target.id)
            text += f"\n<b>Common chats</b>: <code>{len(common)}</code>"
        except Exception:
            pass
    else:
        text = f"<blockquote><b>Info</b></blockquote>\n\n<code>{target}</code>"

    await message.edit_text(text)


@PY.UBOT("chatinfo")
async def cmd_chatinfo(client, message: Message):
    chat = message.chat
    try:
        full = await client.get_chat(chat.id)
    except Exception:
        full = chat

    ctype = full.type.value if hasattr(full.type, "value") else str(full.type)
    members = getattr(full, "members_count", None) or "-"
    desc = (getattr(full, "description", None) or "-")[:200]
    un = f"@{full.username}" if full.username else "-"

    text = (
        f"<blockquote><b>Chat Info</b></blockquote>\n\n"
        f"<b>Title</b>: {full.title or '-'}\n"
        f"<b>ID</b>: <code>{full.id}</code>\n"
        f"<b>Type</b>: <code>{ctype}</code>\n"
        f"<b>Username</b>: {un}\n"
        f"<b>Members</b>: <code>{members}</code>\n"
        f"<b>Desc</b>: {desc}"
    )
    await message.edit_text(text)
