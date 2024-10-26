from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    user_name = State()
    user_group = State()


class AddPoints(StatesGroup):
    tg_member_id = State()
    points_type = State()
    num = State()