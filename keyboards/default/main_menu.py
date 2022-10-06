from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Профиль')),
                KeyboardButton(text=_('Лента объявлений'))
            ],
            [
                KeyboardButton(text=_('Выход'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Главное меню'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
