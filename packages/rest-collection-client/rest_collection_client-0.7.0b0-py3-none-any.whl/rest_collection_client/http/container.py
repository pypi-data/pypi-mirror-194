from contextlib import AbstractContextManager
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Mapping, Optional, Type

from aiohttp import ClientResponse
from aiohttp.typedefs import StrOrURL

__all__ = [
    'ClientResponseContextManager',
    'HttpClientExcData',
]


class ClientResponseContextManager(AbstractContextManager[ClientResponse]):
    """``aiohttp.ClientResponse`` context manager."""

    def __init__(self, resp: ClientResponse) -> None:
        self._resp = resp

    def __enter__(self) -> ClientResponse:
        return self._resp

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._resp.release()


@dataclass(frozen=True)
class HttpClientExcData:
    """Exception data."""

    url: StrOrURL
    method: str
    params: Mapping[str, Any]
