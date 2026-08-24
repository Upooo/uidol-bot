"""Userbot help — list commands by category."""

from pyrogram.types import Message

from Uidol import __version__
from Uidol.config import USERBOT_PREFIX
from Uidol.core.helpers.decorators import PY

p = USERBOT_PREFIX

HELP_TEXT = f"""<blockquote><b>Uidol v{__version__}</b></blockquote>

Prefix: <code>{p}</code>

<b>Basic</b>
<code>{p}ping</code> — latency
<code>{p}alive</code> — status + uptime
<code>{p}help</code> — this menu

<b>Info</b>
<code>{p}id</code> — user/chat id (reply)
<code>{p}info</code> — user info (reply / @user)
<code>{p}chatinfo</code> — chat details

<b>Admin</b>
<code>{p}ban</code> <code>{p}unban</code> <code>{p}kick</code>
<code>{p}mute</code> <code>{p}unmute</code>
<code>{p}promote</code> <code>{p}demote</code>
<code>{p}pin</code> <code>{p}unpin</code>

<b>Tools</b>
<code>{p}del</code> — hapus (reply)
<code>{p}purge</code> — hapus range (reply atas)
<code>{p}join</code> — join @chat / link
<code>{p}leave</code> — keluar chat
<code>{p}invite</code> — export invite link
<code>{p}staff</code> — list admin
"""


@PY.UBOT("help|bantuan")
async def cmd_help(client, message: Message):
    await message.edit_text(HELP_TEXT)
