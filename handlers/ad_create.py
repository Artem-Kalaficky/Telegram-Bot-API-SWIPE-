import base64
import io

from aiogram import F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from data.services.get_house import get_house
from data.services.get_purpose import get_purpose
from data.services.validators import validate_area, compare_values, validate_price
from handlers.authorization import process_authorization
from handlers.profile import process_get_my_profile
from keyboards.default.ad_create import (
    get_back_or_back_to_profile_keyboard, get_purpose_and_back_or_back_to_profile_keyboard,
    get_house_and_back_or_back_to_profile_keyboard, get_complete_creating_ad_and_back_or_back_to_profile_keyboard
)
from keyboards.default.profile import get_back_to_profile_keyboard
from api_requests.requests import UserAPIClient
from states.ad_create import AdCreate
from states.profile import Profile


ad_create_router = Router()
client = UserAPIClient()


@ad_create_router.message(AdCreate.purpose, F.text.casefold() == __('назад'))
@ad_create_router.message(Profile.get_profile, F.text.casefold() == __('создать объявление'))
async def process_create_ad(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AdCreate.address)
    await message.answer(
        _('Введите адрес'),
        reply_markup=get_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.total_area, F.text.casefold() == __('назад'))
@ad_create_router.message(AdCreate.house, F.text.casefold() == __('назад'))
@ad_create_router.message(AdCreate.address)
async def process_create_ad_purpose(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AdCreate.address:
        await state.update_data(address=message.text)
    await state.set_state(AdCreate.purpose)
    await message.answer(
        _('Выберите назначение из доступных'),
        reply_markup=get_purpose_and_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.purpose, F.text.casefold() == __('новострой'))
@ad_create_router.message(AdCreate.purpose, F.text.casefold() == __('квартира'))
async def process_create_ad_house(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AdCreate.purpose:
        text = 'apartment' if message.text.lower() == _('квартира') else 'new_building'
        await state.update_data(purpose=text)
    await state.set_state(AdCreate.house)
    await message.answer(
        _('Выберите жилой комплекс из доступных'),
        reply_markup=get_house_and_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.kitchen_area, F.text.casefold() == __('назад'))
@ad_create_router.message(AdCreate.house, F.text.casefold() == __('ипатий'))
@ad_create_router.message(AdCreate.house, F.text.casefold() == __('ладислав'))
@ad_create_router.message(AdCreate.purpose, F.text.casefold() == __('коттедж'))
async def process_create_ad_total_area(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AdCreate.house:
        house = 1 if message.text.lower() == _('ипатий') else 2
        await state.update_data(house=house)
    if current_state == AdCreate.purpose:
        await state.update_data(purpose='cottage')
    await state.set_state(AdCreate.total_area)
    await message.answer(
        _('Введите общую площадь'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.house)
@ad_create_router.message(AdCreate.purpose)
async def process_create_ad_house(message: Message) -> None:
    await message.reply(_('Такого значения нет среди допустимых'))


@ad_create_router.message(AdCreate.total_area)
async def process_validate_total_area(message: Message, state: FSMContext) -> None:
    if validate_area(message.text):
        await state.update_data(total_area=message.text)
        await process_create_kitchen_area(message, state)
    else:
        await message.reply(_('Введённая площадь некорректна.'))
        await process_create_ad_total_area(message, state)


@ad_create_router.message(AdCreate.agent_commission, F.text.casefold() == __('назад'))
async def process_create_kitchen_area(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.kitchen_area)
    await message.answer(
        _('Введите площадь кухни.'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.kitchen_area)
async def process_validate_kitchen_area(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if validate_area(message.text) and compare_values(data['total_area'], message.text):
        await state.update_data(kitchen_area=message.text)
        await process_create_agent_commission(message, state)
    else:
        await message.reply(_('Введённая площадь некорректна или превышает общую площадь.'))
        await process_create_kitchen_area(message, state)


@ad_create_router.message(AdCreate.description, F.text.casefold() == __('назад'))
async def process_create_agent_commission(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.agent_commission)
    await message.answer(
        _('Введите комиссию для агента.'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.agent_commission)
async def process_validate_commission(message: Message, state: FSMContext) -> None:
    if validate_price(message.text):
        await state.update_data(agent_commission=message.text)
        await process_create_description(message, state)
    else:
        await message.reply(_('Введённая комиссия некорректна.'))
        await process_create_agent_commission(message, state)


@ad_create_router.message(AdCreate.price, F.text.casefold() == __('назад'))
async def process_create_description(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.description)
    await message.answer(
        _('Введите описание.'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.photo, F.text.casefold() == __('назад'))
@ad_create_router.message(AdCreate.description)
async def process_create_price(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AdCreate.description:
        await state.update_data(description=message.text)
    await state.set_state(AdCreate.price)
    await message.answer(
        _('Введите общую стоимость.'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.price)
async def process_validate_price(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if validate_price(message.text) and compare_values(message.text, data['agent_commission']):
        await state.update_data(price=message.text)
        await process_create_photo(message, state)
    else:
        await message.reply(_('Введённая cумма некорректна или меньше, чем комиссия для агента.'))
        await process_create_price(message, state)


@ad_create_router.message(AdCreate.complete, F.text.casefold() == __('назад'))
async def process_create_photo(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.photo)
    await message.answer(
        _('Загрузите фото объявления. Размер не должен превышать 10мб.'),
        reply_markup=get_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.photo, content_types=['photo', 'document'])
async def process_validate_photo(message: Message, state: FSMContext) -> None:
    if message.content_type == 'photo':
        await state.update_data(file_id=message.photo[-1].file_id)
        await process_create_complete(message, state)
    else:
        await message.reply(_('Загруженный файл не валиден.'))
        await process_create_photo(message, state)


async def process_create_complete(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.complete)
    data = await state.get_data()
    await message.answer_photo(
        photo=data['file_id'],
        caption=_(
            '{confirm}\n\n'
            'Адрec: {address}\n'
            'Назначение: {purpose}\n'
            'ЖК: {house}\n'
            'Общая площадь: {total_area}м²\n'
            'Площадь кухни: {kitchen_area}м²\n'
            'Комиссия агенту: {agent_commission} грн.\n'
            'Описание: {description}\n'
            'Цена: {price} грн.\n\n'
            'Всё верно?'
        ).format(
            confirm=html.bold(_('Подтвердите создание объявления!')),
            address=html.bold(data['address']),
            purpose=html.bold(get_purpose(data['purpose'])),
            house=html.bold(get_house(data['house'])) if data.get('house', False) else _('Не задано'),
            total_area=html.bold(data['total_area']),
            kitchen_area=html.bold(data['kitchen_area']),
            agent_commission=html.bold(data['agent_commission']),
            description=html.bold(data['description']),
            price=html.bold(data['price'])
        ),
        reply_markup=get_complete_creating_ad_and_back_or_back_to_profile_keyboard()
    )


@ad_create_router.message(AdCreate.complete)
async def process_create_confirm(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    from bot import bot

    file = await bot.get_file(data['file_id'])
    result: io.BytesIO = await bot.download_file(file.file_path)
    photo_base64 = base64.b64encode(result.read())

    json = {
        'address': data['address'],
        'house': data.get('house', None),
        'purpose': data['purpose'],
        'total_area': data['total_area'],
        'kitchen_area': data['kitchen_area'],
        'agent_commission': data['agent_commission'],
        'description': data['description'],
        'price': data['price'],
        "photos": [
            {
              "order": 1,
              "photo": photo_base64.decode('ascii')
            },
        ],
    }

    response = await client.build_create_ad_request(message.chat.id, json)
    if response:
        await message.answer(_('Создание объявления прошло успешно.'))
        await process_get_my_profile(message, state)
    else:
        await message.answer(
            _('Время сеанса истекло :('),
        )
        await process_authorization(message, state)
