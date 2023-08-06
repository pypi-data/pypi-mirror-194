from __future__ import annotations

import abc
from typing import Any, Callable, Dict, Optional, Sequence, Tuple

from ..anyio import as_async
from ..enums import Match
from ..filters import Filter
from ..utils import transform_filter


class BaseRoute(abc.ABC):
    @abc.abstractmethod
    async def matches(self, *args: Any, **kwargs: Any) -> Tuple[Match, Dict[str, Any]]:
        ...

    @abc.abstractmethod
    async def handle(self, *args: Any, **kwargs: Any) -> None:
        ...


class Route(BaseRoute):
    def __init__(
        self,
        endpoint: Callable[..., Any],
        *,
        method: str,
        filters: Optional[Sequence[Filter]] = None,
        flags: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.endpoint = endpoint
        self.method = method
        self.filters = [] if filters is None else list(map(transform_filter, filters))
        self.flags = {} if flags is None else flags

    async def matches(
        self, *args: Any, method: str, **kwargs: Any
    ) -> Tuple[Match, Dict[str, Any]]:
        if not self.filters:
            return Match.MATCH, kwargs
        for _filter in self.filters:
            call = await as_async(_filter, *args, **kwargs)
            if not call:
                return Match.NONE, kwargs
            if isinstance(call, dict):
                kwargs.update(call)
        return Match.MATCH, kwargs

    async def handle(self, *args: Any, **kwargs: Any) -> None:
        await as_async(self.endpoint, *args, **kwargs)
