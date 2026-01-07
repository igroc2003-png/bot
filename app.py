from maxbot import MaxBot
import os

TOKEN = os.getenv("MAX_BOT_TOKEN")

bot = MaxBot(token=TOKEN)


@bot.message()
async def handle_message(message: dict):
    text = message.get("text", "")
    chat_id = message["chat"]["id"]

    if text == "/start":
        await bot.send_message(chat_id, "✅ Бот работает")
    else:
        await bot.send_message(chat_id, f"Ты написал: {text}")


if __name__ == "__main__":
    bot.run()
