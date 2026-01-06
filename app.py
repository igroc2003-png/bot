from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.getenv("MAX_BOT_TOKEN")

MAX_API = f"https://api.max.ru/bot{f9LHodD0cOKVZp7gFirF4PSYvSvITJ-N_iM68WvIJYslb6uURgZkHTfMAxC4a_8CxH0JdE1CnFu9w5qjQEcv}"

def send_message(chat_id, text):
    requests.post(f"{MAX_API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return {"ok": False}

    message = data.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        if text == "/start":
            send_message(chat_id, "Привет! Бот работает!")
        else:
            send_message(chat_id, f"Ты написал: {text}")

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
