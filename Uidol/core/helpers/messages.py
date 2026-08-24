"""Response texts — blockquote style (Telegram x Discord embed feel)."""

from Uidol.config import USERBOT_PREFIX


class MSG:
    @staticmethod
    def start(user_mention: str) -> str:
        return (
            f"<blockquote><b>Uidol</b></blockquote>\n\n"
            f"Halo {user_mention}!\n\n"
            f"Bot management multi-userbot.\n"
            f"Pakai tombol di bawah untuk navigasi."
        )

    @staticmethod
    def help_user() -> str:
        return (
            "<blockquote><b>Bantuan</b></blockquote>\n\n"
            "<b>Menu</b>\n"
            "• Pasang Userbot — deploy akun (butuh akses)\n"
            "• Status Akun — cek userbot kamu\n"
            "• Restart Ubot — restart client kamu\n\n"
            "<b>Akses</b>\n"
            "Deploy hanya untuk user yang sudah di-verify owner."
        )

    @staticmethod
    def help_owner() -> str:
        return (
            "<blockquote><b>Owner Panel</b></blockquote>\n\n"
            "• Status Sistem\n"
            "• Daftar User / Userbot\n"
            "• Grant / Revoke akses deploy\n"
            "• Git status / pull\n"
            "• Restart bot"
        )

    @staticmethod
    def no_access() -> str:
        return (
            "<blockquote><b>Akses ditolak</b></blockquote>\n\n"
            "Kamu belum punya izin deploy userbot.\n"
            "Hubungi owner untuk di-verify."
        )

    @staticmethod
    def already_ubot() -> str:
        return (
            "<blockquote><b>Sudah terpasang</b></blockquote>\n\n"
            "Kamu sudah punya userbot aktif.\n"
            "Pakai <b>Status Akun</b> atau <b>Restart Ubot</b>."
        )

    @staticmethod
    def slots_full(max_n: int) -> str:
        return (
            f"<blockquote><b>Slot penuh</b></blockquote>\n\n"
            f"Maksimal userbot: <code>{max_n}</code>.\n"
            f"Hubungi owner."
        )

    @staticmethod
    def deploy_phone() -> str:
        return (
            "<blockquote><b>Pasang Userbot</b></blockquote>\n\n"
            "Kirim nomor HP lewat tombol di bawah.\n"
            "<i>Jangan ketik manual.</i>\n\n"
            "Ketik /cancel untuk batalkan."
        )

    @staticmethod
    def deploy_otp() -> str:
        return (
            "<blockquote><b>Kode OTP</b></blockquote>\n\n"
            "OTP sudah dikirim ke Telegram resmi kamu.\n\n"
            "Kirim kode ke sini.\n"
            "Contoh kode <code>12345</code> → kirim <code>1 2 3 4 5</code>\n\n"
            "/cancel untuk batalkan."
        )

    @staticmethod
    def deploy_2fa() -> str:
        return (
            "<blockquote><b>Verifikasi 2 Langkah</b></blockquote>\n\n"
            "Akun ini memakai 2FA.\n"
            "Kirim <b>password 2FA</b> kamu.\n\n"
            "/cancel untuk batalkan."
        )

    @staticmethod
    def deploy_ok(name: str, uid: int) -> str:
        p = USERBOT_PREFIX
        return (
            f"<blockquote><b>Userbot aktif</b></blockquote>\n\n"
            f"<b>Nama</b>: {name}\n"
            f"<b>ID</b>: <code>{uid}</code>\n"
            f"<b>Prefix</b>: <code>{p}</code>\n\n"
            f"Coba <code>{p}ping</code> dari akun userbot."
        )

    @staticmethod
    def deploy_cancel() -> str:
        return (
            "<blockquote><b>Dibatalkan</b></blockquote>\n\n"
            "Deploy dibatalkan. Kembali ke menu dengan /start."
        )

    @staticmethod
    def processing() -> str:
        return "<blockquote>Memproses… tunggu sebentar.</blockquote>"

    @staticmethod
    def error() -> str:
        return (
            "<blockquote><b>Error</b></blockquote>\n\n"
            "Terjadi kesalahan. Coba lagi nanti."
        )

    @staticmethod
    def my_ubot(name: str, uid: int, online: bool, active: bool) -> str:
        return (
            f"<blockquote><b>Status Akun</b></blockquote>\n\n"
            f"<b>Nama</b>: {name}\n"
            f"<b>ID</b>: <code>{uid}</code>\n"
            f"<b>Active</b>: <code>{'ya' if active else 'tidak'}</code>\n"
            f"<b>Online</b>: <code>{'ya' if online else 'tidak'}</code>"
        )

    @staticmethod
    def no_ubot() -> str:
        return (
            "<blockquote><b>Belum ada userbot</b></blockquote>\n\n"
            "Kamu belum memasang userbot.\n"
            "Pakai menu <b>Pasang Userbot</b> (butuh akses)."
        )

    @staticmethod
    def system_status(uptime: str, users: int, ubots: int, online: int, max_n: int) -> str:
        return (
            f"<blockquote><b>Status Sistem</b></blockquote>\n\n"
            f"<b>Uptime</b>: <code>{uptime}</code>\n"
            f"<b>Users</b>: <code>{users}</code>\n"
            f"<b>Userbots</b>: <code>{ubots}</code>\n"
            f"<b>Online</b>: <code>{online}/{max_n}</code>"
        )

    @staticmethod
    def access_granted(uid: int) -> str:
        return (
            f"<blockquote><b>Akses diberikan</b></blockquote>\n\n"
            f"User <code>{uid}</code> sekarang bisa deploy."
        )

    @staticmethod
    def access_revoked(uid: int) -> str:
        return (
            f"<blockquote><b>Akses dicabut</b></blockquote>\n\n"
            f"User <code>{uid}</code> tidak bisa deploy lagi."
        )

    @staticmethod
    def log_start(mention: str, uid: int, username: str = "") -> str:
        extra = f"\n@{username}" if username else ""
        return (
            f"<blockquote><b>/start</b></blockquote>\n\n"
            f"{mention}\n<code>{uid}</code>{extra}"
        )

    @staticmethod
    def log_deploy(mention: str, uid: int, name: str) -> str:
        return (
            f"<blockquote><b>Deploy sukses</b></blockquote>\n\n"
            f"{mention}\n<code>{uid}</code>\n{name}"
        )

    @staticmethod
    def log_boot(bot_name: str, online: int) -> str:
        return (
            f"<blockquote><b>Uidol started</b></blockquote>\n\n"
            f"<b>Bot</b>: {bot_name}\n"
            f"<b>Userbots online</b>: <code>{online}</code>"
        )
