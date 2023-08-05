from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from better_hooks.context.mixins import ScopedHooksContextManagerMixin
from better_hooks.mixins import (
    DecoratorAsContextManagerMixin,
    DecoratorMixin,
    InvertedMixin,
    P,
    R,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from better_hooks.context.types import ScopedHooksToken
    from better_hooks.scope import Scope
    from better_hooks.types import AnyCallable


@dataclass(kw_only=True)
class BaseHook(DecoratorMixin, InvertedMixin, ABC):
    inverted: bool = field(compare=False, default=False)

    @abstractmethod
    def call(
        self,
        call_next: AnyCallable,
        *call_next_args: Any,
        **call_next_kwargs: Any,
    ) -> Any:
        """Call the hook.

        This method should be overridden by subclasses.
        """

    def _wrapper_sync(
        self,
        origin: Callable[P, R],
        /,
        *origin_args: P.args,
        **origin_kwargs: P.kwargs,
    ) -> R:
        return self.call(origin, *origin_args, **origin_kwargs)


@dataclass(kw_only=True, eq=False)
class ScopedHook(
    ScopedHooksContextManagerMixin,
    DecoratorAsContextManagerMixin,
    BaseHook,
    ABC,
):
    scope: Scope

    def _update_current_hooks(self) -> ScopedHooksToken:
        return self._scoped_hooks_manager.append(self)
