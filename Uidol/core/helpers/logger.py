"""Send events to LOG_GROUP_ID."""

from Uidol.config import LOG_GROUP_ID


async def log_event(bot, text: str):
    if not LOG_GROUP_ID:
        return
    try:
        await bot.send_message(LOG_GROUP_ID, text, disable_web_page_preview=True)
    except Exception as e:
        print(f"[LOG] failed: {e}")
