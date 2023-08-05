from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import ChatAdministratorRights
from .base import Request, TelegramMethod

if TYPE_CHECKING:
    from ..bot import Bot


class GetMyDefaultAdministratorRights(TelegramMethod[ChatAdministratorRights]):
    __returns__ = ChatAdministratorRights

    for_channels: Optional[bool] = None

    def request(self, bot: Bot) -> Request:
        data: Dict[str, Any] = self.dict()

        return Request(method="getMyDefaultAdministratorRights", data=data)
