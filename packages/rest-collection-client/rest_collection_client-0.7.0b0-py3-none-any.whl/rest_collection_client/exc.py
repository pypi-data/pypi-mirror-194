from sys import exc_info
from types import TracebackType
from typing import Any, Optional, Type

__all__ = [
    'RestCollectionClientError',
]


class RestCollectionClientError(Exception):
    """Root library exception."""

    def __init__(self, *args: Any, data: Optional[Any] = None) -> None:
        super().__init__(*args)
        self._from = exc_info()
        self.data = data

    @property
    def from_cls(self) -> Optional[Type[BaseException]]:
        return self._from[0]

    @property
    def from_value(self) -> Optional[BaseException]:
        return self._from[1]

    @property
    def from_traceback(self) -> Optional[TracebackType]:
        return self._from[2]
