from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Изменить личные данные'),
            ],
            [
                KeyboardButton(text='Мои объявления'),
                KeyboardButton(text='Создать объявление')
            ],
            [
                KeyboardButton(text='Главное меню')
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
