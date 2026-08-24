"""
Uidol Logger
- Safe console logging (never leaks sessions)
- Optional event logging to Telegram LOG_GROUP
"""

import logging
import re
import sys
from typing import Optional
from Uidol.config.settings import LOG_LEVEL, LOG_GROUP_ID


SENSITIVE_PATTERNS = [
    re.compile(r"1[0-9A-Za-z]{50,}"),
    re.compile(r"BAA[0-9A-Za-z_\-]{20,}"),
    re.compile(r"session[_-]?string", re.I),
    re.compile(r"[0-9]{8,15}:[A-Za-z0-9_-]{30,}"),
]


class SensitiveFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(msg):
                record.msg = "[FILTERED - possible sensitive data]"
                record.args = ()
                break
        return True


def setup_logger(name: str = "Uidol") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)-7s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        handler.addFilter(SensitiveFilter())
        logger.addHandler(handler)

    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.session").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logger


log = setup_logger()
_bot_ref = None


def bind_bot(bot) -> None:
    global _bot_ref
    _bot_ref = bot


async def log_event(text: str, disable_preview: bool = True) -> None:
    if not LOG_GROUP_ID or not _bot_ref:
        return
    try:
        await _bot_ref.send_message(
            LOG_GROUP_ID,
            text,
            disable_web_page_preview=disable_preview,
        )
    except Exception as e:
        log.warning(f"Failed to send log event: {e}")
