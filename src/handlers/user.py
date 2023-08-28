
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from src.services.sql import DataBase
from src.bot import bot, dp
from src.states.user import NUMBER

from src.keyboards.menu import keyboards
db = DataBase('piro_database.db')

@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}👋\n\nМы рады,'
                                            f' что Вы выбрали наш магазин.'
                                            f' Надеемся, Вы найдете что-то интересное в нашем ассортименте!\n\n'
                                            f'Для начала зарегистрируемся. Введите номер телефона (8XXXXXXXXXX), что бы курьер смог с вами связаться.')
    await NUMBER.NUMBer.set()

