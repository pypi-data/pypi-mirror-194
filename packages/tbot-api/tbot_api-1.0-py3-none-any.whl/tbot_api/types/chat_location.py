from __future__ import annotations

from typing import TYPE_CHECKING

from .base import TelegramObject

if TYPE_CHECKING:
    from .location import Location


class ChatLocation(TelegramObject):
    location: Location
    address: str
