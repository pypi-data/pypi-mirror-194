# !/usr/bin/python

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
