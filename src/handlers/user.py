from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from src.services.sql import DataBase
from src.bot import bot, dp
from aiogram.types import CallbackQuery
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import Bot

import datetime
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.states.user import User
from src.keyboards.menu import menu
db = DataBase('barber.db')
cb = CallbackData('btn', 'type', 'id')
sheduler = AsyncIOScheduler(timezone='Europe/Moscow')
async def cron(bot: Bot):
    user_id = await db.get_userss()
    for i in user_id:
        datetime_str = await db.get_opp(f'{i[0]}')
        datetime_str = str(datetime_str[0][0])
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d')

        if datetime_obj.date() == datetime.today().date():
            await bot.send_message(i[0], f'С вашей последней стрижки прошло дочтаточно времени, пора бы подстричься')


@dp.message_handler(content_types='photo')
async def photo(message: Message):
    print(message.photo[0].file_id)
@dp.message_handler(Command('start'))
async def start(message: Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}👋'
                                            f'\n\n Рады Вас приветствовать в нашем боте барбершоп "Четверг"'
                                            f'\n\n Здесь приведут вашу голову в порядок💆'
                                            f'\n\nИспользуйте кнопки в меню ниже👇👇👇')
    if await db.get_users(message.chat.id) == None:
        await db.add_users(message.chat.id)
    await bot.send_message(message.chat.id, "💈ОСНОВНОЕ МЕНЮ💈", reply_markup=menu.menu)

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
    await bot.send_message(callback.message.chat.id, 'Выберите филиал, о котором хотите оставить отзыв', reply_markup=keyboard)
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
        InlineKeyboardButton(text='7 дней - "Стиль Брэда Пита"', callback_data='btn:opp:7'),
        InlineKeyboardButton(text='14 дней - "Четверг рекомендует"', callback_data='btn:opp:14'),
        InlineKeyboardButton(text='21 день - "Оброс, но еще терпимо"', callback_data='btn:opp:21'),
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
    sheduler.add_job(cron, kwargs={'bot': bot},
                     trigger='interval',
                     days=1)
    sheduler.start()
    await db.update_opp(datetime_opp, call.message.chat.id)
    await bot.send_message(call.message.chat.id, f'Хорошо, я напомню вам через {callback_data.get("id")} дней', reply_markup=menu.menu)

@dp.callback_query_handler(lambda call: call.data == 'adres')
async def a(callback: CallbackQuery):
    items = await db.get_filials()
    keyboard = InlineKeyboardMarkup()
    for i in items:
        keyboard.add(
            InlineKeyboardButton(f'{i[2]}', url=f'{i[6]}')
        )
    await bot.send_message(callback.message.chat.id, 'Канал этого филиала👇',
                           reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(lambda call: call.data == 'contacts')
async def a(callback: CallbackQuery):
    await bot.send_message(callback.message.chat.id, 'Наши контакты'
                                                     '\n\n Номер телефона: +79677636976', reply_markup=InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('Vk', url='https://vk.com/4etvergnn'),
        InlineKeyboardButton('Inst', url='https://goo.su/k4hp4V0')
    ))

@dp.callback_query_handler(lambda call: call.data == 'questions')
async def a(callback: CallbackQuery):
    await bot.send_message(callback.message.chat.id, 'Напишите ваш вопрос. Ответим быстрее чем барбер подстрижет двух людей⚡️'
                                                     '\n\nЧтобы вернуться в главное меню нажмите "Назад"', reply_markup=menu.back)

    await User.questions.set()

@dp.message_handler(text='Назад', state=User.questions)
async def a(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, ''
                                            '\n\nМы перенесли вас в главное меню', reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(content_types='text', state=User.questions)
async def a(message: Message, state: FSMContext):
    text = message.text
    await bot.send_message(chat_id='-1001930660607', text='<b>Вопрос</b>'
                                                          f'\n\n{text}'
                                                          f'\n\nВопрос задал @{message.from_user.username}',
                           parse_mode=types.ParseMode.HTML)
    await bot.send_message(message.chat.id, 'Спасибо за вопрос, уже пишем на него ответ.'
                                            '\n\nМы перенесли вас в главное меню', reply_markup=menu.menu)
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'queue')
async def a(callback: CallbackQuery):
    items = await db.get_filials()
    keyboard = InlineKeyboardMarkup()
    for i in items:
        keyboard.add(
            InlineKeyboardButton(f'{i[2]}', url=f'{i[7]}')
        )
    await bot.send_message(callback.message.chat.id, 'Выберите филиал',
                           reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'about_we')
async def a(callback: CallbackQuery):
    await bot.send_photo(callback.message.chat.id, photo='AgACAgIAAxkBAAIBVmTsthaAmNvPd-viN9IuwGPwpttHAAJGzjEbwp9oSxmCbWP2IuYkAQADAgADcwADMAQ', caption=''
                                                                     '\n\nПривет! Мы сеть барбершопов "Четверг" - территория мужского стиля. У нас крутая атмосфера и качество для тех, кто ценит свое время.'
                                                                     '\n\n🗓Стрижем без записи с 10:00 до 21:00 '
                                                                     '\n\n📝Работаем без записи '
                                                                     '\n\n💰Стрижки от 200 рублей'
                                                                     '\n\n🤌 Шестая стрижка бесплатно '
                                                                     '\n\n⏱ Время стрижки 30 минут'
                                                                     '\n\n☎️ +7 (967)-763-69-76')