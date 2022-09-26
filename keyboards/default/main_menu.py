from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Профиль'),
            KeyboardButton(text='Лента')
        ],
        [
            KeyboardButton(text='Создать объявление')
        ],
        [
            KeyboardButton(text='Выход')
        ]
    ],
    resize_keyboard=True
)
