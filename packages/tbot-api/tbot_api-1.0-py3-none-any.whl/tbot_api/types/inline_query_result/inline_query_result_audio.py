from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from ...enums import InlineQueryResultType
from .inline_query_result import InlineQueryResult

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..input_message_content import InputMessageContent
    from ..message_entity import MessageEntity


class InlineQueryResultAudio(InlineQueryResult):
    type: str = Field(InlineQueryResultType.AUDIO, const=True)
    id: str
    audio_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    performer: Optional[str] = None
    audio_duration: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
