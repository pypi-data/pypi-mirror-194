from __future__ import annotations

from typing import TYPE_CHECKING

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User


class ProximityAlertTriggered(TelegramObject):
    traveler: User
    watcher: User
    distance: int
