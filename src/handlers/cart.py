from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from src.states.user import Machine, COUNT, Add_cart, edit_cart, add_categoty, update_category, NUMBER

from src.services.sql import DataBase
from src.bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message

from src.keyboards.menu import keyboards

import base64

#methods
cb = CallbackData('btn', 'type', 'product_id', 'categori_id', 'count')
db = DataBase('piro_database.db')







#number_phone, STATE_MACHINE
@dp.message_handler(text=('Редактировать'), state=NUMBER.NUMBer)
async def next(message: types.Message, state: FSMContext):
    data = await db.admin(message.chat.id)
    if data[0][0] == 1:
        await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboards.admin)
        await state.finish()
    else:
        pass

@dp.message_handler(text=('Изменить'), state=NUMBER.NUMBer)    
async def next(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Введите номер телефона')


@dp.message_handler(text=('Продолжить'), state=NUMBER.NUMBer)    
async def next(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Выберите действие', reply_markup=keyboards.menu)
    await state.finish()
    
@dp.message_handler(lambda message: not message.text.isdigit(), state=NUMBER.NUMBer)
async def number(message: types.Message):
    await bot.send_message(message.chat.id, 'Не поддерживаемый формат')

@dp.message_handler(content_types=['text'], state=NUMBER.NUMBer)
async def number(message: types.Message, state: FSMContext) -> None:
    data = message.text
    await db.number(message.chat.id, data)
    await bot.send_message(message.from_user.id, f'Номер {data} зарегистрирован', reply_markup=keyboards.supmenu)
    await bot.send_message(message.chat.id, 'Все верно?')





#menu
@dp.message_handler(text=('Товары'))
async def start(message: Message):
    data = await db.get_categories()
    categories = InlineKeyboardMarkup()
    for i in data:
        categories.add(InlineKeyboardButton(text = f'{i[0]}', callback_data=f"btn:categori:-:{i[1]}:-"))
    await bot.send_message(message.chat.id, f'Наш ассортимент:', reply_markup=categories)
    await bot.delete_message(message.chat.id, message.message_id)

@dp.callback_query_handler(cb.filter(type='categori'))
async def goods(call: CallbackQuery, callback_data: dict):
    data = await db.get_products(callback_data.get('categori_id'))
    keyboard = await gen_products(data, call.message.chat.id)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type='view'))
async def wiev(call: CallbackQuery, callback_data: dict):
    data = await db.products(callback_data.get('product_id'), callback_data.get('categori_id'))
    count = await db.get_count_in_cart_mb(call.message.chat.id, callback_data.get('product_id'))
    count = str(count).strip("[('',)]")
    for i in data:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='В корзину', callback_data=f'btn:cart:{i[1]}:{i[5]}:-')).add(InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[1]}:{i[5]}:-'), InlineKeyboardButton(text=f'{count} шт', callback_data=f'btn:count_btn:-:-:{i[1]}'), InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[1]}:{i[5]}'))\
            .add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:{i[1]}:{i[5]}:-'))
        await bot.send_photo(call.message.chat.id, photo=f'{i[6]}', caption=f'Наименование: {i[2]} \nОписание:{i[7]}\nЦена: {i[3]}p \nКоличество на складе: {i[4]}', reply_markup=keyboard)


async def qw(data, user_id, count):
    count1 = (str(count).strip("[('',)]"))
    count2 = int(count1)

    for i in data:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='В корзину', callback_data=f'btn:cart:{i[1]}:{i[5]}:-')).add(InlineKeyboardButton(text='🔼', callback_data=f'btn:plus:{i[1]}:{i[5]}:{count}'), InlineKeyboardButton(text=f'{count2} шт', callback_data=f'btn:count_btn:-:-:{i[5]}'), InlineKeyboardButton(text='🔽', callback_data=f'btn:minus:{i[1]}:{i[5]}:{count}'))\
            .add(InlineKeyboardButton(text='Назад', callback_data=f'btn:back:{i[1]}:{i[5]}:-'))
    return keyboard

