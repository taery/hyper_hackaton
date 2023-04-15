# Configure logging
import json
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
    else:
        return await message.reply('Sorry, I don\'t understand you. Please, try again.')

    prompt = f'''AAct like a reading club host. You need to create a quiz for your participants.
The quiz should be based on the {chapter} chapter of the book “{book_name}”.
The quiz should consist of 1 question with hard difficulty with 4 possible answers.
Format output as json "question : string, options: [strings], answer:number"
Answer only JSON'''

    print(prompt)
    try:
        await call_gpt(message, prompt)
    except Exception:
        await handle_message(message)
    # await message.reply(response.choices[0]['message']['content'])

async def call_gpt(message, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": prompt},
        ]
    )
    print(response.choices[0]['message']['content'])
    data = json.loads(response.choices[0]['message']['content'])
    await message.answer_poll(question=data['question'],
                              options=data['options'],
                              type='quiz',
                              correct_option_id=data['answer'] - 1,
                              is_anonymous=False)


@dp.message_handler(regexp='fox.*send.*')
async def handle_message(message: types.Message):
    await message.answer_poll(question='Your answer?',
                              options=['A)', 'B)', 'C'],
                              type='quiz',
                              correct_option_id=0,
                              is_anonymous=False)


def start():
    executor.start_polling(dp, skip_updates=True)
