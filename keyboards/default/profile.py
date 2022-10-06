from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Изменить личные данные')),
            ],
            [
                KeyboardButton(text=_('Мои объявления')),
                KeyboardButton(text=_('Создать объявление'))
            ],
            [
                KeyboardButton(text=_('Главное меню'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Вернуться в профиль')),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_languages_or_back_to_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Русский'),
                KeyboardButton(text='Українська')
            ],
            [
                KeyboardButton(text=_('Вернуться в профиль'))
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_update_profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Фамилия')),
                KeyboardButton(text=_('Имя')),
                KeyboardButton(text=_('Телефон'))
            ],
            [
                KeyboardButton(text=_('Email')),
                KeyboardButton(text=_('Язык')),
                KeyboardButton(text=_('Аватар'))
            ],
            [
                KeyboardButton(text=_('Вернуться в профиль')),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard
