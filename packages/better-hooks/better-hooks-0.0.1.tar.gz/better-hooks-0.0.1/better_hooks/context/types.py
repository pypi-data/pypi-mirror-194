from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, DefaultDict, TypeAlias

if TYPE_CHECKING:
    from better_hooks.hooks import Scope, ScopedHook


@dataclass(frozen=True, slots=True)
class ScopedHooks:
    default: list[ScopedHook] = field(default_factory=list)
    inverted: list[ScopedHook] = field(default_factory=list)


ScopedHooksMapping: TypeAlias = DefaultDict["Scope", ScopedHooks]

ScopedHooksContext: TypeAlias = ContextVar[ScopedHooksMapping]
ScopedHooksToken: TypeAlias = Token[ScopedHooksMapping]
