from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_back_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Вернуться в профиль')),
                KeyboardButton(text=_('Назад'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_purpose_and_back_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Новострой')),
                KeyboardButton(text=_('Квартира')),
                KeyboardButton(text=_('Коттедж'))
            ],
            [
                KeyboardButton(text=_('Вернуться в профиль')),
                KeyboardButton(text=_('Назад'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_house_and_back_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Ипатий')),
                KeyboardButton(text=_('Ладислав'))
            ],
            [
                KeyboardButton(text=_('Вернуться в профиль')),
                KeyboardButton(text=_('Назад'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_complete_creating_ad_and_back_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Подтвердить'))
            ],
            [
                KeyboardButton(text=_('Вернуться в профиль')),
                KeyboardButton(text=_('Назад'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
