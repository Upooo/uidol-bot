"""
Secure userbot deployment flow.
Phone → OTP → 2FA → encrypted session → start client.
Session never logged or sent to chat.
"""

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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

from Uidol.core.clients.bot import Bot
from Uidol.core.clients.manager import manager
from Uidol.core.states.manager import states
from Uidol.core.handlers.messages import get_message
from Uidol.core.database import userbots as db_userbots
from Uidol.core.logger import log, log_event
from Uidol.utils.helpers import mention
from Uidol.config.settings import (
    API_ID,
    API_HASH,
    MAX_USERBOTS,
    DEPLOY_TIMEOUT,
    USERBOT_PREFIX,
    FORCE_JOIN,
)


STATE_PHONE = "deploy_phone"
STATE_OTP = "deploy_otp"
STATE_2FA = "deploy_2fa"


def register(bot: Bot):
    @bot.on_message(filters.command("deploy") & filters.private)
    async def deploy_cmd(_, message: Message):
        user_id = message.from_user.id
        lang = "id"

        existing = await db_userbots.get_userbot(user_id)
        if existing and existing.get("is_active"):
            return await message.reply_text(get_message("deploy_already", lang=lang))

        count = await db_userbots.count_userbots(active_only=True)
        if count >= MAX_USERBOTS:
            return await message.reply_text(
                get_message("deploy_full", lang=lang, max=MAX_USERBOTS)
            )

        states.set(user_id, STATE_PHONE, ttl=DEPLOY_TIMEOUT)
        kb = ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Kirim nomor HP", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await message.reply_text(get_message("deploy_start", lang=lang), reply_markup=kb)

    @bot.on_message(filters.command("cancel") & filters.private)
    async def cancel_cmd(_, message: Message):
        user_id = message.from_user.id
        if states.get(user_id):
            data = states.get(user_id)
            if data and data.data.get("temp_client"):
                try:
                    await data.data["temp_client"].disconnect()
                except Exception:
                    pass
            states.clear(user_id)
            await message.reply_text(
                get_message("deploy_cancel", lang="id"),
                reply_markup=ReplyKeyboardRemove(),
            )

    @bot.on_message(filters.private & filters.contact)
    async def on_contact(_, message: Message):
        user_id = message.from_user.id
        if not states.is_in(user_id, STATE_PHONE):
            return

        if not message.contact or message.contact.user_id != user_id:
            return await message.reply_text(
                "Gunakan tombol untuk share nomor **akun kamu sendiri**."
            )

        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = f"+{phone}"

        status = await message.reply_text(
            get_message("deploy_processing", lang="id"),
            reply_markup=ReplyKeyboardRemove(),
        )

        temp = Client(
            name=f"deploy_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
        )

        try:
            await temp.connect()
            sent = await temp.send_code(phone)
        except (PhoneNumberInvalid, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
            states.clear(user_id)
            await status.edit_text(f"❌ Nomor tidak valid / diblokir.\n`{type(e).__name__}`")
            try:
                await temp.disconnect()
            except Exception:
                pass
            return
        except PhoneNumberFlood:
            states.clear(user_id)
            await status.edit_text("❌ Terlalu banyak percobaan. Coba lagi nanti.")
            try:
                await temp.disconnect()
            except Exception:
                pass
            return
        except ApiIdInvalid:
            states.clear(user_id)
            await status.edit_text("❌ API_ID / API_HASH tidak valid.")
            try:
                await temp.disconnect()
            except Exception:
                pass
            return
        except FloodWait as e:
            states.clear(user_id)
            await status.edit_text(f"❌ FloodWait: tunggu {e.value} detik.")
            try:
                await temp.disconnect()
            except Exception:
                pass
            return
        except Exception as e:
            states.clear(user_id)
            log.error(f"send_code error: {type(e).__name__}")
            await status.edit_text(get_message("error_generic", lang="id"))
            try:
                await temp.disconnect()
            except Exception:
                pass
            return

        states.set(
            user_id,
            STATE_OTP,
            data={
                "phone": phone,
                "phone_code_hash": sent.phone_code_hash,
                "temp_client": temp,
            },
            ttl=DEPLOY_TIMEOUT,
        )
        await status.edit_text(get_message("deploy_otp", lang="id"))

    @bot.on_message(filters.private & filters.text & ~filters.command(["cancel", "start", "help", "ping", "deploy"]))
    async def on_text_during_deploy(_, message: Message):
        user_id = message.from_user.id
        state = states.get(user_id)
        if not state:
            return

        if state.name == STATE_OTP:
            await _handle_otp(bot, message, state)
        elif state.name == STATE_2FA:
            await _handle_2fa(bot, message, state)


async def _handle_otp(bot: Bot, message: Message, state):
    user_id = message.from_user.id
    code_raw = message.text.strip().replace(" ", "")
    phone = state.data["phone"]
    phone_code_hash = state.data["phone_code_hash"]
    temp = state.data["temp_client"]

    status = await message.reply_text(get_message("deploy_processing", lang="id"))

    try:
        await temp.sign_in(phone, phone_code_hash, code_raw)
    except SessionPasswordNeeded:
        states.set(
            user_id,
            STATE_2FA,
            data=state.data,
            ttl=DEPLOY_TIMEOUT,
        )
        await status.edit_text(get_message("deploy_2fa", lang="id"))
        return
    except (PhoneCodeInvalid, PhoneCodeExpired) as e:
        await status.edit_text(f"❌ Kode OTP salah / expired.\n`{type(e).__name__}`")
        return
    except Exception as e:
        log.error(f"sign_in error: {type(e).__name__}")
        await status.edit_text(get_message("error_generic", lang="id"))
        return

    await _finalize_deploy(bot, message, status, temp, user_id)


async def _handle_2fa(bot: Bot, message: Message, state):
    user_id = message.from_user.id
    password = message.text.strip()
    temp = state.data["temp_client"]

    try:
        await message.delete()
    except Exception:
        pass

    status = await message.reply_text(get_message("deploy_processing", lang="id"))

    try:
        await temp.check_password(password)
    except Exception as e:
        log.error(f"2FA error: {type(e).__name__}")
        await status.edit_text("❌ Password 2FA salah. Coba lagi atau /cancel.")
        return

    await _finalize_deploy(bot, message, status, temp, user_id)


async def _finalize_deploy(bot: Bot, message: Message, status: Message, temp: Client, user_id: int):
    try:
        me = await temp.get_me()
        if me.id != user_id:
            await temp.disconnect()
            states.clear(user_id)
            await status.edit_text(
                "❌ Nomor yang dipakai harus milik akun Telegram yang sedang chat dengan bot ini."
            )
            return

        session_string = await temp.export_session_string()
        await temp.disconnect()

        ok = await db_userbots.add_userbot(
            user_id=user_id,
            session_string=session_string,
            name=me.first_name or str(user_id),
        )
        session_string = None

        if not ok:
            states.clear(user_id)
            await status.edit_text(get_message("error_generic", lang="id"))
            return

        ubot = await manager.start_one(user_id)
        states.clear(user_id)

        if not ubot:
            await status.edit_text(
                "Session tersimpan tapi gagal start client. Coba /restartubot nanti."
            )
            await log_event(
                f"⚠️ Deploy partial\nUser: {mention(message.from_user)}\nID: `{user_id}`"
            )
            return

        for chat in FORCE_JOIN:
            try:
                await ubot.join_chat(chat)
            except Exception:
                pass

        await status.edit_text(
            get_message(
                "deploy_success",
                lang="id",
                name=me.first_name,
                uid=me.id,
                prefix=USERBOT_PREFIX,
            )
        )
        await log_event(
            f"✅ **Userbot deployed**\n"
            f"User: {mention(message.from_user)}\n"
            f"ID: `{user_id}`\n"
            f"Name: {me.first_name}"
        )
        log.info(f"Deploy success for {user_id}")

    except Exception as e:
        states.clear(user_id)
        log.error(f"finalize deploy error: {type(e).__name__}: {e}")
        await status.edit_text(get_message("error_generic", lang="id"))
        try:
            await temp.disconnect()
        except Exception:
            pass
