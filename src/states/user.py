
from src.bot import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    questions = State()