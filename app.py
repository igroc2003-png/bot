from flask import Flask, request
import requests
import os

app = Flask(__name__)

MAX_TOKEN = os.environ.get("MAX_TOKEN")
MAX_API_URL = f"https://botapi.max.ru/bot{MAX_TOKEN}/sendMessage"

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("WEBHOOK DATA:", data)

    try:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Привет! Я простой MAX-бот 🤖")
        else:
            send_message(chat_id, f"Ты написал: {text}")

    except Exception as e:
        print("ERROR:", e)

    return {"ok": True}, 200

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    r = requests.post(MAX_API_URL, json=payload)
    print("SEND STATUS:", r.status_code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print("🔥 FLASK BOOTED 🔥")
    app.run(host="0.0.0.0", port=port)
