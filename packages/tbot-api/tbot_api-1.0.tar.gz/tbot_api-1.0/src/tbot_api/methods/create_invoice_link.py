from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import LabeledPrice
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class CreateInvoiceLink(TelegramMethod[str]):
    __returns__ = str

    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: List[LabeledPrice]
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="createInvoiceLink", data=data)
