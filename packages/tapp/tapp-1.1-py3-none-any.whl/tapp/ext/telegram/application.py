from __future__ import annotations

from typing import Any, Callable, Coroutine, Dict, Optional, Sequence, Type

from ...applications import TApp
from ...filters import Filter
from ...middleware import BaseMiddleware
from ...routing import Route
from ...types import Decorated
from .router import TelegramRouter


class TelegramApp(TApp):
    def __init__(
        self,
        *,
        routes: Optional[Sequence[Route]] = None,
        on_startup: Optional[Sequence[Callable[..., Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
        middleware: Optional[Sequence[BaseMiddleware]] = None,
        outer_middleware: Optional[Sequence[BaseMiddleware]] = None,
        exception_handlers: Optional[
            Dict[
                Type[Exception],
                Callable[[Any, Exception], Coroutine[Any, Any, Any]],
            ]
        ] = None,
    ) -> None:
        super(TelegramApp, self).__init__(
            TelegramRouter,
            routes=routes,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            middleware=middleware,
            outer_middleware=outer_middleware,
            exception_handlers=exception_handlers,
        )

    def message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.message(*filters, flags=flags)

    def edited_message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.edited_message(*filters, flags=flags)

    def channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.channel_post(*filters, flags=flags)

    def edited_channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.edited_channel_post(*filters, flags=flags)

    def inline_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.inline_query(*filters, flags=flags)

    def chosen_inline_result(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.chosen_inline_result(*filters, flags=flags)

    def callback_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.callback_query(*filters, flags=flags)

    def shipping_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.shipping_query(*filters, flags=flags)

    def pre_checkout_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.pre_checkout_query(*filters, flags=flags)

    def poll(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.poll(*filters, flags=flags)

    def poll_answer(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.poll_answer(*filters, flags=flags)

    def my_chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.my_chat_member(*filters, flags=flags)

    def chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.chat_member(*filters, flags=flags)

    def chat_join_request(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.chat_join_request(*filters, flags=flags)
