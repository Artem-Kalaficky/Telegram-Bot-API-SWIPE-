from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Русский'),
            KeyboardButton(text='Українська')
        ]
    ],
    resize_keyboard=True
)


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена'),
        ],
    ],
    resize_keyboard=True
)


cancel_back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена'),
            KeyboardButton(text='Назад')
        ],
    ],
    resize_keyboard=True
)
