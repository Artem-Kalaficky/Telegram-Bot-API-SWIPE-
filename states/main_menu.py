from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    main_menu = State()
    feed = State()
