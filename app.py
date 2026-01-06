from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_API = f"https://api.max.ru/bot{TOKEN}"

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

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

    requests.post(
        f"{MAX_API}/sendMessage",
        json={"chat_id": chat_id, "text": f"Ты написал: {text}"},
        timeout=5
    )

    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

