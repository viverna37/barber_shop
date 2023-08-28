from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData


from src.services.sql import DataBase
from src.bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message

from src.keyboards.menu import menu

import base64

#methods
cb = CallbackData('btn', 'type', 'product_id', 'categori_id', 'count')
db = DataBase('barber.db')
