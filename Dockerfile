# Многоэтапная сборка для оптимизации размера образа
FROM python:3.11-slim as builder

# Устанавливаем системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

# Устанавливаем только необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    libffi8 \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создаем рабочую директорию
WORKDIR /app

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash --uid 1000 botuser && \
    chown -R botuser:botuser /app

# Копируем исходный код бота
COPY --chown=botuser:botuser . .

# Переключаемся на пользователя botuser
USER botuser

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Переменные для бота
ENV BOT_TOKEN=""
ENV BOT_ID=""
ENV AUTH_API_URL="https://bothost.ru/api/auth.php"

# Команда запуска
CMD ["python", "app.py"]
