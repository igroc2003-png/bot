from maxgram import Bot

# Токен вашего бота
bot = Bot("8304319779:AAF-cF4I5pjhp6otFrnL2oT0Le2fC9oqpbg")

# Установка подсказок для команд бота
bot.set_my_commands({
    "help": "Получить помощь",
    "ping": "Проверка работы бота",
    "hello": "Приветствие"
})

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(context):
    context.reply("Привет! Скажи что-нибудь и я повторю это!")

# Обработчик для сообщения с текстом 'ping'
@bot.hears("ping")
def ping_handler(context):
    context.reply("pong")

# Обработчик для всех остальных входящих сообщений
@bot.on("message_created")
def echo(context):
    # Проверяем, что есть сообщение и тело сообщения
    if context.message and context.message.get("body") and "text" in context.message["body"]:
        # Получаем текст сообщения
        text = context.message["body"]["text"]
        
        # Проверяем, что это не команда и не специальные сообщения с обработчиками
        if not text.startswith("/") and text != "ping":
            context.reply(text)

# Запуск бота
if __name__ == "__main__":
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()
