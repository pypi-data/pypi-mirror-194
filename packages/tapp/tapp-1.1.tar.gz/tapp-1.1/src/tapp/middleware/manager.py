from __future__ import annotations

import functools
from typing import Any, Callable, Dict, List, Optional, Sequence

from .base import BaseMiddleware


class MiddlewareManager:
    """
    Class providing an interface for working with middleware.
    """

    def __init__(self, middleware: Optional[Sequence[BaseMiddleware]] = None) -> None:
        self.middleware = [] if middleware is None else list(middleware)

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        """
        Adds middleware.
        If the middleware is already registered nothing happens (by `type(middleware)`).

        :param middleware: middleware to add
        :return: None
        """
        if type(middleware) not in map(type, self.middleware):
            self.middleware.append(middleware)

    def copy(self) -> List[BaseMiddleware]:
        """
        Copies middleware.

        :return: all middleware
        """

        return self.middleware.copy()

    def wrap(self, route: Callable[..., Any]) -> Callable[..., Any]:
        """
        Builds a stack of middlewares from registered.

        :param route: function that is called last
        :return: middleware stack
        """

        @functools.wraps(route)
        def wrapped(event: Any, kwargs: Dict[str, Any]) -> Any:
            return route(event, **kwargs)

        app = wrapped
        for middleware in reversed(self.middleware):
            app = functools.partial(middleware, app)
        return app
