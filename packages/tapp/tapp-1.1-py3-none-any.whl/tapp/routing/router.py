from __future__ import annotations

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Optional,
    Sequence,
    Type,
    Union,
)

from ..anyio import as_async
from ..enums import Match
from ..filters import Filter
from ..logger import logger
from ..middleware import BaseMiddleware, ExceptionMiddleware, MiddlewareManager
from ..types import Decorated
from .route import Route


class Router:
    def __init__(
        self,
        routes: Optional[Sequence[Route]] = None,
        on_startup: Optional[Sequence[Callable[..., Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
        middleware: Optional[Sequence[BaseMiddleware]] = None,
        outer_middleware: Optional[Sequence[BaseMiddleware]] = None,
        route_class: Type[Route] = Route,
        *,
        exception_handlers: Optional[
            Dict[
                Type[Exception],
                Callable[[Any, Exception], Coroutine[Any, Any, Any]],
            ]
        ] = None,
    ) -> None:
        self.routes = [] if routes is None else list(routes)
        self.on_startup = [] if on_startup is None else list(on_startup)
        self.on_shutdown = [] if on_shutdown is None else list(on_shutdown)
        self.middleware = MiddlewareManager(middleware)
        self.outer_middleware = MiddlewareManager(outer_middleware)
        self.route_class = route_class
        self.exception_handlers: Dict[
            Any,
            Callable[[Any, Exception], Union[Any, Awaitable[Any]]],
        ] = (
            {} if exception_handlers is None else dict(exception_handlers)
        )
        self.add_outer_middleware(ExceptionMiddleware(self))

    async def startup(self) -> None:
        """
        Emit startup events.
        """

        for startup in self.on_startup:
            await as_async(startup)
        self._started = True

    async def shutdown(self) -> None:
        """
        Emit shutdown events.
        """

        for shutdown in self.on_shutdown:
            await as_async(shutdown)
        self._started = False

    async def lifespan(self) -> None:
        """
        Makes a lifespan events.
        """

        if not hasattr(self, "_started"):
            self._started = False

        if self._started:
            await self.shutdown()
            return
        await self.startup()

    async def __call__(self, method: str, update: Any, **kwargs: Any) -> None:
        if method == "lifespan":
            await self.lifespan()
            return

        for route in self.routes:
            match, data = await route.matches(update, method=method, **kwargs)
            if match == Match.MATCH:
                kwargs.update(data, route=route)
                wrapped = self.middleware.wrap(
                    route=route.handle,
                )
                await wrapped(update, kwargs)
        logger.debug(
            "Update for '%s' was skipped. Reason: match(%s) %s."
            % (method, Match.NONE, "unhandled"),
        )

    def include_router(self, router: Router) -> None:
        for middleware in router.middleware.copy():
            self.add_middleware(middleware=middleware)
        for outer_middleware in router.outer_middleware.copy():
            self.add_outer_middleware(outer_middleware=outer_middleware)
        for exception, endpoint in router.exception_handlers.items():
            self.add_exception_handler(exception=exception, endpoint=endpoint)
        for route in router.routes:
            self.add_route(
                endpoint=route.endpoint,
                method=route.method,
                filters=route.filters,
                flags=route.flags,
            )
        for startup in router.on_startup:
            self.add_lifespan(method="startup", endpoint=startup)
        for shutdown in router.on_shutdown:
            self.add_lifespan(method="shutdown", endpoint=shutdown)

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        self.middleware.add_middleware(middleware=middleware)

    def add_outer_middleware(self, outer_middleware: BaseMiddleware) -> None:
        self.outer_middleware.add_middleware(outer_middleware)

    def add_route(
        self,
        endpoint: Callable[..., Any],
        *,
        method: str,
        filters: Optional[Sequence[Filter]] = None,
        flags: Optional[Dict[str, Any]] = None,
    ) -> None:
        route = self.route_class(endpoint, method=method, filters=filters, flags=flags)
        self.routes.append(route)

    def route(
        self,
        *filters: Filter,
        method: str,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        def decorator(endpoint: Decorated) -> Decorated:
            self.add_route(endpoint, method=method, filters=filters, flags=flags)
            return endpoint

        return decorator

    def add_lifespan(
        self,
        method: str,
        endpoint: Callable[..., Any],
    ) -> None:
        assert method in ("startup", "shutdown"), "Got unsupported method: %s." % method

        if method == "startup":
            self.on_startup.append(endpoint)
        else:
            self.on_shutdown.append(method)

    def on_lifespan(self, method: str) -> Callable[[Decorated], Decorated]:
        def decorator(endpoint: Decorated) -> Decorated:
            self.add_lifespan(method=method, endpoint=endpoint)
            return endpoint

        return decorator

    def add_exception_handler(
        self,
        exception: Type[Exception],
        endpoint: Callable[..., Any],
    ) -> None:
        self.exception_handlers[exception] = endpoint

    def exception_handler(self, exception: Type[Exception]) -> Callable[[Decorated], Decorated]:
        def decorator(endpoint: Decorated) -> Decorated:
            self.add_exception_handler(exception=exception, endpoint=endpoint)
            return decorator

        return decorator
