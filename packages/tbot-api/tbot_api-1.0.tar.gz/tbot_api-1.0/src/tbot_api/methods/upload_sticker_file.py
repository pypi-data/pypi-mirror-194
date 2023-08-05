from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import File, InputFile
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class UploadStickerFile(TelegramMethod[File]):
    __returns__ = File

    user_id: int
    png_sticker: InputFile

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"png_sticker"})
        files: Dict[str, InputFile] = {}

        prepare_file(data=data, files=files, name="png_sticker", value=self.png_sticker)

        return Request(method="uploadStickerFile", data=data, files=files)
