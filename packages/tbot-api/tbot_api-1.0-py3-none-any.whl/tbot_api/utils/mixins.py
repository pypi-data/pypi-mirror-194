from __future__ import annotations

import contextvars
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Generic,
    Mapping,
    Optional,
    TypeVar,
    Union,
)


class ModelExcludesNoneMixin:
    def dict(
        self,
        *,
        include: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        exclude: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        exclude_none = True

        return super(ModelExcludesNoneMixin, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def json(
        self,
        *,
        include: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        exclude: Optional[
            Union[
                AbstractSet[Union[int, str]],
                Mapping[Union[int, str], Any],
            ]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        exclude_none = True

        return super(ModelExcludesNoneMixin, self).json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs,
        )


ContextInstance = TypeVar("ContextInstance")


class ContextInstanceMixin(Generic[ContextInstance]):
    _context_instance: contextvars.ContextVar[ContextInstance]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super(ContextInstanceMixin, cls).__init_subclass__()

        cls._context_instance = contextvars.ContextVar(f"instance_{cls.__name__}")

    @classmethod
    def get_current(cls, no_error: bool = True) -> Optional[ContextInstance]:  # pragma: no cover
        try:
            current: Optional[ContextInstance] = cls._context_instance.get()
        except LookupError:
            if not no_error:
                raise
            current = None

        return current

    @classmethod
    def set_current(cls, value: ContextInstance) -> contextvars.Token[ContextInstance]:
        return cls._context_instance.set(value)

    @classmethod
    def reset_current(cls, token: contextvars.Token[ContextInstance]) -> None:
        cls._context_instance.reset(token)
