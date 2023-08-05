import asyncio
from contextlib import suppress
from typing import Any, AsyncGenerator, List, Optional, Tuple

from tbot_api import Bot
from tbot_api.methods import GetUpdates
from tbot_api.types import TelegramObject

from .app import TApp
from .logger import logger


async def process(
    app: TApp,
    *,
    bot: Bot,
    method: str,
    update: TelegramObject,
    **kwargs: Any,
) -> None:
    token = Bot.set_current(bot)
    try:
        await app(method=method, update=update, **kwargs)
    finally:
        Bot.reset_current(token)


async def listen(
    bot: Bot,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    timeout: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
) -> AsyncGenerator[Tuple[str, TelegramObject], None]:
    get_updates = GetUpdates(offset=offset, limit=limit, timeout=timeout, allowed_updates=allowed_updates)
    logger.info("Polling config: %s." % get_updates)

    while True:
        try:
            updates = await bot.request(get_updates, timeout=timeout)
        except Exception as e:
            updates = []

            logger.info("Skip updates: %s. Sleep 0.5s." % e)
            await asyncio.sleep(0.5)

        for update in updates:
            yield update.type, update.update

            get_updates.offset = update.update_id + 1


async def _polling(
    app: TApp,
    *,
    bot: Bot,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    timeout: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
    **kwargs: Any,
) -> None:
    try:
        async for method, update in listen(bot, offset=offset, limit=limit, timeout=timeout, allowed_updates=allowed_updates):
            await process(app, bot=bot, method=method, update=update, **kwargs)
    finally:
        logger.info("Polling stopped")


async def start_polling(
    app: TApp,
    *bots: Bot,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    timeout: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
    **kwargs: Any,
) -> None:
    logger.info("Run polling")

    await app("lifespan", None)

    try:
        tasks = [asyncio.create_task(
            _polling(
                app,
                bot=bot,
                offset=offset,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates,
                **kwargs
            )) for bot in bots]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        await asyncio.gather(*tasks)
    finally:
        await app("lifespan", None)
