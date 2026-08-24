"""
Uidol entry point.
Run: python -m Uidol  |  bash start.sh
"""

import asyncio
import signal
import time

from Uidol.core.logger import log, bind_bot, log_event
from Uidol.core.database.connection import db
from Uidol.core.clients.bot import Bot
from Uidol.core.clients.manager import manager
from Uidol.core.loader.modules import load_modules, get_userbot_register_hook


async def shutdown(bot: Bot):
    log.info("Shutting down...")
    await manager.stop_all()
    await bot.stop()
    await db.close()
    log.info("Bye.")


async def main():
    await db.connect()

    bot = Bot()
    await bot.start()
    bind_bot(bot)

    # Load bot modules
    loaded = load_modules(bot)
    log.info(f"Loaded modules: {loaded}")

    # Userbot modules hook
    manager.on_userbot_start(get_userbot_register_hook())

    # Start all saved userbots
    await manager.start_all()

    me = await bot.get_me()
    await log_event(
        f"🚀 **Uidol started**\n"
        f"Bot: @{me.username}\n"
        f"Userbots online: `{manager.count}`"
    )

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
