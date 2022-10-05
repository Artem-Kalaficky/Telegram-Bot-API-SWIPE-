from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline.profile import UpdateAdCallback
from requests import UserAPIClient

ad_update_router = Router()
client = UserAPIClient()


@ad_update_router.callback_query(UpdateAdCallback.filter(F.key_word == 'edit'))
async def feed_callback_next(query: CallbackQuery, callback_data: UpdateAdCallback):
    pass