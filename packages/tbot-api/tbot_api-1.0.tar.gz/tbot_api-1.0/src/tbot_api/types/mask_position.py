from __future__ import annotations

from .base import TelegramObject


class MaskPosition(TelegramObject):
    point: str
    x_shift: float
    y_shift: float
    scale: float
