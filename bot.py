import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n

from data.config import BOT_TOKEN, LOCALES_DIR, DOMAIN
from handlers.authorization import authorization_router
from handlers.profile import main_menu_router
from middlewares.locale import LocaleMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    i18n = I18n(path=LOCALES_DIR, default_locale="uk", domain=DOMAIN)
    dp.message.outer_middleware(LocaleMiddleware(i18n))

    dp.include_router(authorization_router)
    dp.include_router(main_menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
