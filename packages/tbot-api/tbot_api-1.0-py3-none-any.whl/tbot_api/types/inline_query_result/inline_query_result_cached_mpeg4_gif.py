from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from ...enums import InlineQueryResultType
from .inline_query_result import InlineQueryResult

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..input_message_content import InputMessageContent
    from ..message_entity import MessageEntity


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    type: str = Field(InlineQueryResultType.MPEG, const=True)
    id: str
    mpeg4_file_id: str
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
