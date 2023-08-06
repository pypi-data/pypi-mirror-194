from __future__ import annotations

from typing import Any, Dict, Union

from magic_filter import AttrDict, MagicFilter

from .filter import Filter


class Data(Filter):
    """
    Helps to filter event with contextual data.

    >>> import asyncio
    >>> from tapp.filters import Data, F
    >>> asyncio.run(Data(F.event == {"data": "hello"})({"data": "hello"}))
    True
    >>> "It's work!"
    """

    def __init__(self, data: MagicFilter) -> None:
        self.data = data

    async def __call__(self, event: Any, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        return self.data.resolve(
            AttrDict({"event": event, **{k: v for k, v in enumerate(args)}}, **kwargs)
        )
