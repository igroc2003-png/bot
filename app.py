from maxbot import MaxBot
from maxbot.types import Message
import os

TOKEN = os.getenv("MAX_BOT_TOKEN")

bot = MaxBot(token=TOKEN)


@bot.message()
async def handle_message(message: Message):
    if message.text == "/start":
        await message.answer("✅ Бот работает")
    else:
        await message.answer(f"Ты написал: {message.text}")


if __name__ == "__main__":
    bot.run()
