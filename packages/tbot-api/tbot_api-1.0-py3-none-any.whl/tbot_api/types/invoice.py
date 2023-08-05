from __future__ import annotations

from .base import TelegramObject


class Invoice(TelegramObject):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int
