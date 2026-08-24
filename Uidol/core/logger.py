"""
Uidol Logger
Safe logging that never leaks sessions or secrets.
"""

import logging
import re
import sys
from Uidol.config.settings import LOG_LEVEL


# Patterns that must never appear in logs
SENSITIVE_PATTERNS = [
    re.compile(r"1[0-9A-Za-z]{50,}"),          # rough session-like strings
    re.compile(r"BAA[0-9A-Za-z_\-]{20,}"),     # common pyro session prefix
    re.compile(r"session[_-]?string", re.I),
]


class SensitiveFilter(logging.Filter):
    """Filter out any log record that might contain session data."""

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

    # Quiet noisy libraries
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.session").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logger


log = setup_logger()
