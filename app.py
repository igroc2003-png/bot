import os
import logging
import asyncio
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("MAX_BOT_TOKEN")
API_URL = f"https://api.max.ru/bot{TOKEN}"

# Логирование (опционально)
logging.basicConfig(level=logging.INFO)

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
    """Обработка входящих сообщений"""
    data = request.json
    logging.info(f"Получены данные: {json.dumps(data, indent=4)}")

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
