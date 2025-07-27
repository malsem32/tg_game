from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TOKEN_BOT

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(storage=MemoryStorage())