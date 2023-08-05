from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .base import TelegramObject

if TYPE_CHECKING:
    from .order_info import OrderInfo


class SuccessfulPayment(TelegramObject):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
