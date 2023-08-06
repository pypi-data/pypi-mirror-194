# tapp

Asyncio library for creating applications for
handling events from the user.

Documentation:
+ [English](docs/index.md)

## Quick start

Install:

```shell
pip install tapp
```

Example:

```python
# !/usr/bin/python

# content examples/some.py

import asyncio

from tapp import TApp

app = TApp()


@app.route(method="method")
async def method_handler(message: str, version: str) -> None:
    print(message, version)


async def main() -> None:
    await app("method", "message", version="version")


if __name__ == "__main__":
    asyncio.run(main())
```
