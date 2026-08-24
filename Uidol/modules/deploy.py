"""Deploy userbot — access-gated, phone → OTP → 2FA → encrypted session."""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneNumberFlood,
    PhoneNumberBanned,
    PhoneNumberUnoccupied,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    FloodWait,
)

from Uidol import bot, ubot, log
from Uidol.config import (
    API_ID,
    API_HASH,
    MAX_USERBOTS,
    DEPLOY_TIMEOUT,
    FORCE_JOIN,
    is_owner,
)
from Uidol.core.database import userbots as db_ubot
from Uidol.core.database import access as db_access
from Uidol.core.helpers import BTN, MSG
from Uidol.core.helpers.logger import log_event
from Uidol.core.helpers.tools import mention

_STATE = {}


def _set(uid, name, data=None, ttl=DEPLOY_TIMEOUT):
    _STATE[uid] = {
        "name": name,
        "data": data or {},
        "expires": asyncio.get_event_loop().time() + ttl,
    }


def _get(uid):
    s = _STATE.get(uid)
    if not s:
        return None
    if asyncio.get_event_loop().time() > s["expires"]:
        _STATE.pop(uid, None)
        return None
    return s


def _clear(uid):
    _STATE.pop(uid, None)


@bot.on_callback_query(filters.regex(r"^menu:deploy$"))
async def cb_deploy(_, callback: CallbackQuery):
    uid = callback.from_user.id
    if not is_owner(uid) and not await db_access.has_access(uid):
        await callback.answer("Tidak ada akses.", show_alert=True)
        await callback.message.edit_text(MSG.no_access(), reply_markup=BTN.back_home())
        return
    existing = await db_ubot.get_ubot(uid)
    if existing and existing.get("is_active"):
        await callback.message.edit_text(MSG.already_ubot(), reply_markup=BTN.back_home())
        await callback.answer()
        return
    if await db_ubot.count_ubots(active_only=True) >= MAX_USERBOTS:
        await callback.message.edit_text(MSG.slots_full(MAX_USERBOTS), reply_markup=BTN.back_home())
        await callback.answer()
        return
    _set(uid, "phone")
    await callback.message.edit_text(MSG.deploy_phone())
    await callback.message.reply_text("Tekan tombol di bawah:", reply_markup=BTN.phone_request())
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^menu:status$"))
async def cb_status(_, callback: CallbackQuery):
    uid = callback.from_user.id
    doc = await db_ubot.get_ubot(uid)
    if not doc:
        await callback.message.edit_text(MSG.no_ubot(), reply_markup=BTN.back_home())
        await callback.answer()
        return
    online = uid in ubot._ids
    await callback.message.edit_text(
        MSG.my_ubot(doc.get("name", "-"), uid, online, doc.get("is_active", False)),
        reply_markup=BTN.back_home(),
    )
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^menu:restart_ubot$"))
async def cb_restart_ubot(_, callback: CallbackQuery):
    uid = callback.from_user.id
    doc = await db_ubot.get_ubot(uid)
    if not doc:
        await callback.message.edit_text(MSG.no_ubot(), reply_markup=BTN.back_home())
        await callback.answer()
        return
    await callback.answer("Restarting…")
    for u in list(ubot._ubot):
        try:
            if u.me and u.me.id == uid:
                await u.stop()
        except Exception:
            pass
    session = await db_ubot.get_session(uid)
    if not session:
        await callback.message.edit_text(MSG.error(), reply_markup=BTN.back_home())
        return
    client = ubot.__class__(session_string=session, name=str(uid))
    try:
        await client.start()
        await callback.message.edit_text(
            "<blockquote><b>Userbot di-restart</b></blockquote>\n\nClient online lagi.",
            reply_markup=BTN.back_home(),
        )
    except Exception as e:
        log.error(f"restart ubot: {e}")
        await callback.message.edit_text(MSG.error(), reply_markup=BTN.back_home())


@bot.on_message(filters.command("cancel") & filters.private)
async def cmd_cancel(_, message: Message):
    uid = message.from_user.id
    st = _get(uid)
    if st and st["data"].get("temp"):
        try:
            await st["data"]["temp"].disconnect()
        except Exception:
            pass
    if st:
        _clear(uid)
        await message.reply_text(MSG.deploy_cancel(), reply_markup=BTN.remove_kb())


