from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..types import File
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetFile(TelegramMethod[File]):
    __returns__ = File

    file_id: str

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getFile", data=data)
