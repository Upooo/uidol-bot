"""
Centralized response messages for Uidol.
Organized, multi-language foundation (Bot first).
"""

from typing import Dict

LANGS = ("id", "en")

BOT: Dict[str, Dict[str, str]] = {
    "start": {
        "id": (
            "Halo {mention}!\n\n"
            "Saya **Uidol**, bot management userbot.\n"
            "Gunakan /help untuk melihat perintah.\n"
            "Gunakan /deploy untuk memasang userbot."
        ),
        "en": (
            "Hello {mention}!\n\n"
            "I am **Uidol**, the userbot management bot.\n"
            "Use /help for commands.\n"
            "Use /deploy to install a userbot."
        ),
    },
    "help": {
        "id": (
            "**Perintah Uidol**\n\n"
            "**User**\n"
            "/start — Mulai bot\n"
            "/help — Bantuan\n"
            "/ping — Cek latency\n"
            "/deploy — Pasang userbot\n"
            "/myubot — Status userbot kamu\n"
            "/restartubot — Restart userbot kamu\n\n"
            "**Developer**\n"
            "/status — Status sistem\n"
            "/users — Daftar user\n"
            "/ubots — Daftar userbot\n"
            "/git — status | pull\n"
            "/restart — Restart bot utama"
        ),
        "en": (
            "**Uidol Commands**\n\n"
            "**User**\n"
            "/start — Start bot\n"
            "/help — Help\n"
            "/ping — Latency\n"
            "/deploy — Install userbot\n"
            "/myubot — Your userbot status\n"
            "/restartubot — Restart your userbot\n\n"
            "**Developer**\n"
            "/status — System status\n"
            "/users — User list\n"
            "/ubots — Userbot list\n"
            "/git — status | pull\n"
            "/restart — Restart main bot"
        ),
    },
    "ping": {
        "id": "Pong! ⚡\nLatency: `{ms}ms`",
        "en": "Pong! ⚡\nLatency: `{ms}ms`",
    },
    "owner_only": {
        "id": "Perintah ini hanya untuk Owner / Sudo.",
        "en": "This command is for Owner / Sudo only.",
    },
    "error_generic": {
        "id": "Terjadi kesalahan. Coba lagi nanti.",
        "en": "An error occurred. Please try again later.",
    },
    "deploy_start": {
        "id": (
            "Siap memasang userbot.\n\n"
            "Kirim **nomor HP** dengan tombol di bawah "
            "(jangan ketik manual).\n\n"
            "Ketik /cancel untuk membatalkan."
        ),
        "en": (
            "Ready to install userbot.\n\n"
            "Send your **phone number** using the button below "
            "(do not type manually).\n\n"
            "Type /cancel to abort."
        ),
    },
    "deploy_otp": {
        "id": (
            "Kode OTP sudah dikirim ke Telegram resmi kamu.\n\n"
            "Kirim kode ke sini.\n"
            "Contoh: jika kode `12345`, kirim: `1 2 3 4 5`\n\n"
            "/cancel untuk batalkan."
        ),
        "en": (
            "OTP sent to your official Telegram app.\n\n"
            "Send the code here.\n"
            "Example: if code is `12345`, send: `1 2 3 4 5`\n\n"
            "/cancel to abort."
        ),
    },
    "deploy_2fa": {
        "id": (
            "Akun ini memakai verifikasi 2 langkah.\n"
            "Kirim **password 2FA** kamu.\n\n"
            "/cancel untuk batalkan."
        ),
        "en": (
            "This account has 2-step verification.\n"
            "Send your **2FA password**.\n\n"
            "/cancel to abort."
        ),
    },
    "deploy_success": {
        "id": (
            "✅ **Userbot aktif**\n\n"
            "Nama: {name}\n"
            "ID: `{uid}`\n"
            "Prefix: `{prefix}`\n\n"
            "Coba kirim `{prefix}ping` dari akun userbot."
        ),
        "en": (
            "✅ **Userbot active**\n\n"
            "Name: {name}\n"
            "ID: `{uid}`\n"
            "Prefix: `{prefix}`\n\n"
            "Try `{prefix}ping` from the userbot account."
        ),
    },
    "deploy_cancel": {
        "id": "Deploy dibatalkan. /start untuk mulai lagi.",
        "en": "Deploy cancelled. /start to begin again.",
    },
    "deploy_already": {
        "id": "Kamu sudah punya userbot. Gunakan /myubot atau /restartubot.",
        "en": "You already have a userbot. Use /myubot or /restartubot.",
    },
    "deploy_full": {
        "id": "Slot userbot penuh ({max}). Hubungi owner.",
        "en": "Userbot slots full ({max}). Contact owner.",
    },
    "deploy_processing": {
        "id": "Memproses... tunggu sebentar.",
        "en": "Processing... please wait.",
    },
    "no_ubot": {
        "id": "Kamu belum punya userbot. Gunakan /deploy.",
        "en": "You don't have a userbot. Use /deploy.",
    },
}


def get_message(key: str, lang: str = "id", **kwargs) -> str:
    lang = lang if lang in LANGS else "id"
    text = BOT.get(key, {}).get(lang) or BOT.get(key, {}).get("id") or key
    try:
        return text.format(**kwargs)
    except Exception:
        return text
