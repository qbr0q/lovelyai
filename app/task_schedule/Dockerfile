FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main,tasks --no-root \
    && rm -rf /root/.cache/pypoetry \
    && pip uninstall -y poetry

COPY . .

ENV PYTHONPATH=/app