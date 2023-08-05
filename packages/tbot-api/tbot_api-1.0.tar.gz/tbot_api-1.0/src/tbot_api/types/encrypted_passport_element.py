from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .passport_file import PassportFile


class EncryptedPassportElement(TelegramObject):
    type: str
    hash: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[List[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[List[PassportFile]] = None
