"""Session encryption — Fernet at rest. Plain only in memory."""

from cryptography.fernet import Fernet, InvalidToken
from Uidol.config import ENCRYPTION_KEY


class Encryptor:
    def __init__(self):
        key = ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY
        self._f = Fernet(key)

    def encrypt(self, data: str) -> str:
        if not data:
            return ""
        return self._f.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        if not token:
            return ""
        try:
            return self._f.decrypt(token.encode()).decode()
        except InvalidToken as e:
            raise ValueError("Decryption failed") from e


encryptor = Encryptor()


def protect(session: str) -> str:
    return encryptor.encrypt(session)


def reveal(token: str) -> str:
    return encryptor.decrypt(token)
