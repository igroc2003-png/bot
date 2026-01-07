from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Получаем токен из переменной окружения
TOKEN = os.getenv("MAX_BOT_TOKEN")
API_URL = f"https://api.max.ru/bot{TOKEN}"

def send_message(chat_id, text):
    """Отправить сообщение через MAX API"""
    response = requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=5
    )
    return response.json()

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Обработка входящих сообщений от MAX"""
    data = request.json
    if not data:
        return {"ok": True}

    message = data.get("object", {}).get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id, "✅ Бот работает!")
    else:
        send_message(chat_id, f"Ты написал: {text}")

    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

print("APP STARTED")

