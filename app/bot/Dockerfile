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
    && poetry install --no-interaction --no-ansi --without ml --no-root

# 2. СЛОЙ: Ставим CPU Torch отдельно (самый тяжелый этап)
# Этот слой будет жить в кэше вечно, пока не обновится версия torch
RUN pip install --no-cache-dir torch==2.10.0 --extra-index-url https://download.pytorch.org/whl/cpu

# 3. СЛОЙ: Ставим ML-обвесы (transformers и т.д.) из группы ml (пока вручную через pip)
# RUN poetry install --no-interaction --no-ansi --only ml --no-root --sync
RUN pip install --no-cache-dir sentence-transformers

COPY . .

CMD ["python", "main.py"]