from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, AsyncGenerator, Callable, Final, Optional, cast

from aiohttp import ClientError, ClientSession

from ..exceptions import TelegramNetworkError
from ..methods import TelegramMethod, TelegramType
from ..telegram import TELEGRAM_SERVER_PRODUCTION, TelegramAPIServer, TelegramNetwork

if TYPE_CHECKING:
    from .bot import Bot

_REQUEST_TIMEOUT: Final[int] = 60


class Session:
    def __init__(
        self,
        *,
        api: TelegramAPIServer = TELEGRAM_SERVER_PRODUCTION,
        json_loads: Callable[..., Any] = json.loads,
        json_dumps: Callable[..., str] = json.dumps,
        session: Optional[ClientSession] = None,
    ) -> None:
        self.api = api
        self.telegram_network = TelegramNetwork(json_loads=json_loads, json_dumps=json_dumps)
        self._session: Optional[ClientSession] = None if session is None else session
        self._should_reset_session = True if self._session is None else False

    async def create(self) -> None:
        if self._should_reset_session:
            await self.close()
        if self._session is None or self._session.closed:
            self._session = ClientSession()
            self._should_reset_session = False

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def request(
        self, bot: Bot, method: TelegramMethod[TelegramType], timeout: Optional[int] = None
    ) -> TelegramType:
        timeout = _REQUEST_TIMEOUT if timeout is None else timeout

        await self.create()

        request = method.request(bot)
        url = self.api.api_url(bot.token, request.method)
        data = self.telegram_network.build_data(request)

        try:
            async with self._session.post(url, data=data, timeout=timeout) as response:
                content = await response.text()
        except asyncio.TimeoutError:
            raise TelegramNetworkError("Exception %s: %s." % (method, "request timeout error"))
        except ClientError as e:
            raise TelegramNetworkError(
                "Exception for method %s: %s." % (method, f"{type(e).__name__}: {e}")
            )
        response = self.telegram_network.transform_response(
            method=method, status_code=response.status, content=content
        )
        return cast(TelegramType, response.result)

    async def stream(
        self, url: str, chunk_size: int, timeout: Optional[int] = None
    ) -> AsyncGenerator[bytes, None, None]:
        timeout = _REQUEST_TIMEOUT if timeout is None else timeout

        await self.create()

        async with self._session.get(url, timeout=timeout) as response:
            async for chunk in response.content.iter_chunked(chunk_size):
                yield chunk
