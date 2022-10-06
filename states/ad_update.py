from aiogram.fsm.state import StatesGroup, State


class AdUpdate(StatesGroup):
    update = State()
    address = State()
    total_area = State()
    kitchen_area = State()
    agent_commission = State()
    description = State()
    price = State()
