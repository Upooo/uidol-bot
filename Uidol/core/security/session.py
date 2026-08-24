"""
Secure Session handling for Uidol.
Sessions are never stored in plain text.
"""

from typing import Optional
from Uidol.core.security.encryption import encryptor
from Uidol.core.logger import log


def protect_session(session_string: str) -> str:
    """Encrypt a session string before storing."""
    if not session_string:
        return ""
    return encryptor.encrypt(session_string)


def reveal_session(encrypted: str) -> Optional[str]:
    """
    Decrypt a session string.
    Only call this when you really need the plain session (in memory only).
    """
    if not encrypted:
        return None
    try:
        return encryptor.decrypt(encrypted)
    except Exception as e:
        log.error(f"Cannot reveal session: {e}")
        return None
