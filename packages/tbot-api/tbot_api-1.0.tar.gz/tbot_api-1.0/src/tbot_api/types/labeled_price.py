from __future__ import annotations

from .base import MutableTelegramObject


class LabeledPrice(MutableTelegramObject):
    label: str
    amount: int
