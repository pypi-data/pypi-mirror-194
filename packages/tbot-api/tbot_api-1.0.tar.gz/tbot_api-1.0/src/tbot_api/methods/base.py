from __future__ import annotations

import abc
import secrets
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseConfig, BaseModel, Extra
from pydantic.generics import GenericModel

from ..types import InputFile, ResponseParameters
from ..utils.mixins import ModelExcludesNoneMixin

if TYPE_CHECKING:
    from ..bot import Bot

TelegramType = TypeVar("TelegramType", bound=Any)


class Request(BaseModel, ModelExcludesNoneMixin):
    method: str

    data: Dict[str, Any]
    files: Optional[Dict[str, InputFile]]

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class Response(ModelExcludesNoneMixin, GenericModel, Generic[TelegramType]):
    ok: bool
    result: Optional[TelegramType] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[ResponseParameters] = None


class TelegramMethod(ABC, ModelExcludesNoneMixin, BaseModel, Generic[TelegramType]):
    class Config(BaseConfig):
        extra = Extra.allow
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        smart_union = True

    @property
    @abc.abstractmethod
    def __returns__(self) -> ...:
        ...

    @abstractmethod
    def request(self, bot: Bot) -> Request:  # pragma: no cover
        ...

    def response(self, data: Dict[str, Any]) -> Response[TelegramType]:
        return Response[self.__returns__].parse_obj(data)

    def __await__(self) -> Response[TelegramType]:
        from ..bot import Bot

        bot = Bot.get_current()
        return bot.request(self).__await__()


def prepare_file(
    name: str,
    value: Any,
    data: Dict[str, Any],
    files: Dict[str, Any],
) -> None:
    if not value:
        return
    if name == "thumb":
        tag = secrets.token_urlsafe(10)
        files[tag] = value
        data["thumb"] = f"attach://{tag}"
    elif isinstance(value, InputFile):
        files[name] = value
    else:
        data[name] = value


def prepare_input_media(data: Dict[str, Any], files: Dict[str, InputFile]) -> None:
    for input_media in data.get("media", []):
        if (
            "media" in input_media
            and input_media["media"]
            and isinstance(input_media["media"], InputFile)
        ):
            tag = secrets.token_urlsafe(10)
            files[tag] = input_media.pop("media")
            input_media["media"] = f"attach://{tag}"


def prepare_media_file(data: Dict[str, Any], files: Dict[str, InputFile]) -> None:
    if (
        data["media"]
        and "media" in data["media"]
        and isinstance(data["media"]["media"], InputFile)
    ):
        tag = secrets.token_urlsafe(10)
        files[tag] = data["media"].pop("media")
        data["media"]["media"] = f"attach://{tag}"


def prepare_parse_mode(
    bot: Bot,
    root: Any,
    parse_mode_property: str = "parse_mode",
    entities_property: str = "entities",
) -> None:
    if isinstance(root, list):
        for item in root:
            prepare_parse_mode(
                bot=bot,
                root=item,
                parse_mode_property=parse_mode_property,
                entities_property=entities_property,
            )
    elif root.get(parse_mode_property) is None:
        if bot.parse_mode and root.get(entities_property, None) is None:
            root[parse_mode_property] = bot.parse_mode
        else:
            root[parse_mode_property] = None
