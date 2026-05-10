# ===== ЭТАП 1: Builder (тяжёлый, для компиляции) =====
FROM python:3.12-slim AS builder
WORKDIR /app

# Системные зависимости ТОЛЬКО для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем манифесты зависимостей
COPY pyproject.toml poetry.lock* ./

# Ставим Poetry и зависимости (включая ml-группу)
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main,bots,ml --no-root \
    # Torch CPU версия (проверь актуальную версию!)
    && pip install --no-cache-dir torch==2.10.0 --extra-index-url https://download.pytorch.org/whl/cpu \
    # Чистим кэш и удаляем Poetry
    && rm -rf /root/.cache/pypoetry \
    && pip uninstall -y poetry

# ===== ЭТАП 2: Runtime (чистый, для прода) =====
FROM python:3.12-slim
WORKDIR /app

# Системные рантайм-зависимости (только то, что нужно для работы)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем только установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код проекта (в конце для кэширования слоёв)
COPY . .

ENV PYTHONPATH=/app PYTHONUNBUFFERED=1
CMD ["python", "-m", "app.bot.main"]