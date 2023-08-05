# Filters

Filters are needed to filter updates from the user.

## In tmebot

`tmebot` package provides a simple interface for writing filters.

```python
import typing

from tmebot import filters, types


class MyOwnFilter(filters.Filter):
    async def __call__(
        self, obj: typing.Union[types.Message, types.CallbackQuery]
    ) -> None:
        if isinstance(obj, types.Message):
            text = obj.text
        elif isinstance(obj, types.CallbackQuery):
            text = obj.data
        else:
            return False
        return text.startswith("Hello")
```

This filter filters all events that come from `Message`
or `CallbackQuery`, these messages must start with `Hello`.

```python
import typing

from tmebot import filters, types, TRouter


class MyOwnFilter(filters.Filter):
    async def __call__(
        self, obj: typing.Union[types.Message, types.CallbackQuery]
    ) -> None:
        if isinstance(obj, types.Message):
            text = obj.text
        elif isinstance(obj, types.CallbackQuery):
            text = obj.data
        else:
            return False
        return text.startswith("Hello")


router = TRouter()


@router.message(MyOwnFilter())
async def message_handler(message: types.Message) -> None:
    await message.answer("Hello too!")
```
