from flask import Flask, request
import os

app = Flask(__name__)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    print(request.json)  # выводим в консоль все данные
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
