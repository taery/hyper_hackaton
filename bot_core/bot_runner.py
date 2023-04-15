# Configure logging
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

API_TOKEN = os.environ.get('API_TOKEN')

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(regexp='fox$')
async def im_here(message: types.Message):
    await message.reply('I\'m here!☕️️')


def start():
    executor.start_polling(dp, skip_updates=True)
