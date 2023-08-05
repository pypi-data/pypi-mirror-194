from __future__ import annotations

import io
from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncGenerator, Optional, Union

import aiofiles

from .base import TelegramObject

DEFAULT_CHUNK_SIZE = 64 * 1024


class _AIterSupport:
    async def __aiter__(self) -> AsyncGenerator[bytes]:
        async for chunk in self.read():  # noqa
            yield chunk


class InputFile(ABC, TelegramObject, _AIterSupport):
    chunk_size: int = DEFAULT_CHUNK_SIZE
    filename: Optional[str] = None

    @abstractmethod
    async def read(self) -> AsyncGenerator[bytes, ...]:
        ...


class FileSystemInputFile(InputFile):
    path: Union[str, Path]

    async def read(self) -> AsyncGenerator[bytes, ...]:
        async with aiofiles.open(self.path, "rb") as file:
            while chunk := await file.read(self.chunk_size):
                yield chunk


class BufferedInputFile(InputFile):
    data: bytes

    async def read(self) -> AsyncGenerator[bytes, None]:
        buffer = io.BytesIO(self.data)
        while chunk := buffer.read(self.chunk_size):
            yield chunk


class URLInputFile(InputFile):
    url: str
    timeout: int = 30

    async def read(self) -> AsyncGenerator[bytes, ...]:
        from ..bot import Bot

        bot = Bot.get_current()

        async for chunk in bot.stream(
            url=self.url, chunk_size=self.chunk_size, timeout=self.timeout
        ):
            yield chunk
