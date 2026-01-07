# ================== НАСТРОЙКИ ==================
from flask import Flask, request
import requests
import os
from openai import OpenAI

MAX_TOKEN = os.getenv("MAX_TOKEN")

client = OpenAI()  # ← КЛЮЧ БЕРЁТСЯ ИЗ ENV

app = Flask(__name__)


# ================== ФУНКЦИИ ==================

def send_message(user_id: int, text: str):
    """Отправка сообщения пользователю в MAX"""
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


def ask_ai(user_text: str) -> str:
    """Запрос к OpenAI"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты полезный, вежливый и понятный ИИ-ассистент. Отвечай кратко и по делу."
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


# ================== WEBHOOK ==================

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # защита от пустых запросов
    if not data or "from" not in data:
        return "ok"

    user_id = data["from"]["id"]
    text = data.get("text", "").strip()

    if not text:
        return "ok"

    # команды
    if text.lower() in ["/start", "старт"]:
        send_message(
            user_id,
            "Привет 👋\nЯ ИИ-ассистент 🤖\n\nЗадай мне любой вопрос."
        )
        return "ok"

    try:
        answer = ask_ai(text)
        send_message(user_id, answer)
    except Exception:
        send_message(
            user_id,
            "⚠️ Произошла ошибка. Попробуй задать вопрос позже."
        )

    return "ok"


# ================== ЗАПУСК ==================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
