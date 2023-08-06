from __future__ import annotations

from magic_filter import MagicFilter

from .filters import Filter


def transform_filter(_filter: Filter) -> Filter:
    if not isinstance(_filter, MagicFilter):
        return _filter
    return _filter.resolve
