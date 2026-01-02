from aiogram import Bot, Dispatcher, executor, types
import os

# Токен вашего бота
TOKEN = '8304319779:AAF-cF4I5pjhp6otFrnL2oT0Le2fC9oqpbg'

# Создаем объект класса Bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Это твой первый бот.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
