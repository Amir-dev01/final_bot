from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import dotenv_values
from database import Database


token = dotenv_values(".env")["BOT_TOKEN"]
STUFF_USERS = [950539675]
bot = Bot(token=token)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

database = Database("database.sqlite3")
