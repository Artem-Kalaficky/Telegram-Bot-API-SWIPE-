from typing import Any, Dict

from aiogram.types import TelegramObject
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
        if redis_language is None:
            redis_language = await REDIS_STORAGE.set(f'{event_from_user.id}', self.i18n.default_locale)
            return redis_language

        if event_from_user is None or redis_language is None:
            return self.i18n.default_locale

        try:
            message_text = data.get('event_update').message.text
            if message_text.lower() == 'русский':
                await REDIS_STORAGE.set(f'{event_from_user.id}', 'ru')
                redis_language = await REDIS_STORAGE.get(f'{event_from_user.id}')
            if message_text.lower() == 'українська':
                await REDIS_STORAGE.set(f'{event_from_user.id}', 'uk')
                redis_language = await REDIS_STORAGE.get(f'{event_from_user.id}')
        except:
            return redis_language

        return redis_language
