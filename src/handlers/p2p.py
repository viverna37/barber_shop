from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.utils.callback_data import CallbackData




from src.states.user import Machine

from src.mess import MESSAGES
from src.config import Config
from src.bot import bot, dp
from src.services.sql import DataBase

import string
import random
from yoomoney import Quickpay, Client


import string
import random
from yoomoney import Quickpay




db = DataBase('piro_database.db')
cb = CallbackData('btn', 'action')

@dp.message_handler(Command('p2p_start'))
async def p2p_start(message: Message):
    try:
        await db.add_users(message.chat.id)
    except Exception as e:
        pass
    finally:
        await message.reply('Привет!!!')

@dp.message_handler(Command('p2p_buy'))
async def p2p_buy(message: Message):
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 10))
    quickpay = Quickpay(
        receiver='4100118138252391',
        quickpay_form='shop',
        targets='Test',
        paymentType='SB',
        sum=2,
        label=rand_string
    )

    await db.update_label(rand_string, message.chat.id)

    claim_keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
    claim_keyboard.add(InlineKeyboardButton(text='Перейти к оплате!',
                                            url=quickpay.redirected_url))
    claim_keyboard.add(InlineKeyboardButton(text='Получить товар!',
                                            callback_data='btn:claim'))
    await bot.send_message(message.chat.id,
                           MESSAGES['buy'],
                           reply_markup=claim_keyboard)

@dp.callback_query_handler(cb.filter(action='claim'))
async def check_payment(call: CallbackQuery):
    data = await db.get_payment_status(call.message.chat.id)
    bought = data[0][0]
    label = data[0][1]
    if bought == 0:
        client = Client(Config.token_p2p)
        history = client.operation_history(label=label)
        try:
            operation = history.operations[-1]
            if operation.status == 'success':





                await db.update_payment_status(call.message.chat.id)
                await bot.send_message(call.message.chat.id,
                                       MESSAGES['successful_payment'])



        except Exception as e:
            await bot.send_message(call.message.chat.id,
                                   MESSAGES['wait_message'])

    else:

        a = 0
        product_id1 = await db.view_cart(call.message.chat.id)
        product_id = list(filter(lambda x: not None in x, product_id1))
        N = 'https://t.me/'
        Messi = ''
        MES = ''
        for i in product_id:
            name = await db.name(i[0])
            name1 = (str(name).strip("[('',)],"))
            count = await db.count(i[0], call.message.chat.id)
            count1 = (str(count).strip("[('',)],"))
            Messi += f'Наименование: {name1}, {count1}шт\n'
            N += f'{call.from_user.username}'
            data2 = await db.get_count_in_stock(i[0])
            data1 = (str(data2).strip("[('',)],"))
            data = int(data1)
            stock = data - int(count1)
            await db.update_stock(stock, i[0])
        number = await db.wiev_num(call.message.chat.id)
        number1 = (str(number).strip("[('',)],"))
        adres = await db.wiev_adres(call.message.chat.id)
        adres1 = (str(adres).strip("[('',)],"))
        comment = await db.wiev_comment(call.message.chat.id)
        comment1 = (str(comment).strip("[('',)],"))
        MES += f'Номер телефона: {number1}\nАдресс: {adres1}\nПозиции:\n{Messi}\nАккаунт: {N}\nКоментарий: {comment1}'
        await bot.send_message(chat_id=Config.chanel_id, text=(f'{MES}'))
        await db.empty_cart(call.message.chat.id)
        await db.unupdate_payment_status(call.message.chat.id)
        await bot.send_message(call.message.chat.id,
                               MESSAGES['successful_payment'])


