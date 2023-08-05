Router can handle exceptions

```python
from tmebot import filters, TRouter, types

router = TRouter()


@router.exception_handler(Exception)
async def exception_handler(
    update: types.Message, exception: Exception
) -> None:
    await update.answer(str(exception))


@router.message(filters.Text("Raise exception"))
async def message_handler(_: types.Message) -> None:
    raise Exception("Okay, done!")
```
