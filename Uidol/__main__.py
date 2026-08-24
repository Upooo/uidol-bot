"""
Uidol entry point.
Run with: python -m Uidol
"""

import asyncio
import signal
from Uidol.core.logger import log
from Uidol.core.database.connection import db
from Uidol.core.clients.bot import Bot
from Uidol.core.clients.manager import manager
from Uidol.core.loader.modules import load_modules


async def shutdown(bot: Bot):
    log.info("Shutting down...")
    await manager.stop_all()
    await bot.stop()
    await db.close()
    log.info("Bye.")


async def main():
    # 1. Connect database
    await db.connect()

    # 2. Create & start management bot
    bot = Bot()
    await bot.start()

    # 3. Load & register modules (auto-discover)
    loaded = load_modules(bot)
    log.info(f"Loaded modules: {loaded}")

    # 4. Start all userbots
    await manager.start_all()

    # 5. Keep running until signal
    stop_event = asyncio.Event()

    def _signal_handler():
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            pass

    log.info("Uidol is running. Press Ctrl+C to stop.")
    await stop_event.wait()

    await shutdown(bot)


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

    asyncio.run(main())
