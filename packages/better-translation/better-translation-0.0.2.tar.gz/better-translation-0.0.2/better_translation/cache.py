from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=Any)


class ICache(ABC, Generic[T]):
    @abstractmethod
    def get(self, *args_keys: Any, **kwargs_keys: Any) -> T | None:
        ...

    @abstractmethod
    def set(self, value: T, *args_keys: Any, **kwargs_keys: Any) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...


class InMemoryCache(ICache[T]):
    def __init__(self) -> None:
        self._cache: dict[tuple[Any, ...], Any] = {}

    def get(self, *args_keys: Any, **kwargs_keys: Any) -> T | None:
        return self._cache.get((*args_keys, *kwargs_keys.items()))

    def set(self, value: T, *args_keys: Any, **kwargs_keys: Any) -> None:
        self._cache[(*args_keys, *kwargs_keys.items())] = value

    def clear(self) -> None:
        self._cache.clear()
