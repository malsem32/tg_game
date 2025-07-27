from bot.create_bot import bot
from bot.create_bot import dp
import logging
from aiogram import F, types

import asyncio

import logging
async def on_startup():
    #  Логгирование
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w',
                        format="%(asctime)s %(levelname)s %(message)s")

    await bot.send_message(735569411, 'Я ебашу')
    print('Я ебашу!')

async def start_bot() -> None:
    from bot.handlers.routers import include_routers
    include_routers(dp)
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':

    asyncio.run(start_bot())