

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class menu:
    menu = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Акции🏷️', callback_data='action'),
        InlineKeyboardButton(text='Цены на услуги💵', callback_data='price'),
        InlineKeyboardButton(text='Оставить отзыв 💬', callback_data='review'),
        InlineKeyboardButton(text='‼️Напомнить о стрижке‼️', callback_data='opp'),
        InlineKeyboardButton(text='Наш адрес🚩', callback_data='adres'),
        InlineKeyboardButton(text='Контакты 📞', callback_data='contacts'),
        InlineKeyboardButton(text='Задать вопрос❓', callback_data='questions'),
        InlineKeyboardButton(text='🧍‍♀️Посмотреть очередь ️🧍‍♂️', callback_data='queue'),
        InlineKeyboardButton(text='О нас 🙋‍♂️', callback_data='about_we')
    )

    back = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Назад'))

