from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


class AdCallback(CallbackData, prefix="test"):
    key_word: str
    data: str


def get_edit_ad_inline_keyboard(ad_id):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Редактировать объявления', callback_data=AdCallback(key_word="edit", data=ad_id).pack()
                )
            ]
        ]
    )
    return inline_keyboard
