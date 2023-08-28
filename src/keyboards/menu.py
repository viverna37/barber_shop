
from dataclasses import dataclass
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

@dataclass()
class keyboards:
    menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    MENU = KeyboardButton('Товары')
    CONTACT_INFORMATION = KeyboardButton('Контактная информация')
    CART = KeyboardButton('Моя корзина')
    menu.add(MENU, CONTACT_INFORMATION, CART)

    supmenu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    next = KeyboardButton('Продолжить')
    red = KeyboardButton('Изменить')
    supmenu.add(next, red)

    korzina = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    korzin1 = KeyboardButton('Очистить')
    korzin2 = KeyboardButton('Назад')
    korzin3 = KeyboardButton('Оплатить')
    korzina.add(korzin1, korzin2, korzin3)

    reg = InlineKeyboardMarkup(row_widnt=2)
    number = InlineKeyboardButton('Номер телефона', callback_data='number')
    reg.add(number)

    admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    plus_cart = KeyboardButton('Добавить карточку')
    del_cart = KeyboardButton('Удалить карточку')
    edit_cart = KeyboardButton('Редактировать карточку')
    plus_category = KeyboardButton('Добавить категорию')
    del_category = KeyboardButton('Удалить категорию')
    edit_category = KeyboardButton('Редактировать категорию')
    back = KeyboardButton('Назад')
    admin.add(plus_cart, del_cart, edit_cart, plus_category, del_category, edit_category).add(back)

    yorn = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton('Пропустить')
    yorn.add(yes)