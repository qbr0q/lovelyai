FROM python:3.12-slim

# Системный обвес
RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Ставим пакеты прямо в систему контейнера
RUN poetry config virtualenvs.create false

# 1. СЛОЙ: Ставим только легкую базу (быстро)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main,bots --no-root

WORKDIR /app

COPY . .

CMD ["python", "-m", "app.support_bot.main"]