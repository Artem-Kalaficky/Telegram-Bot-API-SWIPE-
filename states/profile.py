from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    get_profile = State()
    my_ads = State()
