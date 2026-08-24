# Uidol

**Secure Multi-Client Telegram Userbot Framework**

Version: **0.0.1** (Foundation / Private Development)

---

## About

Uidol is a clean, modular, and security-focused multi-client userbot framework built on **Kurigram**.

This version focuses purely on solid foundation:
- Secure encrypted session storage
- Auto module loader
- Multi-client ready
- Clean architecture
- Easy to extend

## Features (v0.0.1)

- Management Bot + Multi Userbot support
- MongoDB backend
- Sessions encrypted at rest (Fernet)
- Auto-discover modules (just drop file in `modules/`)
- Centralized message responses with multi-language foundation
- Safe logging (never leaks sessions)

## Quick Start

1. Clone / download this repository
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Fill the required values in `.env`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   bash start.sh
   # or
   python -m Uidol
   ```

## Generate Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Project Structure

See the `Uidol/` package for the modular architecture.

## Development Status

- [x] Core architecture
- [x] Config system
- [x] Database layer
- [x] Security / Session encryption
- [x] Auto module loader
- [x] Multi-client manager
- [x] Basic commands (`/start`, `/ping`, `/help`)
- [ ] More modules (coming after foundation is stable)
- [ ] Public Beta (v1.0.0-Beta)

---

**Note**: This is a private development version. Not ready for public use yet.
