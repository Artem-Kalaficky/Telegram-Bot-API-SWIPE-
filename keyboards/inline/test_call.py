from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


class TestCallback(CallbackData, prefix="test"):
    key_word: str
    data: str


def get_test_inline_keyboard(data):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Как дела?', callback_data=TestCallback(key_word="show", data=data).pack())
            ]
        ]
    )
    return inline_keyboard
