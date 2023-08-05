from __future__ import annotations

from .base import TelegramObject


class EncryptedCredentials(TelegramObject):
    data: str
    hash: str
    secret: str
