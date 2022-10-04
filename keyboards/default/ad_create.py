from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_back_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Вернуться в профиль'),
                KeyboardButton(text='Назад')
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
