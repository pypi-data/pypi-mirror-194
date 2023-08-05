from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import AnswerCallbackQuery
    from .message import Message
    from .user import User


class CallbackQuery(TelegramObject):
    id: str
    from_user: User = Field(..., alias="from")
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    def answer(
        self,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
        **kwargs: Dict,
    ) -> AnswerCallbackQuery:
        from ..methods import AnswerCallbackQuery

        return AnswerCallbackQuery(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
            **kwargs,
        )
