import asyncio
import logging
import sys

import aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from data.config import BOT_TOKEN
from handlers.authorization import unauthenticated_router, register_router


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(unauthenticated_router)
    dp.include_router(register_router)

    redis = await aioredis.from_url("redis://localhost:6379", db=1)
    storage = RedisStorage(redis)

    await dp.start_polling(bot, storage=storage)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
