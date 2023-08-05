from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import AnswerPreCheckoutQuery
    from .order_info import OrderInfo
    from .user import User


class PreCheckoutQuery(TelegramObject):
    id: str
    from_user: User = Field(..., alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None

    def answer(self, ok: bool, error_message: Optional[str] = None) -> AnswerPreCheckoutQuery:
        from ..methods import AnswerPreCheckoutQuery

        return AnswerPreCheckoutQuery(
            pre_checkout_query_id=self.id,
            ok=ok,
            error_message=error_message,
        )
