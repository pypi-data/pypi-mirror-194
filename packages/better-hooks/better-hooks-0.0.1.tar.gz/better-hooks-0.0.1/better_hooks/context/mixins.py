from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import LifoQueue
from typing import TYPE_CHECKING, Any

from better_hooks.context.manager import (
    CONTEXT_HOOKS_MANAGER,
    ScopedHooksManager,
)

if TYPE_CHECKING:
    from better_hooks.context.types import ScopedHooksToken

logger = logging.getLogger(__name__)


@dataclass
class ScopedHooksContextManagerMixin(ABC):
    _scoped_hooks_manager: ScopedHooksManager = field(
        init=False,
        compare=False,
        default=CONTEXT_HOOKS_MANAGER,
    )
    _tokens: LifoQueue[ScopedHooksToken] = field(
        init=False,
        compare=False,
        default_factory=LifoQueue,
    )

    @abstractmethod
    def _update_current_hooks(self) -> ScopedHooksToken:
        ...

    def __enter__(self) -> None:
        token = self._update_current_hooks()
        self._tokens.put(token)

    def __exit__(self, *_: Any) -> None:
        token = self._tokens.get(block=False)
        self._scoped_hooks_manager.reset(token)
