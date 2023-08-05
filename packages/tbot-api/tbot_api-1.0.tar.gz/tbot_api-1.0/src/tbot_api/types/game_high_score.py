from __future__ import annotations

from typing import TYPE_CHECKING

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User


class GameHighScore(TelegramObject):
    position: int
    user: User
    score: int
