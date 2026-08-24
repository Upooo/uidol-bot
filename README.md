# Uidol

**Secure Multi-Client Telegram Userbot Framework** — v0.0.1

Fresh rewrite inspired by Goo flow, cleaner architecture, stronger session security, inline-first UI.

## Highlights

- **Inline menu** (bukan flood slash command)
- **Access gate** — hanya user verified owner yang bisa deploy
- **Deploy flow** phone → OTP → 2FA (session string **tidak pernah** plain di DB)
- **Fernet encryption** (AES + HMAC) at rest, plain hanya di memory
- **Multi-client** in-memory + auto-start dari MongoDB
- **PY decorators** (BOT / CALLBACK / OWNER / SUDO / UBOT)
- **Blockquote styling** (Telegram × Discord embed feel)
- Owner panel: grant/revoke, status, git pull, restart
- Log group aman

## Stack

- [Kurigram](https://github.com/KurimuzonTama/kurigram) (Pyrogram drop-in)
- Motor (async MongoDB)
- cryptography (Fernet)

## Setup

```bash
git clone https://github.com/Upooo/uidol-bot.git
cd uidol-bot
cp .env.example .env
# edit .env (lihat di bawah)
pip install -r requirements.txt
bash start.sh
```

Entry point: `python -m Uidol`

### Generate ENCRYPTION_KEY

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Simpan key itu di `.env`. **Jangan ganti** setelah ada session tersimpan, atau session lama tidak bisa di-decrypt.

### .env minimal

```
API_ID=
API_HASH=
BOT_TOKEN=
OWNER_ID=
MONGO_URL=mongodb://localhost:27017
MONGO_DB=uidol_bot
ENCRYPTION_KEY=   # hasil generate di atas
LOG_GROUP_ID=     # optional, group log
```

## Structure

```
Uidol/
├── __init__.py          # Bot + Ubot class, pending handlers
├── __main__.py          # load modules, start userbots, graceful stop
├── config.py            # env-only
├── core/
│   ├── database/        # connection, users, userbots, access
│   ├── security/        # Fernet protect/reveal
│   └── helpers/         # PY, BTN, MSG, tools, logger
└── modules/             # auto-loaded (start, ping, deploy, owner)
```

## Usage singkat

1. Owner grant akses via Owner Panel → Grant Akses
2. User /start → Pasang Userbot → kirim contact → OTP → 2FA
3. Session di-encrypt → disimpan → client start in-memory
4. Userbot: `.ping` (prefix default `.`)

## Catatan keamanan

- Session **tidak** pernah disimpan plain text
- Deploy hanya contact milik sendiri + access gate
- Temp client disconnect setelah export session
- Jangan share `ENCRYPTION_KEY` / `.env`

---

v0.0.1 — foundation only. Feature modules menyusul setelah debug.