@bot.on_message(filters.private & filters.contact)
async def on_contact(_, message: Message):
    uid = message.from_user.id
    st = _get(uid)
    if not st or st["name"] != "phone":
        return
    if not message.contact or message.contact.user_id != uid:
        await message.reply_text("<blockquote>Pakai nomor <b>akun kamu sendiri</b>.</blockquote>")
        return
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = f"+{phone}"
    status = await message.reply_text(MSG.processing(), reply_markup=BTN.remove_kb())
    temp = Client(name=f"deploy_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    try:
        await temp.connect()
        sent = await temp.send_code(phone)
    except (PhoneNumberInvalid, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
        _clear(uid)
        await status.edit_text(f"<blockquote><b>Nomor bermasalah</b></blockquote>\n\n<code>{type(e).__name__}</code>")
        try:
            await temp.disconnect()
        except Exception:
            pass
        return
    except PhoneNumberFlood:
        _clear(uid)
        await status.edit_text("<blockquote><b>Flood</b></blockquote>\n\nCoba lagi nanti.")
        try:
            await temp.disconnect()
        except Exception:
            pass
        return
    except FloodWait as e:
        _clear(uid)
        await status.edit_text(f"<blockquote><b>FloodWait</b></blockquote>\n\nTunggu <code>{e.value}</code> detik.")
        try:
            await temp.disconnect()
        except Exception:
            pass
        return
    except Exception as e:
        _clear(uid)
        log.error(f"send_code: {type(e).__name__}")
        await status.edit_text(MSG.error())
        try:
            await temp.disconnect()
        except Exception:
            pass
        return
    _set(uid, "otp", {"phone": phone, "hash": sent.phone_code_hash, "temp": temp})
    await status.edit_text(MSG.deploy_otp())


@bot.on_message(filters.private & filters.text & ~filters.command(["start", "help", "ping", "cancel"]))
async def on_deploy_text(_, message: Message):
    uid = message.from_user.id
    st = _get(uid)
    if not st:
        return
    if st["name"] == "otp":
        await _otp(message, st)
    elif st["name"] == "2fa":
        await _2fa(message, st)


async def _otp(message: Message, st: dict):
    uid = message.from_user.id
    code = message.text.strip().replace(" ", "")
    temp = st["data"]["temp"]
    status = await message.reply_text(MSG.processing())
    try:
        await temp.sign_in(st["data"]["phone"], st["data"]["hash"], code)
    except SessionPasswordNeeded:
        _set(uid, "2fa", st["data"])
        await status.edit_text(MSG.deploy_2fa())
        return
    except (PhoneCodeInvalid, PhoneCodeExpired) as e:
        await status.edit_text(f"<blockquote><b>OTP salah / expired</b></blockquote>\n\n<code>{type(e).__name__}</code>")
        return
    except Exception as e:
        log.error(f"sign_in: {type(e).__name__}")
        await status.edit_text(MSG.error())
        return
    await _finish(message, status, temp, uid)


async def _2fa(message: Message, st: dict):
    uid = message.from_user.id
    password = message.text.strip()
    temp = st["data"]["temp"]
    try:
        await message.delete()
    except Exception:
        pass
    status = await message.reply_text(MSG.processing())
    try:
        await temp.check_password(password)
    except Exception:
        await status.edit_text("<blockquote><b>2FA salah</b></blockquote>\n\nCoba lagi atau /cancel.")
        return
    await _finish(message, status, temp, uid)


async def _finish(message: Message, status: Message, temp: Client, uid: int):
    try:
        me = await temp.get_me()
        if me.id != uid:
            await temp.disconnect()
            _clear(uid)
            await status.edit_text(
                "<blockquote><b>Nomor tidak cocok</b></blockquote>\n\n"
                "Pakai nomor akun yang sedang chat dengan bot ini."
            )
            return
        plain = await temp.export_session_string()
        await temp.disconnect()
        await db_ubot.add_ubot(uid, plain, me.first_name or str(uid))
        client = ubot.__class__(session_string=plain, name=str(uid))
        plain = None
        await client.start()
        _clear(uid)
        for chat in FORCE_JOIN:
            try:
                await client.join_chat(chat)
            except Exception:
                pass
        await status.edit_text(
            MSG.deploy_ok(me.first_name or "-", me.id),
            reply_markup=BTN.back_home(),
        )
        await log_event(
            bot,
            MSG.log_deploy(mention(message.from_user), uid, me.first_name or "-"),
        )
    except Exception as e:
        _clear(uid)
        log.error(f"finalize: {e}")
        await status.edit_text(MSG.error())
        try:
            await temp.disconnect()
        except Exception:
            pass
