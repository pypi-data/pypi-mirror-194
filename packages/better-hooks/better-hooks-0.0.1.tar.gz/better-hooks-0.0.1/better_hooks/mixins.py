from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from copy import copy
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import Any, ParamSpec, Self, TypeVar, cast, final

from better_hooks.utils import is_coroutine_function

P = ParamSpec("P")
R = TypeVar("R")


class DecoratorMixin(ABC):
    @abstractmethod
    def _wrapper_sync(
        self,
        origin: Callable[P, R],
        /,
        *origin_args: P.args,
        **origin_kwargs: P.kwargs,
    ) -> R:
        """Wrap the callable."""

    async def _wrapper_async(
        self,
        origin: Callable[P, Awaitable[R]],
        /,
        *origin_args: P.args,
        **origin_kwargs: P.kwargs,
    ) -> R:
        """Wrap the callable."""
        return await self._wrapper_sync(origin, *origin_args, **origin_kwargs)

    @final
    def __call__(self, origin: Callable[P, R]) -> Callable[P, R]:
        if is_coroutine_function(origin):
            wrapper = wraps(origin)(
                partial(
                    self._wrapper_async,
                    origin,  # pyright: ignore[reportGeneralTypeIssues]
                ),
            )
        else:
            wrapper = wraps(origin)(partial(self._wrapper_sync, origin))

        return cast(Callable[P, R], wrapper)


class DecoratorAsContextManagerMixin(DecoratorMixin):
    @abstractmethod
    def __enter__(self) -> Any:
        ...

    @abstractmethod
    def __exit__(self, *_: Any) -> None:
        ...

    def _wrapper_sync(
        self,
        origin: Callable[P, R],
        /,
        *origin_args: P.args,
        **origin_kwargs: P.kwargs,
    ) -> R:
        with self:
            return origin(*origin_args, **origin_kwargs)

    async def _wrapper_async(
        self,
        origin: Callable[P, Awaitable[R]],
        /,
        *origin_args: P.args,
        **origin_kwargs: P.kwargs,
    ) -> R:
        with self:
            return await origin(*origin_args, **origin_kwargs)


@dataclass
class InvertedMixin:
    inverted: bool = field(compare=False, default=False)

    def __invert__(self) -> Self:
        copied = copy(self)
        copied.inverted = not copied.inverted
        return copied
