from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_update_ad_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Адрес')),
                KeyboardButton(text=_('Общая площадь')),
                KeyboardButton(text=_('Площадь кухни'))
            ],
            [
                KeyboardButton(text=_('Комиссия агенту')),
                KeyboardButton(text=_('Описание')),
                KeyboardButton(text=_('Цена'))
            ],
            [
                KeyboardButton(text=_('Вернуться к объявлениям')),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_update_ad_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Вернуться к редактированию')),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
