from flask import Flask, request
import requests
import os

app = Flask(__name__)

MAX_TOKEN = os.getenv("MAX_TOKEN")

if not MAX_TOKEN:
    raise RuntimeError("❌ MAX_TOKEN не найден в переменных окружения")

MAX_API_URL = "https://api.max.ru/bot"


def send_message(user_id: int, text: str):
    url = f"{MAX_API_URL}/sendMessage"
    headers = {
        "Authorization": f"Bearer {MAX_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": user_id,
        "text": text
    }
    requests.post(url, headers=headers, json=payload, timeout=10)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data or "from" not in data:
        return "ok"

    user_id = data["from"]["id"]
    text = data.get("text", "").strip()

    if text.lower() in ["/start", "старт"]:
        send_message(user_id, "Привет 👋 Я простой MAX-бот.")
        return "ok"

    send_message(user_id, f"Ты написал: {text}")
    return "ok"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
