from __future__ import annotations

from .base import TelegramObject


class ShippingAddress(TelegramObject):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
