from __future__ import annotations

from collections.abc import Callable, Sequence
from copy import copy
from dataclasses import dataclass
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar

from better_hooks.context.mixins import ScopedHooksContextManagerMixin
from better_hooks.hooks import BaseHook, ScopedHook
from better_hooks.mixins import (
    DecoratorAsContextManagerMixin,
    DecoratorMixin,
    P,
    R,
)
from better_hooks.stack import HookStack, Popable

if TYPE_CHECKING:
    from better_hooks.context.types import ScopedHooksToken


F = TypeVar("F", bound=Callable[..., Any])


@dataclass(slots=True)
class BaseHooksGroup(DecoratorMixin):
    hooks: Popable[BaseHook]

    def _wrapper_sync(
        self,
        callable_: Callable[P, R],
        /,
        *callable_args: P.args,
        **callable_kwargs: P.kwargs,
    ) -> R:
        hooks_stack = HookStack(stack=copy(self.hooks), origin=callable_)
        return hooks_stack.call(*callable_args, **callable_kwargs)


@dataclass(slots=True)
class ScopedHooksGroup(
    ScopedHooksContextManagerMixin,
    DecoratorAsContextManagerMixin,
):
    """Wrapper for a sequence of hooks to use as a context manager or decorator."""

    hooks: Sequence[ScopedHook]

    def _update_current_hooks(self) -> ScopedHooksToken:
        return self._scoped_hooks_manager.extend(self.hooks)


def with_hooks(*hooks: BaseHook) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Create groups and apply them to the function using a decorator."""
    scoped_hooks = tuple(hook for hook in hooks if isinstance(hook, ScopedHook))
    base_hooks = [hook for hook in hooks if not isinstance(hook, ScopedHook)]

    scoped_hooks_group = ScopedHooksGroup(scoped_hooks)
    base_hooks_group = BaseHooksGroup(base_hooks)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        decorated_func = scoped_hooks_group(base_hooks_group(func))
        return wraps(func)(decorated_func)

    return decorator
