from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import InlineKeyboardMarkup, InputFile, InputMedia, Message
from .base import Request, TelegramMethod, prepare_media_file, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class EditMessageMedia(TelegramMethod[Union[bool, Message]]):
    __returns__ = Union[bool, Message]

    media: InputMedia
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()
        files: Dict[str, InputFile] = {}

        prepare_parse_mode(bot, data["media"])
        prepare_media_file(data=data, files=files)

        return Request(method="editMessageMedia", data=data, files=files)
