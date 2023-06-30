from aiogram.dispatcher.filters.state import StatesGroup, State


class FormOne(StatesGroup):
    name = State()
    phone = State()
    email = State()


class FormFour(StatesGroup):
    situation = State()
    price = State()
    reg_home = State()
    reg_auto = State()
    reg_deposit = State()
    transactions = State()
    activity = State()
    family = State()
    parents = State()