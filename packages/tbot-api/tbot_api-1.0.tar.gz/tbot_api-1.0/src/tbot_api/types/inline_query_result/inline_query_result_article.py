from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from ...enums import InlineQueryResultType
from .inline_query_result import InlineQueryResult

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..input_message_content import InputMessageContent


class InlineQueryResultArticle(InlineQueryResult):
    type: str = Field(InlineQueryResultType.ARTICLE, const=True)
    id: str
    title: str
    input_message_content: InputMessageContent
    reply_markup: Optional[InlineKeyboardMarkup] = None
    url: Optional[str] = None
    hide_url: Optional[bool] = None
    description: Optional[str] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None
