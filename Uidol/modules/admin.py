"""Admin tools — ban, mute, kick, promote, demote, pin."""

from pyrogram.types import Message, ChatPrivileges
from pyrogram.errors import UserAdminInvalid, ChatAdminRequired, RPCError

from Uidol.core.helpers.decorators import PY


def _target_user(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    args = message.command[1:] if message.command else []
    if args:
        return args[0]
    return None


async def _resolve(client, message: Message):
    t = _target_user(message)
    if t is None:
        await message.edit_text(
            "<blockquote><b>Target?</b></blockquote>\n\nReply user atau kasih username/id."
        )
        return None
    if not isinstance(t, str):
        return t
    try:
        if t.isdigit() or (t.startswith("-") and t[1:].isdigit()):
            return await client.get_users(int(t))
        return await client.get_users(t)
    except Exception:
        await message.edit_text("<blockquote><b>User tidak ditemukan</b></blockquote>")
        return None


@PY.UBOT("ban")
async def cmd_ban(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.edit_text(
            f"<blockquote><b>Banned</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("unban")
async def cmd_unban(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit_text(
            f"<blockquote><b>Unbanned</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("kick")
async def cmd_kick(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit_text(
            f"<blockquote><b>Kicked</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("mute")
async def cmd_mute(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user.id,
            permissions=client.__class__.RESOLVE_PEER  # placeholder avoided
            if False
            else __import__("pyrogram.types", fromlist=["ChatPermissions"]).ChatPermissions(),
        )
        await message.edit_text(
            f"<blockquote><b>Muted</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("unmute")
async def cmd_unmute(client, message: Message):
    from pyrogram.types import ChatPermissions

    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_change_info=True,
            ),
        )
        await message.edit_text(
            f"<blockquote><b>Unmuted</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("promote")
async def cmd_promote(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=False,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
            ),
        )
        await message.edit_text(
            f"<blockquote><b>Promoted</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("demote")
async def cmd_demote(client, message: Message):
    user = await _resolve(client, message)
    if not user:
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
            ),
        )
        await message.edit_text(
            f"<blockquote><b>Demoted</b></blockquote>\n\n"
            f"{user.mention}\n<code>{user.id}</code>"
        )
    except (UserAdminInvalid, ChatAdminRequired):
        await message.edit_text("<blockquote><b>Butuh admin</b></blockquote>")
    except RPCError as e:
        await message.edit_text(f"<blockquote><b>Gagal</b></blockquote>\n\n<code>{e.NAME}</code>")


@PY.UBOT("pin")
async def cmd_pin(client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("<blockquote>Reply pesan yang mau di-pin.</blockquote>")
        return
    try:
        await message.reply_to_message.pin(disable_notification=False)
        await message.edit_text("<blockquote><b>Pinned</b></blockquote>")
    except (ChatAdminRequired, RPCError) as e:
        await message.edit_text(
            f"<blockquote><b>Gagal pin</b></blockquote>\n\n<code>{getattr(e, 'NAME', type(e).__name__)}</code>"
        )


@PY.UBOT("unpin")
async def cmd_unpin(client, message: Message):
    try:
        if message.reply_to_message:
            await message.reply_to_message.unpin()
        else:
            await client.unpin_all_chat_messages(message.chat.id)
        await message.edit_text("<blockquote><b>Unpinned</b></blockquote>")
    except (ChatAdminRequired, RPCError) as e:
        await message.edit_text(
            f"<blockquote><b>Gagal unpin</b></blockquote>\n\n<code>{getattr(e, 'NAME', type(e).__name__)}</code>"
        )
