from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .input_message_content import InputMessageContent

if TYPE_CHECKING:
    from ..message_entity import MessageEntity


class InputTextMessageContent(InputMessageContent):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None
