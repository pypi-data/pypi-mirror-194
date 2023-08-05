from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import (
    InputFile,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from .base import Request, TelegramMethod, prepare_input_media, prepare_parse_mode

if TYPE_CHECKING:
    from ..bot import Bot


class SendMediaGroup(TelegramMethod[List[Message]]):
    __returns__ = List[Message]

    chat_id: Union[int, str]
    media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]
    message_thread_id: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()
        prepare_parse_mode(bot, data["media"])

        files: Dict[str, InputFile] = {}
        prepare_input_media(data, files)

        return Request(method="sendMediaGroup", data=data, files=files)