@dp.callback_query_handler(cb.filter(type="plus"))
async def plus(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart_mb = await db.get_count_in_cart_mb(call.message.chat.id, product_id)
    count_in_stock = await db.get_count_in_stock(product_id)
    if count_in_stock[0][0] == 0:
        await bot.send_message(call.message.chat.id, 'Товара нет в наличии')
        return 0
    elif not count_in_cart_mb or count_in_cart_mb[0][0] == 0:
        await db.add_to_cart_mb(call.message.chat.id, product_id, 1)
    elif count_in_stock[0][0]>count_in_cart_mb[0][0]:
        await db.change_count_mb(count_in_cart_mb[0][0]+1, call.message.chat.id, product_id)
    else:
        await bot.send_message(call.message.chat.id, 'Больше товара в наличии нет')
        return 0
    count_in_cart_mb = await db.get_count_in_cart_mb(call.message.chat.id, product_id)
    data = await db.products(callback_data.get('product_id'), callback_data.get('categori_id'))
    keyboard = await  qw(data, call.message.chat.id, count_in_cart_mb)

    await call.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(cb.filter(type="minus"))
async def plus(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('product_id')
    count_in_cart_mb = await db.get_count_in_cart_mb(call.message.chat.id, product_id)
    if not count_in_cart_mb or count_in_cart_mb[0][0] == 0:
        await bot.send_message(call.message.chat.id, 'Количество товара не выбрано')
        return 0
    elif count_in_cart_mb[0][0] == 1:
        mb = 0
        await db.remowe_one_item_mb(mb, call.message.chat.id, product_id)
        
    else:
        await db.change_count_mb(count_in_cart_mb[0][0] - 1, call.message.chat.id, product_id)
    count_in_cart_mb = await db.get_count_in_cart_mb(call.message.chat.id, product_id)
    data = await db.products(callback_data.get('product_id'), callback_data.get('categori_id'))
    keyboard = await  qw(data, call.message.chat.id, count_in_cart_mb)

    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(cb.filter(type="back"))
async def asdf(call: CallbackQuery, callback_data: dict):
    data = await db.get_products(callback_data.get('categori_id'))
    # await bot.send_message(call.message.chat.id, f'{data}')
    keyboard = await gen_products(data, call.message.chat.id)
    await bot.send_message(call.message.chat.id, f'Наш ассортимент:', reply_markup=keyboard)
    # data = await db.get_categories()
    # keyboard = InlineKeyboardMarkup()
    # for i in data:
    #     keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:categori:-:{i[1]}:-'))
    # await call.bot.send_message(call.message.chat.id, 'Выберите категорию', reply_markup=keyboard)

@dp.callback_query_handler(cb.filter(type="back1"))
async def asdf(call: CallbackQuery, callback_data: dict):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'btn:categori:-:{i[1]}:-'))
    await call.bot.send_message(call.message.chat.id, 'Выберите категорию', reply_markup=keyboard)

@dp.callback_query_handler(cb.filter(type='cart'))
async def wiev(call: CallbackQuery, callback_data: dict):
    count = await db.get_count_in_cart_mb(call.message.chat.id, callback_data.get('product_id'))
    await db.add_to_cart(count[0][0], call.message.chat.id, callback_data.get('product_id'))
    await bot.send_message(call.from_user.id, 'Товар добавлен в корзину')
#conact_information
@dp.message_handler(text=('Контактная информация'))
async def start(message: Message):
    await bot.send_message(message.chat.id, '<b>Контактная информация:</b>\n'
                                            '<b>Номер телефона: </b>89621193001\n'
                                            '<b>Почта: </b>alexnervous1@gmail.com\n'
                                            '<b>Адресс: </b> г. Александровск - Сахалинский',
                           parse_mode=types.ParseMode.HTML)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#cart_wiev
@dp.message_handler(text=('Моя корзина'))
async def start(message: Message):
    items1 = await db.view_cart(message.chat.id)
    items = list(filter(lambda x: not None in x, items1))

    if len(items) == 0:
        await bot.send_message(message.chat.id, 'Ваша корзина пуста\nПожалуйста, выберите товар в меню')
    else:
        pr = ''
        Mess = 'Товары, добавленные в корзину:\n'
        for item in items:
            name1 = await db.name(item[0])
            name = (str(name1).strip("[('',)],"))
            count3 = await db.count(item[0], message.chat.id)
            count2 = list(filter(lambda x: not None in x, count3))
            count1 = (str(count2).strip("[('',)],"))
            # count1 = int(count2[1][0])
            count = int(count1)
            # await bot.send_message(message.chat.id, f'{count}')
            price1 = await db.price(item[0])
            price = (str(price1).strip("[('',)],"))
            all_price2 = await db.price(item[0])
            all_price1 = (str(all_price2).strip("[('',)],"))
            all_price = int(all_price1) * int(count)
            pr += f'{all_price} '
            Mess += f'\n<b>{name}: {count}шт, цена: {price} руб</b>\n'
            nums_sum = round(sum(int(x) for x in pr.split()), 2)
        await bot.send_message(message.chat.id, text=(f'{Mess}\n<b>Итого: {nums_sum} руб</b>'),parse_mode=types.ParseMode.HTML, reply_markup=keyboards.korzina)

