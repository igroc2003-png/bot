from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_API = f"https://api.max.ru/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{MAX_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=5
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)

    if not data:
        return {"ok": True}

    if "object" not in data or "message" not in data["object"]:
        return {"ok": True}

    message = data["object"]["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id, "✅ Привет! Бот работает!")
    else:
        send_message(chat_id, f"Ты написал: {text}")

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
