"""
Centralized response messages for Uidol.
Organized by category. Easy to maintain and extend.
Supports multi-language for Bot messages (foundation ready for userbots later).
"""

from typing import Dict

# Supported languages for Bot
LANGS = ("id", "en")

# =========================================================
# BOT MESSAGES
# =========================================================

BOT: Dict[str, Dict[str, str]] = {
    # ----- Start / Help -----
    "start": {
        "id": (
            "Halo {mention}!\n\n"
            "Saya adalah **Uidol**, bot management untuk userbot.\n"
            "Gunakan /help untuk melihat perintah yang tersedia."
        ),
        "en": (
            "Hello {mention}!\n\n"
            "I am **Uidol**, the management bot for userbots.\n"
            "Use /help to see available commands."
        ),
    },
    "help": {
        "id": (
            "**Daftar Perintah Uidol**\n\n"
            "/start - Mulai bot\n"
            "/ping - Cek latency\n"
            "/help - Tampilkan bantuan ini"
        ),
        "en": (
            "**Uidol Command List**\n\n"
            "/start - Start the bot\n"
            "/ping - Check latency\n"
            "/help - Show this help"
        ),
    },

    # ----- System -----
    "ping": {
        "id": "Pong! ⚡\nLatency: `{ms}ms`",
        "en": "Pong! ⚡\nLatency: `{ms}ms`",
    },
    "owner_only": {
        "id": "Perintah ini hanya untuk Owner.",
        "en": "This command is for Owner only.",
    },
    "error_generic": {
        "id": "Terjadi kesalahan. Silakan coba lagi nanti.",
        "en": "An error occurred. Please try again later.",
    },
}


# =========================================================
# HELPER
# =========================================================

def get_message(key: str, lang: str = "id", **kwargs) -> str:
    """
    Get a localized message.
    Fallback order: requested lang → id → key name
    """
    lang = lang if lang in LANGS else "id"
    category = BOT  # currently only BOT messages

    text = category.get(key, {}).get(lang)
    if not text:
        text = category.get(key, {}).get("id", key)

    try:
        return text.format(**kwargs)
    except Exception:
        return text
