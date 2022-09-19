import asyncio
import logging
import sys
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F, html, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from data.config import BOT_TOKEN

form_router = Router()


class Form(StatesGroup):
    language = State()
    auth = State()


@form_router.message(Command(commands=["start"], state=Form.language))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.language)
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}!</b> Выберите язык...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Русский'),
                    KeyboardButton(text='Українська')
                ]
            ],
            resize_keyboard=True
        )
    )


@form_router.message(Form.language, F.text.casefold() == 'русский')
async def process_authorization(message: Message, state: FSMContext) -> None:
    await state.update_data(language=message.text)
    await state.set_state(Form.auth)

    await message.answer(
        "Войдите в существующую учетную запись или создайте новую.",
        reply_markup=ReplyKeyboardMarkup(
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
    )


@form_router.message(Form.language, F.text.casefold() == 'українська')
async def process_alter_language(message: Message, state: FSMContext) -> None:
    await process_authorization(message, state)

# @form_router.message(Form.auth)
# async def process_unknown_write_bots(message: Message, state: FSMContext) -> None:
#     await message.reply("Я не понимаю тебя :(")






async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
