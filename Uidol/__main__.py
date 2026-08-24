"""Entry: python -m Uidol"""

import asyncio
import importlib
import pkgutil
import signal
from pathlib import Path

from Uidol import bot, ubot, log, __version__
from Uidol.config import MAX_USERBOTS
from Uidol.core.database.connection import db
from Uidol.core.database import userbots as db_ubot
from Uidol.core.helpers.logger import log_event
from Uidol.core.helpers.messages import MSG


async def load_modules():
    package = "Uidol.modules"
    path = Path(__file__).parent / "modules"
    loaded = []
    for info in pkgutil.iter_modules([str(path)]):
        if info.name.startswith("_"):
            continue
        try:
            importlib.import_module(f"{package}.{info.name}")
            loaded.append(info.name)
            log.info(f"Module: {info.name}")
        except Exception as e:
            log.error(f"Module {info.name} failed: {e}")
    return loaded


async def start_userbots():
    records = await db_ubot.get_all_active()
    count = 0
    for rec in records:
        if count >= MAX_USERBOTS:
            log.warning("MAX_USERBOTS reached")
            break
        uid = rec["user_id"]
        session = await db_ubot.get_session(uid)
        if not session:
            continue
        client = ubot.__class__(session_string=session, name=str(uid))
        try:
            me = await asyncio.wait_for(client.start(), timeout=20)
            if me.id != uid:
                await client.stop()
                log.error(f"ID mismatch {uid}")
                continue
            count += 1
        except Exception as e:
            log.error(f"Start ubot {uid} failed: {e}")
            await db_ubot.set_active(uid, False)
    log.info(f"Userbots online: {len(ubot._ubot)}")


async def main():
    await db.connect()
    await bot.start()
    await load_modules()
    await start_userbots()

    me = await bot.get_me()
    await log_event(bot, MSG.log_boot(f"@{me.username}", len(ubot._ubot)))
    log.info(f"Uidol v{__version__} running")

    stop = asyncio.Event()

    def _stop():
        stop.set()

    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(s, _stop)
        except NotImplementedError:
            pass

    await stop.wait()

    for u in list(ubot._ubot):
        try:
            await u.stop()
        except Exception:
            pass
    await bot.stop()
    await db.close()
    log.info("Stopped")


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass
    asyncio.run(main())
