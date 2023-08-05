from __future__ import annotations

from asyncio import iscoroutinefunction
from typing import Any, TypeVar

T = TypeVar("T")


def is_coroutine_function(obj: Any) -> bool:
    if iscoroutinefunction(obj):
        return True
    if callable(obj) and iscoroutinefunction(obj.__call__):
        return True

    return False
