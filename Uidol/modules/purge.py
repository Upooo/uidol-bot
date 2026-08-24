"""Purge & delete messages."""

import asyncio
from pyrogram.types import Message
from pyrogram.errors import RPCError

from Uidol.core.helpers.decorators import PY


@PY.UBOT("del|delete")
async def cmd_del(client, message: Message):
    if not message.reply_to_message:
        await message.edit_text("<blockquote>Reply pesan yang mau dihapus.</blockquote>")
        return
    try:
        await message.reply_to_message.delete()
        await message.delete()
    except RPCError:
        try:
            await message.edit_text("<blockquote><b>Gagal hapus</b></blockquote>")
        except Exception:
            pass


@PY.UBOT("purge")
async def cmd_purge(client, message: Message):
    if not message.reply_to_message:
        await message.edit_text(
            "<blockquote><b>Purge</b></blockquote>\n\n"
            "Reply pesan paling atas, lalu <code>.purge</code> — hapus sampai pesan ini."
        )
        return

    start_id = message.reply_to_message.id
    end_id = message.id
    chat_id = message.chat.id
    deleted = 0

    try:
        # Delete in chunks of 100
        ids = list(range(start_id, end_id + 1))
        for i in range(0, len(ids), 100):
            chunk = ids[i : i + 100]
            try:
                await client.delete_messages(chat_id, chunk)
                deleted += len(chunk)
            except RPCError:
                for mid in chunk:
                    try:
                        await client.delete_messages(chat_id, mid)
                        deleted += 1
                    except Exception:
                        pass
            await asyncio.sleep(0.3)
    except Exception as e:
        await message.reply_text(
            f"<blockquote><b>Purge partial</b></blockquote>\n\n"
            f"Deleted ~<code>{deleted}</code>\n<code>{type(e).__name__}</code>"
        )
        return

    status = await message.reply_text(
        f"<blockquote><b>Purged</b></blockquote>\n\n<code>{deleted}</code> pesan dihapus."
    )
    await asyncio.sleep(2)
    try:
        await status.delete()
    except Exception:
        pass
