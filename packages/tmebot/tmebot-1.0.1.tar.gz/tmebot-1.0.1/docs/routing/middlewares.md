Before passing the update to the handler, it goes
through several stages through middlewares. For example,
blocking all updates that are not `message`.

Write your simple middleware:

```python
from typing import Any, Awaitable, Callable, Dict
from tmebot import middleware


class MyMiddleware(middleware.BaseMiddleware):
    async def __call__(
        self,
        route: Callable[[Any, Dict[str, Any]], Awaitable[None]],
        event: Any,
        data: Dict[str, Any],
    ) -> None:
        print("In middleware")
        await route(event, data)
```
