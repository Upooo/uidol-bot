# Uidol v1.0.0-Beta

**Secure Multi-Client Telegram Userbot**

Goo-style deploy flow, cleaner structure, encrypted sessions, inline UI + solid client modules.

## Setup

```bash
git clone https://github.com/Upooo/uidol-bot.git
cd uidol-bot
cp .env.example .env
# isi API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_URL, ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
pip install -r requirements.txt
bash start.sh
```

## Bot features

- Inline menu (start)
- Deploy phone → OTP → 2FA (access-gated)
- Session **encrypted at rest** (Fernet)
- Multi userbot + auto-start
- Owner panel: grant/revoke, git, restart
- `/grant <id>` `/revoke <id>`
- Log group + blockquote styling

## Userbot commands (prefix `.` by default)

| Category | Commands |
|----------|----------|
| Basic | `ping` `alive` `help` |
| Info | `id` `info` `chatinfo` |
| Admin | `ban` `unban` `kick` `mute` `unmute` `promote` `demote` `pin` `unpin` |
| Tools | `del` `purge` `join` `leave` `invite` `staff` |

## Structure

```
Uidol/
  __init__.py      # Bot / Ubot classes
  __main__.py      # entry + auto-load modules
  config.py
  core/
    database/      # mongo: users, userbots, access
    helpers/       # PY decorators, BTN, MSG
    security/      # Fernet sessions
  modules/
    start, deploy, owner, ping
    alive, info, admin, purge, tools_ubot, help_cmd
```

## Security notes

- Sessions never stored plain in DB
- Deploy only for verified users (owner grant)
- `ENCRYPTION_KEY` must be Fernet key — losing it = locked sessions
