"""Inline + reply keyboards."""

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)


class BTN:
    @staticmethod
    def main_menu(is_owner: bool = False) -> InlineKeyboardMarkup:
        rows = [
            [InlineKeyboardButton("📦 Pasang Userbot", callback_data="menu:deploy")],
            [
                InlineKeyboardButton("📊 Status Akun", callback_data="menu:status"),
                InlineKeyboardButton("♻️ Restart Ubot", callback_data="menu:restart_ubot"),
            ],
            [InlineKeyboardButton("❓ Bantuan", callback_data="menu:help")],
        ]
        if is_owner:
            rows.append([InlineKeyboardButton("🛠 Owner Panel", callback_data="menu:owner")])
        return InlineKeyboardMarkup(rows)

    @staticmethod
    def owner_panel() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📡 Status Sistem", callback_data="owner:status")],
                [
                    InlineKeyboardButton("👥 Users", callback_data="owner:users"),
                    InlineKeyboardButton("🤖 Ubots", callback_data="owner:ubots"),
                ],
                [
                    InlineKeyboardButton("✅ Grant Akses", callback_data="owner:grant"),
                    InlineKeyboardButton("❌ Revoke Akses", callback_data="owner:revoke"),
                ],
                [
                    InlineKeyboardButton("📥 Git Status", callback_data="owner:git_status"),
                    InlineKeyboardButton("⬆️ Git Pull", callback_data="owner:git_pull"),
                ],
                [InlineKeyboardButton("♻️ Restart Bot", callback_data="owner:restart")],
                [InlineKeyboardButton("« Kembali", callback_data="menu:home")],
            ]
        )

    @staticmethod
    def back_home() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Menu", callback_data="menu:home")]]
        )

    @staticmethod
    def phone_request() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Kirim nomor HP", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    @staticmethod
    def remove_kb() -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()

    @staticmethod
    def confirm(yes_data: str, no_data: str = "menu:home") -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Ya", callback_data=yes_data),
                    InlineKeyboardButton("❌ Tidak", callback_data=no_data),
                ]
            ]
        )
