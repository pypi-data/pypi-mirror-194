# Filters

Filters are needed to filter updates from the user.

```python
from tapp.filters import Filter


class HelloPrefixFilter(Filter):
    """
    Helps to filter data startswith `Hello`.
    """

    async def __call__(self, obj: str) -> None:
        if not isinstance(obj, str):
            return False
        return obj.startswith("Hello")
```
