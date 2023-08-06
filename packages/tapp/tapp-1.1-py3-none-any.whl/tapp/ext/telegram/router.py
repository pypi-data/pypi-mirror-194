from __future__ import annotations

from typing import Any, Callable, Coroutine, Dict, Optional, Sequence, Type

from ...filters import Filter
from ...middleware import BaseMiddleware
from ...routing import Route, Router
from ...types import Decorated


class TelegramRouter(Router):
    def __init__(
        self,
        routes: Optional[Sequence[Route]] = None,
        on_startup: Optional[Sequence[Callable[..., Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
        middleware: Optional[Sequence[BaseMiddleware]] = None,
        outer_middleware: Optional[Sequence[BaseMiddleware]] = None,
        route_class: Type[Route] = Route,
        exception_handlers: Optional[
            Dict[
                Type[Exception],
                Callable[[Any, Exception], Coroutine[Any, Any, Any]],
            ]
        ] = None,
    ) -> None:
        super(TelegramRouter, self).__init__(
            routes=routes,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            middleware=middleware,
            outer_middleware=outer_middleware,
            route_class=route_class,
            exception_handlers=exception_handlers,
        )

    def message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="message", flags=flags)

    def edited_message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="edited_message", flags=flags)

    def channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="channel_post", flags=flags)

    def edited_channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="edited_channel_post", flags=flags)

    def inline_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="inline_query", flags=flags)

    def chosen_inline_result(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="chosen_inline_result", flags=flags)

    def callback_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="callback_query", flags=flags)

    def shipping_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="shipping_query", flags=flags)

    def pre_checkout_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="pre_checkout_query", flags=flags)

    def poll(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="poll", flags=flags)

    def poll_answer(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="poll_answer", flags=flags)

    def my_chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="my_chat_member", flags=flags)

    def chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="chat_member", flags=flags)

    def chat_join_request(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method="chat_join_request", flags=flags)