# #cart_clear
@dp.message_handler(text=('Очистить'))
async def empty_cart(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await db.empty_cart(message.chat.id)
    await message.answer('Корзина очищена')
#BACK
@dp.message_handler(text=('Назад'))
async def empty_cart(message: Message):
    await message.answer("Выберите категорию:", reply_markup=keyboards.menu)
#payments
@dp.message_handler(text=('Оплатить'))
async def buy_process(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    data1 = await db.view_cart(message.chat.id)
    data = list(filter(lambda x: not None in x, data1))
    if len(data) == 0:
        await bot.send_message(message.chat.id, 'Коризна пуста\nПожалуйста выберите в меню')
    else:
        await bot.send_message(message.chat.id, 'Пожалуйста введите адресс доставки')
        await Machine.adress.set()
#MACHINE_STATE_adres&P2P
@dp.message_handler(content_types=['text'], state=Machine.adress)
async def adres(message: types.Message, state: FSMContext) -> None:

    adres1 = message.text
    await db.adres(adres1, message.chat.id)

    await bot.send_message(message.chat.id, f'Адрес записан\nНапишите комментарий к заказу или пропустите этот пункт', reply_markup=keyboards.yorn)
    await Machine.next()

@dp.message_handler(text=('Пропустить'), state=Machine.comment)
async def next(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Клавиатура сменена", reply_markup=keyboards.korzina)
    await state.finish()
    data1 = await db.view_cart(message.chat.id)
    data = list(filter(lambda x: not None in x, data1))
    if len(data) == 0:
        await bot.send_message(message.chat.id, 'Коризна пуста\nПожалуйста выберите в меню')
    else:
        product_id1 = await db.view_cart(message.chat.id)
        product_id = list(filter(lambda x: not None in x, product_id1))
        nnn = ''
        for i in product_id:
            all_price2 = await db.price(i[0])
            all_price1 = (str(all_price2).strip("[('',)],"))
            count2 = await db.count(i[0], message.chat.id)
            count1 = (str(count2).strip("[('',)],"))
            count = int(count1)
            all_price = int(all_price1) * int(count)
            nnn += f'{all_price} '

            nums_sum = round(sum(int(x) for x in nnn.split()), 2)
            print(nums_sum)

        letters_and_digits = string.ascii_lowercase + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        quickpay = Quickpay(
            receiver='4100118138252391',
            quickpay_form='shop',
            targets='Test',
            paymentType='SB',
            sum=nums_sum,
            label=rand_string
        )

        await db.update_label(rand_string, message.chat.id)

        claim_keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
        claim_keyboard.add(InlineKeyboardButton(text='Оплатить',
                                                    url=quickpay.redirected_url))
        claim_keyboard.add(InlineKeyboardButton(text='Проверить оплату',
                                                    callback_data='btn:claim'))
        await bot.send_message(message.chat.id,
                                text = ('Оплатите заказ, нажав кнопку ниже\nПосле оплаты обязательно нажмите кнопку "Проверить оплату"'),
                                reply_markup=claim_keyboard)


@dp.message_handler(content_types=['text'], state=Machine.comment)
async def adres(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(message.chat.id, "Клавиатура сменена", reply_markup=keyboards.korzina)

    comment = message.text
    await db.comment(comment, message.chat.id)
    await state.finish()
    data1 = await db.view_cart(message.chat.id)
    data = list(filter(lambda x: not None in x, data1))
    if len(data) == 0:
        await bot.send_message(message.chat.id, 'Коризна пуста\nПожалуйста выберите в меню')
    else:
        product_id1 = await db.view_cart(message.chat.id)
        product_id = list(filter(lambda x: not None in x, product_id1))
        nnn = ''
        for i in product_id:
            all_price2 = await db.price(i[0])
            all_price1 = (str(all_price2).strip("[('',)],"))
            count2 = await db.count(i[0], message.chat.id)
            count1 = (str(count2).strip("[('',)],"))
            count = int(count1)
            all_price = int(all_price1) * int(count)
            nnn += f'{all_price} '

            nums_sum = round(sum(int(x) for x in nnn.split()), 2)
            print(nums_sum)

        letters_and_digits = string.ascii_lowercase + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        quickpay = Quickpay(
            receiver='4100118138252391',
            quickpay_form='shop',
            targets='Test',
            paymentType='SB',
            sum=nums_sum,
            label=rand_string
        )

        await db.update_label(rand_string, message.chat.id)

        claim_keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
        claim_keyboard.add(InlineKeyboardButton(text='Оплатить',
                                                    url=quickpay.redirected_url))
        claim_keyboard.add(InlineKeyboardButton(text='Проверить оплату',
                                                    callback_data='btn:claim'))
        await bot.send_message(message.chat.id,
                                text = ('Оплатите заказ, нажав кнопку ниже\nПосле оплаты обязательно нажмите кнопку "Проверить оплату"'),
                                reply_markup=claim_keyboard)

#                                                                                   AMIN_PANEL

@dp.message_handler(text=('Редактировать'))
async def start(message: Message):
    data = await db.admin(message.chat.id)
    if data[0][0] == 1:
        await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboards.admin)
    else:
        pass

cbd = CallbackData('butn', 'type', 'product_id', 'category_id')
forms = {
    'category': 1,
    'img': 1,
    'name': 1,
    'opp': 1,
    'price': 1,
    'stock': 1,
    'name_category': 1
}

stock = {
    "product_id": 1
}


@dp.message_handler(text=('Добавить карточку'))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup()
    data = await db.get_categories()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'butn:category:-:{i[1]}'))
    await bot.send_message(message.chat.id, 'Выберите категорию в которой будет находиться карточка', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='category'))
