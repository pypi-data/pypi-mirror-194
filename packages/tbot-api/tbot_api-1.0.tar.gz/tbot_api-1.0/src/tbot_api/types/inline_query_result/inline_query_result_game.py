from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from ...enums import InlineQueryResultType
from .inline_query_result import InlineQueryResult

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultGame(InlineQueryResult):
    type: str = Field(InlineQueryResultType.GAME, const=True)
    id: str
    game_short_name: str
    reply_markup: Optional[InlineKeyboardMarkup] = None
