FROM python:3.12-slim

WORKDIR /app

RUN pip install taskiq taskiq-redis

COPY . .

ENV PYTHONPATH=/app