from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


def get_authorization_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Вход')),
                KeyboardButton(text=_('Регистрация'))
            ],
            [
                KeyboardButton(text=_('Выбор языка'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_register_complete_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Подтвердить'))
            ],
            [
                KeyboardButton(text=_('Изменить Email')),
                KeyboardButton(text=_('Изменить пароль')),
            ],
            [
                KeyboardButton(text=_('Изменить имя')),
                KeyboardButton(text=_('Изменить фамилию')),
            ],
            [
                KeyboardButton(text=_('Отмена'))
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_register_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Вернуться к регистрации')),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_login_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('Авторизоваться')),
            ],
            [
                KeyboardButton(text=_('Отмена'))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
