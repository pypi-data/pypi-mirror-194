Polling is a constant listening to the server 
to receive updates, Telegram has a `getUpdates` method 
for such purposes. Polling is not safer than webhook.

```python
import asyncio

from tmebot import Bot, TApp, start_polling

TOKEN = "1:YOUR_TOKEN"

app = TApp()
bot = Bot(TOKEN)

if __name__ == "__main__":
    asyncio.run(start_polling(
        app,
        bot,
        limit=1,
        timeout=60,
        allowed_updates=["message"]
    ))
```

This code starts long polling with a limit 
of `one` update at a time, with a timeout of `60` 
seconds to receive updates, with updates allowed 
from Telegram `message`.
