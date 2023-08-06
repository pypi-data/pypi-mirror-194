from typing import Any, Awaitable, Callable, Union

from magic_filter import MagicFilter

from ..filters import Filter as BaseFilter

Filter = Union[MagicFilter, BaseFilter, Callable[..., Awaitable[Any]]]
