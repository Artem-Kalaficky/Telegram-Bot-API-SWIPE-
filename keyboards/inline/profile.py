from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


class UpdateAdCallback(CallbackData, prefix="test"):
    key_word: str
    ad_id: str


def get_edit_ad_inline_keyboard(ad_id):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_('Редактировать объявление'), callback_data=UpdateAdCallback(key_word="edit", ad_id=ad_id).pack()
                )
            ]
        ]
    )
    return inline_keyboard
