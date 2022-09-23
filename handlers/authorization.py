import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from data.services.validators import validate_email, validate_password

from keyboards.default.authorization import authorization_keyboard, register_complete_keyboard
from keyboards.default.base import language_keyboard, cancel_keyboard, cancel_back_keyboard
from requests import UserAPIClient
from states.authorization import Start, Register

unauthenticated_router = Router()
register_router = Router()


client = UserAPIClient()


# region Start Bot
@unauthenticated_router.message(Command(commands=["start"]))
@unauthenticated_router.message(Start.login_or_register, F.text.casefold() == 'выбор языка')
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Start.language)
    await message.answer(
        "Выберите язык...",
        reply_markup=language_keyboard
    )


@unauthenticated_router.message(F.text.casefold() == 'отмена')
@unauthenticated_router.message(Start.language, F.text.casefold() == 'русский')
async def process_authorization(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != Start.language:
        logging.info('Отмена состояния %r', current_state)
        await state.clear()

    await state.set_state(Start.login_or_register)
    await message.answer(
        "Войдите в существующую учетную запись или создайте новую.",
        reply_markup=authorization_keyboard
    )


@unauthenticated_router.message(Start.language, F.text.casefold() == 'українська')
async def process_alter_language(message: Message, state: FSMContext) -> None:
    await process_authorization(message, state)


@unauthenticated_router.message(Start.language)
async def process_unknown_language(message: Message, state: FSMContext) -> None:
    await message.reply("Я не понимаю тебя :(")
# endregion Start Bot


# region Register
@register_router.message(Register.complete, F.text.casefold() == 'изменить email')
@register_router.message(Register.password1, F.text.casefold() == 'назад')
@register_router.message(Start.login_or_register, F.text.casefold() == 'регистрация')
async def process_register_email(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.email)
    await message.answer(
        'Введите email',
        reply_markup=cancel_keyboard if current_state != Register.complete else ReplyKeyboardRemove()
    )


@register_router.message(Register.email)
async def process_validate_email(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    last_name = data.get('last_name', False)
    if last_name:
        await state.set_state(Register.complete)
    if validate_email(message.text):
        await state.update_data(email=message.text)
        if await state.get_state() == Register.complete:
            await process_register_complete(message, state)
        else:
            await process_register_password(message, state)
    else:
        await message.reply("Введённая электронная почта некорректна.")
        await process_register_email(message, state)


@register_router.message(Register.complete, F.text.casefold() == 'изменить пароль')
@register_router.message(Register.password2, F.text.casefold() == 'назад')
async def process_register_password(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.password1)
    await message.answer(
        'Введите пароль',
        reply_markup=cancel_back_keyboard if current_state != Register.complete else ReplyKeyboardRemove()
    )


@register_router.message(Register.password1)
async def process_validate_password(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    last_name = data.get('last_name', False)
    if last_name:
        await state.set_state(Register.complete)
    if validate_password(message.text):
        await state.update_data(password1=message.text)
        await process_register_repeat_password(message, state)
    else:
        await message.reply(
            "Пароль должен содержать:\n- минимум 8 символов\n"
            "- алфавит между [a-z]\n"
            "- минимум 1 букву в верхнем регистре [A-Z]\n"
            "- 1 число или цифру между [0-9]"
        )
        await process_register_password(message, state)


@register_router.message(Register.first_name, F.text.casefold() == 'назад')
async def process_register_repeat_password(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.password2)
    await message.answer(
        'Повторите пароль',
        reply_markup=cancel_back_keyboard if current_state != Register.complete else ReplyKeyboardRemove()
    )


@register_router.message(Register.password2)
async def process_compare_passwords(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    last_name = data.get('last_name', False)
    if last_name:
        await state.set_state(Register.complete)
    if data['password1'] == message.text:
        await state.update_data(password2=message.text)
        if await state.get_state() == Register.complete:
            await process_register_complete(message, state)
        else:
            await process_register_first_name(message, state)
    else:
        await message.reply('Пароли не совпадают.')
        await process_register_repeat_password(message, state)


@register_router.message(Register.complete, F.text.casefold() == 'изменить имя')
@register_router.message(Register.last_name, F.text.casefold() == 'назад')
async def process_register_first_name(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.first_name)
    await message.answer(
        'Введите имя',
        reply_markup=cancel_back_keyboard if current_state != Register.complete else ReplyKeyboardRemove()
    )


@register_router.message(Register.first_name)
async def process_change_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    data = await state.get_data()
    last_name = data.get('last_name', False)
    if last_name:
        await state.set_state(Register.complete)
        await process_register_complete(message, state)
    else:
        await process_register_last_name(message, state)


@register_router.message(Register.complete, F.text.casefold() == 'изменить фамилию')
async def process_register_last_name(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Register.first_name:
        await state.update_data(first_name=message.text)
    await state.set_state(Register.last_name)
    await message.answer(
        'Введите фамилию',
        reply_markup=cancel_back_keyboard if current_state != Register.complete else ReplyKeyboardRemove()
    )


@register_router.message(Register.last_name)
async def process_register_complete(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Register.last_name:
        await state.update_data(last_name=message.text)
    await state.set_state(Register.complete)
    data = await state.get_data()
    text = f'Данные успешно введены! Проверьте их корректность:\n\n' \
           f'Email: {data["email"]}\n' \
           f'Пароль: {data["password1"]}\n' \
           f'Имя: {data["first_name"]}\n' \
           f'Фамилия: {data["last_name"]}\n\n' \
           f'Всё верно?'
    await message.answer(
        text=text,
        reply_markup=register_complete_keyboard
    )


@register_router.message(Register.complete, F.text.casefold() == 'подтвердить')
async def process_register_send_email(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if await client.build_register_request(data):
        await message.answer(
            f'Регистрация прошла успешно. На вашу почту {data["email"]}, отправлено письмо с подтверждением.\n'
            f'Перейдите по ссылке для активации учетной записи.'
        )
    else:
        await message.answer(
            'Регистрация не успешна. Введнная почта уже занята другим пользователем.'
        )
    await process_authorization(message, state)
# endregion Register
