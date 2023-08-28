
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from src.services.sql import DataBase
from src.bot import bot, dp
from aiogram.types import CallbackQuery

from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import datetime
from datetime import datetime, timedelta

from src.keyboards.menu import menu
db = DataBase('barber.db')
cb = CallbackData('btn', 'type', 'id')

async def cron(bot: Bot)


@dp.message_handler(content_types='photo')
async def photo(message: Message):
    print(message.photo[0].file_id)
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
    await bot.send_photo(callback.message.chat.id, photo='AgACAgIAAxkBAAPTZOyVCv4ugXh5_nNNR93ncQw7PWYAAkfOMRvCn2hLOPVLrx3k9scBAAMCAANzAAMwBA')
    await callback.answer()
@dp.callback_query_handler(lambda call: call.data == 'price')
async def a(callback: CallbackQuery):
    await bot.send_photo(callback.message.chat.id, photo='AgACAgIAAxkBAAPTZOyVCv4ugXh5_nNNR93ncQw7PWYAAkfOMRvCn2hLOPVLrx3k9scBAAMCAANzAAMwBA')
    await callback.answer()

@dp.callback_query_handler(lambda call: call.data == 'review')
async def a(callback: CallbackQuery):
    items = await db.get_filials()
    keyboard = InlineKeyboardMarkup()
    for i in items:
        keyboard.add(
            InlineKeyboardButton(f'{i[2]}', callback_data=f'btn:review:{i[1]}')
        )
    await bot.send_message(callback.message.chat.id, 'Выберите филиал в котором хотите оставить отзыв', reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(cb.filter(type='review'))
async def review(call: CallbackQuery, callback_data: dict):
    keyboard = InlineKeyboardMarkup()
    items = await db.get_info_filials(callback_data.get('id'))
    for i in items:
        keyboard.add(
            InlineKeyboardButton(f'Yandex карты', url=f'{i[3]}'),
            InlineKeyboardButton(f'Google карты', url=f'{i[4]}'),
            InlineKeyboardButton(f'2ГИС карты', url=f'{i[5]}')
        )
    await bot.send_message(call.message.chat.id, 'Вот отзывы данного филлиала', reply_markup=keyboard)
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == 'opp')
async def a(callback: CallbackQuery):
    keyboards = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='7 дней - "Стиль Брэд Пита"', callback_data='btn:opp:7'),
        InlineKeyboardButton(text='14 дней - "Четверг рекомендует"', callback_data='btn:opp:14'),
        InlineKeyboardButton(text='21 день - "Обросб но еще терпимо"', callback_data='btn:opp:21'),
        InlineKeyboardButton(text='28 дней - "Face_id тебя не узнает"', callback_data='btn:opp:28'),
    )
    await bot.send_message(callback.message.chat.id, 'Через сколько мне вам напомнить?', reply_markup=keyboards)
    await callback.answer()
@dp.callback_query_handler(cb.filter(type='opp'))
async def review(call: CallbackQuery, callback_data: dict):
    days = callback_data.get('id')
    days = int(days)
    datatime = datetime.today().date()
    datetime_opp = datatime + timedelta(days=days)
    await db.update_opp(datetime_opp, call.message.chat.id)

    await bot.send_message(call.message.chat.id, f'Хорошо, я напомню вам через {callback_data.get("id")} дней', reply_markup=menu.menu)