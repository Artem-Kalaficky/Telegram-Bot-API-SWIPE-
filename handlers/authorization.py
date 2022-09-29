import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendPhoto
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    InputFile, BufferedInputFile, URLInputFile
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


from data.config import USERS_COLLECTION
from data.services.validators import validate_email, validate_password
from handlers.main_menu import process_main_menu

from keyboards.default.authorization import (
    get_authorization_keyboard, get_register_complete_keyboard, get_login_keyboard, get_back_to_register_keyboard
)
from keyboards.default.base import (
    get_language_keyboard, get_cancel_keyboard, get_cancel_back_keyboard
)
from keyboards.inline.test_call import TestCallback, get_test_inline_keyboard
from requests import UserAPIClient
from states.authorization import Start, Register, Login
from states.main_menu import Menu


authorization_router = Router()
client = UserAPIClient()


# region Start Bot
@authorization_router.message(Command(commands=["start"]))
@authorization_router.message(Start.login_or_register, F.text.casefold() == __('выбор языка'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Start.language)
    await message.answer(
        _('Выберите язык...'),
        reply_markup=get_language_keyboard()
    )


@authorization_router.message(F.text.casefold() == __('отмена'))
@authorization_router.message(Menu.main_menu, F.text.casefold() == __('выход'))
@authorization_router.message(Start.language)
async def process_authorization(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != Start.language:
        logging.info('Отмена состояния %r', current_state)
        if current_state == Menu.main_menu:
            USERS_COLLECTION.update_one({'user_id': message.chat.id}, {
                '$set': {'is_authenticated': False}
            }, upsert=True)

    await state.clear()
    await state.set_state(Start.login_or_register)
    await message.answer(
        _("Войдите в существующую учетную запись или создайте новую."),
        reply_markup=get_authorization_keyboard()
    )
# endregion Start Bot


# region Register
@authorization_router.message(Register.complete, F.text.casefold() == __('изменить email'))
@authorization_router.message(Register.password1, F.text.casefold() == __('назад'))
@authorization_router.message(Start.login_or_register, F.text.casefold() == __('регистрация'))
async def process_register_email(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.email)
    await message.answer(
        _('Введите email'),
        reply_markup=get_cancel_keyboard() if current_state != Register.complete else get_back_to_register_keyboard()
    )


@authorization_router.message(Register.email)
async def process_validate_email(message: Message, state: FSMContext) -> None:
    if message.text.lower() == _('вернуться к регистрации'):
        await process_register_complete(message, state)
    else:
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
            await message.reply(_("Введённая электронная почта некорректна."))
            await process_register_email(message, state)


@authorization_router.message(Register.complete, F.text.casefold() == __('изменить пароль'))
@authorization_router.message(Register.password2, F.text.casefold() == __('назад'))
async def process_register_password(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.password1)
    await message.answer(
        _('Введите пароль'),
        reply_markup=get_cancel_back_keyboard() if current_state != Register.complete else get_back_to_register_keyboard()
    )


@authorization_router.message(Register.password1)
async def process_validate_password(message: Message, state: FSMContext) -> None:
    if message.text.lower() == _('вернуться к регистрации'):
        await process_register_complete(message, state)
    else:
        data = await state.get_data()
        last_name = data.get('last_name', False)
        if last_name:
            await state.set_state(Register.complete)
        if validate_password(message.text):
            await state.update_data(password1=message.text)
            await process_register_repeat_password(message, state)
        else:
            await message.reply(
                _("Пароль должен содержать:\n- минимум 8 символов\n"
                  "- алфавит между [a-z]\n"
                  "- минимум 1 букву в верхнем регистре [A-Z]\n"
                  "- 1 число или цифру между [0-9]")
            )
            await process_register_password(message, state)


@authorization_router.message(Register.first_name, F.text.casefold() == __('назад'))
async def process_register_repeat_password(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.password2)
    await message.answer(
        _('Повторите пароль'),
        reply_markup=get_cancel_back_keyboard() if current_state != Register.complete else ReplyKeyboardRemove()
    )


@authorization_router.message(Register.password2)
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
        await message.reply(_('Пароли не совпадают.'))
        await process_register_repeat_password(message, state)


@authorization_router.message(Register.complete, F.text.casefold() == __('изменить имя'))
@authorization_router.message(Register.last_name, F.text.casefold() == __('назад'))
async def process_register_first_name(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    await state.set_state(Register.first_name)
    await message.answer(
        _('Введите имя'),
        reply_markup=get_cancel_back_keyboard() if current_state != Register.complete else get_back_to_register_keyboard()
    )


@authorization_router.message(Register.first_name)
async def process_change_first_name(message: Message, state: FSMContext) -> None:
    if message.text.lower() == _('вернуться к регистрации'):
        await process_register_complete(message, state)
    else:
        await state.update_data(first_name=message.text)
        data = await state.get_data()
        last_name = data.get('last_name', False)
        if last_name:
            await state.set_state(Register.complete)
            await process_register_complete(message, state)
        else:
            await process_register_last_name(message, state)


@authorization_router.message(Register.complete, F.text.casefold() == __('изменить фамилию'))
async def process_register_last_name(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Register.first_name:
        await state.update_data(first_name=message.text)
    await state.set_state(Register.last_name)
    await message.answer(
        _('Введите фамилию'),
        reply_markup=get_cancel_back_keyboard() if current_state != Register.complete else get_back_to_register_keyboard()
    )


@authorization_router.message(F.text.casefold() == __('вернуться к регистрации'))
@authorization_router.message(Register.last_name)
async def process_register_complete(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Register.last_name:
        if message.text.lower() == _('вернуться к регистрации'):
            pass
        else:
            await state.update_data(last_name=message.text)
    await state.set_state(Register.complete)
    data = await state.get_data()
    text = _(
        'Данные успешно введены! Проверьте их корректность:\n\n'
        'Email: {email}\n'
        'Пароль: {password}\n'
        'Имя: {first_name}\n'
        'Фамилия: {last_name}\n\n'
        'Всё верно?'
    ).format(
        email=data["email"],
        password=data["password1"],
        first_name=data["first_name"],
        last_name=data["last_name"]
    )
    await message.answer(
        text=text,
        reply_markup=get_register_complete_keyboard()
    )


@authorization_router.message(Register.complete, F.text.casefold() == __('подтвердить'))
async def process_register_send_email(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    json = {
        'email': data['email'],
        'password1': data['password1'],
        'password2': data['password1'],
        'first_name': data['first_name'],
        'last_name': data['last_name']
    }
    if await client.build_register_request(json):
        await message.answer(
            _(
                'Регистрация прошла успешно. На вашу почту {email}, отправлено письмо с подтверждением.\n'
                'Перейдите по ссылке для активации учетной записи.'
            ).format(email=data["email"])
        )
    else:
        await message.answer(
            _('Регистрация не успешна. Введнная почта уже занята другим пользователем.')
        )
    await process_authorization(message, state)
# endregion Register


# region Login
@authorization_router.message(Start.login_or_register, F.text.casefold() == __('вход'))
async def process_login_email(message: Message, state: FSMContext) -> None:
    await state.set_state(Login.email)
    await message.answer(
        _('Введите email'),
        reply_markup=get_cancel_keyboard()
    )


@authorization_router.message(Login.email)
async def process_login_password(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(Login.password)
    await message.answer(
        _('Введите пароль'),
        reply_markup=get_cancel_keyboard()
    )


@authorization_router.message(Login.password)
async def process_login_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await state.set_state(Login.complete)
    data = await state.get_data()
    text = _(
        'Данные успешно введены! Проверьте их корректность:\n\n' 
        'Email: {email}\n' 
        'Пароль: {password}\n' 
        'Всё верно?'
    ).format(email=data["email"], password=data["password"])
    await message.answer(
        text=text,
        reply_markup=get_login_keyboard()
    )


@authorization_router.message(Login.complete)
async def process_login_complete(message: Message, state: FSMContext) -> None:
    await state.set_state(Menu.main_menu)
    data = await state.get_data()
    json = {
        'email': data['email'],
        'password': data['password'],
    }
    user_id = message.chat.id
    if await client.build_login_request(user_id, json):
        await process_main_menu(message, state)
    else:
        await message.answer(
            _('Авторизация прошла не успешно. Введённые данные некорректны.')
        )
        await process_authorization(message, state)
# endregion Login
