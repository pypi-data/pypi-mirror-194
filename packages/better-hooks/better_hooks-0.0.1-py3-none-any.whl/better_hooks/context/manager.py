from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, DefaultDict

from better_hooks.context.types import (
    ScopedHooks,
    ScopedHooksContext,
    ScopedHooksMapping,
    ScopedHooksToken,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from better_hooks.hooks import ScopedHook


@dataclass(frozen=True, slots=True)
class ScopedHooksManager:
    _context: ScopedHooksContext = field(
        default_factory=lambda: ScopedHooksContext("_current_hooks"),
    )

    def get(self) -> ScopedHooksMapping:
        """Get the current hooks.

        Returns a copy of the current hooks,
        to prevent the hooks from being modified.
        """
        try:
            current_hooks = self._context.get()
        except LookupError:
            return DefaultDict(ScopedHooks)
        else:
            return copy(current_hooks)

    def set(self, hooks: ScopedHooksMapping) -> ScopedHooksToken:
        return self._context.set(hooks)

    def reset(self, token: ScopedHooksToken) -> None:
        self._context.reset(token)

    def append(self, hook: ScopedHook) -> ScopedHooksToken:
        """Append a hook to the current hooks."""
        current_hooks = self.get()
        self._append(current_hooks, hook)
        return self.set(current_hooks)

    def extend(self, hooks: Sequence[ScopedHook]) -> ScopedHooksToken:
        """Extend the current hooks with a list of hooks."""
        current_hooks = self.get()
        for hook in hooks:
            self._append(current_hooks, hook)
        return self.set(current_hooks)

    def _append(
        self,
        current_hooks: ScopedHooksMapping,
        hook: ScopedHook,
    ) -> None:
        """Append or remove a hook from the current hooks."""
        scoped_hooks = current_hooks[hook.scope]

        if hook.inverted:
            if hook in scoped_hooks.default:
                scoped_hooks.default.remove(hook)
            else:
                scoped_hooks.inverted.append(hook)
        else:
            if hook in scoped_hooks.inverted:
                scoped_hooks.inverted.remove(hook)
            else:
                scoped_hooks.default.append(hook)


CONTEXT_HOOKS_MANAGER = ScopedHooksManager()


def add_global_hooks(*hooks: ScopedHook) -> ScopedHooksToken:
    """Add a global hooks.

    This hooks will be always active, even if the context is not entered.
    """
    return CONTEXT_HOOKS_MANAGER.extend(hooks)
