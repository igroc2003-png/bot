from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)  # просто лог для проверки
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
