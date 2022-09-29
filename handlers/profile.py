import logging

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from data.services.get_image import get_avatar
from keyboards.default.main_menu import get_main_menu_keyboard
from keyboards.default.profile import get_profile_keyboard
from requests import UserAPIClient
from states.authorization import Start
from states.main_menu import Menu
from states.profile import Profile


main_menu_router = Router()
client = UserAPIClient()


# region My Profile
@main_menu_router.message(Menu.main_menu, F.text.casefold() == 'профиль')
async def process_get_my_profile(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != Menu.main_menu:
        logging.info('Отмена состояния %r', current_state)

    await state.clear()
    await state.set_state(Profile.get_profile)
    profile = await client.build_get_profile_request(message.chat.id)
    if profile:
        await message.answer_photo(
            photo=get_avatar(profile.get('avatar', False)),
            caption='Имя: {first_name}\n'
                    'Фамилия: {last_name}\n'
                    'Телефон: {telephone}\n'
                    'Email: {email}'.format(
                        first_name=html.bold(profile.get('first_name')),
                        last_name=html.bold(profile.get('last_name')),
                        telephone=html.bold(profile.get('telephone', False)) if profile.get('telephone') else 'Не задано',
                        email=html.bold(profile.get('email'))
                    ),
            reply_markup=get_profile_keyboard()
        )
    else:
        await state.set_state(Start.language)
        await message.answer(
            'Время сеанса истекло :(',
            reply_markup=ReplyKeyboardRemove()
        )
# endregion My Profile
