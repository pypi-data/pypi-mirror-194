from __future__ import annotations

import json
from typing import Any, AsyncGenerator, Callable, Optional, cast

from aiohttp import ClientSession

from ..methods import TelegramMethod, TelegramType
from ..telegram import TELEGRAM_SERVER_PRODUCTION, TelegramAPIServer
from ..utils.mixins import ContextInstanceMixin
from .methods import Methods
from .session import Session


class Bot(ContextInstanceMixin["Bot"], Methods):
    def __init__(
        self,
        token: str,
        parse_mode: Optional[str] = None,
        *,
        api: TelegramAPIServer = TELEGRAM_SERVER_PRODUCTION,
        json_loads: Callable[..., Any] = json.loads,
        json_dumps: Callable[..., str] = json.dumps,
        session: Optional[ClientSession] = None,
    ) -> None:
        self.session = Session(
            api=api,
            json_loads=json_loads,
            json_dumps=json_dumps,
            session=session,
        )

        self.token = token
        self.parse_mode = parse_mode

    async def request(
        self, method: TelegramMethod[TelegramType], timeout: Optional[int] = None
    ) -> TelegramType:
        response = await self.session.request(self, method=method, timeout=timeout)
        return cast(TelegramType, response)

    async def stream(
        self, url: str, chunk_size: int, timeout: Optional[int] = None
    ) -> AsyncGenerator[bytes, None, None]:
        async for chunk in self.session.stream(url=url, chunk_size=chunk_size, timeout=timeout):
            yield chunk
