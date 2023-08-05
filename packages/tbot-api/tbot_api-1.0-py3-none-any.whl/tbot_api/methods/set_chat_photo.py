from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union

from ..types import InputFile
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class SetChatPhoto(TelegramMethod[bool]):
    __returns__ = bool

    chat_id: Union[int, str]
    photo: InputFile

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"photo"})
        files: Dict[str, InputFile] = {}

        prepare_file(data=data, files=files, name="photo", value=self.photo)

        return Request(method="setChatPhoto", data=data, files=files)
