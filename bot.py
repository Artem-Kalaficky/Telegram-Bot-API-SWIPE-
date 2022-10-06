from typing import Any, Dict
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n

from data.config import BOT_TOKEN, LOCALES_DIR, DOMAIN, REDIS_STORAGE
from handlers.ad_create import ad_create_router
from handlers.ad_update import ad_update_router
from handlers.authorization import authorization_router
from handlers.profile import main_menu_router
from middlewares.locale import LocaleMiddleware

redis_storage = RedisStorage(REDIS_STORAGE)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=redis_storage)


async def main():
    i18n = I18n(path=LOCALES_DIR, default_locale="ru", domain=DOMAIN)
    dp.message.outer_middleware(LocaleMiddleware(i18n))
    dp.callback_query.outer_middleware(LocaleMiddleware(i18n))

    dp.include_router(authorization_router)
    dp.include_router(main_menu_router)
    dp.include_router(ad_create_router)
    dp.include_router(ad_update_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