async def category(call: CallbackQuery, callback_data: dict):
    await bot.send_message(call.message.chat.id, 'Отправьте фотографию для карточки')
    forms['category'] = callback_data.get('category_id')
    await Add_cart.photo.set()

@dp.message_handler(content_types=['photo'], state=Add_cart.photo)
async def number(message: types.Message, state: FSMContext) -> None:
    photo = message.photo[0].file_id
    forms['img'] = photo
    await bot.send_message(message.chat.id, "Введите имя товара для карточки")
    await Add_cart.next()

@dp.message_handler(content_types=['text'], state=Add_cart.name)
async def number(message: types.Message, state: FSMContext) -> None:
    name = message.text
    forms['name'] = name
    await bot.send_message(message.chat.id, "Введите описание товара для карточки")
    await Add_cart.next()

@dp.message_handler(content_types=['text'], state=Add_cart.opp)
async def number(message: types.Message, state: FSMContext) -> None:
    opp = message.text
    forms['opp'] = opp
    await bot.send_message(message.chat.id, "Введите цену товара для карточки")
    await Add_cart.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Add_cart.price)
async def number(message: types.Message):
    await bot.send_message(message.chat.id, 'Пожалуйста, введите число без буквенных значений')

@dp.message_handler(content_types=['text'], state=Add_cart.price)
async def number(message: types.Message, state: FSMContext) -> None:
    price = message.text
    forms['price'] = price
    await bot.send_message(message.chat.id, "Введите кол-во товара на складе для карточки")
    await Add_cart.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Add_cart.stock)
async def number(message: types.Message):
    await bot.send_message(message.chat.id, 'Пожалуйста, введите число без буквенных значений')

@dp.message_handler(content_types=['text'], state=Add_cart.stock)
async def number(message: types.Message, state: FSMContext) -> None:
    stock = message.text
    forms['stock'] = stock
    await db.add_cart_photo(forms['name'], forms['price'], forms['stock'], forms['category'], forms['img'], forms['opp'])
    await bot.send_message(message.chat.id, "Заполнение окончено, карточка добавлена в выбранную категорию")
    await state.finish()


