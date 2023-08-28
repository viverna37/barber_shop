
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from src.services.sql import DataBase
from src.bot import bot, dp
from aiogram.types import CallbackQuery

from src.keyboards.menu import menu
db = DataBase('barber.db')

@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}👋'
                                            f'\n\n Рыда вас приветствовать в нашем боте барбер-щопа "Четверг"'
                                            f'\n\n Здесь приведут вашу голову в порядок💆'
                                            f'\n\nИспользуйте кнопки в меню ниже👇👇👇')
    if await db.get_users(message.chat.id) == None:
        await db.add_users(message.chat.id)
    await message.reply("💈ОСНОВНОЕ МЕНЮ💈", reply_markup=menu.menu)

@dp.callback_query_handler(lambda call: call.data == 'action')
async def a(callback: CallbackQuery):
    await bot.send_photo(callback.message.chat.id, photo='')

