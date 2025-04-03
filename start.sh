#!/bin/bash

echo "Поточний режим: ${MODE:-не встановлено}"

if [ -z "$MODE" ]; then
    echo "Помилка: Змінна MODE не встановлена. Використовуйте 'dev' або 'prod'."
    exit 1
fi

# Перевірка обов'язкових змінних середовища
REQUIRED_VARS=("SECRET_KEY" "POSTGRES_HOST" "POSTGRES_PORT" "POSTGRES_USER" "POSTGRES_PASSWORD" "POSTGRES_DB")
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "Помилка: Змінна $VAR не встановлена."
        exit 1
    fi
done

if [ "$MODE" = "dev" ]; then
    echo "Запуск у режимі розробки..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Запуск у продакшн-режимі..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000
fi