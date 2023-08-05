from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import AnswerShippingQuery
    from .shipping_address import ShippingAddress
    from .shipping_option import ShippingOption
    from .user import User


class ShippingQuery(TelegramObject):
    id: str
    from_user: User = Field(..., alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress

    def answer(
        self,
        ok: bool,
        shipping_options: Optional[List[ShippingOption]] = None,
        error_message: Optional[str] = None,
    ) -> AnswerShippingQuery:
        from ..methods import AnswerShippingQuery

        return AnswerShippingQuery(
            shipping_query_id=self.id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )
