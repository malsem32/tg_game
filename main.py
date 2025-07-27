import asyncio
import logging

from bot.main import start_bot
from fastapi_app.main import run_fastapi
import threading

from fastapi_app.main import logger
if __name__ == '__main__':
    fastapi_app = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_app.start()
    logger.info("Fastapi Запущен")

    asyncio.run(start_bot())
    logger.info("Бот запущен")