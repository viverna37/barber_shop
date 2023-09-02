from aiogram import Bot, Dispatcher

from config import Config

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio

storage = MemoryStorage()

bot = Bot(token=Config.token)
dp = Dispatcher(bot=bot, storage=storage)

async def main():
    from handlers import dp
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        print('Bot start')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')