# ЭТАП 1: Сборка (тяжёлый, только для компиляции)
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main,bots --no-root

# ЭТАП 2: Рантайм (чистый, для продакшена)
FROM python:3.12-slim
WORKDIR /app
# Копируем только установленные пакеты
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Копируем код (последним, чтобы кэш слоёв не сбрасывался)
COPY . .
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1
CMD ["python", "-m", "app.support_bot.main"]