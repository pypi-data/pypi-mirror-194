from __future__ import annotations

import logging
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from typing import TYPE_CHECKING, Any, Protocol, cast

from better_hooks.context.manager import CONTEXT_HOOKS_MANAGER
from better_hooks.stack import HookStack

if TYPE_CHECKING:
    from types import ModuleType

    from better_hooks.types import AnyCallable


logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Scope:
    namespace: ModuleType | dict[str, Any] | Any
    """The namespace of the `self.callable_`"""
    callable_: AnyCallable
    """The scope."""

    def __post_init__(self) -> None:
        modify_scope(self)

    def __hash__(self) -> int:
        return hash(self.callable_)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Scope):
            return False

        self_callable = getattr(self.callable_, "origin", self.callable_)
        other_callable = getattr(other.callable_, "origin", other.callable_)

        return (
            self.namespace is other.namespace
            and self_callable is other_callable
        )


class _Wrapper(Protocol):
    origin: AnyCallable
    __call__: AnyCallable


def _get_wrapper(origin: AnyCallable, scope: Scope) -> _Wrapper:
    @wraps(origin)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug("Entering the scope: %s", scope)

        hooks_mapping = CONTEXT_HOOKS_MANAGER.get()
        hooks_stack = HookStack(
            stack=hooks_mapping[scope].default,
            origin=origin,
            copy_stack=True,
        )

        logger.debug("Calling hooks stack: %s", hooks_stack)
        return hooks_stack.call(*args, **kwargs)

    wrapper = cast(_Wrapper, wrapper)
    wrapper.origin = origin  # type: ignore[attr-defined]

    return wrapper


def modify_scope(scope: Scope) -> None:
    """Modify the scope to call the hooks stack."""
    if hasattr(scope.callable_, "wrapper_origin"):
        logger.debug("Scope already modified: %s", scope)
        return

    logger.debug("Modifying scope: %s", scope)

    origin = deepcopy(scope.callable_)
    wrapper = _get_wrapper(origin=origin, scope=scope)

    if isinstance(scope.namespace, dict):
        scope.namespace[scope.callable_.__name__] = wrapper
    else:
        setattr(scope.namespace, scope.callable_.__name__, wrapper)
