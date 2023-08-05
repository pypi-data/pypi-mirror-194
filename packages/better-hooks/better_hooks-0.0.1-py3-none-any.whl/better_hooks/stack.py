from __future__ import annotations

import logging
from copy import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:
    from better_hooks.hooks import BaseHook
    from better_hooks.types import AnyCallable


logger = logging.getLogger(__name__)

T = TypeVar("T", covariant=True)


class Popable(Protocol[T]):
    def pop(self, index: int = ...) -> T:
        ...


@dataclass(slots=True)
class HookStack:
    stack: Popable[BaseHook]
    origin: AnyCallable
    """The original callable."""

    copy_stack: bool = True

    def __post_init__(self) -> None:
        logger.debug("Creating hook stack: %s", self)
        if self.copy_stack:
            self.stack = copy(self.stack)

    def call(self, *args: Any, **kwargs: Any) -> Any:
        """Call the hooks stack."""
        if not self.stack:
            logger.debug("Calling origin: %s", self.origin)
            return self.origin(*args, **kwargs)

        hook = self.stack.pop(0)
        logger.debug("Calling hook: %s", hook)
        return hook.call(self.call, *args, **kwargs)
