#!/bin/bash

echo "Поточний режим: ${MODE:-не встановлено}"

if [ -z "$MODE" ]; then
    echo "Помилка: Змінна MODE не встановлена. Використовуйте 'dev' або 'prod'."
    exit 1
fi

if [ "$MODE" = "dev" ]; then
    echo "Запуск у режимі розробки..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Запуск у продакшн-режимі..."
    exec uvicorn src.main:app --host 0.0.0.0 --port 8000
fi
