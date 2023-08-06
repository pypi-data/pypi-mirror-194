from __future__ import annotations

import abc
from typing import Any, Dict, Union


class Filter(abc.ABC):
    """
    Class to register own filters.
    """

    @abc.abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        ...
