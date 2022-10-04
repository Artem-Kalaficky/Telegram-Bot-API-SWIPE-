from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from keyboards.default.profile import get_back_to_profile_keyboard
from requests import UserAPIClient
from states.ad_create import AdCreate
from states.profile import Profile


ad_create_router = Router()
client = UserAPIClient()


@ad_create_router.message(Profile.get_profile, F.text.casefold() == 'создать объявление')
async def process_create_ad(message: Message, state: FSMContext) -> None:
    await state.set_state(AdCreate.address)
    await message.answer(
        'Введите адрес',
        reply_markup=get_back_to_profile_keyboard()
    )
