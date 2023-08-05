The router provides a convenient interface for
processing Telegram events:

```python
from tmebot import Route, TRouter, types


async def my_startup() -> None:
    ...


async def my_route(_: types.Message) -> None:
    ...


router = TRouter(
    on_startup=[my_startup],
    routes=[
        Route(my_route, method="message"),
    ]
)


@router.message()
async def message_handler(message: types.Message) -> None:
    ...


@router.on_lifespan("startup")
async def startup() -> None:
    print("Startup")


async def simple_route(message: types.Message) -> None:
    ...


router.add_route(simple_route, method="message")


async def my_lifespan() -> None:
    ...


router.add_lifespan(method="shutdown", endpoint=my_lifespan)


@router.route(method="message")
async def message_route(message: types.Message) -> None:
    ...
```