@dp.message_handler(text=('Удалить карточку'))
async def start(message: Message):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'butn:del_product:-:{i[1]}'))
    await bot.send_message(message.chat.id, 'Из какой категории вы бы хотели удалить карточку?', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='del_product'))
async def category(call: CallbackQuery, callback_data: dict):
    data = await db.get_products(callback_data.get('category_id'))
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[2]}', callback_data=f'butn:del_products:{i[1]}:-'))
    await bot.send_message(call.message.chat.id, 'Какую карточку вы бы хотели удалить?', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='del_products'))
async def category(call: CallbackQuery, callback_data: dict):
    await db.del_cart(callback_data.get('product_id'))
    await db.del_product(callback_data.get('product_id'))
    await bot.send_message(call.message.chat.id, 'Карточка удалена')


@dp.callback_query_handler(cbd.filter(type='product'))
async def category(call: CallbackQuery, callback_data: dict):
    await db.del_cart(callback_data.get('product_id'))
    await bot.send_message(call.message.chat.id, 'Карточка удалена')


@dp.message_handler(text=('Редактировать карточку'))
async def start(message: Message):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'butn:stock:-:{i[1]}'))
    await bot.send_message(message.chat.id, "Выберите категорию, в которой находится товар", reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='stock'))
async def category(call: CallbackQuery, callback_data: dict):
    data = await db.get_products(callback_data.get('category_id'))
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[2]}', callback_data=f'butn:stock_product:{i[1]}:-'))
    await bot.send_message(call.message.chat.id, 'У какой карточки вы бы хотели поменять количество на складе?', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='stock_product'))
async def category(call: CallbackQuery, callback_data: dict):
    stock['product_id'] = callback_data.get("product_id")
    await bot.send_message(call.message.chat.id, 'Введите количество товара на складе')
    await edit_cart.stock.set()

@dp.message_handler(content_types=['text'], state=edit_cart.stock)
async def number(message: types.Message, state: FSMContext) -> None:
    count = message.text
    await db.update_stock(count, stock['product_id'])
    await bot.send_message(message.chat.id, "Количество товара на складе изменено")
    await state.finish()
#
#
@dp.message_handler(text=('Добавить категорию'))
async def start(message: Message):
    await bot.send_message(message.chat.id, 'Введите имя категории')
    await add_categoty.name.set()

@dp.message_handler(content_types=['text'], state=add_categoty.name)
async def number(message: types.Message, state: FSMContext) -> None:
    name = message.text
    await db.add_category(name)
    await bot.send_message(message.chat.id, "Категория добавлена")
    await state.finish()



@dp.message_handler(text=('Удалить категорию'))
async def start(message: Message):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'butn:del_category:-:{i[1]}'))
    await bot.send_message(message.chat.id, 'Выберите категорию, которую хотите удалить', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='del_category'))
async def category(call: CallbackQuery, callback_data: dict):
    await db.del_category(callback_data.get('category_id'))

    data = await db.get_products(callback_data.get('category_id'))
    for i in data:
        await db.del_product(i[1])
    await bot.send_message(call.message.chat.id, 'Категория удалена')

@dp.message_handler(text=('Редактировать категорию'))
async def start(message: Message):
    data = await db.get_categories()
    keyboard = InlineKeyboardMarkup()
    for i in data:
        keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'butn:red_category:-:{i[1]}'))
    await bot.send_message(message.chat.id, 'Выберите категорию у которой хотите редактировать имя', reply_markup=keyboard)

@dp.callback_query_handler(cbd.filter(type='red_category'))
async def category(call: CallbackQuery, callback_data: dict):
    forms['category'] = callback_data.get('category_id')
    await bot.send_message(call.message.chat.id, 'Введите новое имя для категории')
    await update_category.name.set()


@dp.message_handler(content_types=['text'], state=update_category.name)
async def number(message: types.Message, state: FSMContext) -> None:
    name = message.text
    print(name)
    print(forms['category'])
    await db.update_categoory(name, forms['category'])
    await bot.send_message(message.chat.id, "Имя категории изменено")
    await state.finish()


@dp.message_handler(text=('Назад'))
async def start(message: Message):
    await bot.send_message(message.chat.id, 'Вы в меню', reply_markup=keyboards.menu)