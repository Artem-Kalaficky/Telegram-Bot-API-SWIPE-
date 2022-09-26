import asyncio
import logging
import sys

import aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware, ConstI18nMiddleware
from aioredis import Redis

from data.config import BOT_TOKEN, LOCALES_DIR, DOMAIN
from handlers.authorization import authorization_router


i18n = I18n(path=LOCALES_DIR, default_locale="uk", domain=DOMAIN)

redis_storage = Redis()


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.message.middleware(ConstI18nMiddleware(locale='uk', i18n=i18n))
    dp.include_router(authorization_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
