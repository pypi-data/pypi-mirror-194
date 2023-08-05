from __future__ import annotations

from typing import Optional

from .base import TelegramObject


class Contact(TelegramObject):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None
