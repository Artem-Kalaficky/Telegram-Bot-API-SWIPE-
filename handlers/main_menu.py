from aiogram import F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from data.services.get_image import get_photo
from handlers.profile import main_menu_router
from keyboards.default.main_menu import get_main_menu_keyboard, get_back_to_main_menu_keyboard
from keyboards.inline.main_menu import get_feed_inline_keyboard, FeedCallback
from requests import UserAPIClient
from states.main_menu import Menu
from states.profile import Profile


client = UserAPIClient()


@main_menu_router.message(Menu.feed, F.text.casefold() == __('главное меню'))
@main_menu_router.message(Profile.get_profile, F.text.casefold() == __('главное меню'))
async def process_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Menu.main_menu)
    await message.answer(
        _('Вы в главном меню бота. Выберите интерусующий вас пункт.'),
        reply_markup=get_main_menu_keyboard()
    )


@main_menu_router.message(Menu.main_menu, F.text.casefold() == 'лента объявлений')
async def process_show_feed(message: Message, state: FSMContext) -> None:
    await state.set_state(Menu.feed)
    await message.answer(
        'Вы в ленте объявлений. Листайте объявления от новых к более устаревшим по нажатию клавиш',
        reply_markup=get_back_to_main_menu_keyboard()
    )
    await process_show_one_ad_in_feed(message, message.chat.id, 0)


@main_menu_router.callback_query(FeedCallback.filter(F.key_word == 'geo'))
async def feed_callback_location(query: CallbackQuery, callback_data: FeedCallback):
    await query.message.answer_location(
        46.43986040880162, 30.757641993864407
    )


@main_menu_router.callback_query(FeedCallback.filter(F.key_word == 'next'))
async def feed_callback_next(query: CallbackQuery, callback_data: FeedCallback):
    current_position = callback_data.position + 1
    await process_show_one_ad_in_feed(query.message, query.message.chat.id, current_position)


@main_menu_router.callback_query(FeedCallback.filter(F.key_word == 'previous'))
async def feed_callback_previous(query: CallbackQuery, callback_data: FeedCallback):
    current_position = callback_data.position - 1
    if current_position >= 0:
        await process_show_one_ad_in_feed(query.message, query.message.chat.id, current_position)
    else:
        await query.message.answer('Данное объявление - первое в ленте. Возврат к "предыдущему" объявлению невозможен.')


async def process_show_one_ad_in_feed(message: Message, user_id, position):
    response = await client.build_get_feed_request(user_id)
    if response:
        ad = response[position]
        await message.answer_photo(
            photo=get_photo(ad.get('main_photo', False)),
            caption='Адрес: {address}\n'
                    'Цена: {price}\n'
                    'Дата создания: {date_created}'.format(
                address=html.bold(ad.get("address")),
                price=html.bold(ad.get("price")),
                date_created=html.italic(ad.get("date_created"))
            ),
            reply_markup=get_feed_inline_keyboard(position)
        )
    else:
        from .authorization import process_authorization

        await message.answer(
            _('Время сеанса истекло :('),
        )
        await process_authorization(message)
