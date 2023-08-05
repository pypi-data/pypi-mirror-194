from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import InputFile
from .base import Request, TelegramMethod, prepare_file

if TYPE_CHECKING:
    from ..bot import Bot


class SetWebhook(TelegramMethod[bool]):
    __returns__ = bool

    url: str
    certificate: Optional[InputFile] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict(exclude={"certificate"})
        files: Dict[str, InputFile] = {}

        prepare_file(data=data, files=files, name="certificate", value=self.certificate)

        return Request(method="setWebhook", data=data, files=files)
