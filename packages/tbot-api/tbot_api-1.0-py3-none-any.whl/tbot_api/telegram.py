from __future__ import annotations

import abc
import datetime
import json
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from pathlib import Path
from typing import Any, Callable, Union, cast

from aiohttp import FormData
from pydantic import ValidationError

from .exceptions import (
    DecodeError,
    RestartingTelegram,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramConflictError,
    TelegramEntityTooLarge,
    TelegramForbiddenError,
    TelegramMigrateToChat,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
    TelegramUnauthorizedError,
)
from .methods import Request, Response, TelegramMethod, TelegramType


class TelegramNetwork:
    def __init__(
        self,
        json_loads: Callable[..., Any] = json.loads,
        json_dumps: Callable[..., str] = json.dumps,
    ) -> None:
        self.json_loads = json_loads
        self.json_dumps = json_dumps

    def transform_response(
        self,
        method: TelegramMethod[TelegramType],
        status_code: int,
        content: str,
    ) -> Response[TelegramType]:
        try:
            json_data = self.json_loads(content)
        except Exception as e:
            raise DecodeError("Failed to decode object", e, content)

        try:
            response = method.response(json_data)
        except ValidationError as e:
            raise DecodeError("Failed to deserialize object", e, json_data)

        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED and response.ok:
            return response

        description = cast(str, response.description)

        if response.parameters:
            if response.parameters.retry_after:
                raise TelegramRetryAfter(
                    "Exception %s: %s. Retry after %s."
                    % (method, description, response.parameters.retry_after)
                )
            if response.parameters.migrate_to_chat_id:
                raise TelegramMigrateToChat(
                    "Exception %s: %s. Migrate to chat id %s."
                    % (method, description, response.parameters.migrate_to_chat_id)
                )
        if status_code == HTTPStatus.BAD_REQUEST:
            raise TelegramBadRequest(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.NOT_FOUND:
            raise TelegramNotFound(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.CONFLICT:
            raise TelegramConflictError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise TelegramUnauthorizedError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.FORBIDDEN:
            raise TelegramForbiddenError(
                "Exception %s: %s." % (method, description),
            )
        if status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
            raise TelegramEntityTooLarge(
                "Exception %s: %s." % (method, description),
            )
        if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            if "restart" in description:
                raise RestartingTelegram(
                    "Exception %s: %s." % (method, description),
                )
            raise TelegramServerError(
                "Exception %s: %s." % (method, description),
            )

        raise TelegramAPIError(
            "Exception %s: %s." % (method, description),
        )

    def _prepare_value(self, value: Any) -> Union[str, int, bool]:
        if isinstance(value, str):
            return value
        if isinstance(value, (list, dict)):
            return self.json_dumps(self._clean_json(value))
        if isinstance(value, datetime.timedelta):
            now = datetime.datetime.now()
            return str(round((now + value).timestamp()))
        if isinstance(value, datetime.datetime):
            return str(round(value.timestamp()))
        if isinstance(value, Enum):
            return self._prepare_value(value.value)
        return str(value)

    def _clean_json(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self._clean_json(v) for v in value if v is not None]
        if isinstance(value, dict):
            return {k: self._clean_json(v) for k, v in value.items() if v is not None}
        return value

    def build_data(self, request: Request) -> FormData:
        form = FormData(quote_fields=False)
        for key, value in request.data.items():
            if value is not None:
                form.add_field(key, self._prepare_value(value))
        if request.files:
            for key, value in request.files.items():
                form.add_field(key, value, filename=value.filename or key)
        return form


class _ABCFilesPathWrapper(abc.ABC):
    @abc.abstractmethod
    def to_local(self, path: Union[Path, str]) -> Union[Path, str]:
        ...

    @abc.abstractmethod
    def to_server(self, path: Union[Path, str]) -> Union[Path, str]:
        ...


class FilesPathWrapper(_ABCFilesPathWrapper):
    def to_local(self, path: Union[Path, str]) -> Union[Path, str]:
        return path

    def to_server(self, path: Union[Path, str]) -> Union[Path, str]:
        return path


@dataclass(frozen=True)
class TelegramAPIServer:
    base: str
    file: str
    is_local: bool = False
    wrap_local_file: _ABCFilesPathWrapper = FilesPathWrapper()

    def api_url(self, token: str, method: str) -> str:
        return self.base.format(token=token, method=method)

    def file_url(self, token: str, path: str) -> str:
        return self.file.format(token=token, path=path)

    @classmethod
    def from_base(cls, base: str, **kwargs: Any) -> TelegramAPIServer:
        base = base.rstrip("/")
        return cls(
            base=f"{base}/bot{{token}}/{{method}}",
            file=f"{base}/file/bot{{token}}/{{path}}",
            **kwargs,
        )


TELEGRAM_SERVER_PRODUCTION = TelegramAPIServer(
    base="https://api.telegram.org/bot{token}/{method}",
    file="https://api.telegram.org/file/bot{token}/{path}",
)
