# Configure logging
import logging
import os
import re

from aiogram import Bot, Dispatcher, executor, types
import openai

API_TOKEN = os.environ.get('API_TOKEN')

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

openai.api_key = os.environ.get('OPENAI_API_KEY')


@dp.message_handler(regexp='fox$')
async def im_here(message: types.Message):
    await message.reply('I\'m here!☕️️')


# Define a message handler for the "fox quiz book" pattern
@dp.message_handler(regexp='fox.*quiz.*')
async def handle_message(message: types.Message):
    pattern = r'fox\s+quiz\s+book\s+(?P<book_name>.*)chapter\s+(?P<chapter>\d+)'

    match = re.search(pattern, message.text.lower())

    if match:
        book_name = match.group('book_name')
        chapter = match.group('chapter')
        await message.reply(f"Book Name: {book_name}, Chapter: {chapter}")
    else:
        await message.reply("No match found.")

    # prompt = f"User: {message.text}\nChatGPT:"
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=prompt,
    #     max_tokens=50,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    # Send the response back to the user



def start():
    executor.start_polling(dp, skip_updates=True)
