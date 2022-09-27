from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_language_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Русский'),
                KeyboardButton(text='Українська')
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Отмена')),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_cancel_back_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Отмена')),
                KeyboardButton(text=_('Назад'))
            ],
        ],
        resize_keyboard=True
    )
    return keyboard
