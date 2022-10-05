from aiogram.fsm.state import StatesGroup, State


class AdCreate(StatesGroup):
    address = State()
    purpose = State()
    house = State()
    total_area = State()
    kitchen_area = State()
    agent_commission = State()
    description = State()
    price = State()
    photo = State()
    complete = State()

