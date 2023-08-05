from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import TelegramObject

if TYPE_CHECKING:
    from .encrypted_credentials import EncryptedCredentials
    from .encrypted_passport_element import EncryptedPassportElement


class PassportData(TelegramObject):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials
