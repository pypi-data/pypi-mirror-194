import datetime
from enum import Enum
from typing import Any, Type

import pytest

from tbot_api.exceptions import (
    DecodeError,
    RestartingTelegram,
    TAPIError,
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
from tbot_api.methods import GetUpdates, Request
from tbot_api.telegram import TelegramNetwork
from tbot_api.types import FileSystemInputFile


@pytest.mark.parametrize(
    "status_code,content,error",
    [
        (200, '{"ok":true,"result":[]}', None),
        (400, '{"ok":false,"description":"test"}', TelegramBadRequest),
        (
            400,
            '{"ok":false,"description":"test", "parameters": {"retry_after": 1}}',
            TelegramRetryAfter,
        ),
        (
            400,
            '{"ok":false,"description":"test", "parameters": {"migrate_to_chat_id": -42}}',
            TelegramMigrateToChat,
        ),
        (404, '{"ok":false,"description":"test"}', TelegramNotFound),
        (401, '{"ok":false,"description":"test"}', TelegramUnauthorizedError),
        (403, '{"ok":false,"description":"test"}', TelegramForbiddenError),
        (409, '{"ok":false,"description":"test"}', TelegramConflictError),
        (413, '{"ok":false,"description":"test"}', TelegramEntityTooLarge),
        (500, '{"ok":false,"description":"restarting"}', RestartingTelegram),
        (500, '{"ok":false,"description":"test"}', TelegramServerError),
        (502, '{"ok":false,"description":"test"}', TelegramServerError),
        (499, '{"ok":false,"description":"test"}', TelegramAPIError),
        (499, '{"ok":false,"description":"test"}', TelegramAPIError),
        (200, '{"this": "is_not_a_valid_json', DecodeError),
        (201, '{"ok": "ok"}', DecodeError),
    ],
)
def test_transform_response(status_code: int, content: str, error: Type[TAPIError]) -> None:
    telegram_network = TelegramNetwork()
    method = GetUpdates()
    if error is None:
        telegram_network.transform_response(
            method=method,
            status_code=status_code,
            content=content,
        )
    else:
        with pytest.raises(error):
            telegram_network.transform_response(
                method=method,
                status_code=status_code,
                content=content,
            )


def test_build_form_data_with_data_only() -> None:
    request = Request(
        method="method",
        data={
            "str": "value",
            "int": 42,
            "bool": True,
            "null": None,
            "list": ["foo"],
            "dict": {"hello": "python"},
        },
    )

    telegram_network = TelegramNetwork()
    form = telegram_network.build_data(request)

    fields = form._fields
    assert len(fields) == 5
    assert all(isinstance(field[2], str) for field in fields)
    assert "null" not in [item[0]["name"] for item in fields]


def test_build_form_data_with_files() -> None:
    request = Request(
        method="method",
        data={"key": "value"},
        files={"document": FileSystemInputFile(path=__file__, filename="hello.py")},
    )

    telegram_network = TelegramNetwork()
    form = telegram_network.build_data(request)

    fields = form._fields

    assert len(fields) == 2
    assert fields[1][0]["name"] == "document"
    assert fields[1][0]["filename"] == "hello.py"
    assert isinstance(fields[1][2], FileSystemInputFile)


class EnumInt(int, Enum):
    value = 1


class EnumStr(str, Enum):
    value = "str"


@pytest.mark.parametrize(
    "to_prepare,prepared",
    [
        ("hello", "hello"),
        ([1, 2], "[1, 2]"),
        ([1, {"hello": "python"}, 3], '[1, {"hello": "python"}, 3]'),
        (
            [1, {"hello": "python", "list": [1, {"hello": "python", "list": [1, 2, 3]}]}],
            '[1, {"hello": "python", "list": [1, {"hello": "python", "list": [1, 2, 3]}]}]',
        ),
        ({"hello": "python"}, '{"hello": "python"}'),
        ({"hello": "python", "list": [1, 2]}, '{"hello": "python", "list": [1, 2]}'),
        (datetime.timedelta(minutes=2), "skip"),
        (now := datetime.datetime.now(), str(round(now.timestamp()))),
        (EnumInt.value, "1"),
        (EnumStr.value, "str"),
    ],
)
def test_prepare_value(to_prepare: Any, prepared: str) -> None:
    telegram_network = TelegramNetwork()
    if isinstance(to_prepare, datetime.timedelta):
        assert isinstance(telegram_network._prepare_value(to_prepare), str)
    else:
        assert telegram_network._prepare_value(to_prepare) == prepared


@pytest.mark.parametrize(
    "to_clean,cleaned",
    [
        ({"hello": "python", "some": "value", "none": None}, {"hello": "python", "some": "value"}),
        (
            ["hello", None, "python", {"hello": "python", "none": None}],
            ["hello", "python", {"hello": "python"}],
        ),
    ],
)
def test_clean_json(to_clean: Any, cleaned: Any) -> None:
    telegram_network = TelegramNetwork()
    assert telegram_network._clean_json(to_clean) == cleaned
