from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


class FeedCallback(CallbackData, prefix="feed"):
    key_word: str
    position: int


def get_feed_inline_keyboard(position):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Предыдущее', callback_data=FeedCallback(key_word="previous", position=position).pack()
                ),
                InlineKeyboardButton(
                    text='Следующее', callback_data=FeedCallback(key_word="next", position=position).pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Показать геолокацию', callback_data=FeedCallback(key_word="geo", position=position).pack()
                )
            ]
        ]
    )
    return inline_keyboard
