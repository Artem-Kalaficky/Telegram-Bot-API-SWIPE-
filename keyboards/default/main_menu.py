from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Профиль')),
                KeyboardButton(text=_('Лента'))
            ],
            [
                KeyboardButton(text=_('Создать объявление'))
            ],
            [
                KeyboardButton(text=_('Выход'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
