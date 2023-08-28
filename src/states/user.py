
from src.bot import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State


class NUMBER(StatesGroup):
    NUMBer = State()

class Machine(StatesGroup):
    number = State()
    adress = State()
    comment = State()

class Machine_data(StatesGroup):
    adr = State()

class COUNT(StatesGroup):
        COUNT = State()

class Add_cart(StatesGroup):
    photo = State()
    name = State()
    opp = State()
    price = State()
    stock = State()

class edit_cart(StatesGroup):
    stock = State()

class add_categoty(StatesGroup):
    name = State()

class update_category(StatesGroup):
    name = State()