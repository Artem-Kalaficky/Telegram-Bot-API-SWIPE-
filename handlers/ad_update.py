from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from data.services.validators import validate_area, compare_values, validate_price
from handlers.authorization import process_authorization
from keyboards.default.ad_update import get_update_ad_keyboard, get_back_to_update_ad_keyboard
from keyboards.inline.profile import UpdateAdCallback
from api_requests.requests import UserAPIClient
from states.ad_update import AdUpdate


ad_update_router = Router()
client = UserAPIClient()


@ad_update_router.callback_query(UpdateAdCallback.filter(F.key_word == 'edit'))
async def callback_update_ad(query: CallbackQuery, callback_data: UpdateAdCallback, state: FSMContext):
    await state.update_data(ad_id=callback_data.ad_id)
    await state.set_state(AdUpdate.update)
    await process_update_ad(query.message, state)
    await query.answer()


@ad_update_router.message(AdUpdate.price, F.text.casefold() == __('вернуться к редактированию'))
@ad_update_router.message(AdUpdate.description, F.text.casefold() == __('вернуться к редактированию'))
@ad_update_router.message(AdUpdate.agent_commission, F.text.casefold() == __('вернуться к редактированию'))
@ad_update_router.message(AdUpdate.kitchen_area, F.text.casefold() == __('вернуться к редактированию'))
@ad_update_router.message(AdUpdate.total_area, F.text.casefold() == __('вернуться к редактированию'))
@ad_update_router.message(AdUpdate.address, F.text.casefold() == __('вернуться к редактированию'))
async def process_update_ad(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.update)
    await message.answer(
        _('Выберите пункт для редактирования объявления'),
        reply_markup=get_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('адрес'))
async def process_update_address(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.address)
    await message.answer(
        _('Введите адрес'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('общая площадь'))
async def process_update_total_area(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.total_area)
    await message.answer(
        _('Введите общую площадь'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('площадь кухни'))
async def process_update_kitchen_area(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.kitchen_area)
    await message.answer(
        _('Введите площадь кухни'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('комиссия агенту'))
async def process_update_agent_commission(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.agent_commission)
    await message.answer(
        _('Введите комиссию для агента'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('описание'))
async def process_update_description(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.description)
    await message.answer(
        _('Введите описание'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.update, F.text.casefold() == __('цена'))
async def process_update_price(message: Message, state: FSMContext):
    await state.set_state(AdUpdate.price)
    await message.answer(
        _('Введите цену'),
        reply_markup=get_back_to_update_ad_keyboard()
    )


@ad_update_router.message(AdUpdate.price)
@ad_update_router.message(AdUpdate.description)
@ad_update_router.message(AdUpdate.agent_commission)
@ad_update_router.message(AdUpdate.kitchen_area)
@ad_update_router.message(AdUpdate.total_area)
@ad_update_router.message(AdUpdate.address)
async def process_confirm_update_add(message: Message, state: FSMContext):
    data = await state.get_data()
    ad_id = data.get('ad_id')
    ad = await client.build_get_ad_request(message.chat.id, ad_id)
    if ad:
        current_state = await state.get_state()

        if current_state == AdUpdate.address:
            ad['address'] = message.text
        if current_state == AdUpdate.total_area:
            if validate_area(message.text) and compare_values(message.text, ad['kitchen_area']):
                ad['total_area'] = float(message.text)
            else:
                await message.reply(_('Введённая площадь некорректна или меньше, чем площадь кухни.'))
                await process_update_total_area(message, state)
                return
        if current_state == AdUpdate.kitchen_area:
            if validate_area(message.text) and compare_values(ad['total_area'], message.text):
                ad['kitchen_area'] = float(message.text)
            else:
                await message.reply(_('Введённая площадь некорректна или превышает общую площадь.'))
                await process_update_kitchen_area(message, state)
                return
        if current_state == AdUpdate.agent_commission:
            if validate_price(message.text) and compare_values(ad['price'], message.text):
                ad['agent_commission'] = float(message.text)
            else:
                await message.reply(_('Введённая сумма некорректна или превышает общую сумму.'))
                await process_update_agent_commission(message, state)
                return
        if current_state == AdUpdate.description:
            ad['description'] = message.text
        if current_state == AdUpdate.price:
            if validate_price(message.text) and compare_values(message.text, ad['agent_commission']):
                ad['price'] = float(message.text)
            else:
                await message.reply(_('Введённая сумма некорректна или меньше, чем комиссия для агента.'))
                await process_update_price(message, state)
                return

        update_data = {
            'address': ad['address'],
            'total_area': ad['total_area'],
            'kitchen_area': ad['kitchen_area'],
            'agent_commission': ad['agent_commission'],
            'description': ad['description'],
            'price': ad['price'],
            'photos_order': [],
            "photos": [],
        }
        response = await client.build_update_ad_request(message.chat.id, ad_id, update_data)
        if response:
            await message.answer(_('Объявление успешно обновлено!'))
        else:
            await message.answer(_('Обновление не успешно! Введённые данные были некорректны'))
        await process_update_ad(message, state)
    else:
        await message.answer(_('Время сеанса истекло :('))
        await process_authorization(message)
