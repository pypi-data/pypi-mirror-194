from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

AnyCallable: TypeAlias = Callable[..., Any | Awaitable[Any]]
