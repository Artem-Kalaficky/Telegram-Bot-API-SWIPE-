from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default.main_menu import main_menu_keyboard
from states.main_menu import Menu


async def process_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Menu.main_menu)
    await message.answer(
        'Вы в главном меню бота. Выберите интерусующий вас пункт.',
        reply_markup=main_menu_keyboard
    )
