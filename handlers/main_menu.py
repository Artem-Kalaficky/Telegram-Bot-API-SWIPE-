from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from keyboards.default.main_menu import get_main_menu_keyboard
from states.main_menu import Menu


async def process_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Menu.main_menu)
    await message.answer(
        _('Вы в главном меню бота. Выберите интерусующий вас пункт.'),
        reply_markup=get_main_menu_keyboard()
    )
