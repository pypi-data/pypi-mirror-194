from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base import TelegramObject

if TYPE_CHECKING:
    from .labeled_price import LabeledPrice


class ShippingOption(TelegramObject):
    id: str
    title: str
    prices: List[LabeledPrice]
