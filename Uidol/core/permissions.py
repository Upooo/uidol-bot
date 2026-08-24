"""
Permission helpers and decorators for Uidol.
"""

from functools import wraps
from typing import Callable, Any
from pyrogram.types import Message
from Uidol.config.settings import is_owner, is_sudo
from Uidol.core.handlers.messages import get_message


def owner_only(func: Callable) -> Callable:
    """Only OWNER_ID can run this handler."""

    @wraps(func)
    async def wrapper(client: Any, message: Message, *args, **kwargs):
        if not message.from_user or not is_owner(message.from_user.id):
            await message.reply_text(get_message("owner_only", lang="id"))
            return None
        return await func(client, message, *args, **kwargs)

    return wrapper


def sudo_only(func: Callable) -> Callable:
    """OWNER or SUDO_USERS can run this handler."""

    @wraps(func)
    async def wrapper(client: Any, message: Message, *args, **kwargs):
        if not message.from_user or not is_sudo(message.from_user.id):
            await message.reply_text(get_message("owner_only", lang="id"))
            return None
        return await func(client, message, *args, **kwargs)

    return wrapper
