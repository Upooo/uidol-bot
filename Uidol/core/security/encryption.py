"""
Encryption utilities for Uidol.
All sessions are encrypted at rest using Fernet (AES-128-CBC + HMAC).
"""

from cryptography.fernet import Fernet, InvalidToken
from Uidol.config.settings import ENCRYPTION_KEY
from Uidol.core.logger import log


class Encryptor:
    def __init__(self):
        try:
            self.fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)
        except Exception as e:
            log.critical("Invalid ENCRYPTION_KEY. Generate one with Fernet.generate_key()")
            raise RuntimeError("Invalid ENCRYPTION_KEY") from e

    def encrypt(self, data: str) -> str:
        """Encrypt a string and return base64 token."""
        if not data:
            return ""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        """Decrypt a token back to original string."""
        if not token:
            return ""
        try:
            return self.fernet.decrypt(token.encode()).decode()
        except InvalidToken:
            log.error("Failed to decrypt data – wrong key or corrupted token")
            raise ValueError("Decryption failed")


# Global instance
encryptor = Encryptor()
