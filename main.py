import asyncio
import logging
import re
import sys
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F, html, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
import aioredis

from data.config import BOT_TOKEN
from keyboards.default.authorization import authorization_keyboard, register_complete_keyboard
from keyboards.default.base import language_keyboard, cancel_keyboard, cancel_back_keyboard

form_router = Router()


class Form(StatesGroup):
    language = State()
    auth = State()


class Register(StatesGroup):
    email = State()
    password1 = State()
    password2 = State()
    first_name = State()
    last_name = State()
    end = State()


@form_router.message(Command(commands=["start"], state=Form.language))
@form_router.message(F.text.casefold() == 'выбор языка')
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.language)
    await message.answer(
        "Выберите язык...",
        reply_markup=language_keyboard
    )


@form_router.message(F.text.casefold() == 'отмена')
@form_router.message(Form.language, F.text.casefold() == 'русский')
async def process_authorization(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != Form.language:
        logging.info('Отмена состояния %r', current_state)
        await state.clear()

    await state.set_state(Form.auth)
    await message.answer(
        "Войдите в существующую учетную запись или создайте новую.",
        reply_markup=authorization_keyboard
    )


@form_router.message(Form.language, F.text.casefold() == 'українська')
async def process_alter_language(message: Message, state: FSMContext) -> None:
    await process_authorization(message, state)


@form_router.message(Form.language)
async def process_unknown_language(message: Message, state: FSMContext) -> None:
    await message.reply("Я не понимаю тебя :(")


# region Register
@form_router.message(Register.password1, F.text.casefold() == 'назад')
@form_router.message(Form.auth, F.text.casefold() == 'регистрация')
async def process_register_email(message: Message, state: FSMContext) -> None:
    await state.set_state(Register.email)
    await message.answer(
        'Введите email',
        reply_markup=cancel_keyboard
    )


@form_router.message(Register.password2, F.text.casefold() == 'назад')
@form_router.message(Register.email)
async def process_register_password(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(Register.password1)
    await message.answer(
        'Введите пароль',
        reply_markup=cancel_back_keyboard
    )


@form_router.message(Register.first_name, F.text.casefold() == 'назад')
@form_router.message(Register.password1)
async def process_register_repeat_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password1=message.text)
    await state.set_state(Register.password2)
    await message.answer(
        'Повторите пароль',
        reply_markup=cancel_back_keyboard
    )


@form_router.message(Register.last_name, F.text.casefold() == 'назад')
@form_router.message(Register.password2)
async def process_register_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(password1=message.text)
    await state.set_state(Register.first_name)
    await message.answer(
        'Введите имя',
        reply_markup=cancel_back_keyboard
    )


@form_router.message(Register.first_name)
async def process_register_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(Register.last_name)
    await message.answer(
        'Введите фамилию',
        reply_markup=cancel_back_keyboard
    )


@form_router.message(Register.last_name)
async def process_register_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(Register.end)

    data = await state.get_data()
    await show_register_summary(message=message, data=data)


async def show_register_summary(message: Message, data: Dict[str, Any]) -> None:
    email = data["email"]
    password = data["password1"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    text = 'Данные успешно введены! Проверьте их корректность:\n\n'
    text += (
        f'Email: {email}\nПароль: {password}\nИмя: {first_name}\nФамилия: {last_name}\n\nВсё верно?'
    )
    await message.answer(
        text=text,
        reply_markup=register_complete_keyboard
    )
# endregion Register


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(form_router)

    redis = await aioredis.from_url("redis://localhost:6379", db=1)
    storage = RedisStorage(redis)

    await dp.start_polling(bot, storage=storage)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
