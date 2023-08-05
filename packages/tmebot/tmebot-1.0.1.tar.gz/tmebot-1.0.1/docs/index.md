# Documentation

## Simple usage

```python
import asyncio

from tmebot import Bot, filters, TApp, types, start_polling

TOKEN = "1:YOUR_TOKEN"

app = TApp()
bot = Bot(TOKEN)


@app.message(filters.Text("I love use you!"))
async def message_handler(message: types.Message) -> None:
    await message.answer("Thanks!")


async def main() -> None:
    await start_polling(app, bot)


if __name__ == "__main__":
    asyncio.run(main())
```
