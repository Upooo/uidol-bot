"""Main menu — inline first."""

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from Uidol import bot
from Uidol.config import is_owner
from Uidol.core.database import users as db_users
from Uidol.core.helpers import BTN, MSG
from Uidol.core.helpers.logger import log_event
from Uidol.core.helpers.tools import mention


@bot.on_message(filters.command("start") & filters.private)
async def cmd_start(_, message: Message):
    user = message.from_user
    await db_users.upsert_user(
        user.id,
        user.first_name or "",
        user.last_name or "",
        user.username or "",
    )
    text = MSG.start(mention(user))
    await message.reply_text(
        text,
        reply_markup=BTN.main_menu(is_owner=is_owner(user.id)),
    )
    await log_event(
        bot,
        MSG.log_start(mention(user), user.id, user.username or ""),
    )


@bot.on_message(filters.command("help") & filters.private)
async def cmd_help(_, message: Message):
    await message.reply_text(
        MSG.help_user(),
        reply_markup=BTN.back_home(),
    )


@bot.on_callback_query(filters.regex(r"^menu:home$"))
async def cb_home(_, callback: CallbackQuery):
    user = callback.from_user
    await callback.message.edit_text(
        MSG.start(mention(user)),
        reply_markup=BTN.main_menu(is_owner=is_owner(user.id)),
    )
    await callback.answer()


@bot.on_callback_query(filters.regex(r"^menu:help$"))
async def cb_help(_, callback: CallbackQuery):
    await callback.message.edit_text(
        MSG.help_user(),
        reply_markup=BTN.back_home(),
    )
    await callback.answer()
