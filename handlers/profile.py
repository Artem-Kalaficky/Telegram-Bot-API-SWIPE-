import logging

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from data.services.get_image import get_avatar, get_photo
from keyboards.default.profile import get_profile_keyboard, get_back_to_profile_keyboard, get_update_profile_keyboard, \
    get_confirm_update_keyboard
from keyboards.inline.profile import get_edit_ad_inline_keyboard
from requests import UserAPIClient
from states.main_menu import Menu
from states.profile import Profile


main_menu_router = Router()
client = UserAPIClient()


# region My Profile
@main_menu_router.message(F.text.casefold() == 'вернуться в профиль')
@main_menu_router.message(Menu.main_menu, F.text.casefold() == 'профиль')
async def process_get_my_profile(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != Menu.main_menu:
        logging.info('Отмена состояния %r', current_state)

    await state.clear()
    await state.set_state(Profile.get_profile)
    profile = await client.build_get_profile_request(message.chat.id)
    if profile:
        await state.update_data(profile=profile)
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
        from .authorization import process_authorization

        await message.answer(
            'Время сеанса истекло :(',
        )
        await process_authorization(message, state)
# endregion My Profile


# region My Ads
@main_menu_router.message(Profile.get_profile, F.text.casefold() == 'мои объявления')
async def process_get_my_ads(message: Message, state: FSMContext) -> None:
    response = await client.build_get_my_ads_request(message.chat.id)
    if response is not None:
        text = "Вот все ваши личные объявления.."
    else:
        text = 'У вас ещё нет созданных объявлений.'
    await state.set_state(Profile.my_ads)
    await message.answer(
        text=text,
        reply_markup=get_back_to_profile_keyboard()
    )

    if response:
        for ad in response:
            await message.answer_photo(
                photo=get_photo(ad.get('main_photo', False)),
                caption='Адрес: {address}\n'
                        'Назначение: {purpose}\n'
                        'Общая площадь: {total_area}\n'
                        'Площадь кухни: {kitchen_area}\n'
                        'Комиссия агенту: {agent_commission}\n'
                        'Описание: {description}\n'
                        'Цена: {price}\n'
                        'Дата создания: {date_created}'.format(
                            address=html.bold(ad.get("address")),
                            purpose=html.bold(ad.get("purpose")),
                            total_area=html.bold(ad.get("total_area")),
                            kitchen_area=html.bold(ad.get("kitchen_area")),
                            agent_commission=html.bold(ad.get("agent_commission")),
                            description=html.bold(ad.get("description")),
                            price=html.bold(ad.get("price")),
                            date_created=html.italic(ad.get("date_created")),
                        ),
                reply_markup=get_edit_ad_inline_keyboard(ad.get("id"))
            )
# endregion My Ads


# region Update Personal Data
@main_menu_router.message(Profile.get_profile, F.text.casefold() == 'изменить личные данные')
async def process_update_personal_data(message: Message, state: FSMContext) -> None:
    await state.set_state(Profile.update_data)
    await message.answer(
        'Выберите, что вы хотите изменить о себе...',
        reply_markup=get_update_profile_keyboard()
    )


@main_menu_router.message(Profile.update_data, F.text.casefold() == 'фамилия')
async def process_update_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Profile.update_last_name)
    await message.answer(
        'Введите новую фамилию',
        reply_markup=get_back_to_profile_keyboard()
    )


@main_menu_router.message(Profile.update_data, F.text.casefold() == 'имя')
async def process_update_first_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Profile.update_first_name)
    await message.answer(
        'Введите новое имя',
        reply_markup=get_back_to_profile_keyboard()
    )


@main_menu_router.message(Profile.update_data, F.text.casefold() == 'телефон')
async def process_update_telephone(message: Message, state: FSMContext) -> None:
    await state.set_state(Profile.update_telephone)
    await message.answer(
        'Введите новый телефон, опираясь на предоставленный шаблон:\n'
        '+38 0xx xxx xx xx',
        reply_markup=get_back_to_profile_keyboard()
    )


@main_menu_router.message(Profile.update_data, F.text.casefold() == 'email')
async def process_update_email(message: Message, state: FSMContext) -> None:
    await state.set_state(Profile.update_email)
    await message.answer(
        'Введите новую почту',
        reply_markup=get_back_to_profile_keyboard()
    )


@main_menu_router.message(Profile.update_email)
@main_menu_router.message(Profile.update_telephone)
@main_menu_router.message(Profile.update_first_name)
@main_menu_router.message(Profile.update_last_name)
async def process_confirm_data(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    data = await state.get_data()
    profile = data['profile']
    if current_state == Profile.update_last_name:
        profile['last_name'] = message.text
    if current_state == Profile.update_first_name:
        profile['first_name'] = message.text
    if current_state == Profile.update_telephone:
        profile['telephone'] = message.text
    if current_state == Profile.update_email:
        profile['email'] = message.text

    response = await client.build_update_profile_request(message.chat.id, profile)
    if response:
        await message.answer(
            'Данные успешно обновлены!',
        )
        await process_get_my_profile(message, state)
    else:
        await message.answer(
            'Обновление данных прошло не успешно...',
        )
        await process_get_my_profile(message, state)

# endregion Update Personal Data
