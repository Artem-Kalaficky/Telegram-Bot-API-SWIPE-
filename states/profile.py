from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    get_profile = State()
    my_ads = State()
    update_data = State()
    update_last_name = State()
    update_first_name = State()
    update_telephone = State()
    update_email = State()
