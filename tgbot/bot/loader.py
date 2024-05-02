import os

from aiogram import Bot, Dispatcher


API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(API_TOKEN)
dp = Dispatcher()
