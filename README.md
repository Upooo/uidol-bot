# Uidol

**Secure Multi-Client Telegram Userbot Framework**

Version: **0.0.1** (Foundation / Private Development)

Built with **Kurigram** + MongoDB. Sessions encrypted at rest. Auto module loader.

## Features

- Management bot + multi userbot clients
- Secure deploy flow: phone → OTP → 2FA → encrypted session
- Sessions never logged or written plain to disk (`in_memory`)
- Auto-load modules (`Uidol/modules/`)
- Developer commands: `/status`, `/users`, `/ubots`, `/git`, `/restart`
- Event logs to `LOG_GROUP_ID`
- Userbot `.ping` out of the box

## Setup

```bash
cp .env.example .env
# fill API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_URL, ENCRYPTION_KEY, LOG_GROUP_ID
pip install -r requirements.txt
bash start.sh
```

Generate encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Commands

**User:** `/start` `/help` `/ping` `/deploy` `/myubot` `/restartubot` `/cancel`  
**Owner/Sudo:** `/status` `/users` `/ubots`  
**Owner:** `/git status` `/git pull` `/restart`

Userbot prefix default: `.` → `.ping`

## Structure

```
Uidol/
  config/       settings
  core/
    clients/    bot, userbot, manager
    database/   mongo layers
    security/   encryption, session
    loader/     auto modules
    handlers/   messages, errors
    states/     conversation state
  modules/      drop files here
  utils/
```

## Security notes

- `ENCRYPTION_KEY` must stay on the server only
- No command exports session strings
- 2FA password message is deleted when possible
- Logger filters session-like patterns

## Status

Foundation is the focus of v0.0.1. Client feature modules come later.
