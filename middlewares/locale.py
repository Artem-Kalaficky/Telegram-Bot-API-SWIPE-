from typing import Any, Dict, Optional, cast

from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware

from data.config import REDIS_STORAGE

try:
    from babel import Locale, UnknownLocaleError
except ImportError:
    Locale = None

    class UnknownLocaleError(Exception):
        pass


class LocaleMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user = data.get("event_from_user", None)
        redis_language = await REDIS_STORAGE.get(f'{event_from_user.id}')
        print(redis_language)
        if event_from_user is None or redis_language is None:
            print(self.i18n.default_locale)
            print(type(self.i18n.default_locale))
            return self.i18n.default_locale
        else:
            self.i18n.default_locale = redis_language
            print('else')
            print(self.i18n.default_locale)
            print(type(self.i18n.default_locale))
            return self.i18n.default_locale


