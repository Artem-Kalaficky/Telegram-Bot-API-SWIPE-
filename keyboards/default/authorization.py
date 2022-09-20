from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


authorization_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вход'),
            KeyboardButton(text='Регистрация')
        ],
        [
            KeyboardButton(text='Выбор языка')
        ]
    ],
    resize_keyboard=True
)


register_complete_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить')
        ],
        [
            KeyboardButton(text='Изменить Email'),
            KeyboardButton(text='Изменить пароль'),
        ],
        [
            KeyboardButton(text='Изменить имя'),
            KeyboardButton(text='Изменить фамилию'),
        ],
        [
            KeyboardButton(text='Отмена')
        ],
    ],
    resize_keyboard=True
)
