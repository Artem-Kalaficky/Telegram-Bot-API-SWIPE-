from aiogram.fsm.state import StatesGroup, State


class AdCreate(StatesGroup):
    address = State()
