from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from ..methods import AnswerInlineQuery
    from .inline_query_result import InlineQueryResult
    from .location import Location
    from .user import User


class InlineQuery(TelegramObject):
    id: str
    from_user: User = Field(..., alias="from")
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None

    def answer(
        self,
        results: List[InlineQueryResult],
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        switch_pm_text: Optional[str] = None,
        switch_pm_parameter: Optional[str] = None,
        **kwargs: Dict,
    ) -> AnswerInlineQuery:
        from ..methods import AnswerInlineQuery

        return AnswerInlineQuery(
            inline_query_id=self.id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
            **kwargs,
        )
